from typing import Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(TokenBase):
    cn: Optional[str]
    display_name: Optional[str]
    mail: Optional[str]
    user_principal_name: Optional[str]


class JWTBase(BaseModel):
    username: str
    exp: str


class AccessTokenClaims(JWTBase):
    group: str


class RefreshRequest(BaseModel):
    refresh_token: str
