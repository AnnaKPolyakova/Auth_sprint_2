import json
from http import HTTPStatus

from flask import url_for

from flask_app.db_models import Role


class TestRolesAPI:

    def test_roles_get(self, test_client, roles, superuser_token_headers):
        url = url_for("roles.roles")
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        roles_count_in_db = Role.query.count()
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == roles_count_in_db
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_roles_post(self, test_client, roles, superuser_token_headers):
        url = url_for("roles.roles")
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "name": "test1",
            "description": "test1"
        }
        roles_count_in_db_before_request = Role.query.count()
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers, json=data
        )
        roles_count_in_db_after_request = Role.query.count()
        assert roles_count_in_db_before_request + 1 == \
               roles_count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_roles_patch(self, test_client, role, superuser_token_headers):
        url = url_for("roles.roles_detail", role_id=role.id)
        method = "patch"
        status = HTTPStatus.OK
        data = {
            "name": "test2",
            "description": "test2"
        }
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers, json=data
        )
        assert role.name == "test2"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_roles_delete(self, test_client, role, superuser_token_headers):
        url = url_for("roles.roles_detail", role_id=role.id)
        method = "delete"
        status = HTTPStatus.OK
        roles_count_in_db_before_request = Role.query.count()
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        roles_count_in_db_after_request = Role.query.count()
        assert roles_count_in_db_before_request - 1 == \
               roles_count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
