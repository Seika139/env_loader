このプロジェクトはローカルホストと GitHub Actions 上で環境変数を使用するための Python ライブラリです。
ローカルホストでは `.env` ファイルなどのファイルを load_dotenv() などの関数を使用して環境変数を読み込みます。
GitHub Actions では Secrets に登録した環境変数を読み込みます。

ローカルホストではタスクランナーとして Makefile を使用します。
GitHub にソースコードをアップロードし GitHub Actions で定期的に実行されるように設定します。
ソースコードは poetry のベストプラクティスに則って書いてください。
.python-version ファイルに定義された Python のバージョン以上で動作するように型の定義を厳密に行います。
isort, black, flake8, mypy, pytest を利用してコードの品質を保ちます。
