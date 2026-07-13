# AI 城市出行助手

一个基于 Streamlit 的 AI 出行推荐小平台。

项目使用：

* Tavily Search API 搜索地点资料
* V-API / gpt-5.6-sol 清洗和总结搜索结果
* Streamlit 构建网页界面

这个项目的目标是让用户不再需要自己翻大量杂乱的搜索结果，而是通过一个简单的网页界面，输入城市、天气、出发地点和想去的地点类型，然后由 AI 自动搜索资料、筛选信息，并生成清晰、实用的出行推荐。

---

## 功能

* 根据城市、天气和出发地点推荐适合去的地方
* 自动过滤杂乱搜索结果
* 输出中文结构化推荐
* 提供地图搜索入口
* 支持商场、景点、公园、博物馆、咖啡厅等类型
* 结合天气给出更合理的出行建议
* 根据出发地点生成地图搜索链接
* 将原始搜索结果折叠显示，避免页面混乱
* 使用 LLM 对搜索结果进行二次整理，而不是直接展示网页内容

---

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
```

---

## 项目背景

在日常生活中，如果用户想根据天气和位置找一个适合去的地方，通常需要打开搜索引擎，输入关键词，然后自己浏览大量网页。

但是搜索结果经常会出现这些问题：

* 内容太长，不适合快速阅读
* 结果中混入酒店广告、旅游攻略、交通页面
* 有些网页和用户需求关系不大
* 搜索结果只告诉用户“有什么地方”，但没有告诉用户“为什么适合”
* 很多推荐没有结合天气、出发地点和实际出行方式
* 用户仍然需要自己打开地图 App 查路线

因此，本项目尝试构建一个更完整的 AI 出行推荐流程：

```text
用户输入需求
    ↓
Tavily 搜索实时资料
    ↓
V-API / gpt-5.6-sol 清洗和总结资料
    ↓
Streamlit 展示推荐结果
    ↓
生成地图搜索入口
```

这个项目的核心思想是：
**搜索引擎负责找资料，大语言模型负责理解和整理，网页界面负责展示结果。**

---

## 项目意义

这个项目不仅是一个简单的旅游推荐工具，也可以看作是一个小型 AI Agent 应用原型。

传统搜索工具通常只返回网页列表，用户需要自己判断哪些信息有用。
而这个项目尝试让 AI 在中间多做一步：先理解用户需求，再从搜索结果中筛选有用信息，最后生成更适合用户直接阅读的推荐。

它展示了一个常见的 AI 应用开发模式：

```text
用户输入 → 工具调用 → 信息检索 → LLM 总结 → 结构化输出 → 用户界面展示
```

这种模式可以扩展到很多场景，例如：

* 本地生活推荐
* 旅游路线规划
* 校园周边推荐
* 餐厅推荐
* 室内活动推荐
* 周末出行规划
* 智能导览系统

虽然这个项目目前规模不大，但它已经包含了 AI Agent 的几个核心组成部分：用户输入、外部工具调用、搜索结果处理、LLM 推理总结和网页展示。

---

## 技术栈

本项目主要使用以下技术：

### Python

Python 是整个项目的主要开发语言，用于编写后端逻辑、调用 API 和处理数据。

### Streamlit

Streamlit 用来构建网页界面。
它可以快速把 Python 项目变成一个可交互的 Web App，适合 AI 原型项目开发。

### Tavily Search API

Tavily 用于搜索实时网页资料。
在本项目中，Tavily 不直接生成最终答案，而是负责提供搜索材料。

### V-API / gpt-5.6-sol

V-API 提供 OpenAI-compatible 接口。
本项目使用 `gpt-5.6-sol` 对 Tavily 返回的搜索结果进行筛选、清洗和总结。

### OpenAI Python SDK

虽然项目没有直接使用 OpenAI 官方模型，但由于 V-API 兼容 OpenAI 接口格式，所以可以使用 OpenAI Python SDK 调用模型。

### python-dotenv

用于从 `.env` 文件读取 API key，避免把密钥直接写进代码。

---

## 各文件说明

### `app.py`

项目主入口文件。

它负责：

* 创建 Streamlit 网页界面
* 接收用户输入
* 调用 Tavily 搜索模块
* 调用 LLM 清洗模块
* 展示最终推荐结果
* 展示地图导航按钮
* 折叠展示原始搜索资料

运行项目时，执行：

```bash
streamlit run app.py
```

---

### `services/tavily_service.py`

负责 Tavily 搜索相关逻辑。

主要功能：

* 构造搜索关键词
* 调用 Tavily Search API
* 控制 query 长度
* 清洗搜索结果文本
* 返回标题、摘要和来源链接

Tavily 的作用是“找资料”，不是“直接回答用户”。

---

### `services/llm_service.py`

负责调用 V-API 中的大语言模型。

主要功能：

* 读取 V-API 的 API key
* 读取模型名称
* 调用 OpenAI-compatible Chat Completions 接口
* 添加自动重试机制
* 返回 LLM 生成的推荐内容

这是项目中负责“智能总结”的部分。

---

### `services/prompt_builder.py`

负责构建发送给 LLM 的 Prompt。

Prompt 会告诉模型：

* 用户所在城市
* 当前天气
* 出发地点
* 想去的地点类型
* Tavily 搜索到的资料
* 哪些内容需要过滤
* 最终输出应该是什么格式

这个文件非常重要，因为 Prompt 的质量会直接影响推荐结果的质量。

---

### `services/map_utils.py`

负责地图相关功能。

主要功能：

* 从 LLM 输出中提取推荐地点名称
* 生成高德地图搜索链接
* 生成百度地图搜索链接

这样用户可以直接点击按钮查看实时路线。

---

### `.env.example`

环境变量示例文件。

用于告诉其他开发者需要配置哪些 API key。

示例：

```env
TAVILY_API_KEY=your_tavily_api_key_here

VAPI_API_KEY=your_vapi_api_key_here
VAPI_BASE_URL=https://api.gpt.ge/v1
VAPI_MODEL=gpt-5.6-sol
```

注意：
`.env.example` 可以上传到 GitHub，真正包含密钥的 `.env` 不能上传。

---

### `.gitignore`

用于告诉 Git 哪些文件不应该上传。

常见内容：

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
.streamlit/secrets.toml
```

这样可以避免 API key、缓存文件和虚拟环境被上传到 GitHub。

---

### `requirements.txt`

记录项目依赖。

示例：

```txt
streamlit
tavily-python
openai
python-dotenv
```

安装依赖时运行：

```bash
pip install -r requirements.txt
```

Windows 用户也可以使用：

```bash
py -m pip install -r requirements.txt
```

---

## 安装方法

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-travel-assistant.git
cd ai-travel-assistant
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或者：

```bash
py -m pip install -r requirements.txt
```

### 3. 创建 `.env` 文件

在项目根目录下创建 `.env` 文件：

```env
TAVILY_API_KEY=your_tavily_api_key_here

VAPI_API_KEY=your_vapi_api_key_here
VAPI_BASE_URL=https://api.gpt.ge/v1
VAPI_MODEL=gpt-5.6-sol
```

### 4. 运行项目

```bash
streamlit run app.py
```

或者：

```bash
py -m streamlit run app.py
```

运行成功后，浏览器会打开：

```text
http://localhost:8501
```

---

## 使用方法

打开网页后，用户需要填写以下信息：

### 1. 城市

例如：

```text
东莞
深圳
广州
香港
东京
```

城市会影响搜索结果和最终推荐。

### 2. 当前天气

例如：

```text
晴天
下雨
多云
炎热
阴天
```

天气会影响推荐逻辑。

例如：

* 晴天适合商场、公园、拍照地点
* 雨天更适合室内场所
* 炎热天气适合减少户外步行
* 多云天气适合城市散步或公园类地点

### 3. 出发地点

例如：

```text
东莞站
深圳北站
广州塔
学校
酒店
市中心
```

出发地点会用于生成地图搜索链接。

如果用户没有填写出发地点，系统会默认从城市中心或当前位置出发。

### 4. 地点类型

当前支持：

```text
商场
旅游景点
公园
博物馆
咖啡厅
餐厅
室内娱乐场所
适合约会的地方
适合拍照的地方
适合自习的地方
```

不同地点类型会影响搜索关键词和最终推荐方向。

---

## 示例输入

```text
城市：东莞
天气：晴天
出发地点：东莞站
地点类型：商场
```

系统会执行：

```text
Tavily 搜索东莞适合晴天去的商场
    ↓
LLM 过滤无关内容
    ↓
生成推荐地点、理由、路线建议、游玩建议
    ↓
提供地图搜索入口
```

---

## 示例输出

```text
推荐地点：东莞民盈国贸中心

为什么推荐：
- 位于东莞市中心，交通较方便
- 商场内部有餐饮、购物、娱乐和休息空间
- 晴天可以减少长时间户外暴晒，适合室内活动

怎么去：
- 可以从东莞站出发，使用地图 App 查询地铁、公交或打车路线
- 如果携带行李或天气炎热，打车会更方便
- 实时路线请以高德地图、百度地图或 Google Maps 为准

适合怎么玩：
- 可以安排购物、吃饭、看电影或咖啡休息
- 建议停留 3 到 5 小时

注意事项：
- 周末和晚餐时间人流较多
- 出发前建议查看营业时间
- 地铁和交通信息可能变化，请以地图 App 为准
```

---

## 为什么不直接展示搜索结果？

因为搜索结果通常非常混乱。

例如，用户只是想找一个“东莞晴天适合去的商场”，搜索结果可能会包含：

* 公交路线页面
* 旅游攻略长文
* 酒店推荐
* 不相关景点
* 广告内容
* 重复网页
* 与用户需求不匹配的地点

如果直接展示这些内容，用户体验会很差。

所以本项目的设计是：

```text
搜索结果只是材料，不是最终答案。
```

最终答案由 LLM 根据搜索结果重新整理生成。

---

## 当前限制

本项目仍然是一个原型项目，存在一些限制：

* Tavily 搜索结果质量会影响最终答案
* LLM 可能仍然会总结出不完全准确的信息
* 地图链接只是搜索入口，不是真正的实时路线 API
* 当前天气由用户手动输入
* 当前没有用户账号系统
* 当前没有历史记录保存
* 当前没有个性化偏好记忆

---

## 未来改进方向

未来可以继续扩展以下功能：

### 1. 接入真实天气 API

让系统根据城市自动获取天气，而不是让用户手动输入。

### 2. 接入地图 API

接入高德地图、百度地图或 Google Maps API，获取更准确的路线、距离和时间。

### 3. 加入用户偏好

例如：

* 喜欢安静
* 不想走太远
* 预算较低
* 喜欢拍照
* 喜欢室内
* 喜欢咖啡厅
* 不喜欢人多

这样推荐会更加个性化。

### 4. 支持多地点路线规划

未来可以从“推荐一个地点”扩展成“一日游路线规划”。

例如：

```text
上午：博物馆
中午：餐厅
下午：商场
晚上：夜景地点
```

### 5. 加入评分反馈

用户可以对推荐结果进行反馈：

```text
有用
一般
没用
```

后续可以根据反馈优化 Prompt 和推荐逻辑。

### 6. 支持多语言

未来可以支持中文、英文、日文、韩文等多语言输出。

---

## 安全提醒

请不要把 API key 写进代码。

错误示例：

```python
api_key = "your-real-api-key"
```

推荐做法：

```python
api_key = os.environ.get("VAPI_API_KEY")
```

如果 API key 已经被公开，请立即去对应平台删除并重新生成。

---

## 项目总结

AI 城市出行助手展示了一个简单但完整的 AI 应用流程：

```text
搜索工具 + 大语言模型 + 网页界面
```

它不是单纯依靠 LLM 编答案，也不是简单复制搜索结果，而是把搜索资料交给 LLM 进行清洗、筛选和总结。

这个项目可以作为学习以下内容的入门案例：

* AI Agent 应用开发
* Search + LLM 工作流
* Prompt Engineering
* Streamlit Web App
* OpenAI-compatible API 调用
* 环境变量和 API key 管理
* 项目结构整理和 GitHub 发布

虽然它目前只是一个小型原型，但已经具备实际 AI 应用的基本结构，也可以继续扩展成更完整的城市生活助手或旅行规划系统。

---

## License

This project is for learning and demonstration purposes.
You can modify and extend it for your own AI application experiments.
