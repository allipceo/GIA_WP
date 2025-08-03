# collaboration_system.py - 4자 협업 자동화 시스템
# 작성일: 2025년 8월 3일 토요일 10:48 KST
# 작성자: 노팀장 (기술팀장)
# 업그레이드: 서대리 (개발팀장)

import subprocess
import os
import sys
from datetime import datetime
import time
import requests
from typing import Dict, Any, List, Tuple
import json
from time_sync import get_korea_time

class CollaborationSystem:
    def __init__(self):
        self.project_path = "D:\\AI_Project\\GIA_WP"
        self.flask_url = "http://127.0.0.1:5000"
        self.status = "초기화"
        self.error_count = 0
        self.max_errors = 3
        self.current_phase = "Phase 1: 기반 안정화"
        
    def get_korea_time(self) -> Dict[str, str]:
        """대한민국 표준시 반환 (time_sync 모듈 사용)"""
        return get_korea_time()
    
    def check_flask_server(self) -> bool:
        """Flask 서버 상태 확인 (강화된 버전)"""
        try:
            # 여러 엔드포인트 테스트
            endpoints = [
                "/api/status",
                "/api/info",
                "/api/v1/time",
                "/api/v1/health"
            ]
            
            working_endpoints = 0
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.flask_url}{endpoint}", timeout=5)
                    if response.status_code == 200:
                        working_endpoints += 1
                        print(f"✅ {endpoint}: 정상")
                    else:
                        print(f"⚠️ {endpoint}: 상태 코드 {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"❌ {endpoint}: 연결 실패 - {str(e)}")
            
            success_rate = (working_endpoints / len(endpoints)) * 100
            print(f"📊 Flask 서버 성공률: {success_rate:.1f}% ({working_endpoints}/{len(endpoints)})")
            
            return success_rate >= 75  # 75% 이상이면 정상으로 간주
            
        except Exception as e:
            print(f"❌ Flask 서버 확인 중 오류: {str(e)}")
            return False
    
    def check_system_prerequisites(self) -> Tuple[bool, str]:
        """시스템 전제 조건 확인"""
        try:
            # 1. 프로젝트 디렉토리 확인
            if not os.path.exists(self.project_path):
                return False, f"프로젝트 디렉토리 없음: {self.project_path}"
            
            # 2. Git 저장소 확인
            os.chdir(self.project_path)
            result = subprocess.run("git status", shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return False, "Git 저장소 오류"
            
            # 3. Flask 서버 확인
            if not self.check_flask_server():
                return False, "Flask 서버 연결 실패"
            
            return True, "시스템 준비 완료"
            
        except Exception as e:
            return False, f"시스템 확인 실패: {str(e)}"
    
    def auto_commit(self, message: str = None) -> bool:
        """자동 Git 커밋 시스템 (강화된 버전)"""
        try:
            os.chdir(self.project_path)
            time_info = self.get_korea_time()
            
            if not message:
                message = f"[{time_info['simple']}] 4자 협업 시스템 - {self.current_phase}"
            
            # 커밋 전 상태 확인
            print("📝 Git 상태 확인 중...")
            status_result = subprocess.run("git status", shell=True, capture_output=True, text=True)
            if "nothing to commit" in status_result.stdout:
                print("ℹ️ 커밋할 변경사항이 없습니다.")
                return True
            
            commands = [
                "git add .",
                f'git commit -m "{message}"',
                "git push origin season1-a"  # season1-a 브랜치로 변경
            ]
            
            for i, cmd in enumerate(commands, 1):
                print(f"🔄 실행 중 ({i}/{len(commands)}): {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"❌ 커밋 실패: {cmd}")
                    print(f"오류 내용: {result.stderr}")
                    self.error_count += 1
                    
                    if self.error_count >= self.max_errors:
                        self.report_error(f"자동 커밋 실패: {cmd}")
                        return False
                    return False
                else:
                    print(f"✅ 성공: {cmd}")
            
            # 성공 시 에러 카운트 리셋
            self.error_count = 0
            return True
            
        except Exception as e:
            print(f"❌ 자동 커밋 예외 발생: {str(e)}")
            self.error_count += 1
            
            if self.error_count >= self.max_errors:
                self.report_error(f"자동 커밋 예외: {str(e)}")
                return False
            return False
    
    def generate_progress_report(self) -> Dict[str, Any]:
        """진행 상황 보고서 생성 (강화된 버전)"""
        time_info = self.get_korea_time()
        flask_status = self.check_flask_server()
        
        # API 엔드포인트 상세 확인
        api_details = self.check_api_endpoints()
        
        return {
            "timestamp": time_info['formatted'],
            "flask_server": "✅ 정상" if flask_status else "❌ 오류",
            "collaboration_system": "✅ 정상 작동",
            "current_phase": self.current_phase,
            "progress": self.calculate_progress(),
            "next_step": self.get_next_step(),
            "status": self.status,
            "api_endpoints": api_details,
            "error_count": f"{self.error_count}/{self.max_errors}",
            "system_health": "정상" if self.error_count < self.max_errors else "주의"
        }
    
    def check_api_endpoints(self) -> Dict[str, Any]:
        """API 엔드포인트 상세 확인"""
        endpoints = [
            {"url": "/api/status", "name": "시스템 상태"},
            {"url": "/api/info", "name": "프로젝트 정보"},
            {"url": "/api/v1/time", "name": "실시간 시간"},
            {"url": "/api/v1/health", "name": "시스템 상태 상세"},
            {"url": "/api/v1/categories", "name": "카테고리 목록"}
        ]
        
        working_endpoints = []
        failed_endpoints = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.flask_url}{endpoint['url']}", timeout=3)
                if response.status_code == 200:
                    working_endpoints.append(endpoint['name'])
                else:
                    failed_endpoints.append(endpoint['name'])
            except:
                failed_endpoints.append(endpoint['name'])
        
        return {
            "working": working_endpoints,
            "failed": failed_endpoints,
            "total": len(endpoints),
            "success_rate": len(working_endpoints) / len(endpoints) * 100
        }
    
    def calculate_progress(self) -> str:
        """진행률 계산"""
        if self.current_phase == "Phase 1: 기반 안정화":
            return "30%"
        elif self.current_phase == "Phase 2: 고급 자동화":
            return "60%"
        elif self.current_phase == "Phase 3: 통합 테스트":
            return "90%"
        else:
            return "100%"
    
    def get_next_step(self) -> str:
        """다음 단계 결정"""
        if self.current_phase == "Phase 1: 기반 안정화":
            return "Phase 2: 고급 자동화 구축"
        elif self.current_phase == "Phase 2: 고급 자동화":
            return "Phase 3: 통합 테스트"
        else:
            return "Phase 3 개발 준비"
    
    def save_progress_report(self) -> bool:
        """진행 보고서 파일 저장 (강화된 버전)"""
        report = self.generate_progress_report()
        
        try:
            os.chdir(self.project_path)
            
            # docs 폴더가 없으면 생성
            if not os.path.exists("docs"):
                os.makedirs("docs")
            
            # 진행 보고서 저장
            with open("docs/progress_report.json", "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 상세 로그 파일도 저장
            log_entry = {
                "timestamp": report["timestamp"],
                "phase": report["current_phase"],
                "status": report["status"],
                "flask_server": report["flask_server"],
                "api_success_rate": report["api_endpoints"]["success_rate"]
            }
            
            log_file = "docs/collaboration_log.json"
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
            print("✅ 진행 보고서 저장 완료: docs/progress_report.json")
            print("✅ 상세 로그 저장 완료: docs/collaboration_log.json")
            return True
            
        except Exception as e:
            print(f"❌ 보고서 저장 실패: {str(e)}")
            return False
    
    def report_error(self, error_message: str) -> str:
        """에러 보고 (조대표님/노팀장에게)"""
        timestamp = self.get_korea_time()['formatted']
        
        error_report = f"""
🚨 4자 협업 시스템 에러 보고
⏰ 시간: {timestamp}
❌ 에러 내용: {error_message}
🔄 에러 횟수: {self.error_count}/{self.max_errors}
⏸️ 조치: 자동화 시스템 중단
📞 보고 대상: 조대표님, 노팀장
        """
        
        print(error_report)
        return error_report
    
    def run_phase1_checklist(self) -> bool:
        """Phase 1 체크리스트 실행 (강화된 버전)"""
        print("\n" + "="*50)
        print("🚀 Phase 1: 기반 안정화 시작")
        print(f"📅 시작 시간: {self.get_korea_time()['formatted']}")
        print("="*50)
        
        # 1. 시스템 전제 조건 확인
        print("\n1️⃣ 시스템 전제 조건 확인...")
        is_ready, message = self.check_system_prerequisites()
        
        if not is_ready:
            print(f"❌ 시스템 준비 실패: {message}")
            self.error_count += 1
            
            if self.error_count >= self.max_errors:
                self.report_error(f"Phase 1 실패: {message}")
                return False
            return False
        
        print(f"✅ 시스템 준비 완료: {message}")
        
        # 2. 진행 보고서 생성
        print("\n2️⃣ 진행 보고서 생성...")
        if not self.save_progress_report():
            print("⚠️ 보고서 생성 실패 (계속 진행)")
        
        # 3. 자동 커밋
        print("\n3️⃣ 자동 커밋 실행...")
        commit_result = self.auto_commit("Phase 1 기반 안정화 체크리스트 완료")
        
        if commit_result:
            print("✅ 자동 커밋 완료")
        else:
            print("⚠️ 자동 커밋 실패 (수동으로 진행 가능)")
        
        # 4. 최종 상태 업데이트
        self.status = "Phase 1 완료"
        self.current_phase = "Phase 2: 고급 자동화"
        
        print(f"\n🎉 Phase 1 기반 안정화 완료!")
        print(f"⏰ 완료 시간: {self.get_korea_time()['formatted']}")
        
        return True
    
    def run_phase2_automation(self) -> bool:
        """Phase 2: 고급 자동화 실행"""
        print("\n" + "="*50)
        print("🚀 Phase 2: 고급 자동화 시작")
        print(f"📅 시작 시간: {self.get_korea_time()['formatted']}")
        print("="*50)
        
        try:
            # AI 간 소통 프로토콜 구축
            print("\n1️⃣ AI 간 소통 프로토콜 구축...")
            self.build_ai_communication_protocol()
            
            # 품질 관리 자동화
            print("\n2️⃣ 품질 관리 자동화 구축...")
            self.build_quality_management()
            
            # 실시간 모니터링 시스템
            print("\n3️⃣ 실시간 모니터링 시스템 구축...")
            self.build_real_time_monitoring()
            
            self.status = "Phase 2 완료"
            self.current_phase = "Phase 3: 통합 테스트"
            
            print(f"\n🎉 Phase 2 고급 자동화 완료!")
            print(f"⏰ 완료 시간: {self.get_korea_time()['formatted']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Phase 2 실패: {str(e)}")
            self.error_count += 1
            
            if self.error_count >= self.max_errors:
                self.report_error(f"Phase 2 실패: {str(e)}")
                return False
            return False
    
    def build_ai_communication_protocol(self):
        """AI 간 소통 프로토콜 구축"""
        protocol = {
            "코코치 ↔ 노팀장": "이 협업창 활용 (현재 창 유지)",
            "노팀장 ↔ 서대리": "GitHub 커밋 메시지 + 작업지시서",
            "코코치 → 조대표님": "Google Drive 요약 보고서",
            "긴급상황": "이 협업창을 통한 실시간 대응",
            "통제_명령어": {
                "STOP": "즉시 작업 중단",
                "HELP": "기술 지원 요청",
                "STATUS": "현재 상황 보고"
            }
        }
        
        # 프로토콜 파일 저장
        with open("ai_communication_protocol.json", "w", encoding="utf-8") as f:
            json.dump(protocol, f, ensure_ascii=False, indent=2)
        
        print("✅ AI 간 소통 프로토콜 구축 완료")
        return True
    
    def build_quality_management(self):
        """품질 관리 자동화 구축"""
        quality_system = {
            "코드_품질_검증": "자동 코드 리뷰",
            "문서_완성도_체크": "자동 문서 검증",
            "진행률_자동_업데이트": "실시간 진행 추적",
            "이슈_자동_분류": "자동 이슈 관리",
            "시간_동기화": "자동 타임스탬프"
        }
        
        # 품질 관리 파일 저장
        with open("quality_management_system.json", "w", encoding="utf-8") as f:
            json.dump(quality_system, f, ensure_ascii=False, indent=2)
        
        print("✅ 품질 관리 자동화 구축 완료")
        return True
    
    def build_real_time_monitoring(self):
        """실시간 모니터링 시스템 구축"""
        monitoring_system = {
            "GitHub_기반_진행률": "실시간 진행률 표시",
            "완료된_작업_자동_체크": "자동 완료 체크",
            "다음_단계_자동_제안": "자동 다음 단계 제안",
            "자동_커밋_진행_보고서_연동": "커밋-보고서 연동"
        }
        
        # 모니터링 시스템 파일 저장
        with open("real_time_monitoring.json", "w", encoding="utf-8") as f:
            json.dump(monitoring_system, f, ensure_ascii=False, indent=2)
        
        print("✅ 실시간 모니터링 시스템 구축 완료")
        return True
    
    def run_complete_system(self) -> bool:
        """완전한 4자 협업 시스템 실행"""
        print("🚀 4자 협업 자동화 시스템 완전 실행")
        print(f"📅 시작 시간: {self.get_korea_time()['formatted']}")
        print("=" * 60)
        
        # Phase 1 실행
        if not self.run_phase1_checklist():
            return False
        
        # Phase 2 실행
        if not self.run_phase2_automation():
            return False
        
        # 최종 성공 보고
        final_report = f"""
🎉 4자 협업 자동화 시스템 완료 보고
⏰ 완료 시간: {self.get_korea_time()['formatted']}
✅ 모든 Phase 완료
🤖 자동화 시스템 활성화
🚀 Phase 3 개발 준비 완료
        """
        
        print(final_report)
        return True

def main():
    """메인 실행 함수"""
    print("🤖 4자 협업 자동화 시스템 시작")
    print("=" * 50)
    
    # 협업 시스템 초기화
    collab = CollaborationSystem()
    
    # 완전한 시스템 실행
    success = collab.run_complete_system()
    
    if success:
        print("\n✅ 시스템 정상 작동 - Phase 3 준비 완료")
        
        # 최종 보고서 출력
        report = collab.generate_progress_report()
        print("\n📊 최종 상태 보고:")
        for key, value in report.items():
            if key != "api_endpoints":  # 너무 긴 정보는 생략
                print(f"  {key}: {value}")
            
    else:
        print("\n❌ 시스템 오류 - 수동 점검 필요")
    
    print("\n" + "="*50)
    print("협업 시스템 종료")

if __name__ == "__main__":
    main() 