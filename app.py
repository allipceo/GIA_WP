<<<<<<< HEAD
from flask import Flask, jsonify, request
import json
from datetime import datetime
from time_sync import get_korea_time
from data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

@app.route('/')
def home():
    return """
    <h1>🎉 AICU 시즌2 시작!</h1>
    <h2>서대리 첫 번째 임무 완료</h2>
    <p>시간: 2025년 8월 1일 23:30 KST</p>
    <p><a href="/api/status">API 상태 확인</a></p>
    <p><a href="/api/info">프로젝트 정보</a></p>
    <p><a href="/api/v1/time">실시간 한국시간</a></p>
    <p><a href="/api/v1/health">시스템 상태</a></p>
    <p><a href="/api/v1/categories">카테고리 목록</a></p>
    """

@app.route('/api/status')
def status():
    time_info = get_korea_time()
    return jsonify({
        "status": "✅ 정상 작동",
        "version": "ACIU 시즌2 V1.0",
        "timestamp": time_info['formatted'],
        "message": "서대리 환경 설정 완료!"
    })

@app.route('/api/info')
def info():
    time_info = get_korea_time()
    return jsonify({
        "project": "AICU 퀴즈앱 시즌2",
        "tech_stack": ["Python", "Flask", "JSON", "Heroku"],
        "team": {
            "조대표": "총괄",
            "나실장": "기획팀장 (코코치)",
            "노팀장": "기술팀장 (Claude)",
            "서대리": "개발팀장 (Cursor AI)"
        },
        "current_phase": "개발 착수",
        "branch": "season1-a",
        "timestamp": time_info['formatted']
    })

@app.route('/api/v1/time')
def get_current_time():
    """실시간 한국시간 API"""
    time_info = get_korea_time()
    return jsonify({
        "status": "success",
        "data": {
            "current_time": time_info['formatted'],
            "iso_format": time_info['iso'],
            "timestamp": time_info['timestamp']
        }
    })

# 1. GET /api/v1/categories
@app.route('/api/v1/categories')
def get_categories():
    """카테고리 목록 및 메타데이터"""
    time_info = get_korea_time()
    
    categories = {
        "property_insurance": {
            "display_name": "재산보험",
            "question_count": len(data_manager.get_questions_by_category('property_insurance')),
            "icon": "🏢",
            "color_code": "#3B82F6"
        },
        "specialty_insurance": {
            "display_name": "특종보험",
            "question_count": len(data_manager.get_questions_by_category('specialty_insurance')),
            "icon": "🚗", 
            "color_code": "#10B981"
        },
        "liability_insurance": {
            "display_name": "배상책임보험",
            "question_count": len(data_manager.get_questions_by_category('liability_insurance')),
            "icon": "⚖️",
            "color_code": "#F59E0B"
        },
        "marine_insurance": {
            "display_name": "해상보험",
            "question_count": len(data_manager.get_questions_by_category('marine_insurance')),
            "icon": "🚢",
            "color_code": "#8B5CF6"
        }
    }
    
    return jsonify({
        "status": "success",
        "data": {
            "categories": categories,
            "total_questions": 1379,
            "total_categories": 4
        },
        "timestamp": time_info['formatted']
    })

# 2. GET /api/v1/questions/<category>
@app.route('/api/v1/questions/<category>')
def get_questions_by_category_api(category):
    """카테고리별 문제 목록"""
    time_info = get_korea_time()
    
    # 쿼리 파라미터
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    shuffle = request.args.get('shuffle', False, type=bool)
    
    questions = data_manager.get_questions_by_category(category)
    
    if not questions:
        return jsonify({
            "status": "error",
            "message": f"Category '{category}' not found",
            "timestamp": time_info['formatted']
        }), 404
    
    # 셔플 처리
    if shuffle:
        import random
        random.shuffle(questions)
    
    # 페이지네이션
    paginated_questions = questions[offset:offset+limit]
    
    return jsonify({
        "status": "success",
        "data": {
            "category": category,
            "questions": paginated_questions,
            "pagination": {
                "total": len(questions),
                "limit": limit,
                "offset": offset,
                "has_next": offset + limit < len(questions)
            }
        },
        "timestamp": time_info['formatted']
    })

# 3. GET /api/v1/question/<id>
@app.route('/api/v1/question/<question_id>')
def get_single_question(question_id):
    """개별 문제 상세 조회"""
    time_info = get_korea_time()
    
    if data_manager.master_data is None:
        data_manager.load_master_csv()
    
    question_row = data_manager.master_data[
        data_manager.master_data['QCODE'] == question_id
    ]
    
    if question_row.empty:
        return jsonify({
            "status": "error",
            "message": f"Question '{question_id}' not found",
            "timestamp": time_info['formatted']
        }), 404
    
    row = question_row.iloc[0]
    question = {
        "id": row["QCODE"],
        "question_text": row["QUESTION"],  # 🚨 파싱 절대 금지!
        "correct_answer": row["ANSWER"],
        "question_type": row["TYPE"],
        "explanation": row["EXPLAIN"],
        "layer1": row["LAYER1"],
        "layer2": row["LAYER2"],
        "source": row["SOURCE"]
    }
    
    return jsonify({
        "status": "success",
        "data": question,
        "timestamp": time_info['formatted']
    })

# 4. GET /api/v1/health
@app.route('/api/v1/health')
def health_check():
    """시스템 상태 확인"""
    time_info = get_korea_time()
    
    # 데이터 로드 상태 확인
    data_status = "loaded" if data_manager.master_data is not None else "not_loaded"
    question_count = len(data_manager.master_data) if data_manager.master_data is not None else 0
    
    return jsonify({
        "status": "success",
        "data": {
            "service": "ACIU Quiz API v2.0",
            "status": "healthy",
            "version": "2.0.1",
            "environment": "development",
            "database": {
                "status": data_status,
                "questions_loaded": question_count,
                "categories_loaded": 4,
                "load_time": data_manager.load_time
            },
            "time_sync": {
                "status": "active",
                "current_time": time_info['formatted']
            }
        },
        "timestamp": time_info['formatted']
    })

# 모든 API 응답에 시간 자동 포함
def add_timestamp_to_response(data):
    time_info = get_korea_time()
    data['timestamp'] = time_info['formatted']
    return data

if __name__ == '__main__':
=======
from flask import Flask, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>🎉 AICU 시즌2 시작!</h1>
    <h2>서대리 첫 번째 임무 완료</h2>
    <p>시간: 2025년 8월 1일 23:30 KST</p>
    <p><a href="/api/status">API 상태 확인</a></p>
    <p><a href="/api/info">프로젝트 정보</a></p>
    """

@app.route('/api/status')
def status():
    return jsonify({
        "status": "✅ 정상 작동",
        "version": "ACIU 시즌2 V1.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S KST"),
        "message": "서대리 환경 설정 완료!"
    })

@app.route('/api/info')
def info():
    return jsonify({
        "project": "AICU 퀴즈앱 시즌2",
        "tech_stack": ["Python", "Flask", "JSON", "Heroku"],
        "team": {
            "조대표": "총괄",
            "나실장": "기획팀장 (코코치)",
            "노팀장": "기술팀장 (Claude)",
            "서대리": "개발팀장 (Cursor AI)"
        },
        "current_phase": "개발 착수",
        "branch": "season1-a"
    })

if __name__ == '__main__':
>>>>>>> c16a0d1251fa3fbdca733677facc204627daf68d
    app.run(debug=True) 