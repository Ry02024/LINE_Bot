import os
from linebot.v3.messaging import MessagingApi
from linebot.v3.messaging.models import TextMessage

# LINEのチャネルアクセストークン（GitHub Secretsで設定済み）
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# グループIDを指定（Webhookで取得したIDを設定）
GROUP_ID = "YOUR_GROUP_ID"

def send_message():
    """
    指定されたLINEグループにメッセージを送信する
    """
    messaging_api = MessagingApi(channel_access_token=ACCESS_TOKEN)
    message = TextMessage(text="これはGitHub Actionsを使ったLINE Botからのメッセージです！")
    messaging_api.push_message(to=GROUP_ID, messages=[message])

if __name__ == "__main__":
    send_message()
