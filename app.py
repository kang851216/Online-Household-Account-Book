from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# JSON 파일 경로
DATA_FILE = 'data.json'
TARGET_FILE = 'target.json'  # 목표 금액 파일

# 기본 카테고리
DEFAULT_CATEGORIES = ['식생활', '외식', '헌금', '교육', '교통비', '대접비', '공과금', '기타', '월세']

def load_data():
    """JSON 파일에서 데이터 로드"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'entries' not in data:
                    data = {'entries': data, 'categories': DEFAULT_CATEGORIES}
                if 'categories' not in data:
                    data['categories'] = DEFAULT_CATEGORIES
                # categories에 월세가 없으면 추가
                if '월세' not in data['categories']:
                    data['categories'].append('월세')
                return data
        except:
            return {'entries': [], 'categories': DEFAULT_CATEGORIES}
    return {'entries': [], 'categories': DEFAULT_CATEGORIES}

def save_data(data):
    """JSON 파일에 데이터 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_targets():
    """target.json 파일에서 목표 금액 로드"""
    if os.path.exists(TARGET_FILE):
        try:
            with open(TARGET_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_targets(targets):
    """target.json 파일에 목표 금액 저장"""
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        json.dump(targets, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """모든 가계부 데이터 조회"""
    data = load_data()
    return jsonify({
        'entries': data['entries'],
        'categories': data['categories']
    })

@app.route('/api/entries', methods=['POST'])
def add_entry():
    """새 가계부 항목 추가"""
    new_entry = request.json
    data = load_data()
    
    # ID 생성
    if data['entries']:
        new_entry['id'] = max(e['id'] for e in data['entries']) + 1
    else:
        new_entry['id'] = 1
    
    data['entries'].append(new_entry)
    save_data(data)
    return jsonify(new_entry), 201

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """가계부 항목 수정"""
    updated_entry = request.json
    data = load_data()
    
    for i, entry in enumerate(data['entries']):
        if entry['id'] == entry_id:
            updated_entry['id'] = entry_id
            data['entries'][i] = updated_entry
            save_data(data)
            return jsonify(updated_entry)
    
    return jsonify({'error': 'Entry not found'}), 404

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """가계부 항목 삭제"""
    data = load_data()
    
    for i, entry in enumerate(data['entries']):
        if entry['id'] == entry_id:
            del data['entries'][i]
            save_data(data)
            return jsonify({'message': 'Deleted successfully'})
    
    return jsonify({'error': 'Entry not found'}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """카테고리 목록 조회"""
    data = load_data()
    return jsonify(data['categories'])

@app.route('/api/categories', methods=['POST'])
def add_category():
    """새 카테고리 추가"""
    new_category = request.json.get('category')
    data = load_data()
    
    if new_category and new_category not in data['categories']:
        data['categories'].append(new_category)
        save_data(data)
        return jsonify({'categories': data['categories']}), 201
    
    return jsonify({'error': 'Category already exists or invalid'}), 400

@app.route('/api/goals', methods=['GET'])
def get_goals():
    """목표 금액 조회 (target.json에서 로드)"""
    targets = load_targets()
    return jsonify(targets)

@app.route('/api/goals', methods=['POST'])
def update_goals():
    """목표 금액 저장 (target.json에 저장)"""
    goals = request.json
    save_targets(goals)
    return jsonify(goals), 200

if __name__ == '__main__':
    # data.json 파일이 없으면 생성
    if not os.path.exists(DATA_FILE):
        sample_data = {
            'entries': [
                {'id': 1, 'date': '2025-02-15', 'category': '외식', 'detail': '스시 오마카세', 'amount': 380, 'payment': '신용카드', 'payer': '윤지현', 'remark': '일식당'},
                {'id': 2, 'date': '2025-02-10', 'category': '교통비', 'detail': '택시', 'amount': 75, 'payment': '현금', 'payer': '강경민', 'remark': '출장'},
                {'id': 3, 'date': '2025-01-25', 'category': '헌금', 'detail': '주일헌금', 'amount': 500, 'payment': '현금', 'payer': '윤지현', 'remark': ''},
                {'id': 4, 'date': '2025-02-18', 'category': '대접비', 'detail': '친구 식사대접', 'amount': 450, 'payment': '신용카드', 'payer': '강경민', 'remark': ''},
                {'id': 5, 'date': '2025-02-20', 'category': '공과금', 'detail': '전기세', 'amount': 280, 'payment': '신용카드', 'payer': '윤지현', 'remark': '2월 청구'}
            ],
            'categories': DEFAULT_CATEGORIES
        }
        save_data(sample_data)
    
    # target.json 파일이 없으면 생성
    if not os.path.exists(TARGET_FILE):
        sample_targets = {}
        save_targets(sample_targets)
    
    app.run(debug=True, host='0.0.0.0', port=5000)