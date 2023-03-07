import json
from http import HTTPStatus

from flask import url_for

from flask_app.db import db
from flask_app.db_models import User as Users_db_model


class TestUserRolesAPI:

    def test_user_roles_get(
        self, test_client, user, role, user_role_relation, access_token_headers
    ):
        url = url_for("user_roles.user_roles", user_id=user.id)
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=access_token_headers
        )
        roles_count_in_db = len(db.session.get(Users_db_model, user.id).roles)
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == roles_count_in_db
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_user_roles_post(
        self, test_client, user, role_for_user, superuser,
            superuser_token_headers
    ):
        url = url_for("user_roles.user_roles", user_id=user.id)
        method = "post"
        status = HTTPStatus.CREATED
        roles_count_in_db_before_request = len(user.roles)
        data = {
            "role_id": role_for_user.id
        }
        response = getattr(test_client, method)(
            url, json=data, headers=superuser_token_headers
        )
        roles_count_in_db_after_request = len(user.roles)
        assert roles_count_in_db_before_request + 1 == \
               roles_count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_user_roles_delete(
            self,
            test_client,
            user,
            role,
            user_role_relation,
            superuser,
            superuser_token_headers
    ):
        url = url_for(
            "user_roles.user_roles_detail", role_id=role.id, user_id=user.id
        )
        method = "delete"
        status = HTTPStatus.OK
        roles_count_in_db_before_request = len(user.roles)
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        roles_count_in_db_after_request = len(user.roles)
        assert roles_count_in_db_before_request - 1 == \
               roles_count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
