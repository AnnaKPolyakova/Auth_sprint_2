from typing import Union

from pydantic import BaseModel


class SocialAuthCode(BaseModel):
    code: Union[int, str]

