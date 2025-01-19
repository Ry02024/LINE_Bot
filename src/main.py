import os
import random
import google.generativeai as genai
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.messaging.models import TextMessage

# 環境変数からAPIキーを取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_GROUP_ID = "C63a54a7baf55702d42e417b13fe2ce09"  # 事前に設定したグループID

# デバッグ用に各環境変数の値を出力
print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
print(f"LINE_CHANNEL_ACCESS_TOKEN: {LINE_CHANNEL_ACCESS_TOKEN}")
print(f"LINE_GROUP_ID: {LINE_GROUP_ID}")

# 必須環境変数の確認
if not GEMINI_API_KEY:
    print("❌ 環境変数 'GEMINI_API_KEY' が設定されていません。")
if not LINE_CHANNEL_ACCESS_TOKEN:
    print("❌ 環境変数 'LINE_CHANNEL_ACCESS_TOKEN' が設定されていません。")
if not LINE_GROUP_ID:
    print("❌ 環境変数 'LINE_GROUP_ID' が設定されていません。")

# エラーを出す
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

# 選択されたトピックに基づいて記事を生成
def generate_article(topic):
    prompt = f"""
    以下のトピックについて、100字以内で簡潔かつ具体的に丁寧語（です・ます調）で説明してください。
    トピック: {topic}
    """
    try:
        response = genai.GenerativeModel(model_name="gemini-1.5-pro").generate_content(contents=[prompt])
        generated_text = response.text.strip() if response.text else "記事を生成できませんでした。"
        return generated_text
    except Exception as e:
        raise Exception(f"Gemini APIエラー: {e}")

# 140字に切り詰める
def trim_to_140_chars(text):
    return text[:140]

# LINEグループに投稿する
def post_to_line(text):
    config = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    messaging_api = MessagingApi(configuration=config)

    # LINEに送るメッセージ
    message = TextMessage(text=text)

    try:
        # LINEグループにメッセージを送信
        messaging_api.push_message(to=LINE_GROUP_ID, messages=[message])
        print(f"✅ LINEグループにメッセージを投稿しました: {text}")
    except Exception as e:
        raise Exception(f"LINEグループへの投稿に失敗しました: {e}")

# メイン処理
if __name__ == "__main__":
    try:
        # トピックをランダムに選択
        topic = select_random_topic()
        print(f"選択されたトピック: {topic}")

        # 記事を生成
        article = generate_article(topic)
        print(f"生成された記事: {article}")

        # 140字に切り詰める
        message_content = trim_to_140_chars(article)
        print(f"投稿する文章（140字以内）: {message_content}")

        # LINEグループに投稿
        post_to_line(message_content)

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
