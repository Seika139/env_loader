# env_loader

ローカルと GitHub Actions 上で環境変数を使用する際に便利なライブラリです。
GitHub Actions 環境ならば Secrets に保存している環境変数を優先し、それ以外の環境では `.env` ファイルなどの環境変数用のファイルを読み込みます。

<!-- markdownlint-disable MD029 MD033 -->

<div align="center">
  <a href="./LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/license-MIT-blue.svg">
  </a>
  <a href="https://github.com/Seika139/env_loader/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/Seika139/env_loader/actions/workflows/ci.yml/badge.svg">
  </a>
</div>

## インストール方法

### Poetry を使用する場合（推奨）

```bash
# 最新バージョンをインストール
poetry add git+https://github.com/Seika139/env_loader.git

# 特定のバージョンをインストール（例: v0.2.0）
poetry add git+https://github.com/Seika139/env_loader.git@v0.2.0
```

### pip を使用する場合

```bash
# 最新バージョンをインストール
pip install git+https://github.com/Seika139/env_loader.git

# 特定のバージョンをインストール（例: v0.2.0）
pip install git+https://github.com/Seika139/env_loader.git@v0.2.0
```

## 基本的な使い方

### 1. プロジェクトの設定

#### ローカル環境での設定

1. プロジェクトのルートディレクトリに `.env` ファイルを作成します：

```dotenv
# .env
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
API_KEY=your-secret-api-key
DEBUG=true
```

2. `.gitignore` に `.env` を追加して、秘密情報が Git リポジトリにコミットされないようにします：

```gitignore
.env
```

#### GitHub Actions での設定

1. GitHub リポジトリの Settings > Secrets and variables > Actions で環境変数を設定します
2. 同じ変数名（例：`DATABASE_URL`, `API_KEY`）を使用して設定します

### 2. コードでの使用方法

```python
from pathlib import Path
from env_loader import get_env, require_env

# プロジェクトルートディレクトリの .env を指定（推奨）
env_path = Path(__file__).resolve().parents[1] / ".env"

# オプションの環境変数を取得
debug = get_env("DEBUG", default="false", env_file=env_path)
database_url = get_env("DATABASE_URL", env_file=env_path)

# 必須の環境変数を取得（存在しない場合はエラー）
api_key = require_env("API_KEY", env_file=env_path)
```

### API リファレンス

#### `get_env(key: str, default: Optional[str] = None, env_file: Optional[Union[str, Path]] = None) -> Optional[str]`

環境変数を取得します。存在しない場合は `default` 値または `None` を返します。

- **引数**:
  - `key`: 環境変数のキー
  - `default`: 環境変数が存在しない場合のデフォルト値（省略可能）
  - `env_file`: .env ファイルのパス（省略可能）
- **戻り値**:
  - 環境変数の値、または `default` 値、または `None`

#### `require_env(key: str, env_file: Optional[Union[str, Path]] = None) -> str`

必須の環境変数を取得します。存在しない場合は `ValueError` を発生させます。

- **引数**:
  - `key`: 環境変数のキー
  - `env_file`: .env ファイルのパス（省略可能）
- **戻り値**:
  - 環境変数の値
- **例外**:
  - `ValueError`: 環境変数が存在しない場合

### 高度な使用例

#### 異なる環境ファイルの使用

```python
from env_loader import get_env

# 開発環境用の設定
dev_env = get_env("API_KEY", env_file=".env.development")

# テスト環境用の設定
test_env = get_env("API_KEY", env_file=".env.test")
```

#### GitHub Actions でのワークフロー例

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: pip install git+https://github.com/Seika139/env_loader.git

      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: python deploy_script.py
```

## 開発者向け情報

詳細な開発情報については [DEVELOPMENT.md](DEVELOPMENT.md) を参照してください。

## Contributing

貢献は大歓迎です！Issue の報告や Pull Request の作成をお待ちしています。

Issue を報告する際は、具体的な状況と再現手順を記載してください。
Pull Request を作成する際は、関連する Issue を参照し、変更内容を明確に記述してください。

## License

[MIT License](LICENSE)

## Author

[Seika139](https://github.com/Seika139)
