import json
from http import HTTPStatus

from flask import url_for

from flask_app.db_models import User as Users_db_model
from flask_app.settings import settings


class TestUsersAPI:
    def test_user_all_get(
        self, test_client, users
    ):
        url = url_for("users.users")
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(url)
        users_count_from_db = Users_db_model.query.count()
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == users_count_from_db
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_user_post(self, test_client, users):
        url = url_for("users.users")
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "login": "test",
            "email": "test@test.ru",
            "password": "test"
        }
        before_creation_count = Users_db_model.query.count()
        response = getattr(test_client, method)(url, json=data)
        after_creation_count = Users_db_model.query.count()
        assert after_creation_count == before_creation_count + 1, \
            f"Проверьте, что при {method} запросе {url} " \
            f"создается объект"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_user_patch(self, test_client, user, access_token_headers):
        url = url_for("users.users_detail", user_id=user.id)
        method = "patch"
        status = HTTPStatus.OK
        data = {
            "login": "test2",
            "email": "test2@test.ru",
            "password": "test2"
        }
        response = getattr(test_client, method)(
            url, json=data, headers=access_token_headers
        )
        assert user.login == "test2", \
            f"Проверьте, что при {method} запросе {url} " \
            f"создается объект"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_check_permission(self, test_client, permission, user):
        url = url_for("users.check_permission", user_id=user.id)
        method = "post"
        status = HTTPStatus.OK
        data = {"permission_id": permission.id}
        response = getattr(test_client, method)(url, json=data)
        assert type(
            json.loads(response.data.decode("utf-8"))["result"]
        ) == bool, f"Проверьте ответ при {method} запросе {url}"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_create_is_superuser(self, test_client, superuser,
                                 superuser_token_headers):
        url = url_for("users.create_is_superuser")
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "login": "test3",
            "email": "test3@test.ru",
            "password": "test3"
        }
        response = getattr(test_client, method)(
            url, json=data, headers=superuser_token_headers
        )
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
        assert json.loads(
            response.data.decode("utf-8")
        )["is_superuser"] is True

    def test_login_history(
            self, test_client, user, access_token_headers, login_histories
    ):
        url = url_for("users.histories_get")
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=access_token_headers)
        test_client.get(
            url, headers=access_token_headers
        )
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == settings.PAGE_SIZE
