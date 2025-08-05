from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import json
import requests
import os
from datetime import datetime
from time_sync_v11 import get_korea_time
from data_manager_v11 import DataManager

# Flask 애플리케이션 및 데이터 관리자 초기화
app = Flask(__name__)
# 세션 암호화 키를 환경 변수에서 가져오도록 변경
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_aciu_quiz_secret_key')
data_manager = DataManager()

# OpenWeatherMap API 설정 (환경 변수 사용)
WEATHER_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "demo_key")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Flask 애플리케이션 시작 시 데이터 로드
if data_manager.master_data is None:
    data_manager.load_master_csv()

# 모든 요청 이전에 세션 초기화를 보장하는 데코레이터
@app.before_request
def before_each_request():
    init_user_session()

def init_user_session():
    """사용자 세션 초기화"""
    if 'user_stats' not in session:
        session['user_stats'] = {
            'total_attempted': 0,
            'total_correct': 0,
            'total_accuracy': 0,
            'today_questions': 0,
            'today_correct': 0,
            'today_accuracy': 0,
            'last_study_date': None
        }
    
    if 'learning_progress' not in session:
        session['learning_progress'] = {
            'completed_questions': [],
            'correct_answers': [],
            'wrong_answers': [],
            'current_category': None,
            'current_mode': None
        }
    
    if 'study_history' not in session:
        session['study_history'] = []

def update_user_stats(is_correct, question_id):
    """사용자 통계 업데이트"""
    init_user_session()
    
    # 오늘 날짜 확인
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 마지막 학습 날짜 확인
    if session['user_stats']['last_study_date'] != today:
        # 새로운 날짜면 오늘 통계 초기화
        session['user_stats']['today_questions'] = 0
        session['user_stats']['today_correct'] = 0
        session['user_stats']['today_accuracy'] = 0
        session['user_stats']['last_study_date'] = today
    
    # 통계 업데이트
    session['user_stats']['total_attempted'] += 1
    session['user_stats']['today_questions'] += 1
    
    if is_correct:
        session['user_stats']['total_correct'] += 1
        session['user_stats']['today_correct'] += 1
        if question_id not in session['learning_progress']['correct_answers']:
            session['learning_progress']['correct_answers'].append(question_id)
    else:
        if question_id not in session['learning_progress']['wrong_answers']:
            session['learning_progress']['wrong_answers'].append(question_id)
    
    # 정답률 계산
    session['user_stats']['total_accuracy'] = round(
        (session['user_stats']['total_correct'] / session['user_stats']['total_attempted']) * 100, 1
    )
    session['user_stats']['today_accuracy'] = round(
        (session['user_stats']['today_correct'] / session['user_stats']['today_questions']) * 100, 1
    )
    
    # 학습 기록 추가
    study_record = {
        'question_id': question_id,
        'is_correct': is_correct,
        'timestamp': get_korea_time()['formatted'],
        'category': session['learning_progress']['current_category'],
        'mode': session['learning_progress']['current_mode']
    }
    session['study_history'].append(study_record)
    
    # 세션 저장
    session.modified = True

def get_user_stats():
    """사용자 통계 반환"""
    init_user_session()
    return session['user_stats']

def get_learning_progress():
    """학습 진행 상황 반환"""
    init_user_session()
    return session['learning_progress']

@app.route('/')
def home():
    """메인 페이지를 렌더링합니다. 시즌1과 동일한 UI/UX를 제공합니다."""
    
    user_stats = get_user_stats()
    learning_progress = get_learning_progress()
    
    # 사용자 데이터
    user_data = {
        'user_name': '조대표님',
        'exam_date': '2025년 12월 15일',
        'd_day': 'D-138일'
    }
    
    # 완료된 문제 수 계산 (정답 + 오답)
    completed_questions = len(learning_progress['correct_answers']) + len(learning_progress['wrong_answers'])
    
    # 통계 데이터 (세션 기반)
    stats_data = {
        'ins_questions': data_manager.get_ins_questions_count(),
        'exam_questions': completed_questions,
        'total_questions': data_manager.get_total_questions_count()
    }
    
    # 진도 데이터 (세션 기반)
    progress_data = {
        'completed_questions': completed_questions,
        'overall_progress_rate': round((completed_questions / stats_data['total_questions']) * 100, 1) if stats_data['total_questions'] > 0 else 0,
        'accuracy_rate': user_stats.get('total_accuracy', 0)
    }
    
    # 일일 데이터 (세션 기반)
    daily_data = {
        'today_total_questions': user_stats.get('today_questions', 0),
        'today_correct_answers': user_stats.get('today_correct', 0),
        'today_accuracy_rate': user_stats.get('today_accuracy', 0)
    }
    
    return render_template('pages/home.html',
                         user_name=user_data['user_name'],
                         exam_date=user_data['exam_date'],
                         d_day=user_data['d_day'],
                         stats=stats_data,
                         progress=progress_data,
                         daily=daily_data)

@app.route('/api/status')
def status():
    """API의 현재 상태를 확인하고 JSON 응답을 반환합니다."""
    time_info = get_korea_time()
    return jsonify({
        "status": "✅ 정상 작동",
        "version": "ACIU 시즌2 V1.0",
        "timestamp": time_info['formatted'],
        "message": "서대리 환경 설정 완료!"
    })

@app.route('/api/info')
def info():
    """프로젝트 정보를 JSON 형식으로 반환합니다."""
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
            "iso_format": time_info.get('iso'),
            "timestamp": time_info.get('timestamp')
        }
    })

# 1. GET /api/v1/categories
@app.route('/api/v1/categories')
def get_categories():
    """카테고리 목록 및 메타데이터"""
    time_info = get_korea_time()
    
    categories = data_manager.get_all_categories()
    
    return jsonify({
        "status": "success",
        "data": {
            "categories": categories,
            "total_questions": data_manager.get_total_questions_count(),
            "total_categories": len(categories)
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
    
    question = data_manager.get_question_by_id(question_id)
    
    if question is None:
        return jsonify({
            "status": "error",
            "message": f"Question '{question_id}' not found",
            "timestamp": time_info['formatted']
        }), 404
    
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
                "categories_loaded": len(data_manager.get_all_categories()) if data_manager.master_data is not None else 0,
                "load_time": data_manager.load_time
            },
            "time_sync": {
                "status": "active",
                "current_time": time_info['formatted']
            }
        },
        "timestamp": time_info['formatted']
    })

# 5. GET /api/v1/weather
@app.route('/api/v1/weather')
def get_weather():
    """날씨 정보 API - OpenWeatherMap 연동"""
    try:
        city = request.args.get('city', 'Seoul')
        
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'kr'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        result = {
            "status": "success",
            "data": {
                "city": weather_data.get('name', city),
                "temperature": weather_data.get('main', {}).get('temp'),
                "description": weather_data.get('weather', [{}])[0].get('description'),
                "humidity": weather_data.get('main', {}).get('humidity'),
                "wind_speed": weather_data.get('wind', {}).get('speed'),
                "timestamp": get_korea_time()['formatted']
            }
        }
        
        return jsonify(result)
        
    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"날씨 API 호출 실패: {str(e)}",
            "timestamp": get_korea_time()['formatted']
        }), 500
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"서버 오류: {str(e)}",
            "timestamp": get_korea_time()['formatted']
        }), 500

# 6. GET /api/v1/hello
@app.route('/api/v1/hello', methods=['GET'])
def hello_api():
    """Hello API - V2.1 협업체계 테스트"""
    try:
        return jsonify({
            "message": "Hello ACIU!",
            "status": "success",
            "timestamp": get_korea_time()['formatted']
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": get_korea_time()['formatted']
        }), 500

@app.route('/api/v1/quiz/answer', methods=['POST'])
def check_answer():
    """정답 확인 및 통계 업데이트"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('user_answer')
        
        question = data_manager.get_question_by_id(question_id)
        if not question:
            return jsonify({
                "status": "error",
                "message": "Question not found",
                "timestamp": get_korea_time()['formatted']
            }), 404
        
        is_correct = user_answer == question['correct_answer']
        
        update_user_stats(is_correct, question_id)
        
        user_stats = get_user_stats()
        
        return jsonify({
            "status": "success",
            "data": {
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": question['correct_answer'],
                "updated_stats": user_stats
            },
            "timestamp": get_korea_time()['formatted']
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": get_korea_time()['formatted']
        }), 500

@app.route('/quiz/<mode>')
def quiz(mode):
    return render_template('pages/quiz.html', title='퀴즈 화면')

@app.route('/quiz/category/<category>')
def quiz_by_category(category):
    """카테고리별 퀴즈 화면을 렌더링합니다."""
    session['learning_progress']['current_category'] = category
    session['learning_progress']['current_mode'] = 'large-category'
    session.modified = True
    
    return redirect(url_for('quiz', mode='large-category'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """설정 화면을 렌더링합니다. 시즌1과 동일한 UI/UX를 제공합니다."""
    if request.method == 'POST':
        user_settings = {
            'user_name': request.form.get('user-name', ''),
            'user_phone': request.form.get('user-phone', ''),
            'exam_subject': request.form.get('exam-subject', 'ACIU'),
            'exam_date': request.form.get('exam-date', '')
        }
        
        print(f"설정 저장: {user_settings}")
        
        return redirect(url_for('home'))
    
    user_settings = {
        'user_name': '조대표님',
        'user_phone': '010-1234-5678',
        'exam_subject': 'ACIU',
        'exam_date': '2025-12-15'
    }
    
    return render_template('pages/settings.html', user_settings=user_settings)

if __name__ == '__main__':
    app.run(debug=True)
