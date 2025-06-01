"""
Secrets Manager を操作するためのモジュール。
"""

from logging import getLogger

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

class SecretsManagerDriver:
    """
    Secrets Manager Driver クラス。
    """

    def __init__(
            self,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            region_name: str,
            endpoint_url: str | None = None,
            connect_timeout = 10,
            read_timeout = 10,
            ):
        """
        Secrets Manager クライアントを初期化する。

        :param aws_access_key_id: AWS アクセスキー ID
        :param aws_secret_access_key: AWS シークレットアクセスキー
        :param region_name: Secrets Manager の接続先 AWS リージョン
        :param endpoint_url: Secrets Manager の接続先エンドポイント (default: None)
        :param connect_timeout: Secrets Manager 接続タイムアウト秒数 (default: 10)
        :param read_timeout: Secrets Manager からのデータ受信タイムアウト秒数 (default: 10)
        """
        self.client = boto3.client(
            service_name='secretsmanager',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url,
            config=Config(
                connect_timeout=connect_timeout,
                read_timeout=read_timeout
            )
        )
        self.logger = getLogger(self.__class__.__name__)

    def create_secret(
            self,
            secret_id: str,
            secret_string: str,
            ) -> dict | None:
        """
        シークレットを作成する。

        :param secret_id: シークレット ID
        :param secret_string: シークレットの値
        :return: 作成したシークレットの情報
        """
        try:
            response = self.client.create_secret(
                Name=secret_id,
                SecretString=secret_string
            )
            return response
        except ClientError as e:
            self.logger.error("Error creating secret: %s", e)
            return None

    def get_secret_value(
            self,
            secret_id: str
            ) -> str | None:
        """
        シークレットの値を取得する。

        :param secret_id: シークレット ID
        :return: シークレットの値
        """
        try:
            response = self.client.get_secret_value(
                SecretId=secret_id
            )
            secret_value = response['SecretString']
            return secret_value
        except ClientError as e:
            self.logger.error("Error retrieving secret: %s", e)
            return None

    def delete_secret(
            self,
            secret_id: str,
            force_delete=False
            ) -> dict | None:
        """
        シークレットを削除する。

        :param secret_id: シークレット ID
        :return: 削除したシークレットの情報
        """
        try:
            response = self.client.delete_secret(
                SecretId=secret_id,
                ForceDeleteWithoutRecovery=force_delete
            )
            return response
        except ClientError as e:
            self.logger.error("Error deleting secret: %s", e)
            return None

    def list_secrets(self) -> list | None:
        """
        全シークレットを一覧取得する。

        :return: 取得したシークレットのリスト
        """
        try:
            response = self.client.list_secrets()
            secrets = response['SecretList']
            return secrets
        except ClientError as e:
            self.logger.error("Error listing secrets: %s", e)
            return None
