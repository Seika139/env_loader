# Changelog

<!-- markdownlint-disable MD024 MD029 MD033 -->

全ての注目すべき変更はこのファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/spec/v2.0.0.html) に従います。

## [0.2.0] - 2025-05-22

### Changed

- `get_env` 関数の仕様を変更し、`Optional[str]` を返すシンプルな関数に変更
- `required` パラメータを削除

### Added

- 新しい `require_env` 関数を追加。必須の環境変数を取得し、存在しない場合は `ValueError` を発生させる

## [0.1.0] - 2025-05-21

### Added

- 初期リリース
- `get_env` 関数の実装
- GitHub Actions とローカル環境の両方での環境変数サポート
- `.env` ファイルのサポート
