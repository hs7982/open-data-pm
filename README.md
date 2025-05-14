# 미세먼지 공공데이터 활용 프로젝트

## 프로젝트 소개
공공데이터 포털의 미세먼지 데이터를 수집하고 시각화하여 제공하는 웹 서비스입니다.

## 기술 스택

### Backend
- FastAPI (Python)
- PostgreSQL
- APScheduler (데이터 수집 스케줄링)
- SQLAlchemy (ORM)

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Naver Maps API

## 프로젝트 구조

```
├── backend/
│   ├── api/           # API 라우터
│   ├── core/          # 핵심 설정 (데이터베이스 등)
│   ├── domain/        # 도메인 모델
│   ├── service/       # 비즈니스 로직
│   ├── sql/          # SQL 쿼리
│   ├── utils/        # 유틸리티 함수
│   └── main.py       # 애플리케이션 진입점
│
├── frontend/
│   ├── public/       # 정적 파일
│   └── src/         # 리액트 소스 코드
```

## 주요 기능
- 공공데이터 실시간 미세먼지 데이터 수집(주기적 갱신)
- 측정소별 미세먼지 현황 조회
- 지도 기반 시각화


## API 문서
- Swagger UI: http://localhost:8000/docs

## API 명세

### 미세먼지 데이터 API

#### 1. 주변 대기오염 데이터 조회
```
GET /api/data

Query Parameters:
- latitude: float (필수) - 위도
- longitude: float (필수) - 경도
- radius: int (선택, 기본값: 10000) - 검색 반경(미터)

Response:
- 지정된 위치 주변의 대기오염 측정소 데이터
```

### 데이터 갱신 API

#### 1. 대기오염 데이터 갱신
```
GET /api/refresh/data

Description: OPEN API에서 최신 대기오염 측정 데이터를 즉시 가져와 반영

Response:
- 데이터 갱신 처리 결과
```

#### 2. 측정소 정보 갱신
```
GET /api/refresh/station

Description: OPEN API에서 측정소 정보를 즉시 가져와 반영

Response:
- 측정소 정보 갱신 처리 결과
```
