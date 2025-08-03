# GitHub + Python + JSON 완전 배포 가이드

## 🎯 GitHub 활용 Python 앱 배포 전략

### **조대표님의 현재 장점**
- ✅ **GitHub 사용 가능** (버전 관리 완벽)
- ✅ **배포 인프라 준비됨** (GitHub Pages/Actions 활용 가능)
- ✅ **협업 환경 구축됨** (팀 작업 용이)

---

## 🚀 **배포 방식 3가지 (GitHub 기반)**

### **방식 1: GitHub + Heroku (가장 추천)**

#### **1단계: GitHub 저장소 구조**
```
aicu-quiz-app/
├── app.py                 # Flask 메인 서버
├── requirements.txt       # Python 라이브러리 목록
├── Procfile              # Heroku 배포 설정
├── runtime.txt           # Python 버전 지정
├── data/
│   ├── questions.json    # 문제 데이터
│   └── statistics.json   # 통계 데이터
├── templates/
│   └── index.html        # HTML 템플릿
├── static/
│   ├── css/style.css     # 스타일
│   └── js/quiz.js        # JavaScript
└── README.md
```

#### **2단계: 핵심 파일들**

**requirements.txt**
```txt
Flask==2.3.3
gunicorn==21.2.0
python-dotenv==1.0.0
```

**Procfile** (Heroku 배포용)
```txt
web: gunicorn app:app
```

**app.py** (핵심 서버)
```python
from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# JSON 데이터 로드
def load_questions():
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_statistics():
    with open('data/statistics.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/questions')
def get_questions():
    questions = load_questions()
    return jsonify(questions)

@app.route('/api/statistics')
def get_statistics():
    stats = load_statistics()
    return jsonify(stats)

@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    # 답안 처리 로직
    return jsonify({"result": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### **3단계: 배포 과정**
```bash
# 1. GitHub에 코드 업로드
git add .
git commit -m "퀴즈앱 Python 버전"
git push origin main

# 2. Heroku 연결
# Heroku 웹사이트에서 GitHub 저장소 연결

# 3. 자동 배포 설정
# GitHub main 브랜치 변경 시 자동 배포

# 4. 접속 URL 생성
# https://aicu-quiz-app.herokuapp.com
```

---

### **방식 2: GitHub Pages + GitHub Actions**

#### **정적 사이트 생성 방식**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate static files
      run: |
        python generate_static.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

#### **접속 URL**
```
https://조대표계정.github.io/aicu-quiz-app
```

---

### **방식 3: GitHub Codespaces (개발 환경)**

#### **클라우드 개발 환경**
```json
// .devcontainer/devcontainer.json
{
    "name": "AICU Quiz App",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.9",
    "forwardPorts": [5000],
    "postCreateCommand": "pip install -r requirements.txt",
    "extensions": [
        "ms-python.python",
        "ms-python.flake8"
    ]
}
```

#### **사용 방법**
```
1. GitHub 저장소에서 "Code" → "Codespaces" 클릭
2. 클라우드에서 바로 개발 환경 실행
3. python app.py 실행
4. 포트 포워딩으로 외부 접속 가능
```

---

## 📋 **단계별 실행 계획**

### **Phase 1: 저장소 설정 (30분)**

#### **GitHub 저장소 생성**
```bash
# 1. 새 저장소 생성
Repository name: aicu-quiz-app
Description: AICU 퀴즈앱 Python 버전
Public/Private: Public (무료 배포용)

# 2. 로컬에서 클론
git clone https://github.com/조대표계정/aicu-quiz-app.git
cd aicu-quiz-app
```

#### **기본 구조 생성**
```bash
# 폴더 생성
mkdir data templates static static/css static/js

# 기본 파일 생성
touch app.py requirements.txt Procfile README.md
touch data/questions.json data/statistics.json
touch templates/index.html
touch static/css/style.css static/js/quiz.js
```

### **Phase 2: 코드 변환 (2시간)**

#### **HTML → Python 변환**
```python
# 현재 HTML의 JavaScript 로직을 Python으로 변환
# 예시: 문제 선택 로직
def get_random_question(category=None):
    questions = load_questions()
    if category:
        filtered = [q for q in questions if q['category'] == category]
        return random.choice(filtered)
    return random.choice(questions)

# 통계 처리 로직
def update_statistics(user_id, is_correct, category):
    stats = load_statistics()
    # 통계 업데이트 로직
    save_statistics(stats)
```

#### **JSON 데이터 변환**
```python
# CSV → JSON 변환 스크립트
import pandas as pd
import json

# CSV 파일 읽기
df = pd.read_csv('ins_master_db.csv')

# JSON 형식으로 변환
questions = []
for _, row in df.iterrows():
    question = {
        "id": row['INDEX'],
        "code": row['QCODE'],
        "question": row['QUESTION'],
        "answer": row['ANSWER'],
        "category": row['LAYER1'],
        "subcategory": row['LAYER2'],
        "type": row['TYPE']
    }
    questions.append(question)

# JSON 파일 저장
with open('data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
```

### **Phase 3: 배포 설정 (1시간)**

#### **Heroku 연결**
```bash
# 1. Heroku 계정 생성 (무료)
https://signup.heroku.com/

# 2. Heroku CLI 설치 (선택사항)
# 또는 웹 인터페이스 사용

# 3. Heroku 앱 생성
New App → aicu-quiz-app

# 4. GitHub 연결
Deploy 탭 → GitHub 연결 → 저장소 선택

# 5. 자동 배포 설정
Enable Automatic Deploys
```

### **Phase 4: 테스트 및 최적화 (1시간)**

#### **로컬 테스트**
```bash
# 로컬 환경에서 테스트
pip install -r requirements.txt
python app.py

# 브라우저에서 확인
http://localhost:5000
```

#### **배포 테스트**
```bash
# GitHub에 푸시
git add .
git commit -m "퀴즈앱 배포 준비 완료"
git push origin main

# Heroku 자동 배포 확인
https://aicu-quiz-app.herokuapp.com
```

---

## 🔧 **실제 파일 예시**

### **app.py (핵심 서버 코드)**
```python
from flask import Flask, render_template, jsonify, request, session
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'aicu-quiz-secret-key'

# 데이터 로드 함수들
def load_questions():
    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_user_statistics(user_id):
    try:
        with open(f'data/stats_{user_id}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "user_id": user_id,
            "start_date": "2025-07-29",
            "total_attempted": 0,
            "total_correct": 0,
            "daily_attempted": 0,
            "daily_correct": 0,
            "accuracy": 0
        }

def save_user_statistics(user_id, stats):
    with open(f'data/stats_{user_id}.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# 라우트 정의
@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/questions')
def get_questions():
    questions = load_questions()
    return jsonify(questions)

@app.route('/api/question/<int:question_id>')
def get_question(question_id):
    questions = load_questions()
    if 0 <= question_id < len(questions):
        return jsonify(questions[question_id])
    return jsonify({"error": "Question not found"}), 404

@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    user_id = session.get('user_id')
    data = request.json
    
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    # 정답 확인
    questions = load_questions()
    correct_answer = questions[question_id]['answer']
    is_correct = user_answer == correct_answer
    
    # 통계 업데이트
    stats = load_user_statistics(user_id)
    stats['total_attempted'] += 1
    stats['daily_attempted'] += 1
    
    if is_correct:
        stats['total_correct'] += 1
        stats['daily_correct'] += 1
    
    stats['accuracy'] = round((stats['total_correct'] / stats['total_attempted']) * 100, 2)
    stats['last_updated'] = datetime.now().isoformat()
    
    save_user_statistics(user_id, stats)
    
    return jsonify({
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "statistics": stats
    })

@app.route('/api/statistics')
def get_statistics():
    user_id = session.get('user_id')
    stats = load_user_statistics(user_id)
    return jsonify(stats)

@app.route('/api/reset_daily', methods=['POST'])
def reset_daily_stats():
    user_id = session.get('user_id')
    stats = load_user_statistics(user_id)
    stats['daily_attempted'] = 0
    stats['daily_correct'] = 0
    save_user_statistics(user_id, stats)
    return jsonify({"message": "Daily stats reset"})

if __name__ == '__main__':
    # 개발 환경
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # 프로덕션 환경 (Heroku)
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
```

### **requirements.txt**
```txt
Flask==2.3.3
gunicorn==21.2.0
python-dotenv==1.0.0
pandas==2.0.3
```

### **Procfile** (Heroku 배포용)
```txt
web: gunicorn app:app
release: python data_setup.py
```

---

## 🌐 **배포 후 사용자 경험**

### **접속 방식**
```
개발자 (조대표님):
GitHub → 코드 수정 → 자동 배포

사용자:
브라우저 → https://aicu-quiz-app.herokuapp.com → 퀴즈 사용
```

### **업데이트 프로세스**
```
1. 로컬에서 코드 수정
2. git push origin main
3. Heroku 자동 배포 (2-3분)
4. 사용자는 새로고침만으로 최신 버전 사용
```

### **모바일 지원**
```
모바일 브라우저 → 웹사이트 접속 → "홈 화면에 추가" → 앱처럼 사용
```

---

## 💰 **비용 분석**

### **무료 옵션**
```
✅ GitHub: 무료 (Public 저장소)
✅ Heroku: 무료 플랜 (월 550시간, 소규모 충분)
✅ GitHub Pages: 무료 (정적 사이트)
✅ GitHub Actions: 무료 (월 2000분)

총 비용: $0
```

### **유료 옵션 (확장 시)**
```
💰 Heroku Pro: $7/월 (24/7 운영, 커스텀 도메인)
💰 GitHub Pro: $4/월 (Private 저장소 무제한)
💰 커스텀 도메인: $10-15/년

총 비용: $10-20/월 (본격 운영 시)
```

---

## 🎯 **노팀장 추천 로드맵**

### **Week 1: 기본 구조**
```bash
git clone https://github.com/조대표계정/aicu-quiz-app.git
# 기본 Flask 앱 구조 생성
# 현재 HTML → Python 변환 시작
```

### **Week 2: 핵심 기능**
```python
# 문제 출제, 답안 체크, 통계 업데이트 구현
# JSON 데이터 구조 완성
```

### **Week 3: 배포 및 테스트**
```bash
git push origin main
# Heroku 자동 배포
# 사용자 테스트 진행
```

### **Week 4: 최적화**
```
# 모바일 최적화
# 성능 개선
# 추가 기능 구현
```

---

## 🚀 **즉시 시작 가능한 명령어**

```bash
# 1. 저장소 생성 및 클론
git clone https://github.com/조대표계정/aicu-quiz-app.git
cd aicu-quiz-app

# 2. 기본 구조 생성
mkdir -p data templates static/{css,js}
touch app.py requirements.txt Procfile

# 3. 최소 Flask 앱 생성
echo "Flask==2.3.3" > requirements.txt
echo "web: python app.py" > Procfile

# 4. GitHub에 푸시
git add .
git commit -m "초기 Python 앱 구조"
git push origin main

# 5. Heroku 연결 (웹에서)
# https://dashboard.heroku.com/new-app
```

---

## 🏆 **결론**

**조대표님의 GitHub 기반이 최적의 선택입니다!**

**장점:**
- ✅ **무료로 시작**: GitHub + Heroku 무료 플랜
- ✅ **자동 배포**: 코드 푸시만으로 자동 업데이트  
- ✅ **버전 관리**: Git으로 완벽한 이력 관리
- ✅ **협업 친화적**: 팀원 추가 용이
- ✅ **확장 가능**: 필요 시 유료 플랜으로 업그레이드

**사용자 접속:**
`https://aicu-quiz-app.herokuapp.com` → 전세계 어디서나 접속

**조대표님, GitHub 기반 Python 배포로 현재보다 훨씬 효율적인 시스템을 구축할 수 있습니다!** 🚀