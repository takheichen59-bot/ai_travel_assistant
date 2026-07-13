import os
import re
import time
from tavily import TavilyClient


def clean_text(text: str, max_len: int = 800) -> str:
    text = text or ""
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_len:
        return text[:max_len] + "..."

    return text


def build_search_query(city: str, weather: str, place_type: str) -> str:
    city = city.strip()
    weather = weather.strip()
    place_type = place_type.strip()

    if place_type == "商场":
        query = f"{city} 值得去的大型商场 购物中心 美食 娱乐 交通方便"
    elif place_type == "博物馆":
        query = f"{city} 值得去的博物馆 展览 室内 交通方便"
    elif place_type == "公园":
        query = f"{city} 值得去的公园 散步 拍照 游玩攻略"
    elif place_type == "咖啡厅":
        query = f"{city} 值得去的咖啡厅 安静 拍照 推荐"
    elif place_type == "餐厅":
        query = f"{city} 值得去的餐厅 美食 推荐"
    else:
        query = f"{city} 值得去的{place_type} 推荐 交通方便 游玩攻略"

    if "雨" in weather:
        query += " 雨天 室内"
    elif "晴" in weather or "热" in weather or "炎热" in weather:
        query += " 晴天 适合游玩"

    return query[:380]


def tavily_search(city: str, weather: str, place_type: str) -> dict:
    api_key = os.environ.get("TAVILY_API_KEY")

    if not api_key:
        return {
            "ok": False,
            "error": "未找到 TAVILY_API_KEY，请检查 .env 或环境变量。",
            "query": "",
            "results": [],
        }

    tavily = TavilyClient(api_key=api_key)
    query = build_search_query(city, weather, place_type)

    last_error = None

    for attempt in range(4):
        try:
            response = tavily.search(
                query=query,
                search_depth="basic",
                include_answer=False,
                include_raw_content=False,
                max_results=6,
            )

            results = []

            for item in response.get("results", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "content": clean_text(item.get("content", ""), 700),
                        "url": item.get("url", ""),
                    }
                )

            return {
                "ok": True,
                "error": "",
                "query": query,
                "results": results,
            }

        except Exception as e:
            last_error = e
            time.sleep(2 + attempt * 2)

    return {
        "ok": False,
        "error": str(last_error),
        "query": query,
        "results": [],
    }