# 고양이 커뮤니티 서비스

고양이 커뮤니티 서비스 왓뮤의 백엔드/프론트엔드 깃허브입니다.

---

### 프로젝트 소개

고양이를 사랑하고 아끼는 사람들을 위한 **고양이 전문 커뮤니티 서비스**입니다! <br>
내 고양이를 등록하고 자랑해보세요! <br>
귀여운 고양이 사진들을 구경해보세요! <br>

### 제공기능

- 해시태그 포함 게시글 및 댓글 작성
- 좋아요
- 팔로우 및 팔로잉 게시글 조회
- 내 고양이 등록 및 관련 게시물 조회
- 고양이 품종 판별 AI
- 유저 프로필

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

~~ 기존 팔로우 로직 이용 시 데이터 조회 속도 vs FanOut on Write 로직으로 데이터 조회 속도 비교 ~~
~~ FanOut on Write 로직 그림 삽입 ~~


#### 2. 낙관적 락을 활용한 좋아요

~~ 락에 대한 설명 및 구현 방법 ~~

#### 3. 메모리 확보를 위한 모델 경량화

~~ 당시 상황 설명 및 모델 경량화를 통해 실버 불렛은 없다는 점 작성 ~~
