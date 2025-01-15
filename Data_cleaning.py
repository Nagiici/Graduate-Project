import pandas as pd

# 读取数据
data_path = 'C:/Users/asdfadq/Desktop/Graduation_Project/Madrid_reviews.xlsx'  # 替换为完整数据集的路径
data = pd.read_excel(data_path)

# 数据清洗
def clean_data(data):
    # 删除无关列
    data = data.drop(columns=['Unnamed: 0', 'parse_count', 'review_id', 'url_restaurant', 'author_id'], errors='ignore')
    
    # 删除关键字段中的缺失值
    essential_columns = ['restaurant_name', 'review_full', 'rating_review']
    data = data.dropna(subset=essential_columns)
    
    # 删除重复的评论
    data = data.drop_duplicates(subset='review_full', keep='first')
    
    # 清理文本数据
    def clean_text(text):
        import re
        # 去掉HTML标签和特殊字符
        text = re.sub(r'<.*?>', '', text)  # 去HTML标签
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]', '', text)  # 保留字母和空格
        text = text.lower()  # 转小写
        return text

    # 对 'review_full' 列应用文本清理
    data['review_full'] = data['review_full'].apply(clean_text)
    
    # 重置索引
    data.reset_index(drop=True, inplace=True)
    
    return data

# 应用清理函数
cleaned_data = clean_data(data)

# 保存清理后的数据
output_path = 'cleaned_dataset.xlsx'
cleaned_data.to_excel(output_path, index=False)

print(f"清洗后的数据已保存到: {output_path}")
