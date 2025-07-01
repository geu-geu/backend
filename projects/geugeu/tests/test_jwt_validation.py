"""JWT 토큰 검증 관련 테스트"""

from fastapi.testclient import TestClient


def test_invalid_token_format(client: TestClient, user):
    """잘못된 토큰 형식 테스트"""
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "InvalidTokenFormat"}
    )
    
    # then
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]


def test_invalid_token_type(client: TestClient, user):
    """잘못된 토큰 타입 테스트"""
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "InvalidType jwt_token_here"}
    )
    
    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_missing_authorization_header(client: TestClient, user):
    """Authorization 헤더 누락 테스트"""
    # when
    response = client.get("/api/users/me")
    
    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_empty_authorization_header(client: TestClient, user):
    """빈 Authorization 헤더 테스트"""
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": ""}
    )
    
    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_malformed_jwt_token(client: TestClient, user):
    """형식이 잘못된 JWT 토큰 테스트"""
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    
    # then
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]


def test_expired_jwt_token(client: TestClient, user):
    """만료된 JWT 토큰 테스트"""
    import jwt
    from datetime import datetime, timedelta, UTC
    from app.core.config import settings
    
    # 이미 만료된 토큰 생성
    expired_payload = {
        "sub": user.code,
        "exp": datetime.now(UTC) - timedelta(hours=1)  # 1시간 전에 만료
    }
    expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm="HS256")
    
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    # then
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]


def test_token_with_invalid_user_code(client: TestClient, user):
    """존재하지 않는 사용자 코드를 가진 토큰 테스트"""
    import jwt
    from datetime import datetime, timedelta, UTC
    from app.core.config import settings
    
    # 존재하지 않는 사용자 코드로 토큰 생성
    invalid_payload = {
        "sub": "non_existent_user_code",
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    invalid_token = jwt.encode(invalid_payload, settings.SECRET_KEY, algorithm="HS256")
    
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    
    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_token_with_no_sub_claim(client: TestClient, user):
    """sub 클레임이 없는 토큰 테스트"""
    import jwt
    from datetime import datetime, timedelta, UTC
    from app.core.config import settings
    
    # sub 클레임이 없는 토큰 생성
    no_sub_payload = {
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    no_sub_token = jwt.encode(no_sub_payload, settings.SECRET_KEY, algorithm="HS256")
    
    # when
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {no_sub_token}"}
    )
    
    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
