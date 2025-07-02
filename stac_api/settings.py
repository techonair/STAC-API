from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    PROD = "PROD"
    UAT = "UAT"
    LOCAL = "LOCAL"


class Settings(BaseSettings):
    app_id: str = Field(default="APPXXXXPY", env="APP_ID")
    app_name: str = Field(default="CentientAPI", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    ENVIRONMENT: EnvironmentType = Field(default=EnvironmentType.LOCAL, env="ENVIRONMENT")
    
    @property
    def enable_swagger(self) -> bool:
        return self.ENVIRONMENT != EnvironmentType.PROD

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()