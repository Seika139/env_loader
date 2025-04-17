import os
from pathlib import Path
from unittest.mock import patch

import pytest

from env_loader.env_loader import get_env

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
        with pytest.raises(ValueError):
            get_env("REQUIRED_KEY", required=True)


def test_get_env_github_actions_absent(temp_env_file: Path) -> None:
    """GitHub Actions 環境変数が存在しない場合の .env ファイルからの読み込みテスト"""
    with patch.dict(os.environ, {}, clear=True):
        value = get_env("TEST_KEY", env_file=temp_env_file)
        assert value == "test_value"
        assert get_env("ANOTHER_KEY", env_file=temp_env_file) == "another_value"
        assert get_env("EMPTY_KEY", env_file=temp_env_file) == ""
        assert get_env("NON_EXISTENT_KEY", env_file=temp_env_file) is None
        assert (
            get_env("NON_EXISTENT_KEY", default="default_value", env_file=temp_env_file)
            == "default_value"
        )
        with pytest.raises(ValueError):
            get_env("REQUIRED_KEY", required=True, env_file=temp_env_file)


def test_get_env_default_env_file(tmp_path: Path) -> None:
    """デフォルトの .env ファイルからの読み込みテスト"""
    default_env_file = tmp_path / ".env"
    default_env_file.write_text("DEFAULT_KEY=default_value_from_default")
    with patch.dict(os.environ, {}, clear=True):
        # 一時的にカレントディレクトリをテスト用の tmp_path に変更
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            from dotenv import load_dotenv

            load_dotenv(dotenv_path=default_env_file)  # 明示的にパスを指定
            value = get_env("DEFAULT_KEY")
            assert value == "default_value_from_default"
        finally:
            os.chdir(original_cwd)  # 元のディレクトリに戻す


def test_get_env_required_present_github_actions() -> None:
    """required=True で GitHub Actions 環境変数が存在する場合のテスト"""
    with patch.dict(
        os.environ, {"GITHUB_ACTIONS": "true", "REQUIRED_KEY": "required_value"}
    ):
        value = get_env("REQUIRED_KEY", required=True)
        assert value == "required_value"


def test_get_env_required_present_env_file(temp_env_file: Path) -> None:
    """required=True で .env ファイルに環境変数が存在する場合のテスト"""
    value = get_env("TEST_KEY", required=True, env_file=temp_env_file)
    assert value == "test_value"
