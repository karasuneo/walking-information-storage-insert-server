import os

from dotenv import load_dotenv

load_dotenv()


class PostgresEnv:
    def __init__(
        self,
    ) -> None:
        self.__host = os.getenv("DB_HOST")
        self.__port = os.getenv("DB_PORT")
        self.__database = os.getenv("DB_NAME")
        self.__user = os.getenv("DB_USER")
        self.__password = os.getenv("DB_PASSWORD")

    def get_host_of_private_value(
        self,
    ) -> str:
        if self.__host is None:
            error_message = "DB_HOST is not set"
            raise ValueError(error_message)
        return self.__host

    def get_port_of_private_value(
        self,
    ) -> str:
        if self.__port is None:
            error_message = "DB_PORT is not set"
            raise ValueError(error_message)
        return self.__port

    def get_database_of_private_value(
        self,
    ) -> str:
        if self.__database is None:
            error_message = "DB_NAME is not set"
            raise ValueError(error_message)
        return self.__database

    def get_user_of_private_value(
        self,
    ) -> str:
        if self.__user is None:
            error_message = "DB_USER is not set"
            raise ValueError(error_message)
        return self.__user

    def get_password_of_private_value(
        self,
    ) -> str:
        if self.__password is None:
            error_message = "DB_PASSWORD is not set"
            raise ValueError(error_message)
        return self.__password


class MinioEnv:
    def __init__(
        self,
    ) -> None:
        self.__service_name = "s3"
        self.__endpoint = os.getenv("MINIO_ENDPOINT")
        self.__access_key = os.getenv("MINIO_ACCESS_KEY")
        self.__secret_key = os.getenv("MINIO_SECRET_KEY")
        self.__region = os.getenv("MINIO_REGION")

    def get_service_name_of_private_value(
        self,
    ) -> str:
        if self.__service_name is None:
            error_message = "MINIO_SERVICE_NAME is not set"
            raise ValueError(error_message)
        return self.__service_name

    def get_endpoint_of_private_value(
        self,
    ) -> str:
        if self.__endpoint is None:
            error_message = "MINIO_ENDPOINT is not set"
            raise ValueError(error_message)
        return self.__endpoint

    def get_access_key_of_private_value(
        self,
    ) -> str:
        if self.__access_key is None:
            error_message = "MINIO_ACCESS_KEY is not set"
            raise ValueError(error_message)
        return self.__access_key

    def get_secret_key_of_private_value(
        self,
    ) -> str:
        if self.__secret_key is None:
            error_message = "MINIO_SECRET_KEY is not set"
            raise ValueError(error_message)
        return self.__secret_key

    def get_region_of_private_value(
        self,
    ) -> str:
        if self.__region is None:
            error_message = "MINIO_REGION is not set"
            raise ValueError(error_message)
        return self.__region
