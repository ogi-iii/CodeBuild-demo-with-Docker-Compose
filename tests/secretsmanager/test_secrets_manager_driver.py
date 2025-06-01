"""Test suite for the SecretsManagerDriver class."""

import configparser
import pytest
from secretsmanager.secrets_manager_driver import SecretsManagerDriver;

@pytest.fixture
def driver():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return SecretsManagerDriver(
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name=config.get("secretsmanager", "region_name"),
        endpoint_url=config.get("secretsmanager", "endpoint_url")
    )

def test_create_and_get_secret(driver):
    secret_id = "test-secret"
    secret_value = "super-secret-value"

    # Create secret
    create_response = driver.create_secret(secret_id, secret_value)
    assert create_response is not None
    assert create_response["Name"] == secret_id

    # Get secret value
    fetched_value = driver.get_secret_value(secret_id)
    assert fetched_value == secret_value

    # Cleanup
    driver.delete_secret(secret_id, force_delete=True)

def test_get_secret_value_not_found(driver):
    # Try to get a non-existent secret
    result = driver.get_secret_value("non-existent-secret")
    assert result is None

def test_delete_secret(driver):
    secret_id = "delete-secret"
    secret_value = "to-be-deleted"

    # Create secret
    driver.create_secret(secret_id, secret_value)

    # Delete secret
    delete_response = driver.delete_secret(secret_id, force_delete=True)
    assert delete_response is not None
    assert delete_response["Name"] == secret_id

    # Ensure secret is deleted
    result = driver.get_secret_value(secret_id)
    assert result is None

def test_list_secrets(driver):
    # Create secrets
    driver.create_secret("list-secret-1", "value1")
    driver.create_secret("list-secret-2", "value2")

    secrets = driver.list_secrets()
    assert secrets is not None
    names = [s["Name"] for s in secrets]
    assert "list-secret-1" in names
    assert "list-secret-2" in names

    # Cleanup
    driver.delete_secret("list-secret-1", force_delete=True)
    driver.delete_secret("list-secret-2", force_delete=True)
