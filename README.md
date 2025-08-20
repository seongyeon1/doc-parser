# 🚀 Document Parser

프론트엔드와 백엔드를 분리한 현대적인 문서 파싱 애플리케이션입니다.

## 🏗️ 프로젝트 구조

```
doc-parser/
├── backend/                 # 백엔드 API 서버
│   ├── main.py             # FastAPI 메인 애플리케이션
│   ├── background_processor.py  # 백그라운드 작업 처리
│   ├── file_processor.py   # 파일 처리 로직
│   ├── table_extractor.py  # 테이블 추출 로직
│   ├── requirements.txt    # Python 의존성
│   └── Dockerfile         # 백엔드 Docker 이미지
├── frontend/               # 프론트엔드 애플리케이션
│   ├── package.json       # Node.js 의존성
│   ├── Dockerfile         # 프론트엔드 Docker 이미지
│   └── analyze/           # 기존 분석 도구
├── docker-compose.yml      # 전체 시스템 Docker 설정
├── run.sh                  # 실행 스크립트
├── .env.example           # 환경 변수 예시
└── README.md              # 프로젝트 문서
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 환경 변수 파일 생성
cp .env.example .env

# .env 파일 편집하여 OpenAI API 키 설정
# OPENAI_API_KEY=your_actual_api_key_here
```

### 2. Docker로 실행
```bash
# 전체 시스템 실행
./run.sh

# 또는 수동으로 실행
docker-compose up -d
```

### 3. 서비스 접속
- **백엔드 API**: http://localhost:8000
- **프론트엔드**: http://localhost:3000
- **API 문서**: http://localhost:8000/docs

## 🎯 주요 기능

### 백엔드 (FastAPI)
- 📄 PDF 문서 처리
- 🖼️ 이미지 분석
- 📊 테이블 추출
- 🔄 백그라운드 작업 처리
- 🗄️ Redis 기반 작업 큐

### 프론트엔드 (React)
- 🎨 현대적인 UI/UX
- 📱 반응형 디자인
- 🔍 실시간 결과 시각화
- 📊 차트 및 그래프

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **OpenAI API**: GPT 모델을 활용한 문서 분석
- **Redis**: 작업 큐 및 캐싱
- **Celery**: 백그라운드 작업 처리
- **SQLAlchemy**: 데이터베이스 ORM

### 프론트엔드
- **React**: 사용자 인터페이스
- **Vite**: 빠른 개발 서버 및 빌드 도구
- **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크
- **Axios**: HTTP 클라이언트

### 인프라
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 서비스 오케스트레이션
- **Nginx**: 웹 서버 및 리버스 프록시

## 🔧 개발 환경

### 백엔드 개발
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 프론트엔드 개발
```bash
cd frontend
npm install
npm run dev
```

## 📋 API 엔드포인트

### 문서 처리
- `POST /upload-image`: 이미지 업로드
- `POST /upload-pdf`: PDF 업로드
- `POST /extract-tables`: 테이블 추출

### 백그라운드 작업
- `POST /background/extract-tables`: 백그라운드 테이블 추출
- `GET /background/task-status/{task_id}`: 작업 상태 확인

### 헬스체크
- `GET /health`: 서버 상태 확인

## 🐳 Docker 명령어

```bash
# 전체 시스템 시작
docker-compose up -d

# 특정 서비스만 시작
docker-compose up -d backend
docker-compose up -d frontend

# 로그 확인
docker-compose logs -f backend
docker-compose logs -f frontend

# 서비스 중지
docker-compose down

# 이미지 재빌드
docker-compose build --no-cache
```

## 🔒 보안

- `.env` 파일은 `.gitignore`에 포함되어 Git에 업로드되지 않습니다
- `env.example` 파일을 참고하여 환경 변수를 설정하세요
- OpenAI API 키는 안전하게 관리해야 합니다

## 📝 라이선스

MIT License

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
