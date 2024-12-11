
from sqlmodel import SQLModel

from .util import UUIDModel, TimestampModel
from ..util.encryptor import Encryptor


class UserBase(SQLModel):
    username: str


class UserRead(UserBase, UUIDModel):
    pass


class UserCreate(UserBase):
    password: str


class User(UserRead, TimestampModel, table=True):
    __tablename__ = "users"
    password_digest: str

    @property
    def password(self):
        return self.password_digest

    @password.setter
    def password(self, password):
        self.password_digest = Encryptor.encrypt(password)

    def password_match(self, password):
        return password == Encryptor.decrypt(self.password_digest)
