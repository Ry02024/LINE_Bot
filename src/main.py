import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

# LINEのチャネルアクセストークン（GitHub Secretsで設定済み）
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_SECRET")

# グループID（Webhookで取得したIDを設定）
GROUP_ID = "U139a29bf4fd93b7bf37c16a6d34dde10"  # 取得したグループIDを入力

def send_message():
    """
    指定されたLINEグループにメッセージを送信する
    """
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    message = "これはGitHub Actionsを使ったLINE Botからのメッセージです！"
    line_bot_api.push_message(GROUP_ID, TextSendMessage(text=message))

if __name__ == "__main__":
    send_message()
