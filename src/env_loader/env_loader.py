import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv


def get_env(
    key: str,
    default: Optional[str] = None,
    env_file: Optional[Union[str, Path]] = None,
) -> Optional[str]:
    """
    環境変数を取得します。GitHub Actions 環境またはローカルの .env ファイルから読み込みます。

    Args:
        key: 環境変数のキー。
        default: 環境変数が存在しない場合のデフォルト値 (省略可能)。
        env_file: .env ファイルのパス (省略可能。指定しない場合はデフォルトの場所を探す)。

    Returns:
        環境変数の値 (文字列) または default 値。
        環境変数が存在しない場合は None。
    """
    if not os.getenv("GITHUB_ACTIONS"):
        if env_file:
            load_dotenv(dotenv_path=env_file)
        else:
            load_dotenv()

    return os.getenv(key, default)


def require_env(
    key: str,
    env_file: Optional[Union[str, Path]] = None,
) -> str:
    """
    必須の環境変数を取得します。GitHub Actions 環境またはローカルの .env ファイルから読み込みます。

    Args:
        key: 環境変数のキー。
        env_file: .env ファイルのパス (省略可能。指定しない場合はデフォルトの場所を探す)。

    Returns:
        環境変数の値 (文字列)。

    Raises:
        ValueError: 環境変数が存在しない場合。
    """
    value = get_env(key, env_file=env_file)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' not found.")
    return value
