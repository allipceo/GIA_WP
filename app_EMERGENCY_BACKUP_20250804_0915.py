import pytz
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, jsonify, request, session
import os

def get_korea_time():
    korea_tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea_tz)
    return {
        'formatted': now.strftime('%Y년 %m월 %d일 %H:%M KST'),
        'iso': now.isoformat(),
        'timestamp': int(now.timestamp())
    }

class DataManager:
    def __init__(self):
        self.master_data = None
        self.load_time = None
    
    def load_master_csv(self):
        try:
            self.master_data = pd.read_csv('06_Data/ins_master_db.csv')
            self.load_time = get_korea_time()['formatted']
            print(f"✅ CSV 로드 성공: {len(self.master_data)}개 문제")
        except Exception as e:
            print(f"❌ CSV 로드 실패: {e}")
            self.master_data = pd.DataFrame()
    
    def get_questions_by_category(self, category):
        if self.master_data is None or self.master_data.empty:
            return []
        
        category_map = {
            'property_insurance': '재산보험',
            'specialty_insurance': '특종보험', 
            'liability_insurance': '배상책임보험',
            'marine_insurance': '해상보험'
        }
        
        layer1_name = category_map.get(category, '재산보험')
        filtered_data = self.master_data[self.master_data['LAYER1'] == layer1_name]
        
        questions = []
        for _, row in filtered_data.iterrows():
            questions.append({
                "id": row["QCODE"],
                "question_text": row["QUESTION"],
                "correct_answer": row["ANSWER"],
                "question_type": row["TYPE"],
                "explanation": row.get("EXPLAIN", ""),
                "layer1": row["LAYER1"],
                "layer2": row.get("LAYER2", ""),
                "source": row.get("SOURCE", "")
            })
        
        return questions

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'aciu_quiz_secret_key_2025'

# 데이터 매니저 초기화
data_manager = DataManager()
data_manager.load_master_csv()

print(f"실행 시간: {get_korea_time()['formatted']}")

@app.route('/')
def home():
    # 사용자 세션 초기화
    if 'user_stats' not in session:
        session['user_stats'] = {
            'total_attempted': 0,
            'total_correct': 0,
            'total_accuracy': 0,
            'today_questions': 0,
            'today_correct': 0,
            'today_accuracy': 0,
            'last_study_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    if 'learning_progress' not in session:
        session['learning_progress'] = {
            'completed_questions': [],
            'correct_answers': [],
            'wrong_answers': [],
            'current_mode': None,
            'current_category': None
        }
    
    stats = session['user_stats']
    progress = session['learning_progress']
    
    return render_template('pages/home.html', 
                         user_name="조대표님",
                         exam_date="2025년 12월 15일",
                         d_day="D-132",
                         stats=stats,
                         progress=progress)

@app.route('/quiz/basic')
def quiz_basic():
    stats = session.get('user_stats', {})
    return render_template('pages/quiz.html', 
                         quiz_mode="기본 학습",
                         stats=stats)

@app.route('/quiz/large-category')
def quiz_large_category():
    categories = {
        'property_insurance': {'name': '재산보험', 'icon': '🏠', 'count': 399},
        'specialty_insurance': {'name': '특종보험', 'icon': '🚗', 'count': 245},
        'liability_insurance': {'name': '배상책임보험', 'icon': '⚖️', 'count': 156},
        'marine_insurance': {'name': '해상보험', 'icon': '🚢', 'count': 89}
    }
    return render_template('pages/category_selection.html',
                         quiz_mode="대분류 학습",
                         categories=categories)

@app.route('/quiz/category/<category>')
def quiz_category(category):
    stats = session.get('user_stats', {})
    category_names = {
        'property_insurance': '재산보험 학습',
        'specialty_insurance': '특종보험 학습',
        'liability_insurance': '배상책임보험 학습',
        'marine_insurance': '해상보험 학습'
    }
    quiz_mode = category_names.get(category, '카테고리 학습')
    return render_template('pages/quiz.html',
                         quiz_mode=quiz_mode,
                         stats=stats)

@app.route('/api/v1/quiz/question/<mode>')
def get_quiz_question(mode):
    try:
        if mode == 'basic':
            # 기본 학습: 전체 문제에서 랜덤 선택
            if data_manager.master_data is not None and not data_manager.master_data.empty:
                question_row = data_manager.master_data.sample(n=1).iloc[0]
                question = {
                    "id": question_row["QCODE"],
                    "question_text": question_row["QUESTION"],
                    "correct_answer": question_row["ANSWER"],
                    "question_type": question_row["TYPE"],
                    "layer1": question_row["LAYER1"],
                    "layer2": question_row.get("LAYER2", ""),
                    "explanation": question_row.get("EXPLAIN", "")
                }
                return jsonify({"status": "success", "data": question})
        
        elif mode in ['property_insurance', 'specialty_insurance', 'liability_insurance', 'marine_insurance']:
            # 카테고리별 학습
            questions = data_manager.get_questions_by_category(mode)
            if questions:
                import random
                question = random.choice(questions)
                return jsonify({"status": "success", "data": question})
        
        return jsonify({"status": "error", "message": f"Mode '{mode}' not supported"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v1/quiz/answer', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('user_answer')
        correct_answer = data.get('correct_answer')
        
        is_correct = user_answer == correct_answer
        
        # 세션 통계 업데이트
        if 'user_stats' not in session:
            session['user_stats'] = {
                'total_attempted': 0,
                'total_correct': 0,
                'total_accuracy': 0,
                'today_questions': 0,
                'today_correct': 0,
                'today_accuracy': 0,
                'last_study_date': datetime.now().strftime('%Y-%m-%d')
            }
        
        stats = session['user_stats']
        stats['total_attempted'] += 1
        if is_correct:
            stats['total_correct'] += 1
        
        stats['total_accuracy'] = round((stats['total_correct'] / stats['total_attempted']) * 100, 1)
        
        # 오늘 통계 업데이트
        today = datetime.now().strftime('%Y-%m-%d')
        if stats['last_study_date'] != today:
            stats['today_questions'] = 0
            stats['today_correct'] = 0
            stats['last_study_date'] = today
        
        stats['today_questions'] += 1
        if is_correct:
            stats['today_correct'] += 1
        stats['today_accuracy'] = round((stats['today_correct'] / stats['today_questions']) * 100, 1)
        
        session['user_stats'] = stats
        
        return jsonify({
            "status": "success",
            "data": {
                "is_correct": is_correct,
                "updated_stats": stats
            }
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "success",
        "message": "ACIU QUIZ API is running",
        "time": get_korea_time()['formatted'],
        "data_loaded": data_manager.master_data is not None and not data_manager.master_data.empty
    })

if __name__ == '__main__':
    print(f"실행 시간: {get_korea_time()['formatted']}")
    if data_manager.master_data is not None and not data_manager.master_data.empty:
        print(f"✅ 마스터 데이터 로드 완료: {len(data_manager.master_data)}개 문제")
    else:
        print("❌ 마스터 데이터 로드 실패")
    
    app.run(debug=True, host='127.0.0.1', port=5000) 