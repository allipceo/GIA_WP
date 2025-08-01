# app.py - GIA_WP Hello World 앱
from flask import Flask
import os

# Flask 앱 생성
app = Flask(__name__)

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

if __name__ == '__main__':
    # 로컬 개발용
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 