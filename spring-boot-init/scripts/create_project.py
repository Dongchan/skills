#!/usr/bin/env python3
"""
Spring Boot 프로젝트 생성 스크립트
start.spring.io API를 사용하여 프로젝트를 생성합니다.
"""

import argparse
import json
import os
import subprocess
import sys
import zipfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen, Request


# Spring AI 의존성 ID 목록 (spring-ai- 접두사)
SPRING_AI_DEPENDENCIES = [
    "spring-ai-openai",
    "spring-ai-anthropic",
    "spring-ai-ollama",
    "spring-ai-azure-openai",
    "spring-ai-bedrock",
    "spring-ai-bedrock-converse",
    "spring-ai-google-genai",
    "spring-ai-google-genai-embedding",
    "spring-ai-vertexai-gemini",
    "spring-ai-vertexai-embeddings",
    "spring-ai-mistral",
    "spring-ai-huggingface",
    "spring-ai-minimax",
    "spring-ai-zhipuai",
    "spring-ai-deepseek",
    "spring-ai-oci-genai",
    "spring-ai-postgresml",
    "spring-ai-stabilityai",
    "spring-ai-elevenlabs",
    "spring-ai-transformers",
    "spring-ai-mcp-client",
    "spring-ai-mcp-server",
    "spring-ai-vectordb-pgvector",
    "spring-ai-vectordb-chroma",
    "spring-ai-vectordb-redis",
    "spring-ai-vectordb-milvus",
    "spring-ai-vectordb-qdrant",
    "spring-ai-vectordb-pinecone",
    "spring-ai-vectordb-weaviate",
    "spring-ai-vectordb-elasticsearch",
    "spring-ai-vectordb-opensearch",
    "spring-ai-vectordb-neo4j",
    "spring-ai-vectordb-mongodb-atlas",
    "spring-ai-vectordb-cassandra",
    "spring-ai-vectordb-azure",
    "spring-ai-vectordb-oracle",
    "spring-ai-vectordb-typesense",
    "spring-ai-vectordb-gemfire",
    "spring-ai-vectordb-couchbase",
    "spring-ai-vectordb-mariadb",
    "spring-ai-vectordb-azurecosmosdb",
    "spring-ai-vectordb-aws-opensearch",
    "spring-ai-chat-memory-repository-jdbc",
    "spring-ai-chat-memory-repository-neo4j",
    "spring-ai-chat-memory-repository-mongodb",
    "spring-ai-chat-memory-repository-cassandra",
    "spring-ai-chat-memory-repository-in-memory",
    "spring-ai-pdf-document-reader",
    "spring-ai-markdown-document-reader",
    "spring-ai-tika-document-reader",
]


def has_spring_ai_dependency(dependencies: list[str]) -> bool:
    """의존성 목록에 Spring AI 관련 의존성이 있는지 확인합니다."""
    for dep in dependencies:
        if dep.startswith("spring-ai-") or dep in SPRING_AI_DEPENDENCIES:
            return True
    return False


def fetch_spring_initializr_metadata(boot_version: str | None = None) -> dict:
    """
    start.spring.io API에서 메타데이터를 가져옵니다.

    Args:
        boot_version: Spring Boot 버전 (None이면 기본값 사용)

    Returns:
        API 응답 딕셔너리
    """
    url = "https://start.spring.io/dependencies"
    if boot_version:
        url += f"?bootVersion={boot_version}"

    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            raise RuntimeError(f"API 오류: {error_data.get('message', error_body)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"API 오류 ({e.code}): {error_body}")
    except URLError as e:
        raise RuntimeError(f"네트워크 오류: {e.reason}")


def get_spring_ai_version(boot_version: str) -> str | None:
    """
    특정 Spring Boot 버전에서 사용하는 Spring AI BOM 버전을 조회합니다.

    Args:
        boot_version: Spring Boot 버전

    Returns:
        Spring AI BOM 버전 또는 None
    """
    try:
        metadata = fetch_spring_initializr_metadata(boot_version)
        boms = metadata.get("boms", {})
        spring_ai_bom = boms.get("spring-ai", {})
        return spring_ai_bom.get("version")
    except Exception:
        return None


def get_available_boot_versions() -> list[dict]:
    """
    start.spring.io에서 사용 가능한 Spring Boot 버전 목록을 가져옵니다.

    Returns:
        버전 정보 리스트 [{"id": "3.5.0", "name": "3.5.0", "default": True}, ...]
    """
    try:
        req = Request("https://start.spring.io", headers={"Accept": "application/json"})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("bootVersion", {}).get("values", [])
    except Exception:
        return []


def get_default_boot_version() -> str:
    """기본 Spring Boot 버전을 가져옵니다."""
    versions = get_available_boot_versions()
    for v in versions:
        if v.get("default"):
            return v.get("id", "3.5.0")
    return "3.5.0"


def parse_version(version_str: str) -> tuple:
    """
    버전 문자열을 비교 가능한 튜플로 변환합니다.
    예: "3.5.0" -> (3, 5, 0), "3.5.0.RELEASE" -> (3, 5, 0)
    """
    # 숫자가 아닌 접미사 제거 (.RELEASE 등)
    parts = version_str.split(".")
    version_parts = []
    for p in parts:
        try:
            version_parts.append(int(p))
        except ValueError:
            break  # 숫자가 아닌 부분에서 중단
    return tuple(version_parts) if version_parts else (0,)


def validate_boot_version(version: str) -> bool:
    """
    start.spring.io에서 해당 버전이 실제로 사용 가능한지 검증합니다.

    Args:
        version: 검증할 Spring Boot 버전

    Returns:
        사용 가능하면 True
    """
    try:
        metadata = fetch_spring_initializr_metadata(version)
        # dependencies가 있으면 유효한 버전
        return "dependencies" in metadata
    except Exception:
        return False


def get_compatible_boot_version_for_spring_ai() -> str:
    """
    Spring AI와 호환되는 Spring Boot 버전을 찾습니다.
    Spring AI 1.x는 Spring Boot 3.x와 호환됩니다.

    Returns:
        호환되는 Spring Boot 버전
    """
    versions = get_available_boot_versions()

    # Spring Boot 3.x 중 안정 버전 찾기
    # .RELEASE 접미사가 붙은 패치 버전은 start.spring.io에서 BOM 해결 문제가 있을 수 있음
    # SNAPSHOT, M, RC, 그리고 높은 패치 버전의 .RELEASE는 제외
    stable_3x_versions = []
    for v in versions:
        version_id = v.get("id", "")
        # 3.x 버전이면서 불안정한 접미사가 없는 것
        if version_id.startswith("3."):
            # SNAPSHOT, M, RC 제외
            if any(x in version_id for x in ["SNAPSHOT", "-M", "-RC"]):
                continue
            # .RELEASE 버전도 불안정할 수 있으므로 제외하고 순수 버전만 사용
            # 3.5.0.RELEASE 대신 3.5.0 형태만 허용
            if ".RELEASE" in version_id:
                continue
            stable_3x_versions.append(version_id)

    if stable_3x_versions:
        # 가장 최신 버전 반환
        stable_3x_versions.sort(key=parse_version, reverse=True)
        return stable_3x_versions[0]

    # 순수 버전이 없으면 알려진 안정 버전 사용
    # start.spring.io에서 3.5.0은 항상 지원됨
    return "3.5.0"


def get_build_type_for_language(language: str) -> str:
    """
    언어에 따라 적절한 빌드 타입을 반환합니다.
    - Java → Gradle Groovy DSL
    - Kotlin → Gradle Kotlin DSL
    """
    if language == "kotlin":
        return "gradle-project-kotlin"
    else:
        return "gradle-project"


def convert_properties_to_yaml(project_path: str, artifact_id: str) -> None:
    """
    application.properties를 application.yml로 변환합니다.

    Args:
        project_path: 프로젝트 경로
        artifact_id: 프로젝트 artifact ID (spring.application.name에 사용)
    """
    resources_path = os.path.join(project_path, "src", "main", "resources")
    properties_file = os.path.join(resources_path, "application.properties")
    yaml_file = os.path.join(resources_path, "application.yml")

    if os.path.exists(properties_file):
        # 기본 application.yml 생성 (실제 프로젝트 이름 사용)
        with open(yaml_file, "w") as f:
            f.write("spring:\n")
            f.write("  application:\n")
            f.write(f"    name: {artifact_id}\n")

        # properties 파일 삭제
        os.remove(properties_file)


def validate_zip_file(zip_path: str) -> bool:
    """
    다운로드한 파일이 유효한 ZIP 파일인지 확인합니다.

    Args:
        zip_path: ZIP 파일 경로

    Returns:
        유효한 ZIP 파일이면 True
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # ZIP 파일 무결성 검사
            bad_file = zf.testzip()
            return bad_file is None
    except zipfile.BadZipFile:
        return False
    except Exception:
        return False


def download_project(url: str, zip_path: str) -> None:
    """
    프로젝트를 다운로드합니다.

    Args:
        url: 다운로드 URL
        zip_path: 저장할 ZIP 파일 경로

    Raises:
        RuntimeError: 다운로드 실패 시
    """
    try:
        # urllib로 직접 다운로드 (HTTP 에러 처리 가능)
        req = Request(url)
        with urlopen(req, timeout=60) as response:
            # HTTP 상태 코드 확인
            if response.status != 200:
                raise RuntimeError(f"HTTP 오류: {response.status}")

            # Content-Type 확인
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                # JSON 응답은 에러 메시지
                error_data = json.loads(response.read().decode())
                raise RuntimeError(f"API 오류: {error_data.get('message', error_data)}")

            # ZIP 파일 저장
            with open(zip_path, "wb") as f:
                f.write(response.read())

    except HTTPError as e:
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            error_msg = error_data.get("message", error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        raise RuntimeError(f"다운로드 실패 (HTTP {e.code}): {error_msg}")
    except URLError as e:
        raise RuntimeError(f"네트워크 오류: {e.reason}")


def create_spring_boot_project(
    name: str,
    group_id: str = "com.example",
    artifact_id: str | None = None,
    description: str = "Demo project for Spring Boot",
    package_name: str | None = None,
    boot_version: str | None = None,
    java_version: str = "21",
    language: str = "java",
    dependencies: list[str] | None = None,
    output_dir: str = ".",
) -> str:
    """
    Spring Initializr API를 호출하여 프로젝트를 생성합니다.

    Args:
        name: 프로젝트 이름
        group_id: Maven Group ID (예: com.example)
        artifact_id: Maven Artifact ID (기본값: name)
        description: 프로젝트 설명
        package_name: 기본 패키지명 (기본값: group_id.artifact_id)
        boot_version: Spring Boot 버전 (None이면 자동 결정)
        java_version: Java 버전 (17, 21, 23)
        language: 프로그래밍 언어 (java, kotlin)
        dependencies: 의존성 목록
        output_dir: 출력 디렉토리

    Returns:
        생성된 프로젝트 경로
    """
    if artifact_id is None:
        artifact_id = name.lower().replace(" ", "-").replace("_", "-")

    if package_name is None:
        clean_artifact = artifact_id.replace("-", "").lower()
        package_name = f"{group_id}.{clean_artifact}"

    if dependencies is None:
        dependencies = []

    # Spring AI 의존성이 있으면 호환되는 Spring Boot 버전 사용
    if boot_version is None:
        if has_spring_ai_dependency(dependencies):
            boot_version = get_compatible_boot_version_for_spring_ai()
            print(f"Spring AI 의존성 감지: Spring Boot {boot_version} 사용")

            # Spring AI 버전 정보 출력
            ai_version = get_spring_ai_version(boot_version)
            if ai_version:
                print(f"Spring AI 버전: {ai_version}")
        else:
            boot_version = get_default_boot_version()
            print(f"Spring Boot 버전: {boot_version}")

    # 언어에 따른 빌드 타입 자동 결정
    build_type = get_build_type_for_language(language)

    # API 파라미터 구성
    params = {
        "type": build_type,
        "language": language,
        "bootVersion": boot_version,
        "groupId": group_id,
        "artifactId": artifact_id,
        "name": name,
        "description": description,
        "packageName": package_name,
        "javaVersion": java_version,
        "packaging": "jar",
    }

    if dependencies:
        params["dependencies"] = ",".join(dependencies)

    # URL 생성
    base_url = "https://start.spring.io/starter.zip"
    url = f"{base_url}?{urlencode(params)}"

    # 출력 경로 설정
    project_path = os.path.join(output_dir, artifact_id)
    zip_path = os.path.join(output_dir, f"{artifact_id}.zip")

    # 다운로드
    print(f"Downloading from start.spring.io...")
    download_project(url, zip_path)

    # ZIP 파일 유효성 검사
    if not validate_zip_file(zip_path):
        # 에러 내용 확인 시도
        try:
            with open(zip_path, 'r') as f:
                content = f.read(1000)
                if content.startswith('{'):
                    error_data = json.loads(content)
                    os.remove(zip_path)
                    raise RuntimeError(f"API 오류: {error_data.get('message', content)}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        os.remove(zip_path)
        raise RuntimeError("다운로드한 파일이 유효한 ZIP 파일이 아닙니다.")

    # 압축 해제
    print(f"Extracting project...")
    os.makedirs(project_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # baseDir이 포함된 경우 처리
        members = zf.namelist()

        # 모든 파일이 같은 디렉토리로 시작하는지 확인
        if members and all(m.startswith(f"{artifact_id}/") for m in members):
            # baseDir 포함 - 상위 디렉토리에 압축 해제
            zf.extractall(output_dir)
        else:
            # baseDir 미포함 - 프로젝트 디렉토리에 압축 해제
            zf.extractall(project_path)

    # zip 파일 삭제
    os.remove(zip_path)

    # application.properties → application.yml 변환
    convert_properties_to_yaml(project_path, artifact_id)

    print(f"Project created at: {project_path}")
    return project_path


# 자주 사용하는 의존성 프리셋
PRESETS = {
    "web": ["web", "validation", "devtools"],
    "web-jpa": ["web", "data-jpa", "validation", "h2", "devtools"],
    "web-api": ["web", "validation", "actuator", "devtools"],
    "web-security": ["web", "security", "validation", "devtools"],
    "full": [
        "web",
        "data-jpa",
        "security",
        "validation",
        "actuator",
        "h2",
        "devtools",
        "lombok",
    ],
    "reactive": ["webflux", "data-r2dbc", "validation", "devtools"],
    "batch": ["batch", "data-jpa", "h2", "devtools"],
    "minimal": ["devtools"],
    # AI 프리셋
    "ai-openai": ["web", "spring-ai-openai", "devtools"],
    "ai-anthropic": ["web", "spring-ai-anthropic", "devtools"],
    "ai-ollama": ["web", "spring-ai-ollama", "devtools"],
    "ai-rag": [
        "web",
        "spring-ai-openai",
        "spring-ai-vectordb-pgvector",
        "spring-ai-pdf-document-reader",
        "postgresql",
        "devtools",
    ],
}


def main():
    parser = argparse.ArgumentParser(
        description="Spring Boot 프로젝트 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
프리셋:
  minimal      - devtools만
  web          - web, validation, devtools
  web-jpa      - web, data-jpa, validation, h2, devtools
  web-api      - web, validation, actuator, devtools
  web-security - web, security, validation, devtools
  full         - web, jpa, security, validation, actuator, h2, devtools, lombok
  reactive     - webflux, data-r2dbc, validation, devtools
  batch        - batch, data-jpa, h2, devtools
  ai-openai    - web, spring-ai-openai, devtools
  ai-anthropic - web, spring-ai-anthropic, devtools
  ai-ollama    - web, spring-ai-ollama, devtools
  ai-rag       - web, spring-ai-openai, pgvector, pdf-reader, postgresql, devtools

빌드 타입 (자동 결정):
  Java   → Gradle with Groovy DSL
  Kotlin → Gradle with Kotlin DSL

예시:
  %(prog)s my-app --preset web-jpa
  %(prog)s my-app --lang kotlin --deps web,data-jpa
  %(prog)s my-app --deps web,spring-ai-openai --boot 3.5.0
  %(prog)s my-app --preset ai-rag
        """,
    )

    parser.add_argument("name", nargs="?", help="프로젝트 이름")
    parser.add_argument(
        "--group", "-g", default="com.example", help="Group ID (기본값: com.example)"
    )
    parser.add_argument("--artifact", "-a", help="Artifact ID (기본값: 프로젝트 이름)")
    parser.add_argument(
        "--desc", "-d", default="Demo project for Spring Boot", help="프로젝트 설명"
    )
    parser.add_argument("--package", "-p", help="패키지명 (기본값: groupId.artifactId)")
    parser.add_argument(
        "--boot", "-b",
        dest="boot_version",
        help="Spring Boot 버전 (예: 3.5.0). Spring AI 사용 시 자동으로 호환 버전 선택"
    )
    parser.add_argument(
        "--bootVersion",
        dest="boot_version_alt",
        help="Spring Boot 버전 (--boot의 별칭)"
    )
    parser.add_argument(
        "--java", "-j", default="21", choices=["17", "21", "23"], help="Java 버전 (기본값: 21)"
    )
    parser.add_argument(
        "--lang",
        "-l",
        default="java",
        choices=["java", "kotlin"],
        help="프로그래밍 언어 (기본값: java)",
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        help="의존성 프리셋",
    )
    parser.add_argument(
        "--deps",
        help="의존성 목록 (쉼표로 구분, 예: web,data-jpa,security)",
    )
    parser.add_argument(
        "--output", "-o", default=".", help="출력 디렉토리 (기본값: 현재 디렉토리)"
    )
    parser.add_argument(
        "--check-ai-version",
        action="store_true",
        help="Spring AI 최신 버전 정보 확인"
    )

    args = parser.parse_args()

    # Spring AI 버전 확인 모드
    if args.check_ai_version:
        print("Spring AI 버전 정보 확인 중...")
        boot_version = get_compatible_boot_version_for_spring_ai()
        ai_version = get_spring_ai_version(boot_version)
        print(f"호환 Spring Boot 버전: {boot_version}")
        print(f"Spring AI BOM 버전: {ai_version}")
        return

    # 프로젝트 생성 시 name 필수
    if not args.name:
        parser.error("프로젝트 이름이 필요합니다.")

    # boot_version 결정 (--boot 또는 --bootVersion)
    boot_version = args.boot_version or args.boot_version_alt

    # 의존성 결정
    dependencies = []
    if args.preset:
        dependencies = PRESETS[args.preset].copy()
    if args.deps:
        dependencies = args.deps.split(",")

    try:
        project_path = create_spring_boot_project(
            name=args.name,
            group_id=args.group,
            artifact_id=args.artifact,
            description=args.desc,
            package_name=args.package,
            boot_version=boot_version,
            java_version=args.java,
            language=args.lang,
            dependencies=dependencies,
            output_dir=args.output,
        )

        print(f"\n✅ 프로젝트 생성 완료: {project_path}")
        print(f"\n다음 단계:")
        print(f"  cd {project_path}")
        print(f"  ./gradlew bootRun")

    except Exception as e:
        print(f"❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
