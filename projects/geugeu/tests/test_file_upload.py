"""파일 업로드 관련 테스트"""

import io
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.utils import upload_file


def test_upload_file_no_filename():
    """파일 이름이 없는 경우 테스트"""
    # given
    mock_file = MagicMock()
    mock_file.filename = None
    
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        upload_file(mock_file)
    
    assert exc_info.value.status_code == 400
    assert "File is required" in exc_info.value.detail


def test_upload_file_empty_filename():
    """빈 파일 이름인 경우 테스트"""
    # given
    mock_file = MagicMock()
    mock_file.filename = ""
    
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        upload_file(mock_file)
    
    assert exc_info.value.status_code == 400
    assert "File is required" in exc_info.value.detail


@patch('app.utils.httpx.put')
@patch('app.utils._generate_presigned_url')
def test_upload_file_s3_upload_failure(mock_presigned_url, mock_put):
    """S3 업로드 실패 테스트"""
    # given
    mock_file = MagicMock()
    mock_file.filename = "test.jpg"
    mock_file.file.read.return_value = b"test image data"
    
    mock_presigned_url.return_value = "https://test-presigned-url.com"
    mock_put.return_value.status_code = 500  # S3 업로드 실패
    mock_put.return_value.text = "Internal Server Error"
    
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        upload_file(mock_file)
    
    assert exc_info.value.status_code == 500
    assert "Failed to upload profile image" in exc_info.value.detail


@patch('app.utils.httpx.put')
@patch('app.utils._generate_presigned_url')
def test_upload_file_success(mock_presigned_url, mock_put):
    """파일 업로드 성공 테스트"""
    # given
    mock_file = MagicMock()
    mock_file.filename = "test.jpg"
    mock_file.file.read.return_value = b"test image data"
    
    mock_presigned_url.return_value = "https://test-presigned-url.com"
    mock_put.return_value.status_code = 200  # S3 업로드 성공
    
    # when
    result_url = upload_file(mock_file)
    
    # then
    assert result_url.startswith("https://")
    assert "images/" in result_url
    assert ".jpg" in result_url


def test_profile_image_upload(client, authorized_user):
    """프로필 이미지 업로드 테스트"""
    with patch('app.services.users.upload_file') as mock_upload:
        mock_upload.return_value = "https://test-bucket.s3.amazonaws.com/images/test.jpg"
        
        # when
        response = client.put(
            "/api/users/me/profile-image",
            files={"file": ("test.jpg", io.BytesIO(b"test image"), "image/jpeg")}
        )
        
        # then
        assert response.status_code == 200
        assert response.json()["profile_image_url"] == "https://test-bucket.s3.amazonaws.com/images/test.jpg"


def test_profile_image_upload_unauthorized(client, user):
    """인증되지 않은 사용자의 프로필 이미지 업로드 테스트"""
    # when
    response = client.put(
        "/api/users/me/profile-image",
        files={"file": ("test.jpg", io.BytesIO(b"test image"), "image/jpeg")}
    )
    
    # then
    assert response.status_code == 401
