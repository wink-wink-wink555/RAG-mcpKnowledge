# 🧠 RAG-mcpKnowledge

基于阿里云百炼API（Qwen模型）的MCP协议知识库RAG系统，提供智能问答和文档检索功能。

## 🌟 项目特点

- **🚀 先进的AI技术**：集成阿里云百炼Qwen2.5-72B大模型和text-embedding-v4嵌入模型
- **📚 专业知识库**：包含完整的MCP协议文档和开发指南
- **🔍 智能检索**：基于向量相似度的精准文档检索
- **💬 友好界面**：现代化Web界面，支持实时对话
- **📋 代码高亮**：支持多种编程语言的代码块显示和一键复制
- **📊 相似度显示**：显示检索结果的相似度评分和来源信息

## 🛠️ 技术栈

- **后端框架**：FastAPI
- **AI模型**：阿里云百炼 Qwen2.5-72B + text-embedding-v4
- **向量数据库**：ChromaDB
- **前端**：原生HTML/CSS/JavaScript
- **文本处理**：tiktoken分词器

## 📦 安装部署

### 1. 环境要求

- Python 3.8+
- 阿里云百炼API密钥

### 2. 克隆项目

```bash
git clone https://github.com/wink-wink-wink555/RAG-mcpKnowledge.git
cd RAG-mcpKnowledge
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置API密钥

编辑 `config.py` 文件，设置您的阿里云百炼API密钥：

```python
API_KEY = "your-api-key-here"  # 替换为您的API密钥
```

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## 🎯 使用指南

### Web界面使用

1. 打开浏览器访问 `http://localhost:8000`
2. 在输入框中输入关于MCP协议的问题
3. 系统将基于知识库提供准确回答
4. 查看参考来源和相似度评分

### 示例问题

- 什么是MCP协议？
- 如何使用MCP进行开发？
- MCP的架构是怎样的？
- MCP协议的主要功能是什么？

### 命令行操作

```bash
# 重建知识库（清空现有数据并重新处理所有文档）
python main.py --rebuild

# 查看知识库信息
python main.py --info

# 启动Web界面（默认）
python main.py
```

## 📁 项目结构

```
RAG-mcpKnowledge/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── vector_store.py        # 向量存储管理
├── rag_system.py          # RAG系统核心
├── web_interface.py       # Web界面
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
├── txt/                  # 知识库文档
│   ├── mcp_rule.txt      # MCP协议完整文档 (来源: https://modelcontextprotocol.io/llms-full.txt)
│   ├── mcp_rule_py.txt   # Python SDK文档 (来源: https://github.com/modelcontextprotocol/python-sdk)
│   └── mcp_rule_ts.txt   # TypeScript SDK文档 (来源: https://github.com/modelcontextprotocol/typescript-sdk)
└── chroma_db/            # 向量数据库（自动生成）
```

## ⚙️ 配置说明

### 主要配置项 (config.py)

```python
# API配置
API_KEY = "your-api-key"           # 阿里云百炼API密钥
EMBEDDING_MODEL = "text-embedding-v4"  # 嵌入模型
LLM_MODEL = "qwen2.5-72b-instruct"    # 大语言模型

# 文本分块配置
CHUNK_SIZE = 1000          # 文本块大小
CHUNK_OVERLAP = 200        # 文本块重叠

# 检索配置
TOP_K_RESULTS = 10         # 返回结果数量
SIMILARITY_THRESHOLD = 0.25 # 相似度阈值
```

## 🔧 知识库管理

### 📚 当前知识库文档来源

本项目的知识库包含以下MCP协议官方文档：

1. **MCP协议完整文档** (`mcp_rule.txt`)
   - 来源：https://modelcontextprotocol.io/llms-full.txt
   - 内容：MCP协议的完整规范和说明

2. **Python SDK文档** (`mcp_rule_py.txt`)
   - 来源：https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md
   - 内容：Python SDK的使用指南和API文档

3. **TypeScript SDK文档** (`mcp_rule_ts.txt`)
   - 来源：https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md
   - 内容：TypeScript SDK的使用指南和API文档

### 📝 添加新文档并重新生成向量

如果您想要添加自己的文档到知识库中，请按照以下步骤操作：

#### 步骤1：准备文档
```bash
# 将您的新文档（.txt格式）放入txt目录
# 例如：
cp your_new_document.txt txt/
```

#### 步骤2：查看当前知识库状态
```bash
python main.py --info
```

#### 步骤3：清空现有向量数据库
```bash
# 重建命令会自动清空现有数据库
python main.py --rebuild
```

#### 步骤4：系统自动处理流程
运行重建命令后，系统将自动执行以下步骤：

1. **🔍 扫描文档**：系统扫描`txt/`目录下的所有`.txt`文件
2. **📄 读取内容**：逐个读取文档内容
3. **✂️ 文本分块**：将长文档分割成1000字符的文本块（重叠200字符）
4. **🧠 生成向量**：使用阿里云百炼`text-embedding-v4`模型为每个文本块生成向量
5. **💾 存储向量**：将向量和元数据存储到ChromaDB数据库
6. **✅ 完成构建**：显示构建完成信息

#### 步骤5：验证新知识库
```bash
# 查看更新后的知识库信息
python main.py --info
```

输出示例：
```
📊 知识库信息:
📁 文档总数: 4  # 新增文档后数量会增加
📄 文本块数: 1,580  # 文本块数量会相应增加
🔍 向量维度: 1,536
💾 数据库大小: 58.7 MB
🕐 最后更新: 2024-12-20 15:30:25
```

#### 步骤6：测试新知识库
```bash
# 启动Web界面测试
python main.py
```

然后在浏览器中访问 `http://localhost:8000`，尝试询问与新文档相关的问题。

### ⚠️ 重要注意事项

1. **文档格式**：目前只支持`.txt`格式的文档
2. **文档编码**：请确保文档使用UTF-8编码
3. **处理时间**：向量生成需要时间，文档越多耗时越长
4. **API限制**：注意阿里云百炼API的调用频率限制
5. **存储空间**：大量文档会占用较多磁盘空间

### 🔄 更新现有文档

如果您需要更新现有文档：

1. 直接替换`txt/`目录中的对应文件
2. 运行 `python main.py --rebuild` 重新生成向量
3. 系统会自动处理所有文档，包括更新的内容

### 查看知识库状态

```bash
python main.py --info
```

输出示例：
```
📊 知识库信息:
📁 文档总数: 3
📄 文本块数: 1,245
🔍 向量维度: 1,536
💾 数据库大小: 45.2 MB
```

## 🎨 界面特性

### 现代化设计
- 渐变背景和毛玻璃效果
- 响应式布局，支持移动设备
- 流畅的动画和交互效果

### 代码块功能
- 语言标识和语法高亮
- 一键复制代码内容
- 紧凑的行间距显示

### 智能问答
- 实时加载动画
- 参考来源展示
- 相似度评分显示

## 🔍 API接口

### 聊天接口
```
POST /chat
Content-Type: application/x-www-form-urlencoded

message=你的问题
```

### 知识库信息
```
GET /info
```

## 📊 性能优化

- 使用ChromaDB向量数据库提供高效检索
- 文本分块策略优化内存使用
- 异步处理提升响应速度
- 前端缓存减少重复请求

## 🚀 部署建议

### 生产环境部署

1. 使用Gunicorn或uWSGI作为WSGI服务器
2. 配置Nginx作为反向代理
3. 设置环境变量管理敏感信息
4. 启用HTTPS加密传输

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 🤝 贡献指南

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 更新日志

### v1.0.0 (2024-12-20)
- ✨ 初始版本发布
- 🧠 集成阿里云百炼Qwen模型
- 📚 MCP协议知识库构建
- 💬 Web界面开发
- 🔍 智能检索功能
- 📋 代码块复制功能

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [阿里云百炼](https://bailian.console.aliyun.com/) - 提供强大的AI模型服务
- [ChromaDB](https://www.trychroma.com/) - 高性能向量数据库
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Python Web框架

## 📞 联系方式

- 项目作者：[@wink-wink-wink555](https://github.com/wink-wink-wink555)
- 项目地址：[RAG-mcpKnowledge](https://github.com/wink-wink-wink555/RAG-mcpKnowledge)

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！ 