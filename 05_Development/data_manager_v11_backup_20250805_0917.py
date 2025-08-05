import pandas as pd
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.master_data = None
        self.load_time = None
    
    def load_master_csv(self):
        """마스터 CSV 파일 로드 - 실제 폴더 구조 반영"""
        try:
            # 실제 폴더 구조에 맞는 경로
            possible_paths = [
                '../06_Data/ins_master_db.csv',  # 05_Development에서 06_Data로
                '06_Data/ins_master_db.csv',     # 루트에서 06_Data로
                './06_Data/ins_master_db.csv'    # 현재 경로에서 06_Data로
            ]
            
            csv_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    csv_path = path
                    print(f"✅ CSV 파일 발견: {path}")
                    break
            
            if csv_path is None:
                print("❌ 06_Data/ins_master_db.csv 파일을 찾을 수 없습니다.")
                print("현재 작업 디렉토리:", os.getcwd())
                print("존재하는 파일들:", os.listdir('.'))
                return False
            
            self.master_data = pd.read_csv(csv_path)
            self.load_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"✅ CSV 로드 완료: {len(self.master_data)}개 문제")
            return True
            
        except Exception as e:
            print(f"❌ CSV 로드 실패: {e}")
            return False
    
    def get_total_questions_count(self):
        """전체 문제 수 반환"""
        return len(self.master_data) if self.master_data is not None else 1379
    
    def get_ins_questions_count(self):
        """인스교재 문제 수 반환"""
        if self.master_data is not None:
            return len(self.master_data[self.master_data['SOURCE'].str.contains('인스교재', na=False)])
        return 700
    
    def get_all_categories(self):
        """모든 카테고리 정보 반환"""
        return {
            "property_insurance": {
                "display_name": "재산보험",
                "question_count": 399,
                "icon": "🏢",
                "color_code": "#3B82F6"
            },
            "specialty_insurance": {
                "display_name": "특종보험",
                "question_count": 292,
                "icon": "🚗", 
                "color_code": "#10B981"
            },
            "liability_insurance": {
                "display_name": "배상책임보험",
                "question_count": 268,
                "icon": "⚖️",
                "color_code": "#F59E0B"
            },
            "marine_insurance": {
                "display_name": "해상보험",
                "question_count": 420,
                "icon": "🚢",
                "color_code": "#8B5CF6"
            }
        }
    
    def get_questions_by_category(self, category):
        """카테고리별 문제 반환"""
        if self.master_data is None:
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
                "explanation": row["EXPLAIN"],
                "layer1": row["LAYER1"],
                "layer2": row["LAYER2"],
                "source": row["SOURCE"]
            })
        
        return questions
    
    def get_question_by_id(self, question_id):
        """특정 문제 ID로 문제 반환"""
        if self.master_data is None:
            return None
        
        question_row = self.master_data[self.master_data['QCODE'] == question_id]
        
        if question_row.empty:
            return None
        
        row = question_row.iloc[0]
        return {
            "id": row["QCODE"],
            "question_text": row["QUESTION"],
            "correct_answer": row["ANSWER"],
            "question_type": row["TYPE"],
            "explanation": row["EXPLAIN"],
            "layer1": row["LAYER1"],
            "layer2": row["LAYER2"],
            "source": row["SOURCE"]
        } 