import os
from pathlib import Path
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from env_loader.env_loader import get_env, require_env

# テスト用の .env ファイルの内容
TEST_ENV_CONTENT = """
TEST_KEY=test_value
ANOTHER_KEY=another_value
EMPTY_KEY=
"""


@pytest.fixture
def temp_env_file(tmp_path: Path) -> Path:
    """一時的な .env ファイルを作成するフィクスチャ"""
    env_file = tmp_path / ".env_test"
    env_file.write_text(TEST_ENV_CONTENT)
    return env_file


def test_get_env_github_actions_present() -> None:
    """GitHub Actions 環境変数が存在する場合のテスト"""
    with patch.dict(
        os.environ, {"GITHUB_ACTIONS": "true", "ACTION_INPUT_MY_KEY": "github_value"}
    ):
        value = get_env("ACTION_INPUT_MY_KEY")
        assert value == "github_value"
        assert get_env("NON_EXISTENT_KEY") is None
        assert get_env("NON_EXISTENT_KEY", default="default_value") == "default_value"


def test_get_env_github_actions_absent(temp_env_file: Path) -> None:
    """GitHub Actions 環境変数が存在しない場合の .env ファイルからの読み込みテスト"""
    with patch.dict(os.environ, {}, clear=True):
        load_dotenv(dotenv_path=str(temp_env_file))  # 絶対パスを文字列として渡す
        value = get_env("TEST_KEY")
        assert value == "test_value"
        assert get_env("ANOTHER_KEY") == "another_value"
        assert get_env("EMPTY_KEY") == ""
        assert get_env("NON_EXISTENT_KEY") is None
        assert get_env("NON_EXISTENT_KEY", default="default_value") == "default_value"


def test_get_env_default_env_file(tmp_path: Path) -> None:
    """デフォルトの .env ファイルからの読み込みテスト"""
    default_env_file = tmp_path / ".env"
    default_env_file.write_text("DEFAULT_KEY=default_value_from_default")
    with patch.dict(os.environ, {}, clear=True):
        load_dotenv(dotenv_path=str(default_env_file))  # 絶対パスを文字列として渡す
        value = get_env("DEFAULT_KEY")
        assert value == "default_value_from_default"


def test_require_env_present_github_actions() -> None:
    """require_env で GitHub Actions 環境変数が存在する場合のテスト"""
    with patch.dict(
        os.environ, {"GITHUB_ACTIONS": "true", "REQUIRED_KEY": "required_value"}
    ):
        value = require_env("REQUIRED_KEY")
        assert value == "required_value"


def test_require_env_present_env_file(temp_env_file: Path) -> None:
    """require_env で .env ファイルに環境変数が存在する場合のテスト"""
    with patch.dict(os.environ, {}, clear=True):
        load_dotenv(dotenv_path=str(temp_env_file))  # 絶対パスを文字列として渡す
        value = require_env("TEST_KEY")
        assert value == "test_value"


def test_require_env_missing() -> None:
    """require_env で環境変数が存在しない場合のテスト"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            require_env("NON_EXISTENT_KEY")
        assert (
            str(exc_info.value)
            == "Required environment variable 'NON_EXISTENT_KEY' not found."
        )
