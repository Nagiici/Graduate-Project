import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# 下载 NLTK 数据
nltk.download('punkt')
nltk.download('stopwords')

# 加载清洗后的数据
file_path = 'C:/Users/asdfadq/Desktop/Graduation_Project/cleaned_dataset.xlsx'  # 替换为你的文件路径
cleaned_data = pd.read_excel(file_path)

# 定义英语的停用词
stop_words = set(stopwords.words('english'))

# 定义文本预处理函数
def preprocess_text(text):
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
