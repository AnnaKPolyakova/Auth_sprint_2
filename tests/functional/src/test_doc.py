from http import HTTPStatus


class TestDocAPI:
    def test_doc_get(self, test_client):
        url = "http://localhost/v1/doc/redoc/"
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(url)
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
