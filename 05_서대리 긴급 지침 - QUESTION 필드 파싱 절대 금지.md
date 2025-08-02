# 🚨 서대리 긴급 지침 - QUESTION 필드 파싱 절대 금지

**발령시간**: 2025년 8월 2일 토요일 14:02 KST  
**발령자**: 노팀장 (조대표님 지시사항 전달)  
**수신자**: 서대리 (Cursor AI)  
**우선순위**: 🔴 **최고 긴급 (CRITICAL)**

---

## ⚠️ **절대 금지 사항**

### **QUESTION 필드 파싱 절대 금지**
```python
# ❌ 절대 하지 말 것 - 파싱 시도
def parse_question_content(question_text):
    # 이런 코드 작성 시 프로그램 망가짐
    pass

# ❌ 절대 하지 말 것 - 텍스트 분석
question_parts = question.split("1)")
options = extract_choices(question)

# ❌ 절대 하지 말 것 - 정규식 사용
import re
pattern = r"1\.(.*?)2\.(.*?)"
```

---

## ✅ **올바른 접근 방식**

### **QUESTION 필드는 그대로 출력만**
```python
# ✅ 올바른 방식 - 그대로 표시
def display_question(question_data):
    return {
        "question_text": question_data["QUESTION"],  # 그대로 출력
        "question_type": question_data["TYPE"],      # 진위형/선택형 구분
        "correct_answer": question_data["ANSWER"]    # 정답만 확인
    }

# ✅ 올바른 방식 - 타입별 버튼 생성
def create_answer_buttons(question_type):
    if question_type == "진위형":
        return ["O", "X"]  # O, X 버튼만
    else:
        return ["1", "2", "3", "4"]  # 1,2,3,4 버튼만
```

---

## 🎯 **서대리 작업 방침**

### **1. QUESTION 필드 처리 원칙**
- **입력**: CSV의 QUESTION 필드 값
- **처리**: 아무것도 하지 않음 (NO PARSING!)
- **출력**: 그대로 화면에 표시

### **2. 문제 유형 구분 방법**
```python
def get_question_type(row):
    # TYPE 필드만 확인
    question_type = row["TYPE"]
    
    if "진위" in question_type:
        return "true_false"
    else:
        return "multiple_choice"
```

### **3. 정답 확인 로직**
```python
def check_answer(user_answer, correct_answer):
    # 단순 문자열 비교만
    return user_answer.strip() == correct_answer.strip()
```

### **4. JSON 변환 시 주의사항**
```python
def convert_question_to_json(csv_row):
    return {
        "id": csv_row["QCODE"],
        "question": csv_row["QUESTION"],  # 그대로 저장
        "answer": csv_row["ANSWER"],      # 정답만 저장
        "type": get_question_type(csv_row),
        "explanation": csv_row["EXPLAIN"], # 해설도 그대로
        "category": get_category(csv_row["LAYER1"])
    }
```

---

## 🔍 **시즌1 에러 분석 결과**

### **파싱 에러의 원인**
1. **복잡한 문제 구조**: 문제+보기+선택지가 혼재
2. **불규칙한 형식**: 각 문제마다 다른 레이아웃
3. **특수문자 오류**: 괄호, 숫자, 기호 파싱 실패
4. **텍스트 분할 오류**: 잘못된 분할로 데이터 손실

### **시즌2 해결책**
- **파싱 완전 포기**: 조대표님이 이미 정제 완료
- **있는 그대로 출력**: 화면에 전체 텍스트 표시
- **단순 버튼 매핑**: TYPE 필드만 확인해서 버튼 생성

---

## 🎮 **사용자 인터페이스 설계**

### **화면 구성**
```
┌─────────────────────────────────────┐
│ 문제 번호: Q001                     │
│ 유형: 진위형                        │
├─────────────────────────────────────┤
│                                     │
│ [QUESTION 필드 전체 내용 그대로 출력] │
│                                     │
│ 1. 보험료는...                      │
│ 2. 보상금액은...                    │
│ 3. 계약자는...                      │
│ 4. 피보험자는...                    │
│                                     │
├─────────────────────────────────────┤
│        [1] [2] [3] [4]              │  ← 선택형인 경우
│           [O] [X]                   │  ← 진위형인 경우
└─────────────────────────────────────┘
```

### **사용자 경험**
1. **문제 읽기**: 전체 텍스트 확인
2. **답안 선택**: 하단 버튼 클릭  
3. **결과 확인**: 정답/오답 여부만 표시

---

## 💻 **구체적 구현 지침**

### **CSV 읽기 함수**
```python
def load_questions_from_csv():
    df = pd.read_csv('./data/ins_master_db.csv')
    
    questions = []
    for _, row in df.iterrows():
        question = {
            "id": row["QCODE"],
            "question_text": row["QUESTION"],  # 파싱 금지!
            "correct_answer": row["ANSWER"],
            "question_type": row["TYPE"],
            "explanation": row["EXPLAIN"],     # 파싱 금지!
            "category": row["LAYER1"]
        }
        questions.append(question)
    
    return questions
```

### **API 응답 형식**
```json
{
  "id": "Q001",
  "question_text": "보험계약에서 보험료는 계약자가 지급하는 대가이며, 보상금액은 보험사가 지급하는...",
  "correct_answer": "1",
  "question_type": "선택형",
  "explanation": "보험계약의 기본 원리에 따르면...",
  "category": "property_insurance"
}
```

---

## 🚨 **최종 경고**

### **서대리가 절대 하지 말아야 할 것**
1. ❌ QUESTION 필드 텍스트 분석
2. ❌ 선택지 추출 시도  
3. ❌ 문제 내용 파싱
4. ❌ 정규식 사용
5. ❌ 텍스트 분할 작업

### **서대리가 해야 할 것**
1. ✅ QUESTION 필드 그대로 저장
2. ✅ TYPE 필드로 버튼 종류 결정
3. ✅ ANSWER 필드로 정답 확인
4. ✅ 단순하고 안전한 구현

---

## 🎯 **성공 기준**

**이 지침을 완벽히 따를 경우:**
- ✅ 파싱 에러 0%
- ✅ 모든 문제 정상 출력
- ✅ 안정적인 앱 동작
- ✅ 조대표님 만족

**이 지침을 무시할 경우:**
- ❌ 프로그램 오류 50%
- ❌ 문제 출력 실패
- ❌ 앱 동작 불안정
- ❌ 프로젝트 실패

---

**🔴 이 지침은 프로젝트 성패를 좌우하는 핵심사항입니다!**

**발령 완료**: 2025-08-02 14:02 KST  
**노팀장 (조대표님 지시사항 전달완료)**