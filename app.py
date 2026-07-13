import os
import streamlit as st
from dotenv import load_dotenv

from services.tavily_service import tavily_search, build_search_query
from services.llm_service import generate_clean_recommendation
from services.map_utils import build_map_links, extract_destination_from_answer


load_dotenv()


PLACE_TYPES = [
    "商场",
    "旅游景点",
    "公园",
    "博物馆",
    "咖啡厅",
    "餐厅",
    "室内娱乐场所",
    "适合约会的地方",
    "适合拍照的地方",
    "适合自习的地方",
]


st.set_page_config(
    page_title="AI 城市出行助手",
    page_icon="🧭",
    layout="wide",
)


st.sidebar.title("🧭 控制台")

tavily_status = "已配置" if os.environ.get("TAVILY_API_KEY") else "未配置"
vapi_status = "已配置" if os.environ.get("VAPI_API_KEY") else "未配置"

st.sidebar.metric("Tavily", tavily_status)
st.sidebar.metric("V-API", vapi_status)
st.sidebar.metric("模型", os.environ.get("VAPI_MODEL", "gpt-5.6-sol"))

st.sidebar.markdown("---")
st.sidebar.markdown("### 当前架构")
st.sidebar.markdown("- Tavily：搜索资料")
st.sidebar.markdown("- V-API：清洗、筛选、总结")
st.sidebar.markdown("- Streamlit：网页展示")
st.sidebar.warning("API Key 不要写进代码，也不要上传到 GitHub。")


st.title("🧭 AI 城市出行助手")
st.caption("Tavily 搜索资料，V-API 清洗结果，只输出真正能用的推荐。")

st.divider()


left, right = st.columns([1.05, 0.95])

with left:
    st.subheader("📍 出行信息")

    city = st.text_input(
        "城市",
        placeholder="例如：东莞、深圳、广州",
    )

    weather = st.text_input(
        "当前天气",
        placeholder="例如：晴天、下雨、多云、炎热",
    )

    start_location = st.text_input(
        "出发地点",
        placeholder="例如：东莞站、深圳北站、学校、酒店，可留空",
    )

with right:
    st.subheader("🎯 推荐偏好")

    place_type = st.selectbox(
        "想推荐什么类型的地方？",
        PLACE_TYPES,
    )

    st.info("这版不会直接展示大段搜索结果，而是先交给 V-API 整理。")


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("城市", city if city else "未填写")

with m2:
    st.metric("天气", weather if weather else "未填写")

with m3:
    st.metric("类型", place_type)

with m4:
    st.metric("模型", os.environ.get("VAPI_MODEL", "gpt-5.6-sol"))


with st.expander("🔍 查看 Tavily 搜索关键词"):
    if city and weather:
        q = build_search_query(city, weather, place_type)
        st.code(q)
        st.write(f"关键词长度：{len(q)} / 400")
    else:
        st.write("填写城市和天气后会自动生成搜索关键词。")


st.divider()


if st.button("🚀 生成干净推荐", use_container_width=True):
    if not city.strip() or not weather.strip():
        st.warning("请至少输入城市和天气。")

    else:
        with st.spinner("第一步：Tavily 正在搜索资料..."):
            search_data = tavily_search(city, weather, place_type)

        if not search_data["ok"]:
            st.error("Tavily 搜索失败")
            st.write(search_data["error"])

        elif not search_data["results"]:
            st.warning("Tavily 没有找到可用资料。请换一个地点类型或城市关键词。")

        else:
            with st.spinner("第二步：V-API 正在清洗搜索结果并生成推荐..."):
                try:
                    final_answer = generate_clean_recommendation(
                        city=city,
                        weather=weather,
                        start_location=start_location,
                        place_type=place_type,
                        search_results=search_data["results"],
                    )
                except Exception as e:
                    st.error("V-API 生成失败")
                    st.write(e)
                    final_answer = ""

            if final_answer:
                st.success("推荐生成完成")

                tab1, tab2, tab3 = st.tabs(
                    ["✅ 推荐结果", "🗺️ 地图导航", "🔎 原始资料"]
                )

                with tab1:
                    st.markdown(final_answer)

                with tab2:
                    destination = extract_destination_from_answer(final_answer)

                    if not destination:
                        st.warning("没有自动识别到推荐地点名称。你可以从推荐结果里复制地点名到地图 App 搜索。")

                    else:
                        st.subheader("地图路线")
                        st.write(f"识别到的目的地：**{destination}**")

                        links = build_map_links(
                            start_location=start_location,
                            city=city,
                            destination=destination,
                        )

                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.link_button(
                                "打开高德地图",
                                links["amap"],
                                use_container_width=True,
                            )

                        with col_b:
                            st.link_button(
                                "打开百度地图",
                                links["baidu"],
                                use_container_width=True,
                            )

                        st.caption("地图链接只是快捷搜索入口，具体路线、时间和费用以地图 App 实时结果为准。")

                with tab3:
                    st.subheader("Tavily 原始搜索资料")
                    st.caption("这些资料只作为 LLM 的输入，不直接作为最终推荐。")

                    for idx, item in enumerate(search_data["results"], start=1):
                        title = item.get("title", "无标题")
                        content = item.get("content", "")
                        url = item.get("url", "")

                        with st.expander(f"{idx}. {title}"):
                            st.write(content)

                            if url:
                                st.markdown(f"[打开来源]({url})")

else:
    st.info("填写信息后，点击「生成干净推荐」。")


st.divider()

with st.expander("为什么这版会比之前干净？"):
    st.markdown("之前是：Tavily 搜索 → 网页直接展示搜索结果。")
    st.markdown("现在是：Tavily 搜索 → V-API 清洗整理 → 网页展示最终推荐。")
    st.markdown("所以 V-API 会先过滤无关内容，再生成结构化推荐。")


st.caption("Powered by Tavily Search API + V-API gpt-5.6-sol")
