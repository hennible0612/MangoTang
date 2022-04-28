# MangoTang
## 소개
* 프로젝트 주제 : 쇼핑몰
* 쇼핑몰 url : (수정중) https://blog.naver.com/ghdtjddn0612/222647397155
* 팀원 : 혼자

## 사용 기술
* 프론트엔드 : HTML, CSS, JS, jQuery
* 백엔드 : django 3.2.12
* 데이터베이스 : SQLite3
* 배포 : amazon lightsail, ubuntu 20.04 LTS, nginx, gunicorn
## BPMN (자세한 내용은 drawio 폴더 확인)
draw.io를 사용하여 사용자, 클라이언트백엔드, 관리자 입장의 흐름도를 표현
<img width="758" alt="bpmn" src="https://user-images.githubusercontent.com/48763809/165433920-d1691d86-2305-490f-aa84-937be6c47f71.png">


## 데이터 베이스
<img width="398" alt="db" src="https://user-images.githubusercontent.com/48763809/165434119-643cb1c2-5729-4d7d-bf9f-73ff0e03153a.png">


## 장고 앱별 기능
## store 앱 
메인 화면으로 상품표시, 상품상세정보 표시, 카트, 회원가입등 쇼핑몰의 기본 기능등을 담당한다.
#### 대표 기능
* 로그인
  1. 장고 기본 로그인 사용
  2. django-allauth 사용하여 네이버, 카카오, 구글 로그인 구현
* 상품상세 페이지
  1. 제품 클릭시 해당 제품의 고유 번호에 따라 해당 제품 출력
  2. 후기 / 문의 같은 경우 리뷰가 5가지 넘어갈시 페이징 구현, 다음페이지 넘길시 jquery로 다음 페이지 요청
* 카트
  1. 상품상세 페이지에서 카트에 추가한 제품들 출력
  2. 상품 삭제, 추가 jquery로 url 요청

## iamport 앱
#### 결제 / 환불 기능을 담당 iamport api를 사용
#### 대표 기능
* 결제
  1. 주소입력 부분은 다음 우편번호 api 사용
  2. 필수 정보 입력시 iamport 서버에 요청
  3. view에서 토큰을 받아 위조인지 아닌지 확인 후 결제 완료
* 환불 
  1. 고객이 여러가지 상품을 한번에 구매시 부분 환불 가능
  2. 부분환불 금액 만큼 iamport 서버에 요청


## mypage 앱
#### 고객 정보페이지, 환불/교환신청, 리뷰쓰기, 문의사항, 개인정보 수정이 가능
#### 대표기능
* 주문 / 배송내역
  1. 배송조회 sweettracker api 사용, 제품 상태에 따라서 조회 가능 하거나 불가능
  2. 교환 / 반품 신청, 배송 상태에 따러서 즉시 환불되거나 관리자에게 메시지 전송
  3. 리뷰쓰기 해당 제품의 리뷰 등록
* 사용자 정보
  1. 시용자의 정보 확인가능

 ## 배포 
 아마존 라이트세일 서버를 사용
 Nginx로 정적파일 처리, 그리고 프록시 서버로
 동적파일은 Gunicorn, wsgi를 사용




