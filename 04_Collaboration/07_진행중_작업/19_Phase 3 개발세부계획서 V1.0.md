# Phase 3 개발세부계획서 V1.0

**프로젝트명**: ACIU 시즌2 Phase 3 - 프론트엔드 통합  
**작성일**: 2025년 8월 3일 일요일 23:00 KST  
**작성자**: 노팀장 (기술팀장)  
**승인자**: 조대표님  
**문서 버전**: V1.0  
**예상 기간**: 30-40분

---

## 🎯 **Phase 3 개요**

### **목표**
- 시즌1 UI/UX를 Flask 템플릿으로 완전 통합
- 사용자가 실제 사용 가능한 완전한 웹 애플리케이션 완성
- Phase 2에서 구축한 백엔드 API와 프론트엔드 연동

### **Phase 2 성과 기반**
- ✅ **Flask 백엔드**: 6개 API 정상 작동
- ✅ **협업체계 V2.1**: Hello API로 검증 완료
- ✅ **현실적 템플릿 시스템**: 표준작업템플릿 구축

---

## 📋 **현실적 협업 프로세스**

### **협업체계 V2.1 적용**
```
Step 1: 조대표님 → 작업요청서 작성 (07_진행중_작업/)
Step 2: 코코치 → 기획서 작성 (기능별 상세 명세)
Step 3: 노팀장 → 기술설계서 작성 (Flask 템플릿 구조)
Step 4: 서대리 → 구현 (HTML + Flask 통합)
Step 5: 조대표님 → 최종 승인
```

### **예상 복사-붙여넣기 횟수**
- **총 3회 개입**: 요청서 작성 → 중간 확인 → 최종 승인
- **각 작업당 15분**: Hello API 경험 기반 시간 산정

---

## 🏗️ **기술 아키텍처**

### **시즌1 자산 활용 전략**
```
기존 index.html (2,297줄)
├── HTML 구조 → Flask 템플릿 분할
├── Tailwind CSS → 그대로 유지
├── JavaScript → 필요 부분만 서버사이드 이전
└── 통계 시스템 → Flask 백엔드 연동
```

### **Flask 템플릿 구조**
```
templates/
├── base.html              # 공통 레이아웃 (Tailwind CSS 포함)
├── components/
│   ├── header.html        # 상단 네비게이션
│   ├── stats.html         # 통계 박스들
│   └── quiz_area.html     # 퀴즈 영역
├── pages/
│   ├── home.html          # 메인 화면
│   ├── basic_quiz.html    # 기본학습
│   ├── category_quiz.html # 대분류학습
│   └── settings.html      # 사용자 설정
└── partials/
    ├── d_day.html         # D-day 카운터
    └── learning_stats.html # 학습 통계
```

---

## 📝 **상세 작업 계획**

### **Task 1: 메인 화면 통합 (15분)**

#### **작업요청서 템플릿**
```markdown
작업명: 메인 화면 Flask 템플릿 변환
요구사항: 
- 시즌1 홈 화면 디자인 완전 재현
- D-day 카운터, 학습 통계, 모드 선택 버튼
- 동적 데이터 렌더링 (사용자명, 시험일 등)
```

#### **예상 구현 결과**
```python
@app.route('/')
def home():
    user_data = get_user_settings()  # 사용자 설정
    stats_data = get_learning_stats()  # 학습 통계
    return render_template('pages/home.html', 
                         user=user_data, 
                         stats=stats_data)
```

### **Task 2: 퀴즈 화면 통합 (15분)**

#### **작업요청서 템플릿**
```markdown
작업명: 퀴즈 화면 Flask 템플릿 변환
요구사항:
- 기본학습/대분류학습 화면 구현
- 문제 표시, 답안 선택, 결과 확인 기능
- 실시간 통계 업데이트
```

#### **예상 구현 결과**
```python
@app.route('/quiz/<mode>/<category>')
def quiz_page(mode, category):
    questions = load_questions(category)  # CSV에서 직접 로드
    return render_template('pages/quiz.html', 
                         questions=questions, 
                         mode=mode, 
                         category=category)
```

### **Task 3: 설정 화면 통합 (10분)**

#### **작업요청서 템플릿**
```markdown
작업명: 사용자 설정 화면 구현
요구사항:
- 사용자 정보 입력/수정
- 시험일 설정, D-day 계산
- 통계 초기화 기능
```

#### **예상 구현 결과**
```python
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        save_user_settings(request.form)
        return redirect('/')
    return render_template('pages/settings.html')
```

---

## 📊 **데이터 처리 전략**

### **시즌1 호환성 유지**
```python
# 기존 CSV 로딩 방식 그대로 활용
def load_questions(category):
    df = pd.read_csv('ins_master_db.csv')
    return df[df['LAYER1'] == category_map[category]]

# 기존 통계 시스템 서버사이드 이전
def get_learning_stats():
    return {
        'total_questions': 1379,
        'completed': get_user_progress(),
        'accuracy': calculate_accuracy()
    }
```

### **LocalStorage → 서버 세션**
```python
# 기존: window.statistics (LocalStorage)
# 신규: Flask session 또는 간단한 파일 저장
from flask import session

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    session['user_progress'] = request.json
    return jsonify({'status': 'success'})
```

---

## 🎨 **UI/UX 유지 전략**

### **완전 동일한 사용자 경험**
- **Tailwind CSS**: 모든 스타일 그대로 유지
- **반응형 디자인**: 기존 모바일/데스크톱 호환성
- **애니메이션**: 기존 JavaScript 효과 유지
- **색상 테마**: 시즌1 디자인 시스템 완전 보존

### **개선 사항**
- **서버 렌더링**: 페이지 로딩 속도 향상
- **SEO 최적화**: 검색엔진 친화적
- **상태 관리**: 서버사이드로 안정성 향상

---

## ⚡ **현실적 작업 일정**

### **전체 타임라인: 30-40분**

| 시간 | 작업 | 담당 | 예상 소요시간 |
|------|------|------|---------------|
| 23:00-23:05 | Task 1 요청서 작성 | 조대표님 | 5분 |
| 23:05-23:10 | Task 1 기획서 작성 | 코코치 | 5분 |
| 23:10-23:15 | Task 1 설계서 작성 | 노팀장 | 5분 |
| 23:15-23:30 | Task 1 구현 (메인 화면) | 서대리 | 15분 |
| 23:30-23:35 | Task 2 요청서 작성 | 조대표님 | 5분 |
| 23:35-23:40 | Task 2 기획서 작성 | 코코치 | 5분 |
| 23:40-23:45 | Task 2 설계서 작성 | 노팀장 | 5분 |
| 23:45-24:00 | Task 2 구현 (퀴즈 화면) | 서대리 | 15분 |

### **Task 3 (설정 화면)은 선택사항**
- 시간 여유 있으면 진행
- 필수 기능 완성 후 추가 개발

---

## 🎯 **완료 기준**

### **필수 달성 목표**
- [ ] 메인 화면 완전 재현 (시즌1 수준)
- [ ] 퀴즈 화면 기본 기능 작동
- [ ] 시즌1 디자인 100% 유지
- [ ] 모든 링크 정상 작동

### **성공 지표**
- **시각적 완성도**: 시즌1과 구별 불가능
- **기능적 완성도**: 사용자 실제 사용 가능
- **성능**: 페이지 로딩 2초 이내
- **호환성**: 모바일/데스크톱 모두 지원

---

## 🚀 **Phase 4 준비사항**

### **Phase 3 완료 후 자동으로 준비되는 것들**
- **Heroku 배포 준비**: Flask 앱 완성
- **사용자 테스트**: 실제 사용 가능한 앱
- **성능 최적화**: 필요한 개선사항 파악

---

## 📋 **협업 파일 준비사항**

### **07_진행중_작업/ 폴더 활용**
```
현재작업_요청서.md     # Task별 작업 요청
현재작업_기획서.md     # 코코치 기능 명세
현재작업_설계서.md     # 노팀장 기술 설계
현재작업_결과서.md     # 서대리 구현 결과
현재작업_완료서.md     # 조대표님 최종 승인
```

### **예상 파일 생성**
```
templates/ 폴더 생성
static/ 폴더 생성 (CSS, JS 파일)
app.py 라우트 추가 (약 5-6개)
```

---

## 💡 **리스크 관리**

### **예상 문제점**
1. **CSS 연동**: Tailwind CDN 연결 확인
2. **경로 문제**: static 파일 경로 설정
3. **데이터 연동**: CSV 파일 경로 확인

### **해결 방안**
1. **단계별 테스트**: 각 Task 완료 후 즉시 확인
2. **백업 유지**: 기존 app.py 보존
3. **롤백 계획**: 문제 발생 시 이전 상태 복구

---

## 🎉 **Phase 3 완료 시 기대 효과**

### **사용자 관점**
- 시즌1과 동일한 친숙한 UI/UX
- 더 빠른 로딩 속도 (서버 렌더링)
- 안정적인 데이터 관리

### **개발 관점**  
- Flask 생태계 활용 가능
- 확장성 대폭 향상
- Heroku 배포 준비 완료

### **사업 관점**
- 실제 사용자 서비스 가능
- 피드백 수집 기반 마련
- 추가 기능 개발 토대 완성

---

**Phase 3 개발세부계획서 V1.0 완성!**  
**조대표님 승인 후 즉시 시작 가능합니다!** 🚀✨

---

**문서 작성**: 2025년 8월 3일 일요일 23:00 KST  
**노팀장 (기술팀장)**