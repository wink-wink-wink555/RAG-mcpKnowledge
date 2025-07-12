import requests
from typing import List, Dict, Any
from data_processor import DataProcessor
from vector_store import VectorStore
from config import *

class RAGSystem:
    def __init__(self):
        # 初始化组件
        self.data_processor = DataProcessor()
        self.vector_store = VectorStore()
        
        # 初始化阿里云百炼LLM配置
        self.api_key = API_KEY
        self.llm_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        
        print("RAG系统初始化完成")
    
    def build_knowledge_base(self, use_header_splitting: bool = True, clear_existing: bool = False) -> bool:
        """构建知识库"""
        try:
            print("开始构建MCP知识库...")
            
            # 清空现有数据（如果需要）
            if clear_existing:
                self.vector_store.clear_collection()
            
            # 处理文档
            documents = self.data_processor.process_documents(use_header_splitting)
            
            if not documents:
                print("没有找到可处理的文档")
                return False
            
            # 添加到向量存储
            success = self.vector_store.add_documents(documents)
            
            if success:
                # 显示知识库信息
                info = self.vector_store.get_collection_info()
                print(f"知识库构建完成: {info}")
                return True
            else:
                print("知识库构建失败")
                return False
                
        except Exception as e:
            print(f"构建知识库时出错: {e}")
            return False
    
    def generate_response(self, query: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """生成回答"""
        try:
            print(f"处理查询: {query}")
            
            # 检索相关文档
            relevant_docs = self.vector_store.search(query)
            
            if not relevant_docs:
                return {
                    'success': False,
                    'response': "抱歉，我在知识库中没有找到相关信息。",
                    'sources': [],
                    'reason': "没有找到相关文档"
                }
            
            # 构建上下文
            context = self._build_context(relevant_docs)
            
            # 构建提示词
            prompt = self._build_prompt(query, context)
            
            # 生成回答
            answer = self._generate_response(prompt)
            
            # 准备源文档信息
            sources = []
            for doc in relevant_docs:
                sources.append({
                    'source': doc['metadata']['source'],
                    'header': doc['metadata'].get('header', ''),
                    'similarity': doc['similarity']
                })
            
            return {
                'success': True,
                'response': answer,
                'sources': sources,
                'context_length': len(context)
            }
            
        except Exception as e:
            print(f"生成回答时出错: {e}")
            return {
                'success': False,
                'response': f"处理查询时出错: {str(e)}",
                'sources': [],
                'reason': str(e)
            }
    
    def _build_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """构建上下文"""
        context_parts = []
        
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(f"文档 {i} (来源: {doc['metadata']['source']}, 相似度: {doc['similarity']:.3f}):")
            context_parts.append(doc['content'])
            context_parts.append("---")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, prompt: str) -> str:
        """使用阿里云百炼LLM生成回答"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": LLM_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.7,
                "top_p": 0.8
            }
            
            response = requests.post(self.llm_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                print(f"LLM API响应格式错误: {result}")
                return "抱歉，我无法生成有效的回答。"
                
        except Exception as e:
            print(f"生成回答时出错: {e}")
            return f"处理查询时出错: {str(e)}"
    
    def _build_prompt(self, query: str, context: str) -> str:
        """构建提示词"""
        prompt = f"""你是一个专业的MCP（Model Context Protocol）知识助手。请基于以下上下文信息回答用户的问题。

用户问题: {query}

相关上下文信息:
{context}

请根据上下文信息提供准确、详细的回答。如果上下文中没有相关信息，请明确说明。

**重要格式要求：**
1. 使用Markdown格式组织回答内容
2. 使用标题（#、##、###、####）来组织内容结构
3. 使用粗体（**文本**）来强调重要概念
4. 使用列表（- 或 1.）来列举要点
5. 使用代码块（```）来展示代码示例
6. 使用行内代码（`代码`）来标记技术术语
7. **不要在行首添加多余的空格或制表符**
8. **确保每行文本都顶格对齐，不要有前导空格**
9. **段落之间用空行分隔，但不要有多余的空行**
10. 保持专业性和准确性
11. 如果涉及概念解释，请用通俗易懂的语言
12. 如果上下文中没有足够信息，请说明需要更多信息

**格式示例：**
```
# 标题

内容段落，不要有前导空格。

## 二级标题

1. 列表项一
2. 列表项二

### 三级标题

- 无序列表项
- 另一个列表项

**重要概念**：这是重要内容。
```

请严格按照上述格式要求用Markdown回答:"""
        
        return prompt
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """获取知识库信息"""
        return self.vector_store.get_collection_info()
    
    def test_query(self, query: str) -> None:
        """测试查询功能"""
        print(f"\n{'='*50}")
        print(f"测试查询: {query}")
        print(f"{'='*50}")
        
        result = self.generate_response(query)
        
        if result['success']:
            print(f"\n回答:")
            print(result['response'])
            
            print(f"\n参考来源:")
            for source in result['sources']:
                print(f"- {source['source']} (相似度: {source['similarity']:.3f})")
                if source['header']:
                    print(f"  标题: {source['header']}")
        else:
            print(f"查询失败: {result.get('reason', '未知错误')}")

def main():
    """主函数"""
    rag = RAGSystem()
    
    # 检查知识库状态
    info = rag.get_knowledge_base_info()
    print(f"当前知识库状态: {info}")
    
    # 如果知识库为空，构建知识库
    if info.get('document_count', 0) == 0:
        print("知识库为空，开始构建...")
        success = rag.build_knowledge_base()
        if not success:
            print("知识库构建失败，退出程序")
            return
    
    # 交互式查询
    print("\n欢迎使用MCP知识库RAG系统！")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'info' 查看知识库信息")
    print("输入 'rebuild' 重新构建知识库")
    
    while True:
        try:
            query = input("\n请输入您的问题: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
                
            if query.lower() == 'info':
                info = rag.get_knowledge_base_info()
                print(f"知识库信息: {info}")
                continue
                
            if query.lower() == 'rebuild':
                print("重新构建知识库...")
                success = rag.build_knowledge_base(clear_existing=True)
                if success:
                    print("知识库重建完成")
                else:
                    print("知识库重建失败")
                continue
            
            # 处理查询
            rag.test_query(query)
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"处理输入时出错: {e}")

if __name__ == "__main__":
    main() 