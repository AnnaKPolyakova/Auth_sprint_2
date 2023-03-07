import json
from http import HTTPStatus

from flask import url_for

from flask_app.db_models import RolePermissionRelation


class TestRolePermissionAPI:

    def test_role_permission_all_get(
            self,
            test_client, role,
            role_permission_relation,
            superuser_token_headers
    ):
        url = url_for("role_permissions.role_permissions", role_id=role.id)
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        obj_count_from_db = RolePermissionRelation.query.filter_by(
                role_id=role.id
            ).count()
        assert len(
            json.loads(response.data.decode("utf-8"))
        ) == obj_count_from_db
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_role_permission_post(
            self,
            test_client,
            superuser_token_headers,
            new_permission_for_role,
            role
    ):
        url = url_for("role_permissions.role_permissions", role_id=role.id)
        method = "post"
        status = HTTPStatus.CREATED
        data = {
            "permission_id": new_permission_for_role.id,
        }
        before_creation_count = RolePermissionRelation.query.filter_by(
                role_id=role.id
            ).count()
        response = getattr(test_client, method)(
            url, json=data, headers=superuser_token_headers
        )
        after_creation_count = RolePermissionRelation.query.filter_by(
                role_id=role.id
            ).count()
        assert after_creation_count == before_creation_count + 1, \
            f"Проверьте, что при {method} запросе {url} " \
            f"создается объект"
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"

    def test_role_permission_delete(
            self,
            test_client,
            role,
            superuser_token_headers,
            role_permission_relation
    ):
        url = url_for("roles.roles_detail", role_id=role.id)
        method = "delete"
        status = HTTPStatus.OK
        count_in_db_before_request = RolePermissionRelation.query.filter_by(
                role_id=role.id
            ).count()
        response = getattr(test_client, method)(
            url, headers=superuser_token_headers
        )
        count_in_db_after_request = RolePermissionRelation.query.filter_by(
                role_id=role.id
            ).count()
        assert count_in_db_before_request - 1 == \
               count_in_db_after_request
        assert response.status_code == status, \
            f"Проверьте, что при {method} запросе {url} " \
            f"возвращается статус {status}"
