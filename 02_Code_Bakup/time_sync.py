# time_sync.py - 시간 동기화 모듈
# 작성일: 2025년 8월 3일 토요일 10:48 KST
# 작성자: 노팀장 (기술팀장)

from datetime import datetime

def get_korea_time():
    """대한민국 표준시 반환"""
    now = datetime.now()
    weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday = weekdays[now.weekday()]
    
    return {
        'formatted': now.strftime(f'%Y년 %m월 %d일 {weekday} %H:%M KST'),
        'simple': now.strftime('%Y-%m-%d %H:%M'),
        'timestamp': str(int(now.timestamp()))
    }

def auto_timestamp_decorator(func):
    """함수 실행 시 자동 타임스탬프 추가"""
    def wrapper(*args, **kwargs):
        time_info = get_korea_time()
        print(f"실행 시간: {time_info['formatted']}")
        result = func(*args, **kwargs)
        return result
    return wrapper

def create_report():
    """보고서 생성 시 자동 타임스탬프"""
    time_info = get_korea_time()
    return f"보고서 생성 시간: {time_info['formatted']}"

# 사용 예시
@auto_timestamp_decorator
def flask_app_function():
    """Flask 앱에서 사용할 시간 동기화 함수"""
    time_info = get_korea_time()
    return {
        "current_time": time_info['formatted'],
        "timestamp": time_info['timestamp'],
        "simple_time": time_info['simple']
    }

if __name__ == "__main__":
    # 테스트 실행
    current_time = get_korea_time()
    print(f"🕐 현재 시간: {current_time['formatted']}")
    print(f"📅 간단 형식: {current_time['simple']}")
    print(f"⏰ 타임스탬프: {current_time['timestamp']}") 