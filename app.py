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
    app.run(debug=True) 