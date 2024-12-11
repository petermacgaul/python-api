from sqlmodel import SQLModel
from .util import UUIDModel, TimestampModel
from ..util.encryptor import Encryptor


class DatabaseBase(SQLModel):

    @property
    def db_name(self):
        return "testdb"

    def url(self) -> str:
        return f"mysql+asyncmy://{self.username}:{self.password}@{self.host}:{self.port}"


class DatabaseCreate(DatabaseBase):
    host: str
    port: int
    username: str
    password: str


class DatabaseRead(DatabaseBase, UUIDModel):
    pass


class Database(DatabaseRead, TimestampModel, table=True):
    __tablename__ = "databases"

    host_digest: str
    port_digest: str
    username_digest: str
    password_digest: str

    @property
    def username(self):
        return Encryptor.decrypt(self.username_digest)

    @username.setter
    def username(self, username):
        self.username_digest = Encryptor.encrypt(username)

    @property
    def password(self):
        return Encryptor.decrypt(self.password_digest)

    @password.setter
    def password(self, password):
        self.password_digest = Encryptor.encrypt(password)

    @property
    def host(self):
        return Encryptor.decrypt(self.host_digest)

    @host.setter
    def host(self, host):
        self.host_digest = Encryptor.encrypt(host)

    @property
    def port(self) -> int:
        return int(Encryptor.decrypt(self.port_digest))

    @port.setter
    def port(self, port: int):
        self.port_digest = Encryptor.encrypt(str(port))
