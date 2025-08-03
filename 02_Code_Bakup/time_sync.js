// time_sync.js - 서대리 전용 시간 동기화 모듈
class TimeManager {
    static getKoreanTime() {
        const now = new Date();
        const koreaTime = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
        
        const year = koreaTime.getFullYear();
        const month = (koreaTime.getMonth() + 1).toString().padStart(2, '0');
        const day = koreaTime.getDate().toString().padStart(2, '0');
        const hour = koreaTime.getHours().toString().padStart(2, '0');
        const minute = koreaTime.getMinutes().toString().padStart(2, '0');
        
        const weekdays = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];
        const weekday = weekdays[koreaTime.getDay()];
        
        return `${year}년 ${month}월 ${day}일 ${weekday} ${hour}:${minute} KST`;
    }
    
    static generateTimestamp() {
        const time = this.getKoreanTime();
        console.log(`🕐 현재 시간: ${time}`);
        return time;
    }
    
    static getSimpleTime() {
        const now = new Date();
        const koreaTime = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
        
        const year = koreaTime.getFullYear();
        const month = (koreaTime.getMonth() + 1).toString().padStart(2, '0');
        const day = koreaTime.getDate().toString().padStart(2, '0');
        const hour = koreaTime.getHours().toString().padStart(2, '0');
        const minute = koreaTime.getMinutes().toString().padStart(2, '0');
        
        return `${year}-${month}-${day} ${hour}:${minute}`;
    }
    
    static createDocumentHeader(title, author) {
        const currentTime = this.getKoreanTime();
        return `# ${title}

**작성일**: ${currentTime}  
**작성자**: ${author}  
**문서 ID**: DOC_${Date.now()}  
**버전**: v1.0

---`;
    }
}

module.exports = TimeManager; 