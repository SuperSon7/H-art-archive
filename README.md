# 온라인 아트 플랫폼 🎨

첫발을 내딧는 아티스트와 컬렉터를 연결하는 온라인 아트 마켓플레이스 플랫폼입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [API 설계](#api-설계)
- [설치 및 실행](#설치-및-실행)
- [환경 설정](#환경-설정)
- [사용법](#사용법)
- [API 문서](#api-문서)
- [라이센스](#라이센스)

## 🎯 프로젝트 개요

졸업하는 아티스트들을 위한, 졸업 작품 아카이빙, 커넥팅 플랫폼

## ✨ MVP 주요 기능

### 👨‍🎨 아티스트 기능
- **회원가입 및 로그인** : 이메일 인증, 구글 소셜 로그인 포함
- **사용자 유형** : 선택(아티스트/컬렉타)
- **핵심 프로필 생성/수정** : 작가명, 작가노트, 대표 이미지 등 작가를 알리기 위한 최소한의 정보
- **작품 관리** : 고화질 이미지 지원, 제목, 설명, 가격, 재료, 크기, 해시태그, 저작권 및 라이선스 동의

### 🎨 컬렉터 기능
- **회원가입 및 로그인** : 이메일 인증, 구글 소셜 로그인 포함, 닉네임 및 프로필 설정
- **작가 팔로우** : 커뮤니티의 시작. 관심 작가의 팬이 되는 기능
- **위시리스트**: 구매를 고려하는 작품을 저장. 우리의 핵심적인 잠재 구매 데이터

### 🤖 AI 기능(도입 고려 중)
- **자동 태깅**: 이미지 분석을 통한 자동 해시태그 생성
- **스타일 분석**: 작품의 스타일과 기법 자동 분석
- **가격 제안**: 시장 데이터 기반 적정 가격 제안
- **품질 검사**: 업로드 이미지 품질 자동 검증

### 🔍 검색 및 발견
- **통합 검색**: 아티스트, 작품, 태그 통합 검색
- **고급 필터**: 다양한 조건을 통한 세밀한 검색
- **트렌딩 태그**: 인기 급상승 태그 및 작품 추천

### 👨‍🎨 관리자
- **품질 관리**: 작가 가입 승인, 작품 업로드 승인
- **큐레이션** : 메인 페이지에 노출할 '큐레이터 추천'


## 🛠 기술 스택

### Backend
- **Framework**: Django 4.2+ 
- **Database**: PostgreSQL
- **Cache**: Redis
- **File Storage**: AWS S3 / CloudFront (미정)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Django REST Framework + Swagger

### AI/ML(미정)
- **Computer Vision**: OpenCV, TensorFlow/PyTorch
- **Image Processing**: Pillow, scikit-image
- **Recommendation Engine**: Collaborative Filtering + Content-based

### Infrastructure
- **Deployment**: Docker + Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### Frontend
- **Web**: React.js + TypeScript


## 📡 API 설계

### 앱 구조
MVP 는 Django의 앱 기반 아키텍처로 구성되어 있습니다:

1. **accounts**: 사용자 인증 및 프로필 관리
2. **artists**: 아티스트 프로필 및 승인 관리
3. **artworks**: 작품 등록, 조회, 관리
4. **interactions**: 팔로우, 위시리스트, 구매 문의, 알림
5. **tags**: 해시태그 및 검색 기능
6. **ai_integration**: AI 기반 기능들

### API 엔드포인트 예시

```
POST /v1/accounts/register/          # 회원가입
POST /v1/accounts/login/             # 로그인
GET  /v1/artists/                    # 아티스트 목록
POST /v1/artworks/                   # 작품 업로드
GET  /v1/artworks/{id}/              # 작품 상세보기
POST /v1/interactions/follow/        # 아티스트 팔로우
GET  /v1/tags/search/                # 통합 검색
POST /v1/ai/auto-tag/                # AI 자동 태깅
```


### 개발 가이드라인

- **코드 스타일**: PEP 8 준수
- **테스트**: 새로운 기능에 대한 테스트 코드 작성
- **문서화**: API 변경사항에 대한 문서 업데이트
- **커밋 메시지**: Conventional Commits 형식 사용

---

**Made by the __ Team**
```