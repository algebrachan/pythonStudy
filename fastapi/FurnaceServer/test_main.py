'''
测试文件
'''
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_base():
    response = client.get("/base")
    assert response.status_code == 200
