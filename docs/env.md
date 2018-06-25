## 파티원괌 REST API 개발 가이드

## 에디터

- PyCharm
- Visual Studio Code

`.editorconfig` 을 활용하여 관리

- Tab 은 4 Spaces 로 통일
- JSON / YAML 및 기타 파일들은 2 Spaces 로 통일
- PEP 8 에 맞춰서 코드 스타일 규정 (`autopep8` 에 맞춰서 포맷팅)

## 언어 및 프레임워크

### 기본적인 사항

- Python / Django + Django Rest Framework 사용

### API 문서화

- Django Rest Swagger 이용하여 자동으로 생성
- 부족한 부분은 docstring 을 자동으로 문서화해주는 DRF 내장 기능 사용 + 초반에 스펙 정의한 Wiki 를 참고

### 기타 Third-party 라이브러리

- Django REST Framework 의 token authentication 이 문제가 될 경우, JWT Auth 를 위한 라이브러리가 사용될 수 있음.
- `asyncio`, `aiohttp`, `celery` 를 활용한 비동기 처리
- "이메일 전송" 관련한 라이브러리가 추가로 사용될 수 있음.
- AWS Lambda 배포를 위한 `zappa`

## 데이터베이스

- 로컬 환경 + 테스트 환경의 경우 in-memory 데이터베이스인 `sqlite` 사용
- 스테이징(heroku), 그리고 프로덕션(aws) 의 경우, `postgres` 사용

## 서버 호스팅

- 스테이징 서버(프로덕션 나가기 전에 최종 테스트 서버) 인 경우에, `heroku` 사용
- 프로덕션 서버에서는 `AWS Lambda` 사용 (`zappa` 를 활용하여 배포)

## CI

- `CircleCI` (제가 이것밖에 쓸 줄을 몰라요ㅠㅠ) 를 활용하여 최대한 모든 작업들을 자동화
- `coveralls` 를 활용하여 유닛 테스트 커버리지 측정

## API 스펙 및 일정 산정

대략적인 일정은 다음과 같습니다.

- 6/30 : API 스펙 확정 및 배포 설정 완료
- 7/7 : User API 구현 완료 (발표용)
- 7/14 : 모든 기능 구현 완료 및 스테이징 배포
- ~ 7/21 : 모든 QA 대응 완료 및 프로덕션 배포

## 브랜치 관리 전략

`Git flow` 사용.. 하고 싶으나 팀원하고 상의