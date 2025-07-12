#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP智能知识库助手
使用RAG技术对阿里云百炼大模型进行MCP知识库扩充

作者: wink-wink-wink555
"""

from rag_system import RAGSystem
import argparse

def main():
    parser = argparse.ArgumentParser(description='MCP智能知识库助手')
    parser.add_argument('--rebuild', action='store_true', help='重新构建知识库')
    parser.add_argument('--info', action='store_true', help='显示知识库信息')
    
    args = parser.parse_args()
    
    # 显示系统信息
    print("="*60)
    print("MCP智能知识库助手")
    print("="*60)
    print("使用RAG技术对阿里云百炼大模型进行MCP知识库扩充")
    print("作者: wink-wink-wink555")
    print("="*60)
    
    # 处理命令行参数
    if args.info:
        rag = RAGSystem()
        info = rag.get_knowledge_base_info()
        print(f"知识库信息: {info}")
        return
    
    if args.rebuild:
        rag = RAGSystem()
        print("重新构建知识库...")
        success = rag.build_knowledge_base(clear_existing=True)
        if success:
            print("知识库重建完成")
        else:
            print("知识库重建失败")
        return
    
    # 默认启动Web界面
    print("🚀 启动Web界面...")
    try:
        from web_interface import main as web_main
        web_main()
    except ImportError as e:
        print(f"❌ 启动Web界面失败: {e}")
        print("请确保已安装FastAPI和uvicorn: pip install fastapi uvicorn[standard]")

if __name__ == "__main__":
    main()