# AI 城市出行助手

一个基于 Streamlit 的 AI 出行推荐小平台。

项目使用：

- Tavily Search API 搜索地点资料
- V-API / gpt-5.6-sol 清洗和总结搜索结果
- Streamlit 构建网页界面

## 功能

- 根据城市、天气和出发地点推荐适合去的地方
- 自动过滤杂乱搜索结果
- 输出中文结构化推荐
- 提供地图搜索入口
- 支持商场、景点、公园、博物馆、咖啡厅等类型

## 项目结构

```text
ai-travel-assistant/
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── README.md
└── services/
    ├── __init__.py
    ├── tavily_service.py
    ├── llm_service.py
    ├── prompt_builder.py
    └── map_utils.py
