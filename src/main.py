import os
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import TextMessage, PushMessageRequest

# 環境変数からトークンを取得
LINE_CHANNEL_ACCESS_TOKEN1 = os.getenv("LINE_CHANNEL_ACCESS_TOKEN1")
LINE_GROUP_ID = os.getenv("LINE_GROUP_ID")

# Messaging APIクライアント設定
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN1)
api_client = ApiClient(configuration=configuration)
messaging_api = MessagingApi(api_client=api_client)

# メッセージ送信
try:
    message = TextMessage(text="テストメッセージ: 自動送信テスト")
    push_message_request = PushMessageRequest(to=LINE_GROUP_ID, messages=[message])
    messaging_api.push_message(push_message_request)
    print("✅ メッセージ送信成功")
except Exception as e:
    print(f"❌ メッセージ送信失敗: {e}")


# from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
# from linebot.v3.messaging.models import TextMessage, PushMessageRequest
# import google.generativeai as genai
# import google.api_core.exceptions
# import os, random

# # 環境変数からトークンを取得
# LINE_CHANNEL_ACCESS_TOKEN1 = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# LINE_CHANNEL_ACCESS_TOKEN2 = os.getenv("LINE_CHANNEL_ACCESS_TOKEN2")
# LINE_GROUP_ID = os.getenv("LINE_GROUP_ID")

# # GEMINI_API_KEYを取得
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # アクセストークンリストとインデックス
# access_tokens = [LINE_CHANNEL_ACCESS_TOKEN1, LINE_CHANNEL_ACCESS_TOKEN2]
# current_token_index = 0

# # 必須環境変数の確認
# if not all(access_tokens) or not LINE_GROUP_ID or not GEMINI_API_KEY:
#     raise ValueError("必要な環境変数が設定されていません。")

# # Geminiの初期設定
# def configure_gemini(api_key):
#     genai.configure(api_key=api_key)
#     print("Gemini APIの設定が完了しました。")

# configure_gemini(GEMINI_API_KEY)

# # トピックリスト
# TOPICS = [
#     "食生活の工夫 - 健康的かつ簡単なレシピ。",
#     "時間管理とリフレッシュ方法。",
#     "趣味の探索 - 新しいスキルに挑戦。",
#     "心地よい生活空間作り。",
#     "運動と健康管理。",
#     "言語学習の工夫。",
#     "テクノロジーを活用した生活最適化。",
#     "自己成長のための読書。",
#     "家族や友人との時間の過ごし方。",
#     "季節ごとの楽しみ方。",
# ]

# # トークン切り替え
# def switch_token():
#     """現在のアクセストークンを切り替える"""
#     global current_token_index
#     current_token_index = (current_token_index + 1) % len(access_tokens)
#     return access_tokens[current_token_index]

# # ランダムなトピックを選択
# def select_random_topic():
#     return random.choice(TOPICS)

# # 記事を生成
# def generate_article(topic):
#     prompt = f"""
#     以下のトピックについて、100字以内で簡潔に丁寧語で説明してください。
#     トピック: {topic}
#     """
#     response = genai.GenerativeModel(model_name="gemini-1.5-pro").generate_content(contents=[prompt])
#     return response.text.strip() if response.text else "記事を生成できませんでした。"

# # LINEにメッセージを送信
# def post_to_line(text):
#     global current_token_index
#     for attempt in range(len(access_tokens)):
#         try:
#             current_token = access_tokens[current_token_index]
#             configuration = Configuration(access_token=current_token)
#             api_client = ApiClient(configuration=configuration)
#             messaging_api = MessagingApi(api_client=api_client)

#             # メッセージを作成して送信
#             message = TextMessage(text=text)
#             push_message_request = PushMessageRequest(to=LINE_GROUP_ID, messages=[message])
#             messaging_api.push_message(push_message_request)
#             print(f"✅ メッセージ送信成功: {text}")
#             return
#         except Exception as e:
#             print(f"⚠️ エラー: {e}. トークンを切り替えます...")
#             switch_token()
#     print("❌ 全てのトークンで送信失敗しました。")

# # メイン処理
# if __name__ == "__main__":
#     try:
#         topic = select_random_topic()
#         print(f"✅ 選択されたトピック: {topic}")

#         article = generate_article(topic)
#         print(f"✅ 生成された記事: {article}")

#         message_content = article[:140]  # 140文字に制限
#         print(f"✅ 投稿内容: {message_content}")

#         post_to_line(message_content)
#     except Exception as e:
#         print(f"❌ エラー: {e}")
