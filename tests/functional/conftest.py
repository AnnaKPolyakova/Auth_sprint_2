import pytest
import sqlalchemy
from flask_jwt_extended import (
    create_access_token, JWTManager, create_refresh_token
)
from sqlalchemy import create_engine, text

from flask_app.app import create_app
from flask_app.db_init import db as _db
from flask_app.settings import settings
from tests.functional.settings import test_settings
from tests.functional.utils.factory import UserFactory, PermissionFactory, \
    LoginHistoryFactory, RoleFactory, UserRoleRelationFactory, \
    RolePermissionRelationFactory

USERS_COUNT = 2
TEST_FOR_TOKEN = "test_for_token"


def get_connect(postgres_db):
    uri_template = "postgresql://{username}:{password}@{host}/{database_name}"
    uri = uri_template.format(
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        database_name=postgres_db,
    )
    db = create_engine(uri, isolation_level='AUTOCOMMIT')
    connect = db.connect()
    connect.execution_options(autocommit=False)
    return db, connect


@pytest.fixture(scope='session', autouse=True)
def test_db():
    db, connect = get_connect(settings.POSTGRES_DB)
    try:
        connect.execute(
            text(f"CREATE DATABASE {test_settings.POSTGRES_DB_TEST}")
        )
    except sqlalchemy.exc.ProgrammingError:
        pass
    db, connect = get_connect(test_settings.POSTGRES_DB_TEST)
    yield db
    _db.drop_all()


@pytest.fixture(scope='session', autouse=True)
def test_app(test_db):
    app = create_app(test_settings)
    app.config['SERVER_NAME'] = "localhost"
    yield app


@pytest.fixture(scope='session', autouse=True)
def test_jwt(test_app):
    yield JWTManager(test_app)


@pytest.fixture(scope='session')
def test_client(test_db, test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


@pytest.fixture()
def users(test_db, test_app):
    users = UserFactory.create_batch(USERS_COUNT)
    return users


@pytest.fixture()
def user(test_db, test_app):
    user = UserFactory(password="test")
    return user


@pytest.fixture()
def user_for_token(test_db, test_app):
    user = UserFactory(login=TEST_FOR_TOKEN, password=TEST_FOR_TOKEN)
    return user


@pytest.fixture()
def superuser(test_db, test_app):
    user = UserFactory(is_superuser=True)
    return user


@pytest.fixture()
def token_refresh(test_db, test_app, user):
    refresh_token = create_refresh_token(identity=user.id)
    return refresh_token


@pytest.fixture()
def token_access(test_db, test_app, user):
    access_token = create_access_token(identity=user.id)
    return access_token


@pytest.fixture()
def access_token_headers(test_db, test_app, user, token_access):
    return {"Authorization": f"Bearer {token_access}"}


@pytest.fixture()
def refresh_token_headers(test_db, test_app, user, token_refresh):
    return {"Authorization": f"Bearer {token_refresh}"}


@pytest.fixture()
def superuser_token_headers(test_db, test_app, superuser):
    access_token = create_access_token(identity=superuser.id),
    return {"Authorization": f"Bearer {access_token[0]}"}


@pytest.fixture()
def login_histories(test_db, test_app, user):
    return LoginHistoryFactory.create_batch(size=15, user_id=user.id)


@pytest.fixture()
def permission(test_db, test_app):
    return PermissionFactory()


@pytest.fixture()
def new_permission_for_role(test_db, test_app):
    return PermissionFactory()


@pytest.fixture()
def role(test_db, test_app):
    role = RoleFactory()
    return role


@pytest.fixture()
def roles(test_db, test_app):
    roles = RoleFactory.create_batch(10)
    return roles


@pytest.fixture()
def role_for_user(test_db, test_app):
    role = RoleFactory()
    return role


@pytest.fixture()
def user_role_relation(test_db, test_app, user, role):
    _db.session.commit()
    return UserRoleRelationFactory(user_id=user.id, role_id=role.id)


@pytest.fixture()
def role_permission_relation(test_db, test_app, permission, role):
    _db.session.commit()
    return RolePermissionRelationFactory(
        permission_id=permission.id, role_id=role.id
    )
