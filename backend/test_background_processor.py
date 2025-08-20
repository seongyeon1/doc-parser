#!/usr/bin/env python3
"""
백그라운드 프로세서 테스트 스크립트
"""

import asyncio
import json
from pathlib import Path
from background_processor import BackgroundProcessor

async def test_background_processor():
    """백그라운드 프로세서의 기본 기능을 테스트합니다."""
    
    # 결과 디렉토리 설정
    results_dir = Path("analyze/result")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 백그라운드 프로세서 초기화
    processor = BackgroundProcessor(results_dir, max_workers=2)
    
    try:
        # 프로세서 시작
        print("백그라운드 프로세서 시작...")
        await processor.start()
        
        # 테스트용 더미 데이터
        dummy_file_content = b"dummy image content"
        dummy_filename = "test_image.png"
        
        # 이미지 분석 작업 제출
        print("\n1. 이미지 분석 작업 제출...")
        task_id_1 = await processor.submit_image_analysis_task(
            file_content=dummy_file_content,
            filename=dummy_filename,
            prompt="이 이미지를 분석해주세요.",
            detail="high"
        )
        print(f"   작업 ID: {task_id_1}")
        
        # 표 추출 작업 제출
        print("\n2. 표 추출 작업 제출...")
        task_id_2 = await processor.submit_table_extraction_task(
            file_content=dummy_file_content,
            filename=dummy_filename,
            model="gpt-4o"
        )
        print(f"   작업 ID: {task_id_2}")
        
        # 모든 작업 목록 조회
        print("\n3. 모든 작업 목록 조회...")
        all_tasks = await processor.get_all_tasks()
        print(f"   총 작업 수: {len(all_tasks)}")
        for task in all_tasks:
            print(f"   - {task['task_id']}: {task['status']} ({task['filename']})")
        
        # 작업 상태 조회
        print("\n4. 작업 상태 조회...")
        task_status = await processor.get_task_status(task_id_1)
        if task_status:
            print(f"   작업 {task_id_1} 상태: {task_status['status']}")
            print(f"   진행률: {task_status['progress']}%")
        
        # 잠시 대기 (백그라운드 처리 시뮬레이션)
        print("\n5. 백그라운드 처리 대기 중...")
        await asyncio.sleep(3)
        
        # 업데이트된 상태 조회
        print("\n6. 업데이트된 작업 상태 조회...")
        updated_status = await processor.get_task_status(task_id_1)
        if updated_status:
            print(f"   작업 {task_id_1} 상태: {updated_status['status']}")
            print(f"   진행률: {updated_status['progress']}%")
        
        # 작업 취소 테스트
        print("\n7. 작업 취소 테스트...")
        cancelled = await processor.cancel_task(task_id_2)
        print(f"   작업 {task_id_2} 취소 결과: {cancelled}")
        
        # 최종 상태 확인
        print("\n8. 최종 작업 상태...")
        final_tasks = await processor.get_all_tasks()
        for task in final_tasks:
            print(f"   - {task['task_id']}: {task['status']} ({task['filename']})")
        
        # 오래된 작업 정리
        print("\n9. 오래된 작업 정리...")
        await processor.cleanup_completed_tasks(max_age_hours=0)  # 즉시 정리
        
        print("\n✅ 백그라운드 프로세서 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 프로세서 정리
        print("\n프로세서 정리 중...")
        await processor.stop()
        print("프로세서가 정리되었습니다.")

async def test_concurrent_tasks():
    """동시 작업 처리 테스트"""
    
    results_dir = Path("analyze/result")
    processor = BackgroundProcessor(results_dir, max_workers=3)
    
    try:
        await processor.start()
        
        # 여러 작업을 동시에 제출
        print("\n동시 작업 처리 테스트...")
        tasks = []
        
        for i in range(5):
            task_id = await processor.submit_image_analysis_task(
                file_content=f"dummy content {i}".encode(),
                filename=f"test_image_{i}.png",
                prompt=f"이미지 {i} 분석"
            )
            tasks.append(task_id)
            print(f"   작업 {i+1} 제출: {task_id}")
        
        # 잠시 대기
        print("   백그라운드 처리 대기 중...")
        await asyncio.sleep(5)
        
        # 결과 확인
        all_tasks = await processor.get_all_tasks()
        print(f"   총 작업 수: {len(all_tasks)}")
        
        for task in all_tasks:
            print(f"   - {task['task_id']}: {task['status']} (진행률: {task['progress']}%)")
        
    except Exception as e:
        print(f"동시 작업 테스트 오류: {str(e)}")
    
    finally:
        await processor.stop()

if __name__ == "__main__":
    print("🚀 백그라운드 프로세서 테스트 시작")
    
    # 기본 기능 테스트
    asyncio.run(test_background_processor())
    
    print("\n" + "="*50 + "\n")
    
    # 동시 작업 테스트
    asyncio.run(test_concurrent_tasks())
    
    print("\n🎉 모든 테스트 완료!")
