# 고양이 커뮤니티 서비스

고양이 커뮤니티 서비스 왓뮤의 백엔드/프론트엔드 깃허브입니다.

## 📚 Table of Contents

- [고양이 커뮤니티 서비스](#고양이-커뮤니티-서비스)
  - [📚 Table of Contents](#-table-of-contents)
    - [프로젝트 소개](#프로젝트-소개)
    - [주요 기능](#주요-기능)
    - [데이터 모델 (ERD)](#데이터-모델-erd)
  - [🖥 BE](#-be)
    - [기술스택](#기술스택)
    - [기술적 의사결정](#기술적-의사결정)
      - [1. FanOut on Write 로직으로 팔로우 게시글 조회](#1-fanout-on-write-로직으로-팔로우-게시글-조회)
      - [2. 메모리 확보를 위한 모델 경량화](#2-메모리-확보를-위한-모델-경량화)
  - [🏗️ FE](#️-fe)
    - [Architecture](#architecture)
    - [Directory Structure](#directory-structure)
    - [Technology Stack](#technology-stack)
    - [Setup \& Installation](#setup--installation)
    - [Scripts](#scripts)

---

### 프로젝트 소개

`whatMeow` 프로젝트는 고양이를 사랑하는 사람들을 위한 소셜 미디어 서비스입니다. 사용자는 자신의 고양이 사진을 공유하고 다른 사용자들과 소통할 수 있습니다. React Query를 활용한 효율적인 데이터 관리와 MSW를 통한 API 모킹으로 안정적인 개발 환경을 구축했습니다.

### 주요 기능

- **AI 고양이 품종 분석**: 사용자가 올린 고양이 사진을 AI로 분석하여 품종을 알려줍니다.
- **소셜 피드 (Feed)**: 다른 사용자들의 게시물을 무한 스크롤로 탐색하고, 팔로우/팔로잉하는 유저의 게시글을 따로 조회할 수 있습니다.
- **게시물 및 댓글**: 해시태그를 포함하여 게시물을 작성하고, 댓글로 소통합니다.
- **좋아요 (Like)**: 마음에 드는 게시물에 '좋아요'를 누를 수 있습니다.
- **유저 및 고양이 프로필**: 사용자와 고양이의 프로필을 생성하고 관련 게시물을 모아볼 수 있습니다.
- **인증 (Authentication)**: 소셜 로그인(Google, Kakao)을 포함한 안전한 인증 시스템을 제공합니다.

### 데이터 모델 (ERD)

프론트엔드 서비스 로직을 기반으로 추론한 데이터 모델 관계입니다.

```
User ──< Post ──< Comment
 │      │
 │      └──< Like
 │
 └──< Cat
```

- **User**: 사용자 정보. 여러 개의 `Post`와 `Cat`을 가질 수 있습니다.
- **Post**: 사용자가 작성한 게시물. 여러 개의 `Comment`와 `Like`를 포함합니다.
- **Comment**: 게시물에 대한 댓글.
- **Like**: 게시물에 대한 '좋아요'.
- **Cat**: 사용자가 등록한 고양이 정보.

---

## 🖥 BE

### 기술스택

<div align=left> 
  <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/awsLightsail-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/redis-FF4438?style=for-the-badge&logo=redis&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" width=100 height=50/>
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" width=100 height=50/>
</div>

---

### 기술적 의사결정

#### 1. FanOut on Write 로직으로 팔로우 게시글 조회

테스트 데이터로 유저 10만명, 팔로우 관계 300만개, 게시글 수 10만개를 준비했습니다. <br>
단순히 게시글을 작성하고 조회하는 로직에 있어서 비교를 보기 위해 <br>
고양이 해시태그, 이미지 AWS 업로드 등의 기능은 제외하고 테스트했습니다. <br>
테스트 데이터에서 팔로워가 가장 많은 유저의 팔로워는 57명, 팔로잉이 가장 많은 유저는 59명으로 통계되었습니다. <br>

게시글 조회는 팔로잉 중인 유저들의 최근 게시물 5개를 가져오는 작업입니다. <br>

Loucst를 활용해 100명의 유저가 <br>
조회는 1-2초 사이에 요청, 작성은 8-10초 사이에 요청을 보내도록 세팅해두고 진행했습니다. <br>

- FanOut on Write 로직 적용 전 <br>
  게시글 작성 2100ms <br>
  ![미적용작성2100ms](https://github.com/user-attachments/assets/4ca70504-bb11-4e64-b8fa-8e49561a129b)

  게시글 조회 2200ms <br>
  ![미적용조회2200ms](https://github.com/user-attachments/assets/97a3c22c-fbe6-4080-991d-b0219df6ff92)

- 로직 적용 후 <br>
  게시글 작성 2900ms <br>
  ![fanout적용작성2900ms](https://github.com/user-attachments/assets/329478b5-7af1-4f5a-837e-1370f0289615)

  게시글 조회 1430ms <br>
  ![fanout적용조회1430ms](https://github.com/user-attachments/assets/51e70a96-835b-455a-8c67-00c0b69dffc2)

게시글 작성에 있어서 약 38%의 성능 손실을 봤지만, 게시물 조회에서 약 35%의 속도 향상을 이루어냈습니다. <br>
생성보다 조회의 경우가 압도적으로 많은 커뮤니티 서비스의 특성을 고려하여 <br>
Fanout on Write 로직을 적용하는 것이 유리하다는 판단을 내렸습니다. <br>

#### 2. 메모리 확보를 위한 모델 경량화

AWS Lightsail 프리티어를 사용하게 되면 1GB의 RAM을 사용할 수 있습니다. <br>
Resnet 모델을 서버에서 구동하기 전에는 <br>
Linux + MySQL + FastAPI + NginX가 모두 하나의 인스턴스에서 실행되고 있어 메모리 여유가 없었습니다. <br>
Resnet101 모델에 학습을 완료한 뒤 서버에 이식하자 API 접근 시에 메모리 이슈로 인한 서버 다운이 일어났습니다. <br><br>

우선 MySQL을 AWS상에서 구동해 약 300MB의 메모리를 확보할 수 있었고, Resnet 모델 경량화를 통해 <br>
서버의 가용 메모리를 늘려보고자 했습니다. <br>
Resnet 모델을 경량화 했을 때 모델의 정확도가 크게 떨어지는 것을 우려했으나<br>
비교 결과 정확도 차이가 5% 정도로 크게 없어 Resnet18 모델을 사용하는 것으로 결정했습니다.

---

## 🏗️ FE

> Next.js와 TypeScript 기반의 고양이 사진 공유 소셜 미디어 플랫폼

### Architecture

이 프로젝트는 Next.js 13의 App Router를 기반으로 설계되었습니다. 서버 컴포넌트와 클라이언트 컴포넌트를 적절히 활용하여 렌더링을 최적화하고, API 통신은 `axios`와 `@tanstack/react-query`를 통해 관리합니다. 전역 상태는 `Recoil`을 사용하여 필요한 최소한의 상태(예: 로그인 모달)를 제어합니다.

- **UI Layer**: Next.js (App Router), React, CSS Modules
- **Data Fetching & State**: TanStack Query (React Query), Recoil
- **API Mocking**: MSW (Mock Service Worker)
- **Entry Point**: `app/layout.tsx` -> `app/(main)/page.tsx`

### Directory Structure

프론트엔드 프로젝트의 주요 디렉토리 구조는 다음과 같습니다.

```
frontend/
├── app/
│   ├── (route)/              # 페이지 라우팅 그룹
│   │   ├── (auth)/           # 인증 관련(로그인, 회원가입) 페이지
│   │   └── (main)/           # 메인 서비스 페이지 (피드, 프로필 등)
│   ├── _common/              # 아이콘, 모달 등 범용적인 UI 컴포넌트
│   ├── _components/          # 네비게이션 바, 캐러셀 등 복합 컴포넌트
│   ├── _hooks/               # 커스텀 React Hooks (e.g., useBodyScrollLock)
│   ├── _services/            # API 통신 및 데이터 관리 (React Query hooks)
│   │   ├── mutations/        # CUD 작업을 위한 React Query Mutations
│   │   └── quries/           # READ 작업을 위한 React Query Queries
│   ├── _store/               # Recoil을 사용한 전역 상태 관리
│   ├── _utils/               # 유틸리티 함수 및 전역 프로바이더
│   └── _mocks/               # MSW를 위한 API 핸들러 및 설정
├── public/                   # 정적 에셋 (이미지, 아이콘)
└── ...
```

### Technology Stack

- **Framework**: Next.js 13.4.19
- **Language**: TypeScript
- **Data Fetching & Caching**: `@tanstack/react-query`
  - 서버 상태를 효율적으로 관리하고, 캐싱, 재시도, 데이터 동기화 등을 자동화하여 UX를 개선합니다.
- **State Management**: `Recoil`
  - 로그인 모달 상태 등 최소한의 클라이언트 상태를 원자(atom) 단위로 관리합니다.
- **HTTP Client**: `axios`
  - Promise 기반의 API 클라이언트로, 비동기 통신을 간결하게 처리합니다.
- **API Mocking**: `msw` (Mock Service Worker)
  - 개발 단계에서 백엔드 API를 모킹하여 프론트엔드와 백엔드의 독립적인 개발을 지원합니다.
- **Styling**: CSS Modules, `classnames`
- **Linting & Formatting**: ESLint, Prettier

### Setup & Installation

```bash
# 1. 프로젝트 클론 및 디렉토리 이동
git clone https://your-repository-url.git
cd whatMeow/frontend

# 2. 의존성 설치
npm install

# 3. 개발 서버 실행
npm run dev
```

### Scripts

- `npm run dev`: 개발 모드로 Next.js 서버를 실행합니다. (MSW 활성화)
- `npm run build`: 프로덕션용으로 애플리케이션을 빌드합니다.
- `npm run start`: 빌드된 프로덕션 서버를 시작합니다.
- `npm run lint`: ESLint를 사용하여 코드 스타일을 검사합니다.
