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
