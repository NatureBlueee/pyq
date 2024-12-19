from bs4 import BeautifulSoup
import re

def clean_html(html_content):
    """
    清洗HTML内容，只保留朋友圈文本
    :param html_content: HTML字符串
    :return: 清洗后的纯文本内容列表
    """
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除所有script和style标签
    for script in soup(["script", "style"]):
        script.decompose()
    
    # 找到所有朋友圈内容（在p2类中）
    content_elements = soup.find_all(class_="p2")
    
    cleaned_texts = []
    for element in content_elements:
        # 使用命名表达式优化文本处理
        if text := element.get_text(strip=True):
            # 清理多余的空白字符
            text = re.sub(r'\s+', ' ', text)
            cleaned_texts.append(text)
    
    return cleaned_texts

def process_html_file(file_path):
    """
    处理HTML文件
    :param file_path: HTML文件路径
    :return: 清洗后的文本内容列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return clean_html(html_content)
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return []

def save_to_txt(texts, output_file="cleaned_content.txt"):
    """
    将清洗后的文本保存到文件
    :param texts: 文本列表
    :param output_file: 输出文件名
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, text in enumerate(texts, 1):
                file.write(f"===== 朋友圈 {i} =====\n")
                file.write(text + "\n\n")
        print(f"内容已保存到 {output_file}")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")

if __name__ == "__main__":
    # 示例使用
    html_file = "index.html"
    cleaned_texts = process_html_file(html_file)
    
    # 打印提取的文本
    print("提取的文本内容：")
    for i, text in enumerate(cleaned_texts, 1):
        print(f"\n===== 朋友圈 {i} =====")
        print(text)
    
    # 保存到文件
    save_to_txt(cleaned_texts)