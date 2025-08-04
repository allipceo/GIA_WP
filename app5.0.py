from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import requests
import os
from datetime import datetime
from time_sync import get_korea_time
from data_manager import DataManager

# Flask 애플리케이션 및 데이터 관리자 초기화
app = Flask(__name__)
data_manager = DataManager()

# OpenWeatherMap API 설정 (환경 변수 사용)
WEATHER_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "demo_key")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Flask 애플리케이션 시작 시 데이터 로드
if data_manager.master_data is None:
    data_manager.load_master_csv()

@app.route('/')
def home():
    """메인 페이지를 렌더링합니다. 시즌1과 동일한 UI/UX를 제공합니다."""
    # 기본 사용자 데이터
    user_data = {
        'user_name': '조대표님',
        'exam_date': '2025년 12월 15일',
        'd_day': 'D-138일'
    }
    
    # 기본 통계 데이터
    stats_data = {
        'ins_questions': 1379,
        'exam_questions': 0,
        'total_questions': 1379
    }
    
    # 기본 진도 데이터
    progress_data = {
        'completed_questions': 0,
        'overall_progress_rate': 0,
        'accuracy_rate': 0
    }
    
    # 기본 일일 데이터
    daily_data = {
        'today_total_questions': 0,
        'today_correct_answers': 0,
        'today_accuracy_rate': 0
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
            "iso_format": time_info.get('iso'), # iso 키가 없을 경우를 대비해 get() 사용
            "timestamp": time_info.get('timestamp')
        }
    })

# 1. GET /api/v1/categories
@app.route('/api/v1/categories')
def get_categories():
    """카테고리 목록 및 메타데이터"""
    time_info = get_korea_time()
    
    # 기존 방식 유지 (data_manager.get_all_categories() 메서드가 없을 수 있음)
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
            "total_questions": len(data_manager.master_data) if data_manager.master_data is not None else 0,
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

# 5. GET /api/v1/weather
@app.route('/api/v1/weather')
def get_weather():
    """날씨 정보 API - OpenWeatherMap 연동"""
    try:
        # 기본 위치 (서울)
        city = request.args.get('city', 'Seoul')
        
        # API 호출
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'kr'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # 응답 데이터 구조화
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

@app.route('/quiz/<mode>')
def quiz(mode):
    """퀴즈 화면을 렌더링합니다. 시즌1과 동일한 UI/UX를 제공합니다."""
    # 퀴즈 모드별 설정
    mode_config = {
        'basic': '기본 학습',
        'large-category': '대분류 학습',
        'sub-category': '중분류 학습',
        'choice': '선택형 학습',
        'truefalse': '진위형 학습',
        'mock': '모의고사'
    }
    
    quiz_mode = mode_config.get(mode, '기본 학습')
    
    # 대분류 학습의 경우 카테고리 선택 화면으로 이동
    if mode == 'large-category':
        return render_template('pages/category_selection.html',
                             quiz_mode=quiz_mode,
                             categories={
                                 'property_insurance': {'name': '재산보험', 'icon': '🏢', 'count': len(data_manager.get_questions_by_category('property_insurance'))},
                                 'specialty_insurance': {'name': '특종보험', 'icon': '🚗', 'count': len(data_manager.get_questions_by_category('specialty_insurance'))},
                                 'liability_insurance': {'name': '배상책임보험', 'icon': '⚖️', 'count': len(data_manager.get_questions_by_category('liability_insurance'))},
                                 'marine_insurance': {'name': '해상보험', 'icon': '🚢', 'count': len(data_manager.get_questions_by_category('marine_insurance'))}
                             })
    
    # 기본 통계 데이터
    stats = {
        'total_attempted': 0,
        'total_correct': 0,
        'total_accuracy': 0,
        'total_questions': 1379,
        'correct_answers': 0,
        'accuracy_rate': 0,
        'today_questions': 0,
        'today_correct': 0,
        'today_accuracy': 0
    }
    
    # 기본 문제 데이터 (실제로는 API에서 가져올 예정)
    question = None
    
    return render_template('pages/quiz.html',
                         quiz_mode=quiz_mode,
                         stats=stats,
                         question=question)

@app.route('/api/v1/quiz/question/<mode>')
def get_quiz_question(mode):
    """퀴즈 모드별 문제를 가져옵니다."""
    try:
        # 기본학습 모드의 경우 모든 카테고리에서 문제 가져오기
        if mode == 'basic':
            # 모든 카테고리의 문제를 합쳐서 랜덤 선택
            all_questions = []
            categories = ['property_insurance', 'specialty_insurance', 'liability_insurance', 'marine_insurance']
            
            for category in categories:
                questions = data_manager.get_questions_by_category(category)
                all_questions.extend(questions)
            
            if all_questions:
                import random
                question = random.choice(all_questions)
                return jsonify({
                    "status": "success",
                    "data": question,
                    "timestamp": get_korea_time()['formatted']
                })
        
        # 카테고리별 모드 처리
        elif mode in ['property_insurance', 'specialty_insurance', 'liability_insurance', 'marine_insurance']:
            questions = data_manager.get_questions_by_category(mode)
            
            if questions:
                import random
                question = random.choice(questions)
                return jsonify({
                    "status": "success",
                    "data": question,
                    "timestamp": get_korea_time()['formatted']
                })
        
        # 다른 모드들은 기본 카테고리로 처리
        elif mode in ['large-category', 'sub-category', 'choice', 'truefalse', 'mock']:
            # 기본적으로 재산보험 카테고리 사용
            questions = data_manager.get_questions_by_category('property_insurance')
            
            if questions:
                import random
                question = random.choice(questions)
                return jsonify({
                    "status": "success",
                    "data": question,
                    "timestamp": get_korea_time()['formatted']
                })
        
        return jsonify({
            "status": "error",
            "message": f"Mode '{mode}' not supported",
            "timestamp": get_korea_time()['formatted']
        }), 400
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": get_korea_time()['formatted']
        }), 500

@app.route('/quiz/category/<category>')
def quiz_by_category(category):
    """카테고리별 퀴즈 화면을 렌더링합니다."""
    # 카테고리 정보
    category_info = {
        'property_insurance': {'name': '재산보험', 'icon': '🏢'},
        'specialty_insurance': {'name': '특종보험', 'icon': '🚗'},
        'liability_insurance': {'name': '배상책임보험', 'icon': '⚖️'},
        'marine_insurance': {'name': '해상보험', 'icon': '🚢'}
    }
    
    if category not in category_info:
        return redirect(url_for('home'))
    
    quiz_mode = f"{category_info[category]['name']} 학습"
    
    # 기본 통계 데이터
    stats = {
        'total_attempted': 0,
        'total_correct': 0,
        'total_accuracy': 0,
        'total_questions': len(data_manager.get_questions_by_category(category)),
        'correct_answers': 0,
        'accuracy_rate': 0,
        'today_questions': 0,
        'today_correct': 0,
        'today_accuracy': 0
    }
    
    # 기본 문제 데이터 (실제로는 API에서 가져올 예정)
    question = None
    
    return render_template('pages/quiz.html',
                         quiz_mode=quiz_mode,
                         stats=stats,
                         question=question,
                         category=category)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """설정 화면을 렌더링합니다. 시즌1과 동일한 UI/UX를 제공합니다."""
    if request.method == 'POST':
        # 설정 저장 로직 (실제로는 데이터베이스에 저장)
        user_settings = {
            'user_name': request.form.get('user-name', ''),
            'user_phone': request.form.get('user-phone', ''),
            'exam_subject': request.form.get('exam-subject', 'ACIU'),
            'exam_date': request.form.get('exam-date', '')
        }
        
        # 여기서 실제로는 세션이나 데이터베이스에 저장
        print(f"설정 저장: {user_settings}")
        
        # 성공 후 홈으로 리다이렉트
        return redirect(url_for('home'))
    
    # GET 요청: 설정 화면 표시
    # 기본 설정 데이터 (실제로는 세션이나 데이터베이스에서 가져옴)
    user_settings = {
        'user_name': '조대표님',
        'user_phone': '010-1234-5678',
        'exam_subject': 'ACIU',
        'exam_date': '2025-12-15'
    }
    
    return render_template('pages/settings.html', user_settings=user_settings)

if __name__ == '__main__':
    app.run(debug=True) 