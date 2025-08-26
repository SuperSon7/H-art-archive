# H-Art Archive Frontend

한국 현대미술 아카이브 플랫폼의 프론트엔드 애플리케이션입니다.

## 🚀 기술 스택

- **프레임워크**: Next.js 14+ (App Router)
- **언어**: TypeScript 5.0+
- **스타일링**: Tailwind CSS 3.3+
- **상태 관리**: Zustand
- **폼 관리**: React Hook Form + Zod
- **HTTP 클라이언트**: TanStack Query + Axios
- **UI 컴포넌트**: shadcn/ui
- **이미지 최적화**: Next.js Image 컴포넌트

## 📁 프로젝트 구조

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 루트 레이아웃
│   ├── page.tsx           # 메인 페이지
│   └── globals.css        # 전역 스타일
├── components/             # 재사용 가능한 컴포넌트
│   ├── ui/                # 기본 UI 컴포넌트
│   └── sections/          # 페이지 섹션 컴포넌트
├── lib/                   # 유틸리티 및 설정
│   ├── api.ts             # API 클라이언트
│   └── utils.ts           # 유틸리티 함수
├── store/                 # Zustand 상태 관리
│   ├── auth.ts            # 인증 상태
│   └── artwork.ts         # 작품 상태
└── types/                 # TypeScript 타입 정의
    └── index.ts           # 공통 타입
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
npm install
# 또는
yarn install
# 또는
pnpm install
```

### 2. 환경 변수 설정

`.env.local` 파일을 생성하고 필요한 환경 변수를 설정하세요:

```bash
cp env.example .env.local
```

### 3. 개발 서버 실행

```bash
npm run dev
# 또는
yarn dev
# 또는
pnpm dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 🔧 사용 가능한 스크립트

- `npm run dev` - 개발 서버 실행
- `npm run build` - 프로덕션 빌드
- `npm run start` - 프로덕션 서버 실행
- `npm run lint` - ESLint 실행
- `npm run type-check` - TypeScript 타입 검사

## 🌐 API 연동

백엔드 API와의 연동을 위해 `src/lib/api.ts`에 정의된 API 클라이언트를 사용합니다.

### 주요 API 모듈

- **authAPI**: 인증 관련 (로그인, 회원가입, 프로필)
- **artistAPI**: 작가 관련 (작가 목록, 프로필, 팔로우)
- **artworkAPI**: 작품 관련 (작품 목록, 상세, 업로드)
- **wishlistAPI**: 위시리스트 관련
- **purchaseInquiryAPI**: 구매 문의 관련

## 🎨 디자인 시스템

### 색상 팔레트

- **Primary**: 오렌지 계열 (#ed7516)
- **Secondary**: 그레이 계열 (#64748b)
- **Accent**: 퍼플 계열 (#d946ef)

### 컴포넌트

- **Button**: 다양한 변형과 크기를 지원하는 버튼 컴포넌트
- **LoadingSpinner**: 로딩 상태를 표시하는 스피너
- **Card**: 일관된 카드 레이아웃

## 📱 반응형 디자인

모바일, 태블릿, 데스크톱을 모두 지원하는 반응형 디자인을 적용했습니다.

## 🌍 다국어 지원

한국어와 영어를 기본으로 지원하며, `next-intl`을 사용하여 국제화를 구현했습니다.

## 🔐 인증 시스템

- JWT 기반 인증
- 소셜 로그인 (Google)
- 자동 토큰 갱신
- 보호된 라우트

## 📸 이미지 처리

- Next.js Image 컴포넌트를 사용한 최적화
- WebP, AVIF 포맷 지원
- 반응형 이미지 크기 조정

## 🚀 배포

### Vercel 배포 (권장)

```bash
npm run build
vercel --prod
```

### Docker 배포

```bash
docker build -t h-art-frontend .
docker run -p 3000:3000 h-art-frontend
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
