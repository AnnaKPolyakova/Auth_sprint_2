import json
from http import HTTPStatus

from flask import url_for

from tests.functional.conftest import TEST_FOR_TOKEN


class TestTokensAPI:

    def test_token_get(
        self, test_client, user_for_token
    ):
        url = url_for("tokens.get_tokens")
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "login": TEST_FOR_TOKEN,
            "password": TEST_FOR_TOKEN
        }
        response = getattr(test_client, method)(url, json=data)
        assert "access" in json.loads(response.data.decode("utf-8"))
        assert "refresh" in json.loads(response.data.decode("utf-8"))
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_token_refresh(
        self, test_client, user, refresh_token_headers
    ):
        url = url_for("tokens.refresh")
        method = "post"
        status = HTTPStatus.CREATED
        response = getattr(test_client, method)(
            url, headers=refresh_token_headers
        )
        assert "access" in json.loads(response.data.decode("utf-8"))
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_logout(
        self, test_client, user, access_token_headers
    ):
        url = url_for("tokens.logout")
        method = "delete"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=access_token_headers
        )
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
