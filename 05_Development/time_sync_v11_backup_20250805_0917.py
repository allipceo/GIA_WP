from datetime import datetime
import pytz

def get_korea_time():
    """한국 시간 반환"""
    try:
        korea_tz = pytz.timezone('Asia/Seoul')
        now = datetime.now(korea_tz)
        return {
            'formatted': now.strftime('%Y년 %m월 %d일 %H:%M KST'),
            'iso': now.isoformat(),
            'timestamp': int(now.timestamp())
        }
    except Exception as e:
        # pytz 없을 경우 기본 시간 사용
        now = datetime.now()
        return {
            'formatted': now.strftime('%Y년 %m월 %d일 %H:%M KST'),
            'iso': now.isoformat(),
            'timestamp': int(now.timestamp())
        } 