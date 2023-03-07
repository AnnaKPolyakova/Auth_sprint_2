from pydantic import BaseModel


class SocialAuthCode(BaseModel):
    code: int

