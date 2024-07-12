from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic.networks import PostgresDsn


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_", case_sensitive=False)

    pg_hostname: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "postgres"
    pg_password: str = "postgres"
    pg_db_name: str = "temp_db"

    @property
    def db_dsn(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.pg_username,
            password=self.pg_password,
            host=self.pg_hostname,
            port=self.pg_port,
            path=self.pg_db_name,
        )
        return str(dsn)
