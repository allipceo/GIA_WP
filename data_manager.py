import pandas as pd
from time_sync import get_korea_time, auto_timestamp_decorator

class DataManager:
    def __init__(self):
        self.master_data = None
        self.categories_cache = {}
        self.load_time = None
    
    @auto_timestamp_decorator
    def load_master_csv(self):
        """마스터 CSV 파일 로드 (시간 자동 기록)"""
        try:
            self.master_data = pd.read_csv('./data/ins_master_db.csv')
            self.load_time = get_korea_time()['formatted']
            print(f"✅ 마스터 데이터 로드 완료: {len(self.master_data)}개 문제")
            return True
        except Exception as e:
            print(f"❌ 마스터 데이터 로드 실패: {e}")
            return False
    
    def get_questions_by_category(self, category):
        """카테고리별 문제 추출 (QUESTION 필드 파싱 절대 금지!)"""
        if self.master_data is None:
            self.load_master_csv()
        
        category_map = {
            'property_insurance': '06재산보험',
            'specialty_insurance': '07특종보험',
            'liability_insurance': '08배상책임보험',
            'marine_insurance': '09해상보험'
        }
        
        if category not in category_map:
            return []
        
        # LAYER1 기준 필터링
        filtered_df = self.master_data[
            self.master_data['LAYER1'] == category_map[category]
        ]
        
        questions = []
        for _, row in filtered_df.iterrows():
            # 🚨 QUESTION 필드 파싱 절대 금지 - 그대로 사용!
            question = {
                "id": row["QCODE"],
                "question_text": row["QUESTION"],  # 파싱 없이 그대로
                "correct_answer": row["ANSWER"],
                "question_type": row["TYPE"],
                "explanation": row["EXPLAIN"],      # 파싱 없이 그대로
                "category": category,
                "layer1": row["LAYER1"],
                "layer2": row["LAYER2"],
                "source": row["SOURCE"]
            }
            questions.append(question)
        
        return questions

@auto_timestamp_decorator
def validate_csv_data():
    """CSV 데이터 무결성 검증"""
    data_manager = DataManager()
    
    # 1. 파일 로드 검증
    if not data_manager.load_master_csv():
        return False
    
    # 2. 총 문제 수 검증
    total_questions = len(data_manager.master_data)
    print(f"📊 총 문제 수: {total_questions}개")
    
    # 3. 카테고리별 문제 수 검증
    categories = ['property_insurance', 'specialty_insurance', 
                 'liability_insurance', 'marine_insurance']
    
    for category in categories:
        questions = data_manager.get_questions_by_category(category)
        print(f"✅ {category}: {len(questions)}개 문제")
    
    return True

if __name__ == "__main__":
    # 테스트 실행
    print("🔄 CSV 데이터 검증 시작...")
    validate_csv_data() 