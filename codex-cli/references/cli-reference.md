# Codex CLI 전체 레퍼런스

codex-cli 0.128 기준. `codex --help` / `codex <subcommand> --help` 로 항상 최신 확인 가능. 출처: https://developers.openai.com/codex/cli/reference

## 글로벌 옵션 (모든 서브커맨드 공통)

| 플래그 | 값 | 설명 |
|--------|------|------|
| `-c, --config <key=value>` | TOML 파싱(실패 시 문자열) | `~/.codex/config.toml` 임시 오버라이드. 점 표기로 중첩 키. 예: `-c model="gpt-5.4-high"`, `-c 'sandbox_permissions=["disk-full-read-access"]'`, `-c shell_environment_policy.inherit=all` |
| `--enable <FEATURE>` | 반복 가능 | 피처 플래그 활성. `-c features.<name>=true` 와 동일 |
| `--disable <FEATURE>` | 반복 가능 | 피처 플래그 비활성 |
| `-i, --image <FILE>` | 반복 가능 | 초기 프롬프트에 이미지 첨부 |
| `-m, --model <MODEL>` | 문자열 | 사용할 모델 강제 (예: `gpt-5.4`, `gpt-5.4-high`, `o3`) |
| `--oss` | bool | 오픈소스 로컬 프로바이더 사용 |
| `--local-provider <NAME>` | `lmstudio`/`ollama` | OSS 백엔드 선택 |
| `-p, --profile <NAME>` | 문자열 | `config.toml` 의 named profile 사용 |
| `-s, --sandbox <MODE>` | `read-only` / `workspace-write` / `danger-full-access` | 모델이 실행하는 셸 명령의 샌드박스 정책 |
| `--dangerously-bypass-approvals-and-sandbox` | (별칭 `--yolo`) | 모든 승인·샌드박스 우회. 외부 격리 환경에서만 |
| `-C, --cd <DIR>` | 경로 | 에이전트 작업 루트 변경 |
| `--add-dir <DIR>` | 경로, 반복 가능 | `workspace-write` 모드에서 추가 쓰기 허용 디렉토리 |
| `-a, --ask-for-approval <POLICY>` | `untrusted` / `on-failure`(deprecated) / `on-request` / `never` | **인터랙티브 `codex` 전용**. `codex exec` 에 주면 에러로 종료. 비대화형은 승인 개념이 없다 |
| `--search` | bool | 라이브 `web_search` 툴 활성화 |
| `--no-alt-screen` | bool | TUI 인라인 모드(스크롤백 보존) |
| `--remote <ADDR>` | `ws://` / `wss://` | TUI 를 원격 app-server 에 연결 |
| `--remote-auth-token-env <ENV>` | 환경변수명 | 원격 연결용 베어러 토큰 |

## 서브커맨드

### `codex` (인터랙티브 TUI)

```bash
codex [OPTIONS] [PROMPT]
```

서브커맨드 없이 호출하면 대화형 TUI 진입. 자동화에서는 사용 금지.

키보드: `Ctrl+R` 프롬프트 히스토리 검색, `Tab` 후속 입력 큐, `Ctrl+G` 외부 에디터, `@` 파일 경로 퍼지 삽입, `/theme` 테마 변경, `/review` 리뷰 워크플로.

### `codex exec` (별칭 `e`) — 비대화형 실행

```bash
codex exec [OPTIONS] [PROMPT]
codex exec [OPTIONS] resume [SESSION_ID] [--last] [--all] [PROMPT]
codex exec [OPTIONS] review [PROMPT]
```

전용 옵션 (글로벌 외 추가):

| 플래그 | 설명 |
|--------|------|
| `--color <always\|never\|auto>` | ANSI 색상 |
| `--ephemeral` | 세션 디스크 미저장 |
| `--full-auto` | (deprecated) `--sandbox workspace-write` 사용 권장 |
| `--ignore-rules` | execpolicy `.rules` 무시 |
| `--ignore-user-config` | `config.toml` 미로드 (auth 는 그대로) |
| `--json` | 줄 단위 JSON 이벤트 스트림 stdout |
| `-o, --output-last-message <FILE>` | 최종 메시지를 파일로 |
| `--output-schema <FILE>` | 응답 형태를 검증할 JSON Schema |
| `--skip-git-repo-check` | Git 리포 외부 허용 |
| `PROMPT` | 인자 또는 `-` (stdin). 둘 다 주면 stdin 이 `<stdin>` 블록으로 덧붙음 |

> `codex exec` 는 비대화형이라 승인 정책이 없다. 글로벌 표의 `-a, --ask-for-approval` 은 `codex exec` 에선 사용할 수 없고 즉시 에러로 종료한다.

**예제:**

```bash
# 가장 안전한 분석 호출
codex exec -s read-only -o /tmp/out.md "이 파일 분석"

# 워크스페이스 패치
codex exec -s workspace-write -C /repo "버그 수정"

# JSONL 이벤트 + 최종 메시지 분리
codex exec --json -o /tmp/last.txt "..." > /tmp/events.jsonl

# 스키마 강제
codex exec --output-schema schema.json -o out.json -s read-only "..."

# stdin 컨텍스트
git diff main | codex exec -s read-only -o /tmp/r.md "diff 리뷰"

# 마지막 exec 세션 이어가기
codex exec resume --last "추가 지시"
```

### `codex review` — 비대화형 코드 리뷰

```bash
codex review [OPTIONS] [PROMPT]
```

| 플래그 | 설명 |
|--------|------|
| `--uncommitted` | 스테이징·언스테이징·언트랙 변경 리뷰 |
| `--base <BRANCH>` | base 브랜치 대비 |
| `--commit <SHA>` | 특정 커밋 변경 |
| `--title <TITLE>` | 리뷰 요약 헤더 제목 |
| `PROMPT` (`-` 가능) | 커스텀 리뷰 지시 |

### `codex resume` — 인터랙티브 세션 재개

```bash
codex resume [SESSION_ID] [--last] [--all]
```

`--last` 는 현재 디렉토리에서 가장 최근 세션, `--all` 은 디렉토리 무관 전체.

### `codex fork` — 세션 분기 (원본 보존)

```bash
codex fork [SESSION_ID] [--last] [--all]
```

### `codex login` / `codex logout`

```bash
codex login                      # ChatGPT OAuth (브라우저)
codex login --device-auth        # 디바이스 코드 (헤드리스)
codex login --with-api-key       # stdin 으로 API 키
codex login --with-agent-identity   # 실험적 Agent Identity 토큰
codex login status               # 인증 상태 (logged in 시 exit 0)
codex logout                     # 자격 증명 삭제
```

### `codex mcp` — MCP 서버 관리

```bash
codex mcp list [--json]
codex mcp add <name> -- <command...>            # stdio
codex mcp add <name> --url https://...          # HTTP
codex mcp add <name> --env KEY=VALUE -- ...     # stdio 환경변수
codex mcp add <name> --url ... --bearer-token-env-var ENV   # HTTP bearer
codex mcp get <name> [--json]
codex mcp login <name> --scopes scope1,scope2
codex mcp logout <name>
codex mcp remove <name>
```

### `codex mcp-server` — Codex 를 MCP 서버로 노출

stdio 기반. 다른 MCP 클라이언트가 spawn 해서 사용. 글로벌 `-c` 오버라이드 상속.

### `codex plugin marketplace` — 플러그인 마켓플레이스

```bash
codex plugin marketplace add <source> [--ref REF] [--sparse PATH]
codex plugin marketplace remove <name>
codex plugin marketplace upgrade [name]
```

`<source>` 는 GitHub shorthand(`owner/repo`), Git/SSH URL, 로컬 경로 모두 가능.

### `codex features` — 피처 플래그

```bash
codex features list
codex features enable <feature>
codex features disable <feature>
```

`config.toml` 의 `[features]` 섹션에 영구 반영.

### `codex completion` — 셸 컴플리션

```bash
codex completion bash | zsh | fish | power-shell | elvish
```

각 셸의 컴플리션 디렉토리로 리다이렉트.

### `codex apply` (별칭 `a`)

```bash
codex apply <TASK_ID>
```

Codex Cloud 에서 만든 최신 diff 를 `git apply` 로 로컬에 적용.

### `codex cloud` (실험적)

```bash
codex cloud --env <ENV_ID> [--attempts 1-4] [QUERY]
codex cloud list [--env ENV_ID] [--limit 1-20] [--cursor STR] [--json]
```

`--attempts` 는 best-of-N. `QUERY` 생략 시 인터랙티브.

### `codex sandbox` — 샌드박스 단독 실행

```bash
# macOS (Seatbelt)
codex sandbox --permissions-profile NAME --cd DIR [--log-denials] [--allow-unix-socket PATH] -- COMMAND...

# Linux (Landlock) / Windows
codex sandbox --permissions-profile NAME --cd DIR -- COMMAND...
```

공통: `--include-managed-config`, `-c key=value`.

### `codex execpolicy` — 룰 검증

```bash
codex execpolicy check --rules file.rules [--rules other.rules] [--pretty] -- COMMAND...
```

가장 엄격한 결정과 매칭 룰을 JSON 으로 출력.

### `codex update`

CLI 셀프 업데이트 확인·적용 (지원되는 설치 방식 한정).

### `codex app` / `codex app-server`

```bash
codex app [PATH] [--download-url URL]
```

데스크톱 앱 실행 (macOS 는 워크스페이스로 열고, Windows 는 경로 출력).

```bash
codex app-server --listen stdio:// | ws://IP:PORT \
                 --ws-auth capability-token | signed-bearer-token \
                 --ws-token-file PATH \
                 --ws-shared-secret-file PATH \
                 --ws-issuer ISS --ws-audience AUD \
                 --ws-max-clock-skew-seconds N
```

### `codex exec-server` (실험적)

독립 exec-server 서비스. 자세한 옵션은 `--help`.

### `codex debug`

```bash
codex debug models [--bundled]
codex debug app-server send-message-v2 "USER_MESSAGE"
```

`models --bundled` 는 번들 카탈로그만, 그 외엔 갱신된 카탈로그.

## 안전 권장 조합

- 인터랙티브 로컬 운용 (`codex` TUI): `--sandbox workspace-write --ask-for-approval on-request`
- 자동화·에이전트 호출 (`codex exec`): `--sandbox read-only` (분석) / `--sandbox workspace-write` (패치) — `exec` 는 승인 플래그를 받지 않는다
- 격리된 컨테이너 안에서만: `--dangerously-bypass-approvals-and-sandbox`
- 선택적 쓰기 확장: `danger-full-access` 대신 `--add-dir` 사용
- CI: `--json` + `--output-last-message` 조합

## 환경 변수·경로

- `CODEX_HOME` — 기본 `~/.codex/`. 설정·세션·자격 증명 위치
- `~/.codex/config.toml` — 기본 모델·프로파일·피처 플래그·MCP 설정
- `~/.codex/sessions/` — 세션 transcript (`--ephemeral` 시 미생성)
- `OPENAI_API_KEY` — `--with-api-key` 로그인 또는 일부 자동화 흐름에서 사용

## 참고 링크

- 기능 개요: https://developers.openai.com/codex/cli/features
- 명령 레퍼런스: https://developers.openai.com/codex/cli/reference
