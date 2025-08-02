# ACIU 시즌2 API 엔드포인트 상세 명세
# 작성: 노팀장 (기술팀장)
# 일시: 2025-08-02 13:14 KST

"""
Flask 기반 7개 API 엔드포인트 설계
시즌1 HTML 기반 → 시즌2 JSON API 완전 전환
"""

# ========== 1. GET /api/v1/categories ==========
"""
카테고리 목록 및 메타데이터 조회

Response:
{
  "status": "success",
  "data": {
    "categories": {
      "property_insurance": {
        "display_name": "재산보험",
        "question_count": 399,
        "icon": "🏢",
        "color_code": "#3B82F6"
      },
      ...
    },
    "total_questions": 1379,
    "total_categories": 4
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 2. GET /api/v1/questions/<category> ==========
"""
카테고리별 문제 목록 조회

Parameters:
- category: property_insurance, specialty_insurance, liability_insurance, marine_insurance
- limit (optional): 반환할 문제 수 (기본값: 50)
- offset (optional): 시작 위치 (기본값: 0)
- shuffle (optional): 랜덤 순서 여부 (기본값: false)

Response:
{
  "status": "success",
  "data": {
    "category": "property_insurance",
    "questions": [
      {
        "id": "Q001",
        "question": "문제 내용",
        "type": "true_false",
        "options": ["O", "X"] // true_false인 경우
      },
      ...
    ],
    "pagination": {
      "total": 399,
      "limit": 50,
      "offset": 0,
      "has_next": true
    }
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 3. GET /api/v1/question/<id> ==========
"""
개별 문제 상세 조회

Parameters:
- id: 문제 ID (Q001, Q002, ...)

Response:
{
  "status": "success",
  "data": {
    "id": "Q001",
    "qcode": "원본_QCODE",
    "category": "property_insurance",
    "type": "true_false",
    "question": "문제 내용",
    "answer": "O",
    "explanation": "해설 내용",
    "layer1": "재산보험",
    "layer2": "일반재산보험",
    "statistics": {
      "total_attempts": 150,
      "correct_attempts": 120,
      "accuracy_rate": 80
    }
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 4. POST /api/v1/stats ==========
"""
통계 업데이트 (시즌1 updateAllStatistics 함수 대체)

Request Body:
{
  "user_id": "user_12345",
  "question_id": "Q001",
  "user_answer": "O",
  "is_correct": true,
  "category": "property_insurance",
  "mode": "large-category",
  "session_id": "session_abc123"
}

Response:
{
  "status": "success",
  "data": {
    "updated": true,
    "user_stats": {
      "global": {
        "total_attempted": 25,
        "total_correct": 20,
        "accuracy_rate": 80
      },
      "today": {
        "attempted": 5,
        "correct": 4,
        "accuracy_rate": 80
      },
      "category_stats": {
        "property_insurance": {
          "attempted": 10,
          "correct": 8,
          "accuracy_rate": 80
        }
      }
    }
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 5. GET /api/v1/stats/<user_id> ==========
"""
사용자별 통계 조회

Parameters:
- user_id: 사용자 ID
- date (optional): 특정 날짜 통계 (YYYY-MM-DD)
- category (optional): 특정 카테고리 통계

Response:
{
  "status": "success",
  "data": {
    "user_id": "user_12345",
    "global_stats": {
      "total_attempted": 100,
      "total_correct": 85,
      "accuracy_rate": 85,
      "study_days": 15,
      "avg_daily_questions": 6.7
    },
    "category_breakdown": {
      "property_insurance": {
        "attempted": 30,
        "correct": 25,
        "accuracy_rate": 83
      },
      ...
    },
    "daily_progress": {
      "2025-08-02": {
        "attempted": 5,
        "correct": 4,
        "accuracy_rate": 80
      }
    },
    "achievements": [
      {
        "type": "accuracy_streak",
        "description": "5일 연속 80% 이상",
        "earned_at": "2025-08-02"
      }
    ]
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 6. GET /api/v1/health ==========
"""
시스템 상태 확인

Response:
{
  "status": "success",
  "data": {
    "service": "ACIU Quiz API v2.0",
    "status": "healthy",
    "uptime": "2h 30m 15s",
    "version": "2.0.1",
    "environment": "production",
    "database": {
      "status": "connected",
      "questions_loaded": 1379,
      "categories_loaded": 4
    },
    "performance": {
      "avg_response_time": "150ms",
      "requests_per_minute": 45
    }
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 7. POST /api/v1/migrate ==========
"""
시즌1 데이터 마이그레이션

Request Body:
{
  "migration_type": "user_stats", // "csv_data", "user_stats", "full"
  "source_data": {
    "localStorage_backup": "base64_encoded_data",
    "user_settings": {...}
  },
  "options": {
    "preserve_timestamps": true,
    "merge_duplicates": false
  }
}

Response:
{
  "status": "success",
  "data": {
    "migration_id": "migration_001",
    "migrated_items": {
      "questions": 1379,
      "user_stats": 1,
      "categories": 4
    },
    "errors": [],
    "warnings": [
      "Some legacy data formats were automatically converted"
    ],
    "completion_time": "15.3s"
  },
  "timestamp": "2025-08-02T13:14:00Z"
}
"""

# ========== 공통 에러 응답 형식 ==========
"""
Error Response Format:
{
  "status": "error",
  "error": {
    "code": "QUESTION_NOT_FOUND",
    "message": "Question with ID 'Q999' not found",
    "details": {
      "requested_id": "Q999",
      "available_range": "Q001-Q1379"
    }
  },
  "timestamp": "2025-08-02T13:14:00Z"
}

HTTP Status Codes:
- 200: Success
- 400: Bad Request (잘못된 파라미터)
- 404: Not Found (리소스 없음)
- 500: Internal Server Error (서버 오류)
"""

# ========== API 보안 및 제한사항 ==========
"""
Rate Limiting:
- 일반 요청: 100 requests/minute
- 통계 업데이트: 50 requests/minute
- 마이그레이션: 5 requests/hour

CORS Policy:
- 허용 도메인: *.herokuapp.com, localhost
- 허용 메서드: GET, POST, OPTIONS
- 허용 헤더: Content-Type, Authorization

Caching Strategy:
- 카테고리 정보: 1시간 캐시
- 문제 데이터: 30분 캐시
- 사용자 통계: 실시간 (캐시 없음)
"""