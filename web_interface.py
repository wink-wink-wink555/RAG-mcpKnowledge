#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP RAG系统 Web界面
基于FastAPI提供美观的Web界面，支持RAG知识库查询
"""

import sys
from pathlib import Path
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
from typing import Optional
import json

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from rag_system import RAGSystem
from config import *

# 创建FastAPI应用
app = FastAPI(title="MCP智能知识库助手")

# 创建全局RAG系统实例
rag_system = RAGSystem()


def get_web_interface():
    """生成RAG系统Web界面HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MCP智能知识库助手</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }

            body {
                font-family: 'Segoe UI', 'Microsoft YaHei', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                line-height: 1.6;
            }

            .container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }

            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 15px 20px;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }

            .header h1 {
                color: #2d3748;
                font-size: 1.8em;
                margin: 0;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .header p {
                color: #4a5568;
                margin: 5px 0 0 0;
                font-size: 0.9em;
            }

            .chat-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 20px;
                flex: 1;
                display: flex;
                flex-direction: column;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }

            .messages {
                flex: 1;
                overflow-y: auto;
                overflow-x: hidden;
                padding: 15px;
                margin-bottom: 15px;
                background: rgba(248, 250, 252, 0.5);
                border-radius: 15px;
                border: 1px solid rgba(226, 232, 240, 0.5);
                height: calc(100vh - 300px);
                min-height: 400px;
                max-height: calc(100vh - 300px);
                scroll-behavior: smooth;
            }

            .message {
                margin-bottom: 15px;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 85%;
                word-wrap: break-word;
                position: relative;
                animation: messageSlide 0.3s ease-out;
            }

            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .user-message {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                margin-left: auto;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                border-bottom-right-radius: 5px;
            }

            .assistant-message {
                background: linear-gradient(135deg, #f8fafc, #e2e8f0);
                color: #2d3748;
                margin-right: auto;
                border-left: 4px solid #667eea;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                border-bottom-left-radius: 5px;
                text-align: left;
                white-space: normal;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }

            .sources-info {
                background: rgba(102, 126, 234, 0.05);
                margin-top: 10px;
                border-radius: 10px;
                font-size: 0.9em;
                border: 1px solid rgba(102, 126, 234, 0.2);
                overflow: hidden;
            }

            .sources-header {
                background: rgba(102, 126, 234, 0.1);
                padding: 10px 12px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-weight: 600;
                color: #667eea;
                transition: all 0.3s ease;
            }

            .sources-header:hover {
                background: rgba(102, 126, 234, 0.15);
            }

            .sources-toggle {
                font-size: 0.9em;
                transition: all 0.3s ease;
                font-weight: bold;
            }

            .sources-content {
                padding: 12px;
                display: none;
                border-top: 1px solid rgba(102, 126, 234, 0.1);
            }

            .sources-content.show {
                display: block;
            }

            .input-form {
                display: flex;
                gap: 12px;
                align-items: flex-end;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
                padding: 15px;
                border-radius: 15px;
                border: 1px solid rgba(102, 126, 234, 0.2);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
            }

            .message-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid transparent;
                border-radius: 12px;
                background: white;
                font-size: 0.95em;
                resize: none;
                min-height: 44px;
                max-height: 120px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-family: inherit;
                line-height: 1.4;
            }

            .message-input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15), 0 4px 15px rgba(0, 0, 0, 0.15);
                transform: translateY(-1px);
            }

            .message-input::placeholder {
                color: #9ca3af;
                font-style: italic;
            }

            .send-button {
                width: 44px;
                height: 44px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                position: relative;
            }

            .send-button i {
                color: white;
                font-size: 16px;
            }

            .send-button:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
                background: linear-gradient(135deg, #5a67d8, #6b46c1);
            }

            .send-button:active:not(:disabled) {
                transform: translateY(0px);
                box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
            }

            .send-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
                background: linear-gradient(135deg, #9ca3af, #6b7280);
            }

            .loading {
                display: none;
                text-align: center;
                padding: 25px;
                margin: 15px 0;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                border-radius: 15px;
                border: 1px solid rgba(102, 126, 234, 0.2);
            }

            .loading.show { 
                display: block; 
            }

            .loading-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }

            .loading-text {
                color: #667eea;
                font-weight: 600;
                font-size: 1.2em;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .loading-spinner {
                width: 24px;
                height: 24px;
                border: 3px solid rgba(102, 126, 234, 0.2);
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            .example-questions {
                background: linear-gradient(135deg, rgba(248, 250, 252, 0.8), rgba(241, 245, 249, 0.8));
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                border: 1px solid rgba(226, 232, 240, 0.5);
                backdrop-filter: blur(5px);
            }

            .welcome-message {
                color: #4a5568;
                margin-bottom: 15px;
                font-size: 1em;
                line-height: 1.5;
                text-align: center;
                padding: 15px;
                background: rgba(255, 255, 255, 0.6);
                border-radius: 12px;
                border-left: 4px solid #667eea;
            }

            .example-questions h3 {
                color: #2d3748;
                margin-bottom: 15px;
                font-size: 1em;
                text-align: center;
                font-weight: 600;
            }

            .examples-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }

            .example-item {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
                border-radius: 10px;
                padding: 12px 16px;
                cursor: pointer;
                transition: all 0.3s ease;
                border-left: 3px solid #667eea;
                font-size: 0.9em;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(226, 232, 240, 0.3);
                text-align: center;
            }

            .example-item:hover {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }

                        .assistant-message h1 {
                font-size: 1.4em;
                color: #2d3748;
                margin: 15px 0 10px 0;
                font-weight: 700;
            }
            
            .assistant-message h2 {
                font-size: 1.2em;
                color: #2d3748;
                margin: 12px 0 8px 0;
                font-weight: 600;
            }
            
            .assistant-message h3 {
                font-size: 1.1em;
                color: #2d3748;
                margin: 10px 0 6px 0;
                font-weight: 600;
            }
            
            .assistant-message h4 {
                font-size: 1.05em;
                color: #2d3748;
                margin: 8px 0 4px 0;
                font-weight: 600;
            }
            
            .assistant-message p {
                margin: 10px 0;
                line-height: 1.6;
                text-align: left;
                padding: 0;
                text-indent: 0;
            }
            
            .assistant-message strong {
                color: #2d3748;
                font-weight: 600;
            }
            
            /* 自定义列表样式 */
            .custom-list {
                list-style: none;
                padding-left: 0;
                margin: 15px 0;
            }
            
            .custom-list li {
                margin: 8px 0;
                position: relative;
                line-height: 1.6;
                display: block;
            }
            
            .main-item {
                font-weight: 600;
                color: #2d3748;
                font-size: 1.05em;
                margin: 12px 0;
                padding-left: 20px;
            }
            
            .sub-item {
                font-weight: 400;
                color: #4a5568;
                font-size: 0.95em;
                margin: 6px 0;
                padding-left: 35px;
            }
            
            .main-item::before {
                content: '';
                position: absolute;
                left: 5px;
                top: 0.6em;
                width: 6px;
                height: 6px;
                background: #667eea;
                border-radius: 50%;
            }
            
            .sub-item::before {
                content: '';
                position: absolute;
                left: 20px;
                top: 0.6em;
                width: 4px;
                height: 4px;
                background: #a0aec0;
                border-radius: 50%;
            }
            
            .assistant-message a {
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
            }
            
            .assistant-message a:hover {
                text-decoration: underline;
            }
            
            .assistant-message p {
                margin: 8px 0;
                line-height: 1.6;
            }
            
            .assistant-message ul, .assistant-message ol {
                margin: 8px 0;
                padding-left: 20px;
            }
            
            .assistant-message li {
                margin: 4px 0;
                line-height: 1.5;
            }
            
            .assistant-message blockquote {
                border-left: 4px solid #667eea;
                margin: 10px 0;
                padding: 10px 15px;
                background: rgba(102, 126, 234, 0.05);
                border-radius: 0 8px 8px 0;
            }
            
            .assistant-message code {
                background: rgba(102, 126, 234, 0.1);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }
            
            .code-block {
                background: rgba(45, 55, 72, 0.05);
                border-radius: 8px;
                margin: 10px 0;
                border: 1px solid rgba(226, 232, 240, 0.5);
                position: relative;
            }
            
            .code-header {
                background: rgba(102, 126, 234, 0.1);
                padding: 8px 12px;
                border-bottom: 1px solid rgba(226, 232, 240, 0.3);
                border-radius: 8px 8px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .code-language {
                font-weight: bold;
                color: #2d3748;
                font-size: 0.9em;
                text-transform: uppercase;
            }
            
            .copy-button {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .copy-button:hover {
                background: linear-gradient(135deg, #5a67d8, #6b46c1);
                transform: translateY(-1px);
            }
            
            .copy-button:active {
                transform: translateY(0);
            }
            
            .copy-button.copied {
                background: linear-gradient(135deg, #48bb78, #38a169);
            }
            
            .assistant-message pre {
                background: none;
                padding: 12px;
                margin: 0;
                border-radius: 0 0 8px 8px;
                overflow-x: auto;
                line-height: 1.3;
            }
            
            .assistant-message pre code {
                background: none;
                padding: 0;
                border-radius: 0;
                line-height: 1.3;
                white-space: pre;
            }

            /* 响应式设计 */
            @media (max-width: 768px) {
                .container {
                    padding: 10px;
                }

                .header h1 {
                    font-size: 1.5em;
                }

                .message {
                    max-width: 95%;
                    padding: 12px 15px;
                }

                .examples-grid {
                    grid-template-columns: 1fr;
                    gap: 8px;
                }

                .input-form {
                    flex-direction: column;
                    gap: 12px;
                    padding: 12px;
                }

                .message-input {
                    min-height: 40px;
                }

                .send-button {
                    width: 100%;
                    height: 44px;
                }

                .messages {
                    height: calc(100vh - 340px);
                }
            }

            /* 滚动条美化 */
            .messages::-webkit-scrollbar {
                width: 6px;
            }

            .messages::-webkit-scrollbar-track {
                background: rgba(226, 232, 240, 0.3);
                border-radius: 3px;
            }

            .messages::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 3px;
            }

            .messages::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a67d8, #6b46c1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 MCP智能知识库助手</h1>
            </div>

            <div class="chat-container">
                <div class="messages" id="messages">
                    <div class="example-questions">
                        <div class="welcome-message">
                            👋 欢迎使用基于RAG和Qwen的MCP智能知识库助手！
                            <br><br>
                            <em>注：如果您的问题不包含在知识库中，大模型可能无法回答。</em>
                        </div>
                        <h3>💡 试试这些问题：</h3>
                        <div class="examples-grid">
                            <div class="example-item" onclick="askExample('什么是MCP？')">
                                🤔 什么是MCP？
                            </div>
                            <div class="example-item" onclick="askExample('MCP协议的主要功能是什么？')">
                                🔧 MCP协议功能
                            </div>
                            <div class="example-item" onclick="askExample('如何使用MCP进行开发？')">
                                💻 MCP开发指南
                            </div>
                            <div class="example-item" onclick="askExample('MCP的架构是怎样的？')">
                                🏗️ MCP架构设计
                            </div>
                        </div>
                    </div>
                </div>

                <div class="loading" id="loading">
                    <div class="loading-content">
                        <div class="loading-text">
                            <div class="loading-spinner"></div>
                            <span>正在生成回答...</span>
                        </div>
                    </div>
                </div>

                <form class="input-form" onsubmit="return submitForm(event)">
                    <textarea 
                        id="messageInput" 
                        class="message-input" 
                        placeholder="问我任何关于MCP协议的问题，我会基于知识库为您提供准确回答..."
                        rows="2"
                        onkeydown="handleKeyPress(event)"
                    ></textarea>
                    <button type="submit" class="send-button" id="sendButton">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>

<script>
function askExample(text) {
    document.getElementById('messageInput').value = text;
    submitMessage();
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        submitMessage();
    }
}

function submitForm(event) {
    event.preventDefault();
    submitMessage();
    return false;
}

async function submitMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';
    showLoading(true);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'message=' + encodeURIComponent(message)
        });

        if (response.ok) {
            const result = await response.json();
            addMessage(result.message, 'assistant', result.sources);
        } else {
            addMessage('抱歉，发生了错误，请稍后重试。', 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('网络连接错误，请检查网络后重试。', 'assistant');
    } finally {
        showLoading(false);
    }
}

function parseMarkdown(text) {
    // 首先对文本进行彻底的清理
    let result = text;
    
    // 将文本按行分割，逐行处理
    let initialLines = result.split('\\n');
    let cleanedLines = [];
    
    for (let i = 0; i < initialLines.length; i++) {
        let line = initialLines[i];
        
        // 完全清理行首的空格和制表符
        line = line.replace(/^[\\s\\t]+/, '');
        
        // 如果不是空行，就添加到结果中
        if (line.trim().length > 0) {
            cleanedLines.push(line);
        }
    }
    
    // 重新组合文本
    result = cleanedLines.join('\\n');
    
    // 先处理代码块，保护其中的内容不被其他规则处理
    let codeBlocks = [];
    let codeBlockIndex = 0;
    
    // 提取代码块并用占位符替换
    result = result.replace(/```(\\w+)?([\\s\\S]*?)```/g, function(match, language, content) {
        let placeholder = `__CODEBLOCK_${codeBlockIndex}__`;
        let lang = language || 'code';
        let codeId = `code-${Date.now()}-${codeBlockIndex}`;
        
        codeBlocks[codeBlockIndex] = `
            <div class="code-block">
                <div class="code-header">
                    <span class="code-language">${lang}</span>
                    <button class="copy-button" onclick="copyCode('${codeId}')">
                        <i class="fas fa-copy"></i>
                        复制
                    </button>
                </div>
                <pre><code id="${codeId}">${content}</code></pre>
            </div>
        `;
        codeBlockIndex++;
        return placeholder;
    });
    
    // 处理标题（现在代码块已经被保护）
    result = result.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
    result = result.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    result = result.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    result = result.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // 处理粗体
    result = result.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
    
    // 处理斜体
    result = result.replace(/\\*(.+?)\\*/g, '<em>$1</em>');
    
    // 处理行内代码
    result = result.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // 处理链接
    result = result.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // 处理列表项 - 更精确的方法
    let listLines = result.split('\\n');
    let processedLines = [];
    let inList = false;
    
    for (let j = 0; j < listLines.length; j++) {
        let currentLine = listLines[j];
        
        // 检查是否是有序列表项
        if (/^\\d+\\.\\s*(.+)$/.test(currentLine)) {
            let content = currentLine.replace(/^\\d+\\.\\s*/, '').trim();
            if (!inList) {
                processedLines.push('<ul class="custom-list">');
                inList = true;
            }
            processedLines.push('<li class="main-item">' + content + '</li>');
        }
        // 检查是否是无序列表项
        else if (/^[-*+]\\s*(.+)$/.test(currentLine)) {
            let content = currentLine.replace(/^[-*+]\\s*/, '').trim();
            if (!inList) {
                processedLines.push('<ul class="custom-list">');
                inList = true;
            }
            processedLines.push('<li class="sub-item">' + content + '</li>');
        }
        // 不是列表项
        else {
            if (inList) {
                processedLines.push('</ul>');
                inList = false;
            }
            processedLines.push(currentLine);
        }
    }
    
    // 如果最后还在列表中，关闭列表
    if (inList) {
        processedLines.push('</ul>');
    }
    
    result = processedLines.join('\\n');
    
    // 处理引用
    result = result.replace(/^>\\s*(.+)$/gm, '<blockquote>$1</blockquote>');
    
    // 处理段落（将连续的文本包装在p标签中）
    result = result.replace(/^(?!<[h|u|o|b|p|d])(.+)$/gm, function(match, content) {
        return '<p>' + content.trim() + '</p>';
    });
    
    // 清理多余的p标签
    result = result.replace(/<p><\\/p>/g, '');
    result = result.replace(/<p>(<h[1-6]>.*<\\/h[1-6]>)<\\/p>/g, '$1');
    result = result.replace(/<p>(<ul.*<\\/ul>)<\\/p>/g, '$1');
    result = result.replace(/<p>(<blockquote>.*<\\/blockquote>)<\\/p>/g, '$1');
    result = result.replace(/<p>(<pre>.*<\\/pre>)<\\/p>/g, '$1');
    
    // 最后恢复代码块
    for (let k = 0; k < codeBlocks.length; k++) {
        result = result.replace(`__CODEBLOCK_${k}__`, codeBlocks[k]);
    }
    
    return result;
}

function addMessage(content, sender, sources) {
    const messages = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    let html = '';
    if (sender === 'assistant') {
        html = `<div>${parseMarkdown(content)}</div>`;
    } else {
        html = `<div>${content}</div>`;
    }
    
    if (sources && sources.length > 0) {
        const sourcesId = 'sources-' + Date.now();
        html += `
            <div class="sources-info">
                <div class="sources-header" onclick="toggleSources('${sourcesId}')">
                    <span>📚 参考来源 (${sources.length}个)</span>
                    <span class="sources-toggle" id="toggle-${sourcesId}">▼</span>
                </div>
                <div class="sources-content" id="${sourcesId}">`;
        
        for (let i = 0; i < sources.length; i++) {
            const source = sources[i];
            html += `<div>• <strong>${source.source}</strong> (相似度: ${(source.similarity * 100).toFixed(1)}%)`;
            if (source.header) {
                html += `<br>&nbsp;&nbsp;&nbsp;&nbsp;标题: ${source.header}`;
            }
            html += `</div>`;
        }
        
        html += `
                </div>
            </div>`;
    }
    
    messageDiv.innerHTML = html;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function toggleSources(sourcesId) {
    const content = document.getElementById(sourcesId);
    const toggle = document.getElementById('toggle-' + sourcesId);

    if (content.classList.contains('show')) {
        content.classList.remove('show');
        toggle.classList.remove('expanded');
        toggle.textContent = '▼';
    } else {
        content.classList.add('show');
        toggle.classList.add('expanded');
        toggle.textContent = '▲';
    }
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    const sendButton = document.getElementById('sendButton');

    if (show) {
        loading.classList.add('show');
        sendButton.disabled = true;
    } else {
        loading.classList.remove('show');
        sendButton.disabled = false;
    }
}

function copyCode(codeId) {
    const codeElement = document.getElementById(codeId);
    const button = event.target.closest('.copy-button');
    
    if (codeElement) {
        const text = codeElement.textContent;
        
        // 使用现代的 Clipboard API
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showCopySuccess(button);
            }).catch(() => {
                // 降级到传统方法
                fallbackCopyText(text, button);
            });
        } else {
            // 降级到传统方法
            fallbackCopyText(text, button);
        }
    }
}

function fallbackCopyText(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(button);
    } catch (err) {
        console.error('复制失败:', err);
    } finally {
        document.body.removeChild(textArea);
    }
}

function showCopySuccess(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> 已复制';
    button.classList.add('copied');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('copied');
    }, 2000);
}
</script>
    </body>
    </html>
    """
    return html_content


@app.get("/", response_class=HTMLResponse)
async def index():
    """主页面 - RAG对话界面"""
    return get_web_interface()


@app.post("/chat")
async def chat(message: str = Form(...)):
    """处理聊天请求 - RAG系统查询"""
    try:
        # 检查知识库状态
        info = rag_system.get_knowledge_base_info()

        # 如果知识库为空，先构建知识库
        if info.get('document_count', 0) == 0:
            print("知识库为空，开始构建...")
            success = rag_system.build_knowledge_base()
            if not success:
                return {
                    "success": False,
                    "message": "知识库构建失败，请检查配置和依赖。",
                    "sources": []
                }

        # 生成回答
        result = rag_system.generate_response(message)

        if result['success']:
            return {
                "success": True,
                "message": result['response'],
                "sources": result['sources']
            }
        else:
            return {
                "success": False,
                "message": result.get('response', '抱歉，无法生成回答。'),
                "sources": []
            }

    except Exception as e:
        print(f"❌ RAG聊天处理失败: {str(e)}")
        return {
            "success": False,
            "message": f"抱歉，处理您的请求时出现错误: {str(e)}",
            "sources": []
        }


@app.get("/info")
async def get_info():
    """获取知识库信息"""
    try:
        info = rag_system.get_knowledge_base_info()
        return {
            "success": True,
            "info": info
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """主函数 - 启动Web界面"""
    print("🚀 启动MCP知识库RAG系统Web界面...")
    print("🧠 基于阿里云百炼Qwen3-Embedding + 千问2.5-72B")
    print("📚 知识库: MCP协议相关文档")
    print("🌐 访问地址: http://localhost:8000")
    print("💡 功能: 智能问答、向量检索、知识库管理")
    print()

    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()