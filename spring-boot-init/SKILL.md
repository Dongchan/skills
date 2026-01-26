---
name: spring-boot-init
description: "Spring Boot 프로젝트 초기 생성 스킬. start.spring.io API를 사용하여 프로젝트를 생성합니다. 사용 시점: (1) 새 Spring Boot 프로젝트 생성, (2) 스프링 부트 프로젝트 만들어줘, (3) Spring Boot로 API 서버 만들어줘, (4) 웹 애플리케이션 시작하고 싶어, (5) Spring Initializr 관련 요청"
---

# Spring Boot 프로젝트 생성

## 워크플로우

### 1. 사용자에게 질문하기 (조건부 플로우)

프로젝트 생성 전 AskUserQuestion 도구로 다음을 확인. **한 번에 최대 4개 질문까지 가능하므로 관련 질문을 묶어서 진행**.

#### Step 1: 기본 정보 (첫 번째 질문 세트)

**질문 1: 프로그래밍 언어**
- Java (Recommended) - Gradle Groovy DSL 사용
- Kotlin - Gradle Kotlin DSL 사용

**질문 2: 프로젝트 유형**
- REST API 서버
- 웹 애플리케이션 (MVC + 템플릿)
- AI 애플리케이션
- 배치 처리
- 마이크로서비스

#### Step 2: 유형별 추가 질문 (조건부)

##### REST API / 웹 애플리케이션 선택 시:

**질문 3: 데이터베이스**
- H2 (개발/테스트용, Recommended)
- PostgreSQL
- MySQL
- MongoDB
- 사용 안함

**질문 4: 추가 기능** (multiSelect: true)
- Spring Security (인증/인가)
- API 문서 (SpringDoc OpenAPI)
- Actuator (모니터링)

##### AI 애플리케이션 선택 시:

**질문 3: AI 모델 (LLM)**
- OpenAI (ChatGPT, Recommended)
- Anthropic Claude
- Ollama (로컬 LLM)
- Azure OpenAI
- Amazon Bedrock

**질문 4: RAG 구성**
- 벡터 DB + 문서 리더 포함 (RAG 구축)
- 채팅 메모리만 (대화 기록 저장)
- LLM만 사용 (심플)

**질문 5 (RAG 선택 시): 벡터 데이터베이스**
- PGvector (PostgreSQL, Recommended)
- Chroma
- Redis
- Qdrant
- Milvus

##### 마이크로서비스 선택 시:

**질문 3: 인프라 구성** (multiSelect: true)
- Eureka (서비스 디스커버리)
- Config Server (외부 설정)
- Gateway (API 게이트웨이)
- Resilience4j (서킷 브레이커)

**질문 4: 메시징**
- Kafka
- RabbitMQ
- 사용 안함

##### 배치 처리 선택 시:

**질문 3: 데이터 소스**
- H2 (개발용, Recommended)
- PostgreSQL
- MySQL

**질문 4: 스케줄링**
- Quartz Scheduler 포함
- Spring @Scheduled만 사용

### 2. 프로젝트 이름 추천

용도에 따라 이름 제안:
- REST API: `user-api`, `order-service`, `product-api`
- 웹 애플리케이션: `admin-portal`, `dashboard-app`, `web-shop`
- AI 애플리케이션: `ai-assistant`, `chatbot-service`, `rag-search`, `doc-analyzer`
- 배치: `data-batch`, `report-batch`, `sync-job`
- 마이크로서비스: `auth-service`, `payment-service`, `notification-service`

사용자가 원하면 직접 이름 입력 가능.

### 3. 프로젝트 생성

```bash
python3 scripts/create_project.py <프로젝트명> --lang <java|kotlin> --preset <프리셋> --output <경로>
```

## 자동 설정 (고정값)

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot 버전 | 자동 선택 | Spring AI 사용 시 3.x, 그 외 서버 기본값 |
| Java 버전 | 21 | LTS |
| 패키징 | JAR | - |
| 설정 파일 | application.yml | properties → yml 자동 변환 |
| 빌드 도구 | Gradle | Java=Groovy DSL, Kotlin=Kotlin DSL |

### Spring AI 버전 호환성

- **Spring AI 1.x** → Spring Boot 3.x와 호환
- **Spring AI 2.x** → Spring Boot 4.x와 호환

스크립트가 `spring-ai-*` 의존성을 감지하면 자동으로 호환되는 Spring Boot 버전을 선택합니다.

## 프리셋 선택 가이드

### 기본 프리셋

| 용도 | 추천 프리셋 | 포함 의존성 |
|------|------------|-------------|
| REST API | `web-api` | web, validation, actuator, devtools |
| 웹 + DB | `web-jpa` | web, data-jpa, validation, h2, devtools |
| 보안 필요 | `web-security` | web, security, validation, devtools |
| 풀스택 | `full` | web, jpa, security, validation, actuator, h2, devtools, lombok |
| 리액티브 | `reactive` | webflux, data-r2dbc, validation, devtools |
| 배치 | `batch` | batch, data-jpa, h2, devtools |

### AI 프리셋

| 용도 | 추천 프리셋 | 포함 의존성 |
|------|------------|-------------|
| OpenAI 기반 | `ai-openai` | web, spring-ai-openai, devtools |
| Claude 기반 | `ai-anthropic` | web, spring-ai-anthropic, devtools |
| 로컬 LLM | `ai-ollama` | web, spring-ai-ollama, devtools |
| RAG 앱 | `ai-rag` | web, spring-ai-openai, spring-ai-vectordb-pgvector, spring-ai-pdf-document-reader, postgresql, devtools |
| 채팅봇 | `ai-chatbot` | web, spring-ai-openai, spring-ai-chat-memory-repository-jdbc, data-jpa, h2, devtools |
| MCP 서버 | `ai-mcp` | web, spring-ai-mcp-server, spring-ai-openai, devtools |

## 사용자 선택 → 의존성 매핑

질문 응답에 따라 프리셋 대신 `--deps` 옵션으로 직접 조합:

```
# 기본 구성
REST API + PostgreSQL + Security + OpenAPI
→ --deps web,validation,data-jpa,postgresql,security,springdoc-openapi,actuator,devtools

# AI 구성
AI (OpenAI) + RAG (PGvector)
→ --deps web,spring-ai-openai,spring-ai-vectordb-pgvector,spring-ai-pdf-document-reader,postgresql,devtools

# AI 구성 (Claude + 채팅 메모리)
→ --deps web,spring-ai-anthropic,spring-ai-chat-memory-repository-jdbc,data-jpa,h2,devtools

# 마이크로서비스
→ --deps web,cloud-eureka,cloud-config-client,cloud-openfeign,actuator,devtools
```

## 추가 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--group` | Group ID | com.example |
| `--desc` | 프로젝트 설명 | Demo project for Spring Boot |
| `--deps` | 커스텀 의존성 (쉼표 구분) | - |
| `--boot` / `--bootVersion` | Spring Boot 버전 명시 (예: 3.5.0) | 자동 선택 |
| `--check-ai-version` | Spring AI 최신 버전 정보 확인 | - |

### Spring Boot 버전 지정

Spring AI와 함께 사용할 때 버전을 명시적으로 지정할 수 있습니다:

```bash
# Spring Boot 버전 명시
python3 scripts/create_project.py my-app --deps web,spring-ai-openai --boot 3.5.0

# Spring AI 버전 확인
python3 scripts/create_project.py --check-ai-version
```

## 예시

```bash
# Java REST API
python3 scripts/create_project.py user-api --lang java --preset web-api

# Kotlin 웹앱 + DB
python3 scripts/create_project.py admin-portal --lang kotlin --preset web-jpa

# 커스텀 의존성 (REST API + PostgreSQL + Security)
python3 scripts/create_project.py my-service --lang java --deps web,validation,data-jpa,postgresql,security,actuator,devtools

# AI 앱 - OpenAI (자동으로 호환 버전 선택)
python3 scripts/create_project.py ai-app --lang kotlin --deps web,spring-ai-openai,actuator,devtools

# AI 앱 - OpenAI RAG (프리셋 사용)
python3 scripts/create_project.py ai-assistant --lang java --preset ai-rag

# AI 앱 - Claude 채팅봇
python3 scripts/create_project.py claude-chatbot --lang java --deps web,spring-ai-anthropic,spring-ai-chat-memory-repository-jdbc,data-jpa,h2,devtools

# AI 앱 - Ollama 로컬 LLM
python3 scripts/create_project.py local-ai --lang java --preset ai-ollama

# 마이크로서비스 (Eureka + Kafka)
python3 scripts/create_project.py order-service --lang java --deps web,cloud-eureka,kafka,data-jpa,postgresql,actuator,devtools

# Spring Boot 버전 명시적 지정
python3 scripts/create_project.py my-app --lang java --deps web,data-jpa --boot 3.5.0

# Spring AI 최신 버전 확인
python3 scripts/create_project.py --check-ai-version
```

## 생성 후 실행

```bash
cd <프로젝트명>
./gradlew bootRun
```

## 의존성 참조

전체 의존성 목록: [references/dependencies.md](references/dependencies.md)
