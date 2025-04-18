# env_loader

ローカルと GitHub Actions 上で環境変数を使用する際に便利なライブラリです。
GitHub Actions 環境ならば Secrets に保存している環境変数を優先し、それ以外の環境では `.env` ファイルなどの環境変数用のファイルを読み込みます。

<!-- markdownlint-disable MD033 -->

<div align="center">
  <a href="./LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/license-MIT-blue.svg">
  </a>
  <a href="https://github.com/Seika139/env_loader/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/Seika139/env_loader/actions/workflows/ci.yml/badge.svg">
  </a>
</div>

## Installation

poetry で管理しているプロジェクトであれば、以下のコマンドを実行することでインストールできます。

```bash
poetry add git+https://github.com/Seika139/env_loader.git
```

## Usage

### Use in Local Environment

ローカル環境であればあなたのプロジェクトに `.env` ファイルがあることを前提としています。
`.env` ファイルは、環境変数を定義するためのファイルです。

`.env` ファイルの例:

```dotenv
WEBHOOK_URL=https://example.com/webhook
```

### Use in GitHub Actions

GitHub Actions 上で利用する場合は Secrets に環境変数を事前に登録しておく必要があります。

上記の `.env` ファイルを例にすると、GitHub の設定から Secrets を選択し、キーが `WEBHOOK_URL` で値が `https://example.com/webhook` の環境変数を登録します。この時、値に改行を含んだ状態で登録すると、改行が含まれた状態で取得されてしまうため、注意が必要です。

### Read Environment Variables in Python

環境変数を Python で読み込むには、以下のようにします。

```python
from pathlib import Path
from env_loader.env_loader import get_env

webhook_url = get_env("WEBHOOK_URL", env_file=Path(__file__).resolve().parents[1] / ".env")
```

`get_env()` 内で環境が GitHub Actions 上であるかを判断し環境変数を返します。
GitHub Actions 上であれば `env_file` 引数は無視され、Secrets に登録した環境変数を優先して取得します。
したがって、GitHub に `env` ファイルをアップロードする必要はありません。
ローカルで正しく動作するためには `env_file=...` に `.env` ファイルの絶対パスを指定するのが望ましいです。

### Details of `get_env()`

```python
def get_env(
    key: str,
    default: Optional[str] = None,
    required: bool = False,
    env_file: Optional[Union[str, Path]] = None,
) -> Optional[str]: ...
```

- `key`: 環境変数のキー
- `default`: 環境変数が存在しない場合に返すデフォルト値。指定しない場合は `None` を返します。
- `required`: `True` の場合、環境変数が存在しないと `ValueError` をスローします。
- `env_file`: 環境変数を読み込むファイルのパス。指定しない場合は `.env` ファイルを読み込みます。

## For Developers

See [DEVELOPMENT.md](DEVELOPMENT.md).

## Contributing

貢献は大歓迎です！Issue の報告や Pull Request の作成をお待ちしています。

Issue を報告する際は、具体的な状況と再現手順を記載してください。
Pull Request を作成する際は、関連する Issue を参照し、変更内容を明確に記述してください。

## Author

[Seika139](https://github.com/Seika139)
