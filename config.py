# 阿里云百炼API配置
API_KEY = "your-api-key-here"  # 你的阿里云百炼API密钥
EMBEDDING_MODEL = "text-embedding-v4"  # 阿里云百炼Embedding模型
LLM_MODEL = "qwen2.5-72b-instruct"  # 千问2.5 72B指令模型

# ChromaDB配置
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "mcp_knowledge"

# 文本分块配置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# 检索配置
TOP_K_RESULTS = 10
SIMILARITY_THRESHOLD = 0.25
