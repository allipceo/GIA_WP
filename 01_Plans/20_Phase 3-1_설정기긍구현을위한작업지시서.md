# Phase 3-1.5 설정 기능 우선 완성 계획서

**작성일**: 2025년 8월 5일 화요일 22:32 KST  
**작성자**: 노팀장 (기술팀장)  
**목적**: 조대표님 지적사항 반영 - 통계 출발점 설정 기능 우선 구현  
**예상 소요시간**: 20분

---

## 🎯 **Phase 3-1.5 목표**

### **핵심 목표**
- ✅ 사용자 설정 기능 완전 구현 (이름, 시험일)
- ✅ 설정일 = 통계 시작점 확립
- ✅ 동적 D-day 계산
- ✅ 세션 기반 사용자 데이터 관리

### **수정 최소화 원칙**
- 🔒 기존 템플릿 구조 보존
- 🔒 통계 로직 핵심 유지
- 🔒 Phase 3-1 성과 보존

---

## 🔧 **구체적 수정 사항**

### **Task 1: 사용자 설정 관리 함수 추가 (10분)**

#### **app_v1.3.py에 추가할 함수들**
```python
from datetime import datetime, date

def init_user_settings():
    """사용자 설정 초기화"""
    if 'user_settings' not in session:
        session['user_settings'] = {
            'user_name': None,
            'user_phone': None,
            'exam_date': None,
            'registration_date': None,  # 통계 시작점
            'is_configured': False
        }

def get_user_settings():
    """사용자 설정 반환"""
    init_user_settings()
    return session['user_settings']

def save_user_settings(form_data):
    """사용자 설정 저장"""
    init_user_settings()
    
    session['user_settings'].update({
        'user_name': form_data.get('user-name', ''),
        'user_phone': form_data.get('user-phone', ''),
        'exam_date': form_data.get('exam-date', ''),
        'registration_date': datetime.now().strftime('%Y-%m-%d'),  # 오늘이 통계 시작점
        'is_configured': True
    })
    session.modified = True
    
    # 통계 초기화 (새 사용자 등록 시)
    reset_user_statistics()

def calculate_dday(exam_date_str):
    """D-day 계산"""
    if not exam_date_str:
        return "D-day 미설정"
    
    try:
        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        today = date.today()
        diff = (exam_date - today).days
        
        if diff > 0:
            return f"D-{diff}일"
        elif diff == 0:
            return "D-day"
        else:
            return f"D+{abs(diff)}일"
    except:
        return "D-day 계산 오류"

def reset_user_statistics():
    """사용자 통계 초기화 (새 등록 시)"""
    session['user_stats'] = {
        'total_attempted': 0,
        'total_correct': 0,
        'total_accuracy': 0,
        'today_questions': 0,
        'today_correct': 0,
        'today_accuracy': 0,
        'last_study_date': None
    }
    
    session['learning_progress'] = {
        'completed_questions': [],
        'correct_answers': [],
        'wrong_answers': [],
        'current_category': None,
        'current_mode': None
    }
    
    session['study_history'] = []
    session.modified = True
```

### **Task 2: 홈 화면 동적 데이터 로딩 (5분)**

#### **home() 함수 수정**
```python
@app.route('/')
def home():
    """메인 페이지 - 동적 사용자 데이터 사용"""
    
    user_stats = get_user_stats()
    learning_progress = get_learning_progress()
    user_settings = get_user_settings()
    
    # 사용자 미설정 시 기본값 사용
    if not user_settings['is_configured']:
        user_data = {
            'user_name': '사용자 (미설정)',
            'exam_date': '시험일 미설정',
            'd_day': '설정 필요'
        }
    else:
        user_data = {
            'user_name': user_settings['user_name'],
            'exam_date': user_settings['exam_date'],
            'd_day': calculate_dday(user_settings['exam_date'])
        }
    
    # 나머지 코드 동일...
    return render_template('pages/home.html',
                         user_name=user_data['user_name'],
                         exam_date=user_data['exam_date'],
                         d_day=user_data['d_day'],
                         stats=stats_data,
                         progress=progress_data,
                         daily=daily_data)
```

### **Task 3: 설정 화면 완전 구현 (5분)**

#### **settings() 함수 수정**
```python
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """설정 화면 - 완전 구현"""
    if request.method == 'POST':
        # 사용자 설정 저장
        save_user_settings(request.form)
        
        # 성공 메시지와 함께 홈으로 리다이렉트
        return redirect(url_for('home'))
    
    # GET 요청: 현재 설정 로드
    user_settings = get_user_settings()
    
    return render_template('pages/settings.html', 
                         user_settings=user_settings)
```

---

## 🎨 **템플릿 수정 (최소한)**

### **templates/pages/home.html 수정**
```html
<!-- 사용자 정보 부분만 수정 -->
<div class="text-left">
    <div class="text-lg font-semibold text-gray-800">사용자: {{ user_name }}</div>
    <div class="text-sm text-gray-600">시험명: ACIU</div>
</div>

<!-- 우측상단: 시험일 -->
<div class="text-right">
    <div class="text-sm text-gray-600">시험일</div>
    <div class="text-lg font-semibold text-gray-800">{{ exam_date }}</div>
</div>

<!-- D-day 카운터 -->
<div class="text-center mb-6">
    <div class="text-6xl font-bold text-blue-600 mb-2">{{ d_day }}</div>
    <div class="text-sm text-gray-600">시험까지 남은 일수</div>
</div>
```

### **설정 버튼 링크 수정**
```html
<!-- 기존 설정 버튼에 실제 링크 연결 -->
<a href="/settings" class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm">
    ⚙️ 설정
</a>
```

---

## ⚡ **실행 순서 (20분)**

### **Step 1: 엄격한 형상관리 백업 (3분)**
```bash
cd 05_Development/

# 1. 타임스탬프 생성
TIMESTAMP=$(date +%Y%m%d_%H%M)
echo "백업 시작: $TIMESTAMP"

# 2. 검증된 Phase 3-1 마스터 버전 백업
cp app_v1.2.py app_v1.2_MASTER_backup_${TIMESTAMP}.py
cp time_sync_v11.py time_sync_v11_backup_${TIMESTAMP}.py
cp data_manager_v11.py data_manager_v11_backup_${TIMESTAMP}.py

# 3. 백업 완료 확인
ls -la *backup*${TIMESTAMP}*
echo "✅ 검증된 마스터 버전 안전 백업 완료"

# 4. 백업 정보 기록
echo "# Phase 3-1.5 설정기능 개발 전 백업
백업일시: $(date)
백업 파일들:
- app_v1.2_MASTER_backup_${TIMESTAMP}.py (홈페이지 로딩 검증 완료)
- time_sync_v11_backup_${TIMESTAMP}.py
- data_manager_v11_backup_${TIMESTAMP}.py

복구 방법:
cp app_v1.2_MASTER_backup_${TIMESTAMP}.py app_v1.2.py
python app_v1.2.py
" > backup_info_phase3-1-5_${TIMESTAMP}.md

echo "✅ 백업 정보 기록 완료"
```

### **Step 2: 안전한 새 버전 생성 (1분)**
```bash
# 1. 새 버전 파일 생성 (마스터는 절대 건드리지 않음)
cp app_v1.2.py app_v1.3_settings_dev.py
echo "✅ app_v1.3_settings_dev.py 생성 - 설정 기능 개발 전용"

# 2. 개발 환경 확인
echo "현재 개발 환경:"
echo "- 마스터 보존: app_v1.2.py (절대 수정 금지)"
echo "- 개발용: app_v1.3_settings_dev.py (수정 가능)"
echo "- 롤백: app_v1.2_MASTER_backup_${TIMESTAMP}.py (비상용)"
```

### **Step 3: 코드 수정 (15분) - app_v1.3_settings_dev.py에서만**
- ⚠️ **절대 app_v1.2.py 수정 금지**
- ✅ **app_v1.3_settings_dev.py에서만 작업**
- Task 1: 함수들 추가
- Task 2: home() 함수 수정  
- Task 3: settings() 함수 수정

### **Step 4: 안전 테스트 (3분)**
```bash
# 1. 새 버전 테스트
python app_v1.3_settings_dev.py

# 2. 문제 발생 시 즉시 롤백
# Ctrl+C로 서버 중단 후
cp app_v1.2_MASTER_backup_${TIMESTAMP}.py app_v1.2.py
python app_v1.2.py
echo "✅ 마스터 버전으로 즉시 복구 완료"

# 3. 성공 시에만 버전업
# 테스트 성공 확인 후
mv app_v1.3_settings_dev.py app_v1.3.py
echo "✅ 설정 기능 개발 완료 - 새 마스터 버전"
```

---

## 🎯 **완료 기준**

### **필수 달성 목표**
- [ ] 설정 화면 정상 표시
- [ ] 사용자 이름, 시험일 입력 가능
- [ ] 저장 후 홈 화면에 반영
- [ ] D-day 자동 계산 표시
- [ ] 통계 시작점 = 설정 등록일

### **성공 시나리오**
```
1. 홈 화면: "사용자 (미설정)" 표시
2. 설정 클릭 → 설정 화면 이동
3. 이름: "조대표님", 시험일: "2025-12-15" 입력
4. 저장 클릭 → 홈 화면 복귀
5. 홈 화면: "조대표님", "2025년 12월 15일", "D-132일" 표시
6. 이후 모든 통계는 오늘부터 시작
```

---

## 🔒 **형상관리 안전장치**

### **3단계 안전망**
```
1단계: 검증된 마스터 (app_v1.2.py) - 절대 수정 금지
2단계: 백업 파일 (app_v1.2_MASTER_backup_YYYYMMDD_HHMM.py) - 비상 복구용
3단계: 개발 파일 (app_v1.3_settings_dev.py) - 수정 가능
```

### **작업 중 절대 규칙**
- 🚫 **절대 금지**: app_v1.2.py 직접 수정
- ✅ **허용**: app_v1.3_settings_dev.py에서만 작업
- 🆘 **비상시**: 언제든 백업으로 즉시 복구

### **성공 시에만 승격**
```bash
# 설정 기능 완전 성공 후에만
mv app_v1.3_settings_dev.py app_v1.3.py
echo "✅ 새로운 검증된 마스터 버전 승격"
```

---

## 🚀 **Phase 3-2 연계**

### **설정 완료 후 장점**
- ✅ 사용자별 통계 관리 기반 완성
- ✅ 실제 사용 가능한 앱으로 발전
- ✅ 문제풀이 기능 개발 시 올바른 통계 시작점 확보
- ✅ 다중 사용자 지원 기반 마련

**조대표님의 판단이 정확합니다. 지금이 설정 기능을 완성할 최적의 타이밍입니다!**

---

**작성 완료**: 2025년 8월 5일 화요일 22:32 KST  
**노팀장 (기술팀장)**