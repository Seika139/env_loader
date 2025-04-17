# env_loader

ローカルと GitHub Actions 内で環境変数の読み込みを簡易的に行うためのパッケージです。

<!-- markdownlint-disable MD033 -->

<div align="center">
  <a href="./LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/license-MIT-blue.svg">
  </a>
  <a href="https://github.com/Seika139/env_laoder/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/Seika139/env_laoder/actions/workflows/ci.yml/badge.svg">
  </a>
</div>

## Installation

poetry を利用してこのパッケージを利用する場合は以下のコマンドを実行してください。

```bash
poetry add git+https://github.com/Seika139/env_laoder.git
```

## Usage

ローカルでは `.env` ファイルを読み込み、GitHub Actions では Secrets を読み込むようになっています。
GitHub Actions では Secrets を読み込むため、`.env` ファイルは必要ありません。
引数の `env_file` を指定することで、任意のファイルを読み込むことができます。
特に、Docker や CI においては `.env` ファイルのパスが異なる場合があるため、絶対パスで指定することをお勧めします。

```python
from pathlib import Path
from env_loader.env_loader import get_env

# 環境変数を取得する
webhook_url = get_env("WEBHOOK_URL", env_file=Path(__file__).resolve().parents[1] / ".env")
```

## For Developers

See [DEVELOPMENT.md](DEVELOPMENT.md).

## How to Contribute

貢献は大歓迎です！Issue の報告や Pull Request の作成をお待ちしています。

Issue を報告する際は、具体的な状況と再現手順を記載してください。
Pull Request を作成する際は、関連する Issue を参照し、変更内容を明確に記述してください。

## Author

[Seika139](https://github.com/Seika139)
