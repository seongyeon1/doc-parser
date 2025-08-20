import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundProcessor:
    """백그라운드에서 이미지 처리를 담당하는 클래스"""
    
    def __init__(self, results_dir: Path, max_workers: int = 3):
        self.results_dir = results_dir
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_queue = asyncio.Queue()
        self.is_running = False
        self.worker_task = None
        
    async def start(self):
        """백그라운드 워커를 시작합니다."""
        if not self.is_running:
            self.is_running = True
            self.worker_task = asyncio.create_task(self._worker_loop())
            logger.info("백그라운드 프로세서가 시작되었습니다.")
    
    async def stop(self):
        """백그라운드 워커를 중지합니다."""
        if self.is_running:
            self.is_running = False
            if self.worker_task:
                self.worker_task.cancel()
                try:
                    await self.worker_task
                except asyncio.CancelledError:
                    pass
            self.executor.shutdown(wait=True)
            logger.info("백그라운드 프로세서가 중지되었습니다.")
    
    async def submit_image_analysis_task(
        self,
        file_content: bytes,
        filename: str,
        prompt: str = "이 이미지를 분석하고 주요 내용을 설명해주세요.",
        detail: str = "auto",
        callback_url: Optional[str] = None
    ) -> str:
        """이미지 분석 작업을 제출합니다."""
        task_id = str(uuid.uuid4())
        
        # 작업 정보 생성
        task_info = {
            "task_id": task_id,
            "filename": filename,
            "prompt": prompt,
            "detail": detail,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "callback_url": callback_url,
            "progress": 0
        }
        
        # 작업을 큐에 추가
        await self.task_queue.put({
            "task_id": task_id,
            "type": "image_analysis",
            "file_content": file_content,
            "task_info": task_info,
            "filename": filename  # 파일명도 함께 전달
        })
        
        # 작업 정보 저장
        self.tasks[task_id] = task_info
        
        # 작업 상태 파일 생성
        await self._save_task_status(task_id, task_info)
        
        logger.info(f"이미지 분석 작업이 제출되었습니다. Task ID: {task_id}")
        return task_id
    
    async def submit_table_extraction_task(
        self,
        file_content: bytes,
        filename: str,
        model: str = "gpt-4o",
        callback_url: Optional[str] = None
    ) -> str:
        """표 추출 작업을 제출합니다."""
        task_id = str(uuid.uuid4())
        
        # 작업 정보 생성
        task_info = {
            "task_id": task_id,
            "filename": filename,
            "model": model,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "callback_url": callback_url,
            "progress": 0
        }
        
        # 작업을 큐에 추가
        await self.task_queue.put({
            "task_id": task_id,
            "type": "table_extraction",
            "file_content": file_content,
            "task_info": task_info,
            "filename": filename  # 파일명도 함께 전달
        })
        
        # 작업 정보 저장
        self.tasks[task_id] = task_info
        
        # 작업 상태 파일 저장
        await self._save_task_status(task_id, task_info)
        
        logger.info(f"표 추출 작업이 제출되었습니다. Task ID: {task_id}")
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """작업 상태를 조회합니다."""
        if task_id in self.tasks:
            return self.tasks[task_id]
        return None
    
    async def get_all_tasks(self) -> List[Dict[str, Any]]:
        """모든 작업 목록을 반환합니다."""
        return list(self.tasks.values())
    
    async def cancel_task(self, task_id: str) -> bool:
        """작업을 취소합니다."""
        if task_id in self.tasks:
            task_info = self.tasks[task_id]
            if task_info["status"] in ["pending", "processing"]:
                task_info["status"] = "cancelled"
                task_info["cancelled_at"] = datetime.now().isoformat()
                await self._save_task_status(task_id, task_info)
                logger.info(f"작업이 취소되었습니다. Task ID: {task_id}")
                return True
        return False
    
    async def _worker_loop(self):
        """백그라운드 워커 루프"""
        logger.info("백그라운드 워커 루프가 시작되었습니다.")
        
        while self.is_running:
            try:
                # 큐에서 작업 가져오기 (1초 타임아웃)
                try:
                    task_data = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                
                # 작업 처리
                await self._process_task(task_data)
                
            except asyncio.CancelledError:
                logger.info("백그라운드 워커가 취소되었습니다.")
                break
            except Exception as e:
                logger.error(f"백그라운드 워커에서 오류 발생: {str(e)}")
                logger.error(traceback.format_exc())
    
    async def _process_task(self, task_data: Dict[str, Any]):
        """작업을 처리합니다."""
        task_id = task_data["task_id"]
        task_type = task_data["type"]
        file_content = task_data["file_content"]
        task_info = task_data["task_info"]
        filename = task_data.get("filename", "")
        
        try:
            # 작업 상태를 processing으로 변경
            task_info["status"] = "processing"
            task_info["started_at"] = datetime.now().isoformat()
            task_info["progress"] = 10
            await self._save_task_status(task_id, task_info)
            
            if task_type == "image_analysis":
                await self._process_image_analysis(task_id, file_content, task_info, filename)
            elif task_type == "table_extraction":
                await self._process_table_extraction(task_id, file_content, task_info, filename)
            
        except Exception as e:
            # 오류 발생 시 상태 업데이트
            task_info["status"] = "failed"
            task_info["error"] = str(e)
            task_info["failed_at"] = datetime.now().isoformat()
            await self._save_task_status(task_id, task_info)
            logger.error(f"작업 처리 중 오류 발생. Task ID: {task_id}, Error: {str(e)}")
    
    async def _process_image_analysis(self, task_id: str, file_content: bytes, task_info: Dict[str, Any], filename: str):
        """이미지 분석 작업을 처리합니다."""
        try:
            # 여기서 실제 이미지 분석 로직을 실행
            # file_processor.analyze_image_with_vision을 호출
            from file_processor import FileProcessor
            import os
            
            file_processor = FileProcessor()
            
            # 파일 확장자 추출
            file_extension = os.path.splitext(filename.lower())[1] if filename else ".png"
            
            # 진행률 업데이트
            task_info["progress"] = 30
            await self._save_task_status(task_id, task_info)
            
            # 이미지 분석 실행
            result = await file_processor.analyze_image_with_vision(
                file_content, 
                file_extension,
                task_info["prompt"], 
                task_info["detail"]
            )
            
            # 진행률 업데이트
            task_info["progress"] = 80
            await self._save_task_status(task_id, task_info)
            
            if result["success"]:
                # 성공 시 결과 저장
                task_info["status"] = "completed"
                task_info["result"] = result
                task_info["completed_at"] = datetime.now().isoformat()
                task_info["progress"] = 100
                
                # 결과 파일 저장
                result_filename = f"background_analysis_{task_id}.json"
                result_file_path = self.results_dir / result_filename
                
                with open(result_file_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                task_info["result_file"] = str(result_file_path)
                
            else:
                # 실패 시 상태 업데이트
                task_info["status"] = "failed"
                task_info["error"] = result.get("error", "알 수 없는 오류")
                task_info["failed_at"] = datetime.now().isoformat()
            
            await self._save_task_status(task_id, task_info)
            
        except Exception as e:
            raise e
    
    async def _process_table_extraction(self, task_id: str, file_content: bytes, task_info: Dict[str, Any], filename: str):
        """표 추출 작업을 처리합니다."""
        try:
            # 여기서 실제 표 추출 로직을 실행
            from table_extractor import TableExtractor
            import os
            
            table_extractor = TableExtractor()
            
            # 파일 확장자 추출
            file_extension = os.path.splitext(filename.lower())[1] if filename else ".png"
            
            # 진행률 업데이트
            task_info["progress"] = 30
            await self._save_task_status(task_id, task_info)
            
            # 표 추출 실행
            result = await table_extractor.extract_tables_from_image(
                file_content, 
                file_extension,
                task_info["model"]
            )
            
            # 진행률 업데이트
            task_info["progress"] = 80
            await self._save_task_status(task_id, task_info)
            
            if result["success"]:
                # 성공 시 결과 저장
                task_info["status"] = "completed"
                task_info["result"] = result
                task_info["completed_at"] = datetime.now().isoformat()
                task_info["progress"] = 100
                
                # 결과 파일 저장
                result_filename = f"background_table_extraction_{task_id}.json"
                result_file_path = self.results_dir / result_filename
                
                with open(result_file_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                task_info["result_file"] = str(result_file_path)
                
            else:
                # 실패 시 상태 업데이트
                task_info["status"] = "failed"
                task_info["error"] = result.get("error", "알 수 없는 오류")
                task_info["failed_at"] = datetime.now().isoformat()
            
            await self._save_task_status(task_id, task_info)
            
        except Exception as e:
            raise e
    
    async def _save_task_status(self, task_id: str, task_info: Dict[str, Any]):
        """작업 상태를 파일에 저장합니다."""
        try:
            status_filename = f"task_status_{task_id}.json"
            status_file_path = self.results_dir / status_filename
            
            with open(status_file_path, "w", encoding="utf-8") as f:
                json.dump(task_info, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"작업 상태 저장 중 오류 발생: {str(e)}")
    
    async def cleanup_completed_tasks(self, max_age_hours: int = 24):
        """완료된 오래된 작업들을 정리합니다."""
        try:
            current_time = datetime.now()
            tasks_to_remove = []
            
            for task_id, task_info in self.tasks.items():
                if task_info["status"] in ["completed", "failed", "cancelled"]:
                    # 작업 완료 시간 확인
                    if "completed_at" in task_info:
                        completed_time = datetime.fromisoformat(task_info["completed_at"])
                    elif "failed_at" in task_info:
                        completed_time = datetime.fromisoformat(task_info["failed_at"])
                    elif "cancelled_at" in task_info:
                        completed_time = datetime.fromisoformat(task_info["cancelled_at"])
                    else:
                        continue
                    
                    # 지정된 시간보다 오래된 작업인지 확인
                    if (current_time - completed_time).total_seconds() > max_age_hours * 3600:
                        tasks_to_remove.append(task_id)
            
            # 오래된 작업 제거
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
                
                # 상태 파일도 삭제
                status_filename = f"task_status_{task_id}.json"
                status_file_path = self.results_dir / status_filename
                if status_file_path.exists():
                    status_file_path.unlink()
            
            if tasks_to_remove:
                logger.info(f"{len(tasks_to_remove)}개의 오래된 작업이 정리되었습니다.")
                
        except Exception as e:
            logger.error(f"작업 정리 중 오류 발생: {str(e)}")
