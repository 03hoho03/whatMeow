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

테스트 데이터로 유저 10만명, 팔로우 관계 300만개, 게시글 수 10만개를 준비했습니다. <br>
단순히 게시글을 작성하고 조회하는 로직에 있어서 비교를 보기 위해 <br>
고양이 해시태그, 이미지 AWS 업로드 등의 기능은 제외하고 테스트했습니다. <br>
테스트 데이터에서 팔로워가 가장 많은 유저의 팔로워는 57명, 팔로잉이 가장 많은 유저는 59명으로 통계되었습니다. <br>

- FanOut on Write 로직 적용 전 <br>
  게시글 작성 33ms <br>
  ![image](https://github.com/user-attachments/assets/8d7327bd-2a25-46ba-aa12-9896d70b0ff2)

  게시글 조회 144ms <br>
  ![image](https://github.com/user-attachments/assets/2b5ccbcf-c543-4745-b70f-6060a99a29c5)

  
- 로직 적용 후 <br>
  게시글 작성 109ms <br>
  ![image](https://github.com/user-attachments/assets/333557ce-ee49-4bf4-88cd-260d868411ac)


  게시글 조회 65ms <br>
  ![image](https://github.com/user-attachments/assets/6c99658b-d01c-4559-9f7c-f18c9997dd36)


게시글 작성에 있어서 성능의 손실을 봤지만, 조회에서 약 54%의 속도 향상을 이루어냈습니다. <br>
생성보다 조회의 경우가 압도적으로 많은 커뮤니티 서비스의 특성을 고려하여 <br>
Fanout on Write 로직을 적용하는 것이 유리하다는 판단을 내렸습니다. <br>


#### 2. 낙관적 락을 활용한 좋아요

~~ 락에 대한 설명 및 구현 방법 ~~

#### 3. 메모리 확보를 위한 모델 경량화

~~ 당시 상황 설명 및 모델 경량화를 통해 실버 불렛은 없다는 점 작성 ~~
