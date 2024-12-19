from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from html_cleaner import clean_html
import re
from datetime import datetime
from bs4 import BeautifulSoup
import logging
import tempfile

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

def extract_date(html_content, element):
    """从HTML内容中提取日期"""
    try:
        # 首先尝试从元素的父级查找日期
        parent = element.parent
        if parent:
            date_element = parent.find(class_="time")
            if date_element and date_element.string:
                logger.debug(f"从time类中提取到日期: {date_element.string.strip()}")
                return date_element.string.strip()
        
        # 如果没找到，尝试在整个文档中查找日期模式
        date_pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'
        matches = re.findall(date_pattern, html_content)
        if matches:
            logger.debug(f"从文本中提取到日期: {matches[0]}")
            return matches[0]
        
        # 如果还是没找到，返回当前时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.warning(f"未找到日期，使用当前时间: {current_time}")
        return current_time
    except Exception as e:
        logger.error(f"提取日期时出错: {str(e)}")
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def process_html_content(html_content):
    """处理HTML内容并返回带日期的文本列表"""
    try:
        logger.info("开始处理HTML内容")
        results = []
        texts = clean_html(html_content)
        logger.debug(f"清洗后得到 {len(texts)} 条文本")
        
        # 创建BeautifulSoup对象用于提取日期
        soup = BeautifulSoup(html_content, 'html.parser')
        content_elements = soup.find_all(class_="p2")
        logger.debug(f"找到 {len(content_elements)} 个p2类元素")
        
        # 如果找到了内容元素，使用它们来提取日期
        if content_elements:
            for i, (element, text) in enumerate(zip(content_elements, texts)):
                if text.strip():  # 确保文本不为空
                    date = extract_date(html_content, element)
                    results.append({
                        'date': date,
                        'content': text.strip()
                    })
                    logger.debug(f"处理第 {i+1} 条内容: {date}")
        else:
            logger.warning("未找到p2类元素，使用纯文本处理")
            # 如果没有找到内容元素，只处理文本
            for i, text in enumerate(texts):
                if text.strip():  # 确保文本不为空
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    results.append({
                        'date': current_time,
                        'content': text.strip()
                    })
                    logger.debug(f"处理第 {i+1} 条纯文本内容")
        
        # 按日期排序
        results.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        logger.info(f"成功处理 {len(results)} 条内容")
        return results
    except Exception as e:
        logger.error(f"处理HTML内容时出错: {str(e)}", exc_info=True)
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("收到文件上传请求")
    
    if 'file' not in request.files:
        logger.error("请求中没有文件")
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.error("文件名为空")
        return jsonify({'error': '没有选择文件'}), 400
    
    if not file.filename.endswith('.html'):
        logger.error(f"文件类型错误: {file.filename}")
        return jsonify({'error': '请上传HTML文件'}), 400
    
    try:
        # 读取文件内容
        logger.info(f"开始读取文件: {file.filename}")
        html_content = file.read().decode('utf-8')
        logger.debug(f"成功读取文件，内容长度: {len(html_content)}")
        
        # 处理HTML内容
        results = process_html_content(html_content)
        
        if not results:
            logger.warning("未能提取到任何内容")
            return jsonify({'error': '未能从文件中提取到任何内容'}), 400
        
        logger.info(f"成功处理文件，返回 {len(results)} 条结果")
        return jsonify({'results': results})
    
    except UnicodeDecodeError:
        logger.error("文件编码错误", exc_info=True)
        return jsonify({'error': '文件编码错误，请确保文件为UTF-8编码'}), 400
    except Exception as e:
        logger.error(f"处理文件时出错: {str(e)}", exc_info=True)
        return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500

# Vercel 需要的 WSGI 应用
app.debug = False 