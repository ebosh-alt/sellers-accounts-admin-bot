from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from config.settings.base import ConfigBase


class TelegramBotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_bot_")
    token: str


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")
    dbms: str
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def link_connect(self):
        return f"{self.dbms}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class ManagerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="manager_")
    seller_id: int


class AdminConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="admin_")
    ids: Annotated[list[int], NoDecode]
    main_id: int

    @field_validator("ids", mode="before")
    def decode_numbers(cls, v: str) -> list[int]:
        return [int(x) for x in v.split(",")]


class ProjectConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="project_")
    name: str
    link_manager_panel: str
    manager_panel_signing_key: str


class Config(BaseSettings):
    telegram_bot: TelegramBotConfig = Field(default_factory=TelegramBotConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    manager: ManagerConfig = Field(default_factory=ManagerConfig)
    admin: AdminConfig = Field(default_factory=AdminConfig)
    project: ProjectConfig = Field(default_factory=ProjectConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
