import pandas as pd

class DataManager:
    def __init__(self):
        self.master_data = None
        self.load_time = None
        self.category_map = {
            'property_insurance': '06재산보험',
            'specialty_insurance': '07특종보험',
            'liability_insurance': '08배상책임보험',
            'marine_insurance': '09해상보험'
        }

    def load_master_csv(self):
        """마스터 CSV 파일을 로드합니다."""
        try:
            from time_sync import get_korea_time
            self.master_data = pd.read_csv('../06_Data/ins_master_db.csv')
            self.load_time = get_korea_time()['formatted']
            print(f"✅ 마스터 데이터 로드 완료: {len(self.master_data)}개 문제")
            return True
        except FileNotFoundError:
            print(f"❌ 마스터 데이터 로드 실패: '../06_Data/ins_master_db.csv' 파일을 찾을 수 없습니다.")
            return False
        except Exception as e:
            print(f"❌ 마스터 데이터 로드 중 오류 발생: {e}")
            return False

    def get_questions_by_category(self, category_key):
        """카테고리 키를 기반으로 문제 목록을 반환합니다."""
        if self.master_data is None:
            self.load_master_csv()
        
        category_value = self.category_map.get(category_key)
        
        if category_value:
            filtered_df = self.master_data[self.master_data['LAYER1'] == category_value]
            questions = filtered_df.to_dict('records')
            
            for q in questions:
                q['category'] = category_key
            
            return questions
        return []

    def get_question_by_id(self):
        """문제 ID로 단일 문제를 찾아서 반환합니다."""
        if self.master_data is None:
            self.load_master_csv()

        question_row = self.master_data[self.master_data['QCODE'] == question_id]
        if not question_row.empty:
            return question_row.iloc[0].to_dict()
        return None

    def get_ins_questions_count(self):
        """인스교재 문제 수를 반환합니다."""
        if self.master_data is None:
            self.load_master_csv()
        
        ins_questions = self.master_data[
            self.master_data['SOURCE'].str.contains('인스교재', na=False)
        ]
        return len(ins_questions)

    def get_total_questions_count(self):
        """전체 문제 수를 반환합니다."""
        if self.master_data is None:
            self.load_master_csv()
        return len(self.master_data)

    def get_all_categories(self):
        """모든 카테고리 정보와 문제 수를 반환합니다."""
        if self.master_data is None:
            self.load_master_csv()
        
        categories_info = {}
        for key, value in self.category_map.items():
            count = len(self.master_data[self.master_data['LAYER1'] == value])
            categories_info[key] = {
                'display_name': value.replace('0', '').replace('재산보험', '재산보험').replace('특종보험', '특종보험').replace('배상책임보험', '배상책임보험').replace('해상보험', '해상보험'),
                'question_count': count
            }
        return categories_info
