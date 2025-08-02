# test_api.py - API 엔드포인트 자동 테스트 시스템
import requests
from time_sync import get_korea_time

def run_api_tests():
    """API 엔드포인트 자동 테스트"""
    
    base_url = "http://localhost:5000"  # 로컬 테스트
    # base_url = "https://gia-wp-test01-77059d2986d6.herokuapp.com"  # 배포 테스트
    
    tests = [
        {"endpoint": "/api/v1/time", "method": "GET", "name": "실시간 시간 API"},
        {"endpoint": "/api/v1/categories", "method": "GET", "name": "카테고리 목록 API"},
        {"endpoint": "/api/v1/questions/property_insurance", "method": "GET", "name": "재산보험 문제 API"},
        {"endpoint": "/api/v1/question/Q001", "method": "GET", "name": "개별 문제 API"},
        {"endpoint": "/api/v1/health", "method": "GET", "name": "시스템 상태 API"}
    ]
    
    print("🔄 API 테스트 시작...")
    print(f"📅 테스트 시간: {get_korea_time()['formatted']}")
    print("=" * 50)
    
    results = []
    success_count = 0
    
    for i, test in enumerate(tests, 1):
        try:
            print(f"🔍 테스트 {i}: {test['name']}")
            response = requests.get(f"{base_url}{test['endpoint']}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 성공: {response.status_code}")
                success_count += 1
            else:
                print(f"❌ 실패: {response.status_code}")
            
            results.append({
                "endpoint": test['endpoint'],
                "name": test['name'],
                "status": response.status_code,
                "success": response.status_code == 200,
                "time": get_korea_time()['formatted']
            })
            
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            results.append({
                "endpoint": test['endpoint'],
                "name": test['name'],
                "status": "ERROR",
                "success": False,
                "error": str(e),
                "time": get_korea_time()['formatted']
            })
    
    print("=" * 50)
    print(f"📊 테스트 결과: {success_count}/{len(tests)} 성공")
    print(f"📅 완료 시간: {get_korea_time()['formatted']}")
    
    return results

if __name__ == "__main__":
    run_api_tests() 