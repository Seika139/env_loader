"""
env_loader - GitHub ActionsとLocal環境で環境変数を簡単に扱うためのライブラリ
"""

from env_loader.env_loader import get_env, require_env

__version__ = "0.2.0"  # バージョンを直接指定
__all__ = ["get_env", "require_env", "__version__"]
