from typing import List, Dict, Any
from pathlib import Path
import tiktoken

class DataProcessor:
    def __init__(self, txt_dir: str = "txt"):
        self.txt_dir = Path(txt_dir)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def read_txt_files(self) -> List[Dict[str, Any]]:
        """读取所有txt文件并返回结构化数据"""
        documents = []
        
        for txt_file in self.txt_dir.glob("*.txt"):
            print(f"正在处理文件: {txt_file.name}")
            
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取文件名作为文档类型
                doc_type = txt_file.stem
                
                documents.append({
                    'content': content,
                    'source': txt_file.name,
                    'type': doc_type,
                    'size': len(content)
                })
                
            except Exception as e:
                print(f"处理文件 {txt_file.name} 时出错: {e}")
                
        return documents
    
    def split_text_by_headers(self, text: str, source: str) -> List[Dict[str, Any]]:
        """按标题分割文本"""
        chunks = []
        
        # 分割文本为段落
        paragraphs = text.split('\n\n')
        
        current_header = ""
        current_content = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # 检查是否是标题（以#开头）
            if para.startswith('#'):
                # 保存之前的块
                if current_content:
                    chunk_text = f"{current_header}\n\n" + '\n\n'.join(current_content)
                    chunks.append({
                        'content': chunk_text,
                        'source': source,
                        'header': current_header.strip('#').strip(),
                        'size': len(chunk_text)
                    })
                
                # 开始新的块
                current_header = para
                current_content = []
            else:
                current_content.append(para)
        
        # 保存最后一个块
        if current_content:
            chunk_text = f"{current_header}\n\n" + '\n\n'.join(current_content)
            chunks.append({
                'content': chunk_text,
                'source': source,
                'header': current_header.strip('#').strip(),
                'size': len(chunk_text)
            })
        
        return chunks
    
    def split_text_by_size(self, text: str, source: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """按大小分割文本"""
        chunks = []
        
        # 使用tiktoken计算token数量
        tokens = self.encoding.encode(text)
        
        start = 0
        while start < len(tokens):
            end = start + chunk_size
            
            # 提取当前块的tokens
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append({
                'content': chunk_text,
                'source': source,
                'size': len(chunk_text),
                'token_count': len(chunk_tokens)
            })
            
            # 移动到下一个块，考虑重叠
            start = end - overlap
            
            # 如果剩余内容少于chunk_size，直接结束
            if start >= len(tokens):
                break
        
        return chunks
    
    def process_documents(self, use_header_splitting: bool = True) -> List[Dict[str, Any]]:
        """处理所有文档并返回分块结果"""
        documents = self.read_txt_files()
        all_chunks = []
        
        for doc in documents:
            if use_header_splitting:
                chunks = self.split_text_by_headers(doc['content'], doc['source'])
            else:
                chunks = self.split_text_by_size(doc['content'], doc['source'])
            
            all_chunks.extend(chunks)
            print(f"文档 {doc['source']} 分割为 {len(chunks)} 个块")
        
        print(f"总共生成 {len(all_chunks)} 个文本块")
        return all_chunks

if __name__ == "__main__":
    processor = DataProcessor()
    chunks = processor.process_documents()
    
    # 显示前几个块的示例
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n=== 块 {i+1} ===")
        print(f"来源: {chunk['source']}")
        print(f"大小: {chunk['size']} 字符")
        if 'header' in chunk:
            print(f"标题: {chunk['header']}")
        print(f"内容预览: {chunk['content'][:200]}...") 