# ACIU 시즌2 개발기획서 목차 V4.0

## 1. 프로젝트 개요
### 1.1 시즌1 개발 결과 심화 분석
- 완성된 기능 현황 및 성과
- StatisticsCache와 updateAllStatistics 함수 경험 분석
- 코코치 개발경과보고서 0731.MD 반영
- 한계점 및 문제점 도출 (HTML 기반 비효율성)
- 미완성 기능 (통계 분석) 상세 분석

### 1.2 시즌2 개발 목표
- 기술 스택 현대화
- 개발 효율성 향상
- 통계 기능 완성
- AI 협업 체계 혁신

## 2. 기술 스택 전환 계획
### 2.1 백엔드 프레임워크
- Python Flask 기반 웹 애플리케이션
- HTML/CSS/JS → Flask 템플릿 엔진 활용

### 2.2 백엔드 아키텍처
- 로컬 파일 시스템 → JSON API 구조

### 2.3 배포 환경
- 정적 호스팅 → Heroku 클라우드 배포

### 2.4 개발 환경
- GitHub 기반 버전 관리
- Cursor AI 통합 개발 환경

## 3. 데이터 마이그레이션 및 구조 재설계
### 3.1 단계적 데이터 마이그레이션 전략
- CSV → JSON 변환 스크립트 개발
- 데이터 무결성 검증 프로세스
- 시즌1 사용자 통계 데이터 보존 방안
- 롤백 계획 수립

### 3.2 JSON 데이터 구조 설계
- ins_master_db.csv → 통합 JSON 스키마
- Layer1 기준 대분류별 JSON 파일 분할
- 지연 로딩 및 캐싱 전략 구현

### 3.3 RESTful API 설계 및 확장성
- API 버전 관리 전략 (/api/v1/)
- 확장 가능한 엔드포인트 구조
  - GET /api/v1/questions/<category>
  - POST /api/v1/stats/<user_id>
  - GET /api/v1/stats/<user_id>
- 인증/인가 시스템 (향후 확장)
- API 요청 제한(Rate Limiting) 고려

## 4. 핵