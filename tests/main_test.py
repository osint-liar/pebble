import uuid
from starlette.testclient import TestClient
import tests.data.files.file_utils


def test_ocr(client: TestClient):
    file_name = 'osintliar.com.png'
    with open(tests.data.files.file_utils.get_test_file_path(file_name), 'rb') as f:
        response = client.post('/v1/upload',
                               data=dict(ContentUuid=str(uuid.uuid4()), Cmd='pytesseract_ocr_command'),
                               files={'ContentData': (file_name, f)})
        assert response.status_code == 200
        json = response.json()
        t = json

def test_email(client: TestClient):
    file_name = 'osintliar.com.png'
    with open(tests.data.files.file_utils.get_test_file_path(file_name), 'rb') as f:
        response = client.post('/v1/upload',
                               data=dict(ContentUuid=str(uuid.uuid4()), Cmd='pytesseract_ocr_command'),
                               files={'ContentData': (file_name, f)})
        assert response.status_code == 200
        json = response.json()
        t = json