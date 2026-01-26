# Claude Code Skills

Robin이 만들어 사용하는 Claude Code Skill 모음입니다.

## Skills 목록

### spring-boot-init

Spring Boot 프로젝트를 빠르게 생성하는 skill입니다.

- start.spring.io API를 활용하여 프로젝트 생성
- 다양한 프리셋 지원: REST API, 웹 애플리케이션, AI 애플리케이션, 배치 처리, 마이크로서비스
- Spring AI (OpenAI, Claude, Ollama 등) 통합 지원
- Java/Kotlin 선택 가능

**사용 예시:**
```
/spring-boot-init 스킬을 이용해서 @API_SPEC.md 문서를 토대로 api 서버 개발해줘
```

## 설치 방법

1. 이 repository를 clone합니다:
```bash
git clone <repository-url>
```

2. 원하는 skill 폴더를 `~/.claude/skills/` 디렉토리에 복사하거나 심볼릭 링크를 생성합니다:
```bash
ln -s /path/to/skills/spring-boot-init ~/.claude/skills/spring-boot-init
```

## 라이선스

MIT License
