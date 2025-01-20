from flask import Flask, request, jsonify
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import TextMessage, PushMessageRequest
import google.generativeai as genai
import google.api_core.exceptions  # 追加
import os

# 環境変数から値を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_GROUP_ID = "C63a54a7baf55702d42e417b13fe2ce09"

# GEMINI_API_KEYの取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# GEMINI_API_KEYがNoneの場合、GEMINI_API_KEY2を試す
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found. Trying GEMINI_API_KEY2...")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY2")

# エラー処理: GEMINI_API_KEYが最終的にNoneの場合
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY and GEMINI_API_KEY2 are both not set.")
    
# 必須環境変数の確認
if not all([GEMINI_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_GROUP_ID]):
    raise ValueError("必要な環境変数が設定されていません。")

# Geminiの初期設定
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    print("Gemini APIの設定が完了しました。")

configure_gemini(GEMINI_API_KEY)

# トピックリスト
TOPICS = [
    "食生活の工夫 - 厚めの鶏ハムやチゲ丼など、健康的かつ簡単に作れるレシピ。",
    "時間管理とリフレッシュ方法 - 忙しいスケジュールの中で効率よく休む方法やストレス解消の工夫。",
    "趣味の探索 - 新しい趣味やスキル（例えば絵画、陶芸、音楽など）に挑戦する方法。",
    "心地よい生活空間作り - ミニマリズムや片付けの工夫で、居心地の良い部屋を作るヒント。",
    "運動と健康管理 - 日常生活に取り入れられる軽い運動や健康的な生活習慣。",
    "言語学習の工夫 - 効率的な英語学習法や、実生活に役立つフレーズの習得。",
    "テクノロジーを活用した生活の最適化 - 家事やスケジュール管理に役立つアプリやツールの活用法。",
    "自己成長のための読書 - 日々の生活やキャリアにインスピレーションを与える書籍の選び方。",
    "家族や友人との時間の過ごし方 - 大切な人ともっと充実した時間を過ごすためのアイデア。",
    "季節ごとの楽しみ方 - 季節に合わせた旅行プランや、趣味（花見、紅葉狩り、雪景色の楽しみ方）。"
]

# トピックをランダムに選択
def select_random_topic():
    return random.choice(TOPICS)

# 記事を生成
def generate_article(topic):
    prompt = f"""
    以下のトピックについて、100字以内で簡潔かつ具体的に丁寧語（です・ます調）で説明してください。
    トピック: {topic}
    """
    try:
        # トークン1でリクエスト
        response = genai.GenerativeModel(model_name="gemini-1.5-pro").generate_content(contents=[prompt])
        generated_text = response.text.strip() if response.text else "記事を生成できませんでした。"
        return generated_text
    except google.api_core.exceptions.ResourceExhausted as e:
        print(f"⚠️ GEMINI_API_KEY のクォータが上限に達しました: {e}")
        # トークン2に切り替え
        fallback_api_key = os.getenv("GEMINI_API_KEY2")
        if not fallback_api_key:
            raise Exception("GEMINI_API_KEY2 が設定されていません。")
        print("🔄 GEMINI_API_KEY2 に切り替えます...")
        genai.configure(api_key=fallback_api_key)
        try:
            # トークン2で再試行
            response = genai.GenerativeModel(model_name="gemini-1.5-pro").generate_content(contents=[prompt])
            generated_text = response.text.strip() if response.text else "記事を生成できませんでした。"
            return generated_text
        except Exception as e2:
            raise Exception(f"トークン2でもGemini APIエラーが発生しました: {e2}")
    except Exception as e:
        raise Exception(f"Gemini APIエラー: {e}")

# 140字に切り詰める
def trim_to_140_chars(text):
    return text[:200]

# LINEグループに投稿する
def post_to_line(text):
    # デバッグ用出力
    print(f"デバッグ: LINE_CHANNEL_ACCESS_TOKEN = {LINE_CHANNEL_ACCESS_TOKEN}")
    print(f"デバッグ: LINE_GROUP_ID = {LINE_GROUP_ID}")
    print(f"デバッグ: text = {text}")

    # Configurationを用いてアクセストークンを設定
    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    api_client = ApiClient(configuration=configuration)
    messaging_api = MessagingApi(api_client=api_client)

    # メッセージを作成
    message = TextMessage(text=text)

    try:
        # LINEグループにメッセージを送信
        push_message_request = PushMessageRequest(to=LINE_GROUP_ID, messages=[message])
        messaging_api.push_message(push_message_request)
        print(f"✅ LINEグループにメッセージを投稿しました: {text}")
    except Exception as e:
        raise Exception(f"LINEグループへの投稿に失敗しました: {e}")

# メイン処理
if __name__ == "__main__":
    try:
        print("🔍 トピックを選択中...")
        topic = select_random_topic()
        print(f"✅ 選択されたトピック: {topic}")

        print("🔍 記事を生成中...")
        article = generate_article(topic)
        print(f"✅ 生成された記事: {article}")

        print("🔍 記事を140字に切り詰め中...")
        message_content = trim_to_140_chars(article)
        print(f"✅ 投稿する文章（140字以内）: {message_content}")

        print("🔍 LINEグループにメッセージを投稿中...")
        post_to_line(message_content)

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
