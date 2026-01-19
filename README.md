# til app

### database setup
- mysql docker
  - `docker run --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=test -d mysql:8`
- mysql 컨테이너 띄우고 스키마 생성
  - `docker run --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=test -d mysql:8` 컨테이너 띄우기
  - `docker exec -it 컨테이너id bash` 컨테이너 접속
  - `mysql -u root -p` 후 비밀번호 `test` 입력하여 mysql 접속 `create schema `fastapi-ca`` 으로 스키마 생성
- alembic 을 이용하여 User 테이블 생성
  - `alembic init migrations` 하고 `alembic.ini` 파일과 `migrations/env.py` 파일 수정
  - `alembic revision --autogenerate -m "add User Table"`
  - `alembic upgrade head`

### 구조
- 아키텍처: 단일 FastAPI 앱과 단일 DB/설정으로 동작하는 모듈러 모놀리스입니다. 진입점은 main.py, DB 설정은 database.py.
- 레이어링: DDD 레이어를 모듈별로 분리했습니다. domain(엔티티/리포지토리 인터페이스), application(유스케이스), infra(ORM 모델/리포지토리 구현), interface(컨트롤러).
- 모듈 경계: 기능별로 user와 note로 나뉘지만 같은 프로세스와 DB를 공유합니다.
- 공용 코드: 인증/로깅은 common, 유틸은 utils, 설정은 config.py·containers.py로 중앙 관리합니다.
- 테스트: 모듈/레이어별로 test 아래에 모아져 있으며 단일 테스트 러너로 실행됩니다.
```
.
├── README.md
├── alembic.ini
├── common
│   ├── auth.py
│   └── logger.py
├── config.py
├── containers.py
├── context_vars.py
├── database.py
├── database_models.py
├── main.py
├── middlewares.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 2026
│           └── 01
│               ├── 11_1825_04_5971f7326482_add_user_table.py
│               ├── 12_2258_29_202a717bf86c_user_add_memo.py
│               └── 18_1432_50_e5dc76447f60_add_note_tag.py
├── note
│   ├── application
│   │   └── note_service.py
│   ├── domain
│   │   ├── note.py
│   │   └── repository
│   │       └── note_repo.py
│   ├── infra
│   │   ├── db_models
│   │   │   └── note.py
│   │   └── repository
│   │       └── note_repo.py
│   └── interface
│       └── controllers
│           └── note_controller.py
├── pyproject.toml
├── test
│   ├── note
│   └── user
│       ├── application
│       │   └── test_user_service.py
│       └── infra
│           └── repository
│               └── test_user_repo.py
├── user
│   ├── application
│   │   └── user_service.py
│   ├── domain
│   │   ├── repository
│   │   │   └── user_repo.py
│   │   └── user.py
│   ├── infra
│   │   ├── db_models
│   │   │   └── user.py
│   │   └── repository
│   │       └── user_repo.py
│   └── interface
│       └── controllers
│           └── user_controller.py
├── utils
│   ├── crypto.py
│   └── db_utils.py
└── uv.lock
```