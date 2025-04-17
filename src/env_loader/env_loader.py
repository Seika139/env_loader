import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv


def get_env(
    key: str,
    default: Optional[str] = None,
    required: bool = False,
    env_file: Optional[Union[str, Path]] = None,
) -> Optional[str]:
    """
    環境変数を取得します。GitHub Actions 環境またはローカルの .env ファイルから読み込みます。

    Args:
        key: 環境変数のキー。
        default: 環境変数が存在しない場合のデフォルト値 (省略可能)。
        required: 環境変数が必須かどうか (True の場合、存在しなければ ValueError を発生)。
        env_file: .env ファイルのパス (省略可能。指定しない場合はデフォルトの場所を探す)。

    Returns:
        環境変数の値 (文字列) または default 値。
        required=False かつ環境変数が存在しない場合は None。

    Raises:
        ValueError: required=True かつ環境変数が存在しない場合。
    """
    if not os.getenv("GITHUB_ACTIONS"):
        if env_file:
            load_dotenv(dotenv_path=env_file)
        else:
            load_dotenv()

    value = os.getenv(key)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{key}' not found.")
        return default

    return value
