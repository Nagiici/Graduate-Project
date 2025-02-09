from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from datasets import Dataset

# 加载预处理好的数据
file_path = 'C:/Users/asdfa/Desktop/毕业设计/Graduation_Design/preprocessed_reviews.xlsx'  # 替换为你的实际文件路径
preprocessed_data = pd.read_excel(file_path)

# 确保所有列的数据类型一致
preprocessed_data = preprocessed_data.astype({
    'restaurant_name': 'str',
    'rating_review': 'int',  # 如果是整数类型可以保持不变
    'sample': 'str',
    'title_review': 'str',
    'review_preview': 'str',
    'review_full': 'str',
    'date': 'str',  # 如果是日期类型可以转换为字符串
    'city': 'str',
    'processed_review': 'str'  # 确保文本列为字符串
})

# 检查数据结构
print("数据概览:")
print(preprocessed_data.head())

# --------------------------------------------
# 数据分析：词频统计与可视化
# --------------------------------------------

# 定义词频统计函数
def get_common_words(text_column, num_words=20):
    # 将非字符串类型的值转换为空字符串
    text_column = text_column.fillna('').astype(str)
    all_words = ' '.join(text_column).split()
    word_counts = Counter(all_words)
    return word_counts.most_common(num_words)

# 绘制词频图
common_words = get_common_words(preprocessed_data['processed_review'])
words, counts = zip(*common_words)
plt.figure(figsize=(10, 6))
plt.bar(words, counts)
plt.title("Top 20 Most Common Words in Reviews")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

# --------------------------------------------
# 文本摘要生成：使用 Hugging Face Dataset
# --------------------------------------------

# 初始化 HuggingFace 的生成式摘要模型（使用 BART）
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn", device=0)  # device=0 表示使用 GPU

# 将 Pandas DataFrame 转换为 Hugging Face Dataset
preprocessed_data['processed_review'] = preprocessed_data['processed_review'].fillna('').astype(str)
hf_dataset = Dataset.from_pandas(preprocessed_data)

# 定义生成摘要的函数
def generate_summary(batch):
    # 使用 pipeline 处理批量数据
    results = summarizer(batch['processed_review'], max_length=50, min_length=25, truncation=True)  # 调整 max_length 和 min_length
    batch['summary'] = [result['summary_text'] for result in results]
    return batch

# 使用 dataset.map 批量生成摘要
print("开始生成摘要...")
hf_dataset = hf_dataset.map(generate_summary, batched=True, batch_size=32)  # 调整 batch_size 以适应 BART 的计算需求

# 将结果转换回 Pandas DataFrame 并保存
result_df = hf_dataset.to_pandas()
output_file = 'C:/Users/asdfa/Desktop/毕业设计/Graduation_Design/summaries_dataset_bart.xlsx'
result_df.to_excel(output_file, index=False)

print(f"生成式摘要已保存到: {output_file}")