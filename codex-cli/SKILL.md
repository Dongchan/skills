---
name: codex-cli
description: "OpenAI Codex CLI(`codex`) 사용 스킬. 터미널에서 OpenAI 코딩 에이전트를 호출해 비대화형 작업(`codex exec`), 코드 리뷰(`codex review`), 세션 재개(`codex resume`), MCP 서버 등록(`codex mcp`)을 수행한다. 사용 시점: 사용자가 'codex', 'codex cli', 'codex exec', 'OpenAI 코덱스', 'GPT 로 한 번 더', 'codex 로 두 번째 의견', 'codex 로 리뷰', 'codex 로 패치', 'OpenAI 모델로 코딩 시켜', 'codex 백그라운드 실행', 'codex JSON 출력', 'codex 샌드박스', 'codex MCP 등록' 등을 언급할 때. Claude Code 자체 작업에 OpenAI 의 두 번째 시각을 더하거나, 별도 모델로 동일 작업을 비교할 때 반드시 이 스킬을 사용한다. 단, ChatGPT 웹/앱·OpenAI Responses API 직접 호출·gpt-image-2 이미지 생성은 이 스킬의 범위가 아니다."
---

# OpenAI Codex CLI

OpenAI 의 코딩 에이전트 CLI(`codex`)를 Claude Code 세션 안에서 안전하게 호출하기 위한 스킬. (참고: codex-cli 0.128 / 2026-04 기준)

Codex CLI 는 Claude Code 와 같은 결의 코딩 에이전트지만 모델이 OpenAI(이 빌드 기본은 `gpt-5.5`, 또는 `--oss` 로컬) 라는 점이 핵심 차이. 이 스킬은 주로 **`codex exec` 비대화형 호출**을 통해 Claude 가 자신의 작업에 OpenAI 시각을 더하거나, 독립 작업을 위임할 때 쓴다.

**중요한 동작 원리.** `codex exec` 는 비대화형이므로 승인(approval) 개념 자체가 없다. 모든 명령은 자동으로 시도되고, 위험성은 오직 `--sandbox` 정책으로만 제어한다. 따라서 인터랙티브 `codex` 의 `--ask-for-approval` 플래그는 `codex exec` 에서 **에러**를 낸다. 이 스킬의 모든 예제는 이 점을 반영한다.

## 언제 쓰는가

- **두 번째 의견(second opinion)**. 중요한 설계·디버깅 결정에 OpenAI 모델의 독립 분석을 받고 싶을 때
- **병렬 위임**. 메인 컨텍스트를 보호하면서 Codex 에 별개 하위 작업(빌드 검증, 리팩터 초안 등)을 시킬 때
- **코드 리뷰**. `codex review` 로 브랜치/커밋/언커밋 변경을 비대화형 리뷰
- **JSON 자동화**. `--json --output-last-message` 조합으로 결과를 파일·파이프라인에 흘려보낼 때
- **MCP 동기화**. Codex 에 MCP 서버를 등록·관리해 도구 풀을 확장할 때

대화형 TUI(`codex` 인자 없이) 자체는 사람이 직접 다루는 모드라, 에이전트 입장에서는 거의 항상 `codex exec` 를 쓴다.

## 사전 점검 (호출 전 1회)

```bash
codex --version          # 설치 확인
codex login status       # 인증 상태 (logged in 이면 OK)
```

`codex login status` 가 실패하면 사용자에게 다음 중 하나를 안내한다.

```bash
codex login                              # ChatGPT OAuth (권장)
codex login --device-auth                # 헤드리스 환경
printenv OPENAI_API_KEY | codex login --with-api-key   # API 키 사용
```

API 키 모드는 사용량이 OpenAI Platform 결제로 계산되므로 ChatGPT Plus/Pro/Team 구독자라면 OAuth 로그인이 비용상 유리하다.

## 핵심 패턴: `codex exec`

기본 골격.

```bash
codex exec [OPTIONS] "프롬프트"
```

작은 작업이라도 Claude 가 호출할 때는 **항상 비대화형 옵션을 명시**한다. 그렇지 않으면 TUI 가 떠서 세션이 멈춘다.

### 1) 안전한 읽기 전용 호출 (분석·리뷰)

```bash
codex exec \
  --sandbox read-only \
  --skip-git-repo-check \
  --output-last-message /tmp/codex-out.md \
  "이 디렉토리의 src/auth/*.ts 파일을 읽고 잠재적 보안 취약점을 마크다운 표로 정리해라"
```

`read-only` 샌드박스는 부작용이 없어 자동화의 가장 안전한 기본값이다. 결과물은 `--output-last-message` 로 받는 게 확실하다(stdout 에는 헤더·진행 로그·토큰 사용량이 섞인다).

### 2) 워크스페이스 쓰기 호출 (패치 생성)

```bash
codex exec \
  --sandbox workspace-write \
  --cd /path/to/repo \
  --output-last-message /tmp/codex-patch.md \
  "tests/integration/login.spec.ts 에서 401 케이스가 빠져 있다. 추가하고 npm test 로 통과시켜라"
```

`workspace-write` 는 작업 루트(또는 `--cd`)와 `--add-dir` 로 추가한 디렉토리에만 쓰기를 허용한다. 비대화형이라 사람에게 묻지 않으므로, 결과를 사용자에게 다시 보여 주고 검토받는 흐름을 유지하라.

### 3) JSONL 이벤트 스트림 (파이프라인 통합)

```bash
codex exec \
  --json \
  --sandbox read-only \
  --output-last-message /tmp/last.txt \
  "package.json 의 의존성을 분석해 outdated 한 것만 JSON 배열로 알려줘" \
  > /tmp/codex.jsonl
```

`--json` 은 줄 단위 JSON 이벤트(시작·도구 호출·메시지·완료)를 stdout 에 흘리고, `--output-last-message` 는 모델 최종 답만 별도 파일로 떨어뜨린다. CI 자동화에서는 둘을 함께 쓴다.

### 4) 출력 스키마 강제

```bash
codex exec \
  --output-schema /tmp/schema.json \
  --output-last-message /tmp/result.json \
  --sandbox read-only \
  "이 README 에서 설치 명령어들을 추출해 schema 에 맞춰 JSON 으로 반환"
```

`--output-schema` 에 JSON Schema 파일 경로를 주면 최종 응답이 그 형태로 검증된다. 표/엔터티 추출 같은 구조화 작업에 쓴다.

### 5) stdin 으로 큰 컨텍스트 전달

```bash
git diff main..HEAD | codex exec \
  --sandbox read-only \
  -o /tmp/review.md \
  "표준 입력으로 들어온 diff 를 리뷰해라. 위험·개선·테스트 가능성 순으로 정리"
```

PROMPT 인자에 `-` 만 주거나 인자를 생략하면 stdin 전체가 프롬프트가 된다. PROMPT 와 stdin 을 동시에 주면 stdin 이 `<stdin>` 블록으로 덧붙는다.

### 6) 이미지 첨부

```bash
codex exec -i screenshot.png \
  --sandbox read-only \
  -o /tmp/codex-out.md \
  "이 스크린샷의 UI 구조를 React 컴포넌트 트리로 표현해줘"
```

`-i` 는 반복 가능. PNG/JPG/WebP 등을 멀티 첨부할 수 있다.

## 샌드박스 정책 가이드

| Sandbox | 적합한 상황 |
|---------|-------------|
| `read-only` | 분석·문서화·리뷰. **에이전트 호출 기본값.** |
| `workspace-write` | 자동화된 패치 생성. 작업 루트·`--add-dir` 만 쓰기 가능. |
| `danger-full-access` | 사용 금지 — 사용자의 명시 요청 + 격리 환경에서만. |

`--dangerously-bypass-approvals-and-sandbox`(별칭 `--yolo`)는 격리된 컨테이너 외부에서는 절대 쓰지 않는다.

> **인터랙티브 `codex` 는 다르다.** TUI 모드에서만 `-a, --ask-for-approval <untrusted|on-request|never>` 가 의미를 가진다. `codex exec` 에 같은 플래그를 주면 즉시 에러로 종료하므로 절대 섞지 말 것.

## 모델 / 프로파일 선택

```bash
codex exec -m gpt-5.5 "..."              # 모델 직접 지정
codex exec -p review "..."               # ~/.codex/config.toml 의 [profiles.review] 사용
codex exec --oss --local-provider ollama -m gpt-oss:20b "..."   # 로컬 OSS 모델
```

기본 모델은 ChatGPT 계정 플랜과 `~/.codex/config.toml` 의 `model =` 설정에 따른다 (이 빌드 기본 `gpt-5.5`). 모델 카탈로그는 `codex debug models` 로 확인. `-c model_reasoning_effort=high` 같은 인라인 오버라이드도 동일 효과.

## 두 번째 의견(second opinion) 패턴

Claude 의 분석을 그대로 두고, 같은 입력을 OpenAI 에 한 번 더 돌려 비교하는 구조.

```bash
# 1) Claude 가 결론을 적어 둔 메모
echo "## Claude 결론\n$CLAUDE_CONCLUSION" > /tmp/handoff.md
echo "## 원본 컨텍스트" >> /tmp/handoff.md
cat path/to/relevant.ts >> /tmp/handoff.md

# 2) Codex 에 독립 판단 요청
codex exec \
  --sandbox read-only \
  -o /tmp/codex-opinion.md \
  "$(cat /tmp/handoff.md)\n\n위 결론에 동의하는지, 놓친 부분은 없는지 독립적으로 판단해 마크다운으로 답해라."
```

핵심은 Claude 의 결론을 같이 넘기되 "독립적으로" 판단하라고 명시하는 것. 동일 모델 반복보다 가짜 합의(echo chamber)를 줄인다.

## 코드 리뷰: `codex review`

브랜치/커밋/언커밋 단위로 리뷰만 돌리는 전용 서브커맨드. `codex exec` 와 달리 리뷰 포맷이 정형화돼 있다.

```bash
codex review --base main                    # main 대비 현재 브랜치
codex review --uncommitted                  # 스테이징·언스테이징·언트랙
codex review --commit abc1234               # 특정 커밋
codex review --base main --title "Auth refactor"   # 요약 헤더용 제목
codex review -                              # stdin 으로 커스텀 지시 받기
```

`-c model="..."`, `--enable`/`--disable` 같은 글로벌 플래그도 동일하게 받는다. 결과는 stdout 으로 흘러나오므로 `tee` 로 저장한다.

## 세션 재개·포크

```bash
codex resume --last                          # 가장 최근 인터랙티브 세션 재개 (TUI)
codex resume --all                           # 모든 디렉토리의 세션 중 선택
codex exec resume --last "추가 지시"         # 비대화형으로 마지막 exec 세션 이어가기
codex fork --last                            # 분기 (원본 보존)
```

`codex exec` 도 기본적으로 세션을 디스크에 남긴다. 일회성이라면 `--ephemeral` 로 비활성화.

## MCP 서버 관리

```bash
codex mcp list
codex mcp add my-tool -- node mcp-server.js              # stdio 서버
codex mcp add web-tool --url https://mcp.example.com     # HTTP 서버
codex mcp add github --url https://api.githubcopilot.com/mcp \
    --bearer-token-env-var GITHUB_TOKEN
codex mcp get my-tool --json
codex mcp login web-tool --scopes "read:repo,write:repo"
codex mcp remove my-tool
```

Claude Code 의 `claude mcp` 와 별개로, Codex 자신이 사용하는 MCP 풀을 관리한다. 같은 서버를 두 CLI 가 공유하려면 양쪽에 각각 등록한다.

Codex 자체를 MCP 서버로 띄우려면(다른 에이전트의 도구로 노출):

```bash
codex mcp-server   # stdio 기반. 호출 측 MCP 클라이언트가 spawn
```

## 자주 쓰는 글로벌 옵션

| 플래그 | 효과 |
|--------|------|
| `-c key=value` | `~/.codex/config.toml` 값을 임시 오버라이드. 값은 TOML 로 파싱 (실패 시 문자열). 예: `-c model="gpt-5.4-high" -c 'sandbox_permissions=["disk-full-read-access"]'` |
| `--enable <feature>` / `--disable <feature>` | 피처 플래그 토글. `codex features list` 로 목록 확인 |
| `-C, --cd <DIR>` | 작업 루트 변경 |
| `--add-dir <DIR>` | `workspace-write` 에서 추가로 쓰기 가능한 디렉토리 |
| `--skip-git-repo-check` | Git 리포지토리 밖에서도 실행 |
| `--ignore-user-config` | `config.toml` 무시 (재현성 보장) |
| `--ignore-rules` | 사용자/프로젝트 execpolicy `.rules` 무시 |
| `--search` | `web_search` 툴 활성화 (라이브 검색) |

전체 플래그·서브커맨드 목록은 `references/cli-reference.md` 참고.

## 비용·속도 가이드

- 단발성 분석은 `--sandbox read-only` + 짧은 프롬프트가 가장 저렴·빠름
- 큰 컨텍스트는 stdin 으로 흘려라(인자 길이 제한·이스케이프 회피)
- 동일 작업을 반복할 거라면 `~/.codex/config.toml` 에 프로파일 정의하고 `-p name` 으로 호출 — 인자 노이즈 감소
- 매 호출마다 세션이 디스크에 남는다. 일회성·민감 데이터는 `--ephemeral`

## 안티패턴

- **TUI 모드 호출**. 인자 없는 `codex` 또는 `codex "..."`(서브커맨드 없이)는 풀스크린 TUI. 자동화에서 절대 쓰지 말 것 — 항상 `codex exec` 로 시작.
- **`codex exec` 에 `--ask-for-approval` 부착**. 비대화형엔 승인 개념이 없어 즉시 에러로 종료한다. 인터랙티브 `codex` 전용 옵션이다.
- **`--yolo`/`-c sandbox=danger-full-access`**. 사용자의 명시 동의 없이 절대 사용 금지.
- **stdout 만으로 결과 파싱**. 진행 이벤트가 섞여 들어온다. `--output-last-message` 로 최종 메시지만 파일 캡처.
- **장시간 작업을 포그라운드로**. 5분 이상 걸릴 작업은 Bash `run_in_background: true` 와 결합하고, 완료 알림으로 결과 파일을 읽는다.
- **민감 정보 로그 남김**. 기본 세션은 `~/.codex/sessions/` 에 저장된다. 비밀 데이터는 `--ephemeral` 또는 사용자 동의 후 삭제.

## 트러블슈팅

- `not logged in` → `codex login status` 후 위 로그인 명령 중 택일
- `not in a git repository` → `--skip-git-repo-check`
- `unexpected argument '--ask-for-approval'` → `codex exec` 에 인터랙티브 전용 플래그를 줬다. 빼고 `--sandbox` 만 사용.
- TUI 가 떠서 멈춤 → `codex exec` 가 아닌 `codex` 로 호출했는지 확인
- 출력이 어디 갔는지 모를 때 → `--json` 으로 이벤트 스트림 확인 + `--output-last-message` 로 최종 답 분리
- `workspace-write` 인데 권한 거부 → 파일이 작업 루트 밖. `--add-dir` 또는 `--cd` 로 루트 변경
- 모델·플랜 한도 초과 → `-m` 으로 다른 모델 지정, 또는 `--oss` + 로컬 모델

## 확장 레퍼런스

- `references/cli-reference.md` — 전체 서브커맨드·플래그·예제 (exec / review / resume / fork / login / mcp / sandbox / features / cloud / app-server / debug 등)
