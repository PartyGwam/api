# User API

기능 : 로그인 및 회원가입, 유저 정보 조회 (프로필이랑 다름)

## 문서 목차

1.  [POST `/users/login`]()
2.  [POST `/users`]()
3.  [GET `/users`]()
4.  [GET `/users/<uuid>`]()
5.  [POST `/users/forgot`]()
6.  [PUT `/users`]()
7.  [DELETE `/users`]()

## POST `/users/login`

로그인 기능  
클라이언트에 요구하는 정보 : 이메일, 비밀번호
토큰 인증 사용!

## Request Format

```json
{
    "email": "sample@gmail.com",
    "password": "sample_password"
}
```

## Response Format - Success

성공 시 다음의 데이터와 함께 200 응답을 리턴.

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

## Response Format - Failure

실패 시 에러 메시지와 함께 400 응답을 리턴

```json
{
    "success": false,
    "errors": {
        "non_field_errors": ["이메일 혹은 비밀번호가 잘못되었습니다."]
    }
}
```

## POST `/users`

회원가입 기능  
클라이언트에 요구하는 정보 : 이메일, 닉네임, 비밀번호

## Request Format

```json
{
    "email": "sample@gmail.com",
    "username": "sample",
    "password": "sample_password"
}
```

## Response Format - Success

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

## Response Format - Failure

```json
{
    "success": false,
    "errors": {
        "email": ["유효한 이메일 주소를 입력하십시오."]
    }
}
```

## GET `/users` (인증 필요)

전체 유저 조회, 쿼리 가능.

Query String Parameters:

-   `?email=sample@gmail.com` : 이메일 매칭
-   `?username=sample` : 닉네임 매칭

## Response Format - Success

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

## GET `/users/<uuid>`

특정 유저 1 명 조회

## Response Format

```json
{
    "success": true,
    "data": {
        "uuid": "1b35ef43-8084-499b-94a6-597fca9b70f9",
        "is_active": "활성",
        "is_admin": "관리자",
        "last_login": "2018-06-22T15:18:58.579853+09:00",
        "email": "bisschoi9541@gmail.com",
        "username": "최병규"
    }
}
```

## POST `/users/forgot`

비밀번호 찾기

## PUT `/users`

비밀번호 변경

## DELETE `/users`

유저 비활성화
