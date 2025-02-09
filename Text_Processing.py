import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# 指定 NLTK 的数据存储目录
nltk.data.path.append(r'C:/Users/asdfadq/Desktop/Graduation_Design/nltk_data')

# 确保 punkt 和 stopwords 已经下载
nltk.download('punkt', download_dir=r'C:/Users/asdfadq/Desktop/Graduation_Design/nltk_data')
nltk.download('stopwords', download_dir=r'C:/Users/asdfadq/Desktop/Graduation_Design/nltk_data')
nltk.download('punkt_tab', download_dir=r'C:/Users/asdfadq/Desktop/Graduation_Design/nltk_data')

# 加载清洗后的数据
file_path = 'C:/Users/asdfadq/Desktop/Graduation_Design/cleaned_dataset.xlsx'
cleaned_data = pd.read_excel(file_path)

# 定义英语的停用词
stop_words = set(stopwords.words('english'))

# 定义文本预处理函数
def preprocess_text(text):
    if not isinstance(text, str):  # 确保处理的文本是字符串
        return ''
    # 去掉特殊字符和数字，仅保留字母
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()  # 转换为小写
    tokens = word_tokenize(text)  # 分词
    tokens = [word for word in tokens if word not in stop_words]  # 去停用词
    return ' '.join(tokens)

# 对 'review_full' 列进行预处理
cleaned_data['processed_review'] = cleaned_data['review_full'].apply(preprocess_text)

# 保存预处理后的数据
output_path = 'preprocessed_reviews.xlsx'
cleaned_data.to_excel(output_path, index=False)

print(f"预处理完成的数据已保存到: {output_path}")

