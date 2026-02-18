from pydantic_settings import BaseSettings , SettingsConfigDict
import os

class Settings(BaseSettings):
    DB_HOSTNAME : str
    DB_PORT : str
    DB_PASSWORD : str
    DB_NAME : str
    DB_USERNAME :str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXP_TIME_MINUTES : int  

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), ".env"),
        extra="ignore"
    )

settings = Settings()


# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_HOSTNAME : str
#     DB_PORT : str
#     DB_PASSWORD : str
#     DB_NAME : str
#     DB_USERNAME :str
#     SECRET_KEY : str
#     ALGORITHM : str
#     ACCESS_TOKEN_EXP_TIME_MINUTES : int  

#     class Config:
#         env_file = ".env"

# Setting = Settings()