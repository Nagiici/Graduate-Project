from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_caching import Cache
import pandas as pd
from pathlib import Path
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# 配置日志
logging.basicConfig(level=logging.INFO)

# 优化数据加载
@cache.cached(timeout=3600, key_prefix='restaurant_data')
def load_data():
    data_path = Path("C:/Users/asdfa/Desktop/毕业设计/Graduation_Design/summaries_dataset.xlsx")
    if not data_path.exists():
        logging.error(f"数据文件不存在: {data_path}")
        raise FileNotFoundError(f"数据文件不存在: {data_path}")
    data = pd.read_excel(data_path)
    
    # 数据增强
    data['review_date'] = pd.to_datetime(data['date'], errors='coerce')
    data['review_year'] = data['review_date'].dt.year
    data['review_month'] = data['review_date'].dt.month_name()
    
    # 类型转换
    conversions = {
        'restaurant_name': 'str',
        'rating_review': 'float',  # 修改为 float 以便后续计算平均值
        'sample': 'str',
        'title_review': 'str',
        'review_preview': 'str',
        'review_full': 'str',
        'date': 'str',
        'city': 'str',
        'processed_review': 'str',
        'summary': 'str'
    }
    try:
        data = data.astype(conversions, errors='ignore')
    except Exception as e:
        logging.warning(f"数据类型转换警告: {e}")
    return data

# 公共数据加载
data = load_data()

# 静态文件路由
@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

# API路由
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """获取所有餐厅名称（去重后返回）"""
    try:
        restaurant_names = data['restaurant_name'].dropna().unique().tolist()
        return jsonify(sorted(restaurant_names))
    except Exception as e:
        logging.error(f"Error in get_restaurants: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restaurant_details', methods=['GET'])
def get_restaurant_details():
    """获取餐厅详细信息"""
    try:
        restaurant_name = request.args.get('name')
        if not restaurant_name:
            return jsonify({'error': 'Missing restaurant name'}), 400

        filtered = data[data['restaurant_name'] == restaurant_name]
        if filtered.empty:
            return jsonify({'error': 'Restaurant not found'}), 404

        response = {
            'average_rating': round(filtered['rating_review'].mean(), 2),
            'summaries': filtered['summary'].dropna().tolist()
        }
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in get_restaurant_details: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sorted_restaurants', methods=['GET'])
def get_sorted_restaurants():
    """获取排序后的餐厅列表"""
    try:
        grouped = data.groupby('restaurant_name', observed=True).agg({
            'rating_review': 'mean',
            'summary': 'first'
        }).reset_index()
        
        sorted_data = grouped.sort_values(by='rating_review', ascending=False)
        sorted_data['rating_review'] = sorted_data['rating_review'].round(2)
        
        return jsonify(sorted_data.to_dict(orient='records'))
    except Exception as e:
        logging.error(f"Error in get_sorted_restaurants: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 创建必要目录
    Path("static/js").mkdir(parents=True, exist_ok=True)
    Path("static/css").mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
