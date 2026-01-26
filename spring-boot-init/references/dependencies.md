# Spring Boot 주요 의존성 참조

## 자주 사용하는 의존성

### Web & API
| ID | 이름 | 설명 |
|----|------|------|
| web | Spring Web | Spring MVC, RESTful 웹 서비스 |
| webflux | Spring Reactive Web | WebFlux 기반 리액티브 웹 |
| graphql | Spring for GraphQL | GraphQL API 지원 |
| websocket | WebSocket | WebSocket 지원 |

### Data Access
| ID | 이름 | 설명 |
|----|------|------|
| data-jpa | Spring Data JPA | JPA + Hibernate |
| data-jdbc | Spring Data JDBC | 심플한 JDBC 추상화 |
| data-r2dbc | Spring Data R2DBC | 리액티브 SQL |
| data-mongodb | Spring Data MongoDB | MongoDB 지원 |
| data-redis | Spring Data Redis | Redis 지원 |
| mybatis | MyBatis Framework | MyBatis ORM |

### Database Drivers
| ID | 이름 | 설명 |
|----|------|------|
| h2 | H2 Database | 인메모리/파일 DB |
| mysql | MySQL Driver | MySQL 드라이버 |
| postgresql | PostgreSQL Driver | PostgreSQL 드라이버 |
| mariadb | MariaDB Driver | MariaDB 드라이버 |
| oracle | Oracle Driver | Oracle 드라이버 |

### Security
| ID | 이름 | 설명 |
|----|------|------|
| security | Spring Security | 인증/인가 |
| oauth2-client | OAuth2 Client | OAuth2 로그인 |
| oauth2-resource-server | OAuth2 Resource Server | JWT 리소스 서버 |

### Messaging
| ID | 이름 | 설명 |
|----|------|------|
| amqp | Spring AMQP | RabbitMQ |
| kafka | Spring for Apache Kafka | Kafka |
| artemis | Spring Artemis | ActiveMQ Artemis |

### Cloud
| ID | 이름 | 설명 |
|----|------|------|
| cloud-config-client | Config Client | 외부 설정 |
| cloud-eureka | Eureka Discovery Client | 서비스 디스커버리 |
| cloud-gateway | Gateway | API Gateway |
| cloud-openfeign | OpenFeign | 선언적 REST 클라이언트 |
| cloud-resilience4j | Resilience4J | Circuit Breaker |

### Observability
| ID | 이름 | 설명 |
|----|------|------|
| actuator | Spring Boot Actuator | 모니터링 엔드포인트 |
| prometheus | Prometheus | Prometheus 메트릭 |
| zipkin | Zipkin Client | 분산 추적 |
| datadog | Datadog | Datadog 메트릭 |

### Developer Tools
| ID | 이름 | 설명 |
|----|------|------|
| devtools | Spring Boot DevTools | 핫 리로드 |
| lombok | Lombok | 보일러플레이트 제거 |
| configuration-processor | Configuration Processor | @ConfigurationProperties IDE 지원 |

### Testing
| ID | 이름 | 설명 |
|----|------|------|
| testcontainers | Testcontainers | 통합 테스트용 컨테이너 |

### Validation & Documentation
| ID | 이름 | 설명 |
|----|------|------|
| validation | Validation | Bean Validation (Hibernate Validator) |
| springdoc-openapi | SpringDoc OpenAPI | OpenAPI 문서 생성 |

### Batch & Scheduling
| ID | 이름 | 설명 |
|----|------|------|
| batch | Spring Batch | 배치 처리 |
| quartz | Quartz Scheduler | 스케줄링 |

### AI - Models (Chat/LLM)
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-openai | OpenAI | ChatGPT, DALL-E 지원 |
| spring-ai-anthropic | Anthropic Claude | Claude AI 모델 지원 |
| spring-ai-ollama | Ollama | 로컬 LLM 실행 |
| spring-ai-azure-openai | Azure OpenAI | Azure의 OpenAI 서비스 |
| spring-ai-bedrock | Amazon Bedrock | AWS Bedrock 모델 |
| spring-ai-bedrock-converse | Amazon Bedrock Converse | Bedrock 통합 대화 인터페이스 |
| spring-ai-mistral | Mistral AI | Mistral AI 모델 |
| spring-ai-vertexai-gemini | Vertex AI Gemini | Google Vertex Gemini |
| spring-ai-google-genai | Google GenAI | Google Gemini 모델 |
| spring-ai-deepseek | DeepSeek | DeepSeek AI 모델 |
| spring-ai-huggingface | HuggingFace | HuggingFace 모델 |
| spring-ai-zhipuai | ZhipuAI | ZhipuAI 모델 |

### AI - Vector Database
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-vectordb-pgvector | PGvector | PostgreSQL 벡터 확장 |
| spring-ai-vectordb-redis | Redis Vector | Redis 벡터 검색 |
| spring-ai-vectordb-chroma | Chroma | 오픈소스 임베딩 DB |
| spring-ai-vectordb-qdrant | Qdrant | 고성능 벡터 검색 엔진 |
| spring-ai-vectordb-milvus | Milvus | 오픈소스 벡터 DB |
| spring-ai-vectordb-pinecone | Pinecone | 클라우드 벡터 DB |
| spring-ai-vectordb-weaviate | Weaviate | 오픈소스 벡터 DB |
| spring-ai-vectordb-elasticsearch | Elasticsearch | Elasticsearch 벡터 지원 |
| spring-ai-vectordb-neo4j | Neo4j | Neo4j 벡터 검색 |
| spring-ai-vectordb-mongodb-atlas | MongoDB Atlas | MongoDB 벡터 저장소 |

### AI - MCP (Model Context Protocol)
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-mcp-server | MCP Server | MCP 서버 지원 |
| spring-ai-mcp-client | MCP Client | MCP 클라이언트 지원 |

### AI - Chat Memory
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-chat-memory-repository-in-memory | In-memory Chat Memory | 인메모리 대화 기록 |
| spring-ai-chat-memory-repository-jdbc | JDBC Chat Memory | JDBC 기반 대화 기록 |
| spring-ai-chat-memory-repository-mongodb | MongoDB Chat Memory | MongoDB 기반 대화 기록 |
| spring-ai-chat-memory-repository-neo4j | Neo4j Chat Memory | Neo4j 기반 대화 기록 |

### AI - Document Reader
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-pdf-document-reader | PDF Reader | PDF 문서 읽기 |
| spring-ai-tika-document-reader | Tika Reader | 다양한 문서 형식 읽기 |
| spring-ai-markdown-document-reader | Markdown Reader | Markdown 문서 읽기 |

### AI - Embeddings & Others
| ID | 이름 | 설명 |
|----|------|------|
| spring-ai-transformers | Transformers (ONNX) | ONNX 포맷 트랜스포머 모델 |
| spring-ai-vertexai-embeddings | Vertex AI Embeddings | Google 임베딩 모델 |
| spring-ai-postgresml | PostgresML | PostgresML 임베딩 |
| spring-ai-stabilityai | Stability AI | 이미지 생성 모델 |
| spring-ai-elevenlabs | ElevenLabs | TTS(음성 합성) 모델 |

## 프리셋 조합

### minimal
- devtools

### web (기본 웹 애플리케이션)
- web, validation, devtools

### web-jpa (웹 + 데이터베이스)
- web, data-jpa, validation, h2, devtools

### web-api (REST API 서버)
- web, validation, actuator, devtools

### web-security (보안 적용 웹)
- web, security, validation, devtools

### full (풀스택)
- web, data-jpa, security, validation, actuator, h2, devtools, lombok

### reactive (리액티브)
- webflux, data-r2dbc, validation, devtools

### batch (배치 처리)
- batch, data-jpa, h2, devtools

### ai-openai (OpenAI 기반 AI 앱)
- web, spring-ai-openai, devtools

### ai-ollama (로컬 LLM AI 앱)
- web, spring-ai-ollama, devtools

### ai-anthropic (Claude AI 앱)
- web, spring-ai-anthropic, devtools

### ai-rag (RAG 애플리케이션)
- web, spring-ai-openai, spring-ai-vectordb-pgvector, spring-ai-pdf-document-reader, postgresql, devtools

### ai-chatbot (채팅봇 + 대화 기록)
- web, spring-ai-openai, spring-ai-chat-memory-repository-jdbc, data-jpa, h2, devtools

### ai-mcp (MCP 서버 앱)
- web, spring-ai-mcp-server, spring-ai-openai, devtools
