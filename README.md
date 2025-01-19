# LINE_Bot

このリポジトリは、GitHub Actionsを使用してLINEグループに自動的にメッセージを送信するLINE Botのプロジェクトです。Pythonを使用し、LINE Messaging APIを通じてメッセージを送信します。

---

## 特徴
- **GitHub Actions対応**: 手動実行や定期実行が可能。
- **環境変数の安全な管理**: GitHub Secretsを使用してアクセストークンを保護。
- **シンプルな構成**: PythonスクリプトでLINE Messaging APIを簡単に利用。

---

## ディレクトリ構造

```
your_project/
├── src/
│   ├── main.py              # メインスクリプト
├── .github/
│   └── workflows/
│       └── line_bot_task.yml # GitHub Actionsのワークフロー定義
├── requirements.txt         # Pythonの依存ライブラリ
├── README.md                # プロジェクトの説明
└── .gitignore               # 無視するファイルのリスト
```

---

## 必要条件

1. **LINE Messaging APIのチャネル**
   - [LINE Developers](https://developers.line.biz/)で新しいチャネルを作成し、チャネルアクセストークンを取得します。

2. **GitHubリポジトリ**
   - GitHubで新しいリポジトリを作成します。

3. **Python環境**
   - GitHub Actions上でPython 3.9を使用します。

---

## セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. GitHub Secretsの設定
- GitHubリポジトリの`Settings > Secrets and variables > Actions`に移動し、以下のSecretsを追加します。

| Key                       | Value                     |
|---------------------------|---------------------------|
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging APIのアクセストークン |

### 3. 必要なライブラリを記述
- `requirements.txt`に以下を記載済み:
  ```
  line-bot-sdk
  ```

### 4. スクリプトを確認
- `src/main.py`を編集し、以下を設定してください:
  - **LINEグループID**:
    ```python
    group_id = "YOUR_GROUP_ID"  # LINEグループIDを指定
    ```

### 5. GitHub Actionsワークフローの確認
- `.github/workflows/line_bot_task.yml`でスケジュール（cron）を設定済み。
  - 例: 毎日午前9時（UTC時間）に実行。

---

## 使用方法

### 定期実行
- ワークフローは、設定されたスケジュールに基づいて自動的に実行されます。

### 手動実行
- GitHub Actionsの`Run workflow`ボタンをクリックして手動で実行できます。

---

## 注意事項

- **LINEグループIDの取得**: LINE Botがグループ内で最初にアクションを実行する際にWebhookで取得できます。
- **GitHub Secrets**: トークンやキーをコードに直接記述せず、必ずSecretsを使用してください。

---

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。

---

## 問い合わせ

プロジェクトについて質問がある場合は、[Issues](https://github.com/your-username/your-repository/issues)で報告してください。

---
