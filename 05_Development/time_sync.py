from datetime import datetime
import pytz

def get_korea_time():
    """대한민국 표준시를 반환합니다."""
    try:
        korea_tz = pytz.timezone('Asia/Seoul')
        now = datetime.now(korea_tz)
        weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday = weekdays[now.weekday()]

        return {
            'iso': now.isoformat(),
            'formatted': now.strftime(f'%Y년 %m월 %d일 {weekday} %H:%M KST'),
            'simple': now.strftime('%Y-%m-%d %H:%M'),
            'timestamp': int(now.timestamp())
        }
    except Exception as e:
        print(f"시간 동기화 오류: {e}")
        return {
            'formatted': '시간 동기화 실패',
            'iso': None,
            'simple': None,
            'timestamp': 0
        }

def auto_timestamp_decorator(func):
    """함수 실행 시 자동 타임스탬프를 추가하는 데코레이터입니다."""
    def wrapper(*args, **kwargs):
        time_info = get_korea_time()
        print(f"실행 시간: {time_info['formatted']}")
        result = func(*args, **kwargs)
        return result
    return wrapper

if __name__ == '__main__':
    k_time = get_korea_time()
    print(f"현재 시간 정보: {k_time}")
