import uuid
from starlette.testclient import TestClient
import tests.data.files.file_utils


def test_ocr(client: TestClient):
    file_name = 'osintliar.com.png'
    with open(tests.data.files.file_utils.get_test_file_path(file_name), 'rb') as f:
        response = client.post('/v1/upload',
                               data=dict(
                                   ContentUuid=str(uuid.uuid4()),
                                   Cmd='pytesseract_ocr_command',
                                   ContentMimeType='image/png'
                               ),
                               files={'ContentData': (file_name, f)})
        assert response.status_code == 200
        json = response.json()
        assert 'OSINT LIAR' in json['Record']['ContentData']


def test_email(client: TestClient):
    file_name = '6e937341-bba0-4ac5-95f2-f679119bd9a5.mhtml'
    with open(tests.data.files.file_utils.get_test_file_path(file_name), 'rb') as f:
        response = client.post('/v1/upload',
                               data=dict(
                                   ContentUuid=str(uuid.uuid4()),
                                   Cmd='email_extract',
                                   ContentMimeType='message/rfc822'
                               ),
                               files={'ContentData': (file_name, f)})
        assert response.status_code == 200
        json = response.json()
        assert len(json['Record']['ContentSelectorsJson']) == 0
