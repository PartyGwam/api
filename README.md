# 파티원괌 REST API

- 스테이지 URL : https://partygwam-staging.herokuapp.com/
- 프로덕션 URL : (WIP)

## 셋업

### 1. 로컬로 클론

```
$ git clone https://github.com/partygwam/api
```

**`master`, `develop`, `staging` 브랜치에 업스트림을 달아 놓으면 로컬과 리모트의 차이를 알 수 있게 됨**

```
$ git branch -u origin/<branch> <branch>
```

### 2. 가상환경 설정 및 패키지 설치

독립된 가상환경을 만들어서 패키지를 설치하는 것이 의존성 관리에 편함

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

가상환경이 존재하지 않을 때는, 다음 명령어를 활용해서 먼저 설치한 후 실행

```
$ pip3 install virtualenv
```

### 3. 데이터베이스 마이그레이션

```
(venv) $ python manage.py migrate
```

## 실행

### 로컬 서버 실행

```
(venv) $ python manage.py runserver
```

### 관리자 만들기

```
(venv) $ python manage.py createsuperuser
```

## API 문서

- 가장 최상단 URL 에 **Swagger 문서 자동 생성**
- 초기 스펙에 관해서는 wiki 참고
- (WIP) 포스트맨 컬렉션
