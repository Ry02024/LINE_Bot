import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

def send_line_message(user_ids, message):
    """
    指定されたユーザーにLINEメッセージを送信します。
    """
    # LINE Channel Access Token（Secretsから取得）
    access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    line_bot_api = LineBotApi(access_token)

    # メッセージを送信
    for user_id in user_ids:
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

if __name__ == "__main__":
    # 送信先ユーザーのID
    user_ids = ["USER_ID_1", "USER_ID_2"]  # 必要に応じて設定
    message = "これはGitHub Actionsを使用したLINE Botからのメッセージです！"
    send_line_message(user_ids, message)
