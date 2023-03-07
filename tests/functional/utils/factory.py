import random
import uuid

from flask_app.db_init import db as _db
import factory

from flask_app.db_models import User, Permission, LoginHistory, Role, \
    UserRoleRelation, RolePermissionRelation


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = _db.session
        exclude = ["name"]

    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    name = factory.Faker("first_name", locale="en_US")
    login = factory.LazyAttribute(
        lambda a: "{}.{}".format(a.name, random.random())
    )
    email = factory.LazyAttribute(
        lambda a: "{}@auth.com".format(a.login).lower()
    )
    password = factory.PostGenerationMethodCall("set_password", "test")
    is_superuser = False
    create_at = factory.Faker("date_time_this_year", before_now=True)


class PermissionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Permission
        sqlalchemy_session = _db.session
        exclude = ["word"]

    word = factory.Faker("word", locale="en_US")
    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    name = factory.LazyAttribute(
        lambda a: "{}.{}".format(a.word, random.random())
    )
    description = factory.Faker("sentence", locale="en_US", nb_words=5)
    model = factory.LazyAttribute(lambda a: 'test')
    action = factory.LazyAttribute(lambda a: 'test')
    create_at = factory.Faker("date_time_this_year", before_now=True)


class LoginHistoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = LoginHistory
        sqlalchemy_session = _db.session

    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    user_id = factory.SubFactory(UserFactory)
    create_at = factory.Faker("date_time_this_year", before_now=True)


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = _db.session
        exclude = ["word"]

    word = factory.Faker("word", locale="en_US")
    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    name = factory.LazyAttribute(
        lambda a: "{}.{}".format(a.word, random.random())
    )
    description = factory.Faker("sentence", locale="en_US", nb_words=5)
    create_at = factory.Faker("date_time_this_year", before_now=True)


class UserRoleRelationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserRoleRelation
        sqlalchemy_session = _db.session

    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    user_id = factory.SubFactory(UserFactory)
    role_id = factory.SubFactory(RoleFactory)
    create_at = factory.Faker("date_time_this_year", before_now=True)


class RolePermissionRelationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RolePermissionRelation
        sqlalchemy_session = _db.session

    id = factory.LazyAttribute(lambda a: uuid.uuid4())
    permission_id = factory.SubFactory(PermissionFactory)
    role_id = factory.SubFactory(RoleFactory)
    create_at = factory.Faker("date_time_this_year", before_now=True)
