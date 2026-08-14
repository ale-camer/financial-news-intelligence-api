from pathlib import Path


def test_dockerfile_exists_and_valid_directives() -> None:
    dockerfile_path = Path(__file__).parent.parent.parent / "infra" / "docker" / "Dockerfile"
    assert dockerfile_path.exists(), "infra/docker/Dockerfile does not exist"

    content = dockerfile_path.read_text(encoding="utf-8")
    assert "FROM python:3.14-slim AS builder" in content
    assert "FROM python:3.14-slim AS runner" in content
    assert "USER appuser" in content
    assert "EXPOSE 8000" in content
    assert "uvicorn" in content


def test_docker_compose_exists_and_valid_services() -> None:
    compose_path = Path(__file__).parent.parent.parent / "docker-compose.yml"
    assert compose_path.exists(), "docker-compose.yml does not exist"

    content = compose_path.read_text(encoding="utf-8")
    assert "financial-news-api" in content
    assert "financial-news-mongodb" in content
    assert "financial-news-redis" in content
    assert "financial-news-kafka" in content
