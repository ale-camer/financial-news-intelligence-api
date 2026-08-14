from fastapi.testclient import TestClient

from src.api.main import create_app


def test_process_time_header_present() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers


def test_global_exception_handler() -> None:
    app = create_app()

    @app.get("/test-error")
    def raise_error() -> None:
        raise ValueError("Simulated unexpected crash")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/test-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal Server Error",
        "error_code": "INTERNAL_SERVER_ERROR",
    }
