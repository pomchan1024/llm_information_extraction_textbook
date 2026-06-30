! pip install google-generativeai

import google.generativeai as genai

# APIの設定
genai.configure(api_key="YOUR_API_KEY")

# パラメータの設定 (Generation Config)
generation_config = {
    "temperature": 0.2,      # 0に近いほど正確・保守的、1に近いほど独創的
    "top_p": 0.95,           # 累積確率に基づき単語を選択する範囲を制限
    "top_k": 40,             # 選択肢となる単語数を上位k個に制限
    "max_output_tokens": 2048, # 生成される回答の最大文字数トークン数を指定
    "response_mime_type": "text/plain", # JSONで出力したい場合は "application/json" を指定する
}

# システム指示を含めたモデルの初期化
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="あなたは優秀な要約アシスタントです。入力されたテキストの重要なポイントを抽出し、簡潔な箇条書きで出力してください。",
    generation_config=generation_config
)

# 具体的な実行例
target_text = """
ここに解析したい非常に文章を入力
"""

response = model.generate_content(target_text)

# 実行結果の出力
print("--- 要約結果 ---")
print(response.text)