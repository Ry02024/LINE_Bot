import os
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.messaging.models import TextMessage

# 環境変数からアクセストークンを取得
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# グループID（Webhookで取得済みのものを設定）
GROUP_ID = "YOUR_GROUP_ID"  # 必要に応じて正しいIDを設定

def send_message():
    """
    指定されたLINEグループにメッセージを送信する
    """
    # MessagingApi用のConfigurationを設定
    config = Configuration(access_token=ACCESS_TOKEN)
    messaging_api = MessagingApi(configuration=config)

    # 送信するメッセージ
    message = TextMessage(text="これはGitHub Actionsを使ったLINE Botからのメッセージです！")

    try:
        # メッセージ送信
        messaging_api.push_message(to=GROUP_ID, messages=[message])
        print("メッセージが正常に送信されました！")
    except Exception as e:
        print(f"メッセージ送信中にエラーが発生しました: {e}")

if __name__ == "__main__":
    send_message()
