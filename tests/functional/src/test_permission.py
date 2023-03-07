import json
from http import HTTPStatus

from flask import url_for

from flask_app.db_models import Permission


class TestPermissionAPI:

    def test_permission_all_get(
            self,
            test_client, role,
            permission,
            superuser_token_headers
    ):
        url = url_for("permissions.permissions")
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        obj_count_from_db = Permission.query.count()
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == obj_count_from_db
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_permission_post(
            self,
            test_client,
            superuser_token_headers,
    ):
        url = url_for("permissions.permissions")
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "name": "test3",
            "description": "test3",
            "model": "test3",
            "action": "test3",
        }
        obj_count_before_creation = Permission.query.count()
        response = getattr(test_client, method)(
            url, json=data, headers=superuser_token_headers
        )
        obj_count_after_creation = Permission.query.count()
        assert obj_count_after_creation == obj_count_before_creation + 1, \
            f"Проверьте, что при {method} запросе {url} " \
            f"создается объект"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_permission_delete(
            self,
            test_client,
            permission,
            superuser_token_headers,
    ):
        url = url_for(
            "permissions.permission_detail", permission_id=permission.id
        )
        method = "delete"
        status = HTTPStatus.OK
        count_in_db_before_request = Permission.query.count()
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        count_in_db_after_request = Permission.query.count()
        assert count_in_db_before_request - 1 == \
               count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
