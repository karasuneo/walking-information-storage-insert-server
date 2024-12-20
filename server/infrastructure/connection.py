import boto3
from botocore.client import BaseClient
from config import MinioEnv, PostgresEnv
from psycopg2 import connect
from psycopg2.extensions import connection


class DBConnection:
    @staticmethod
    def connect() -> connection:
        env = PostgresEnv()
        return connect(
            host=env.get_host_of_private_value(),
            port=env.get_port_of_private_value(),
            user=env.get_user_of_private_value(),
            password=env.get_password_of_private_value(),
            dbname=env.get_database_of_private_value(),
        )


class MinIOConnection:
    @staticmethod
    def connect() -> BaseClient:
        env = MinioEnv()
        return boto3.client(
            service_name=env.get_service_name_of_private_value(),
            endpoint_url=env.get_endpoint_of_private_value(),
            aws_access_key_id=env.get_access_key_of_private_value(),
            aws_secret_access_key=env.get_secret_key_of_private_value(),
            region_name=env.get_region_of_private_value(),
        )
