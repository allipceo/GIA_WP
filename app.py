# app.py - GIA_WP Hello World 앱
from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

# Flask 앱 생성
app = Flask(__name__)

def load_json_data():
    """JSON 파일 읽기 함수 (에러 처리 포함)"""
    try:
        with open('data/sample_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 데이터 생성 및 저장
        default_data = {
            "app_info": {"name": "GIA_WP", "version": "1.0"},
            "users": [],
            "messages": []
        }
        save_json_data(default_data)
        return default_data
    except json.JSONDecodeError:
        # JSON 오류 시 기본 데이터 반환
        return {"error": "JSON 형식 오류"}

def save_json_data(data):
    """JSON 파일 쓰기 함수 (안전 저장)"""
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/sample_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"저장 오류: {e}")
        return False

@app.route('/')
def hello_gia_wp():
    """GIA_WP 메인 페이지"""
    return '''
    <h1>🚀 Hello GIA_WP!</h1>
    <h2>GIA Work Platform 첫 번째 앱</h2>
    <p>Python + Flask + Heroku 연동 성공!</p>
    <p>조대표님의 GIA_WP 환경 구축 완료 🎉</p>
    '''

@app.route('/status')
def status():
    """시스템 상태 확인"""
    return {
        "status": "running",
        "platform": "GIA_WP",
        "version": "1.0",
        "message": "GIA Work Platform 정상 작동 중"
    }

@app.route('/api/data')
def get_data():
    """JSON 데이터 조회 API"""
    data = load_json_data()
    return jsonify(data)

@app.route('/api/update', methods=['POST'])
def update_data():
    """JSON 데이터 업데이트 API"""
    try:
        # POST 요청 데이터 받기
        new_data = request.get_json()
        if new_data:
            # 기존 데이터 로드
            current_data = load_json_data()
            # 새로운 데이터 병합
            current_data.update(new_data)
            # 저장
            if save_json_data(current_data):
                return jsonify({"status": "success", "message": "데이터 업데이트 완료"})
            else:
                return jsonify({"status": "error", "message": "저장 실패"}), 500
        else:
            return jsonify({"status": "error", "message": "데이터가 없습니다"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"오류: {str(e)}"}), 500

if __name__ == '__main__':
    # 로컬 개발용
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 