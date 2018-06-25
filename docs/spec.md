## User API

기능 : 로그인 및 회원가입, 유저 정보 조회 (프로필이랑 다름)

### POST `/users/login`

로그인

### POST `/users`

회원가입

### GET `/users` (인증 필요)

유저 전체 조희

### GET `/users/<uuid>`

특정 유저 조회

### POST `/users/forgot`

비밀번호 찾기

### PUT `/users`

비밀번호 변경

### DELETE `/users`

유저 비활성화

## 프로필 API

### GET `/profiles`

전체 프로필 조회

### GET `/profiles/<uuid>`

특정 프로필 1 개 조희

### PUT `/profiles`

프로필 수정

### POST `/profiles/<uuid>/notification`

알림 켜기

### DELETE `/profiles/<uuid>/notification`

알림 끄기

## 파티 API

### GET `/parties` (인증 필요)

전체 파티 조희

### GET `/parties/<slug>` (인증 필요)

특정 파티 1 개 조희

### POST `/parties` (인증 필요)

파티 생성

### PUT `/parties` (인증 필요)

파티 정보 수정

### DELETE `/parties` (인증 필요)

파티 삭제

### GET `/parties/<slug>/participants`

파티 1 개에 참여한 전체 멤버 조회

### GET `/parties/<slug>/participants/owner`

파티의 파티장 조희

### PUT `/parties/<slug>/participants/owner`

파티의 파티장 위임

### POST `/parties/<slug>/participants`

파티에 참여

### DELETE `/parties/<slug>/participants`

파티에 참여 취소

## 댓글 API

### GET `/parties/<slug>/comments`

파티 1 개의 댓글 전체 조희

### POST `/parties/<slug>/comments`

파티 1 개에 종속된 댓글 작성

### PUT `/parties/<slug>/comments`

파티 1 개에 종속된 댓글 수정

### DELETE `/parties/<slug>/comments`

파티 1 개에 종속된 댓글 삭제

## 알림 API

### GET `/notifications`

전체 알림 조희

### GET `/notifications/<slug>`

알림 1 개 상세 조희

### POST `/notifications`

알림 생성

### PUT `/notifications`

알림 읽기

### DELETE `/notifications`

알림 삭제

## 문의 API

### POST `/complain`

문의 등록
