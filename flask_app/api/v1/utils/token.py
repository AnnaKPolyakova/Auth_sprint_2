from flask_jwt_extended import create_access_token, create_refresh_token


def get_tokens_for_user(user):
    return {
        "access": create_access_token(identity=user.id),
        "refresh": create_refresh_token(identity=user.id),
    }


def get_access_tokens(identity):
    return {
        "access": create_access_token(identity=identity),
    }
