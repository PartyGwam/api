# 파티원괌 REST API

Base URL Endpoint : `http://<DOMAIN>/api`

## Authorization & Headers

- Token prefix 는 PG (파티원괌)
- 기본 `Content-Type` 는 `application/json`
- 인증이 필요한 API 의 경우는 `Authorization` 을 추가.

```json
{
  "Content-Type": "application/json",
  "Authorization": "PG <TOKEN>"
}
```

## User API

기능 : 로그인 및 회원가입, 유저 정보 조회 (프로필이랑 다름)

### POST `/users/login`

로그인 기능  
클라이언트에 요구하는 정보 : 이메일, 비밀번호
토큰 인증 사용!

#### Request Format

```json
{
  "email": "sample@gmail.com",
  "password": "sample_password"
}
```

#### Response Format - Success

```json
{
  "success": true,
  "data": {
    "username": "username",
    "email": "sample@gmail.com",
    "token": "asjf9sfjsafjsakfjasf"
  }
}
```

#### Response Format - Failure

```json
{
  "success": false,
  "errors": {
    "non_field_errors": ["이메일 혹은 비밀번호가 잘못되었습니다."]
  }
}
```

### POST `/users`

회원가입 기능  
클라이언트에 요구하는 정보 : 이메일, 닉네임, 비밀번호

#### Request Format

```json
{
  "email": "sample@gmail.com",
  "username": "sample",
  "password": "sample_password"
}
```

#### Response Format - Success

```json
{
  "success": true,
  "data": {
    "username": "username",
    "email": "sample@gmail.com",
    "token": "asjf9sfjsafjsakfjasf"
  }
}
```

#### Response Format - Failure

```json
{
  "success": false,
  "errors": {
    "email": ["유효한 이메일 주소를 입력하십시오."]
  }
}
```

### GET `/users` (인증 필요)

전체 유저 조회, 쿼리 가능.

Query String Parameters:

- `?email=sample@gmail.com` : 이메일 매칭
- `?username=sample` : 닉네임 매칭

#### Response Format - Success

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "1b35ef43-8084-499b-94a6-597fca9b70f9",
      "is_active": "활성",
      "is_admin": "관리자",
      "last_login": "2018-06-22T15:18:58.579853+09:00",
      "email": "bisschoi9541@gmail.com",
      "username": "최병규"
    },
    {
      "uuid": "80d970d1-23f3-4884-8cbc-bd7d4cbe924e",
      "is_active": "활성",
      "is_admin": "관리자 아님",
      "last_login": null,
      "email": "sample4@gmail.com",
      "username": "샘플 유저4"
    }
  ]
}
```

### GET `/users/<uuid>`

특정 유저 1 명 조회

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

### POST `/profiles`

프로필 생성

### PUT `/profiles`

프로필 수정

### DELETE `/profiles`

프로필 삭제

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

### GET `/parties/<slug>/members`

파티 1 개에 참여한 전체 멤버 조회

### GET `/parties/<slug>/members/<slug>`

파티 1 개에 참여한 멤버 중 1 명 조회

### GET `/parties/<slug>/members/owner`

파티의 파티장 조희

### PUT `/parties/<slug>/members/owner`

파티의 파티장 위임

### POST `/parties/<slug>/members`

파티에 참여

### DELETE `/parties/<slug>/members`

파티에 참여 취소

## 댓글 API

### GET `/parties/<slug>/comments`

파티 1 개의 댓글 전체 조희

### GET `/parties/<slug>/comments/<slug>`

파티 1 개의 댓글 1 개 조희

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

알림 수정

### DELETE `/notifications`

알림 삭제

## 문의 API

### POST `/complain`

문의 등록
