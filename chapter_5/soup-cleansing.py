! pip install beautifulsoup4==4.14.3

from bs4 import BeautifulSoup
import re

def clean_html_text(html_content):
    # 解析対象のHTMLをパース
    soup = BeautifulSoup(html_content, 'html.parser')

    # 不要なタグ（スクリプト、スタイルなど）を完全に除去
    # これを行わないと、JavaScriptのコードなどがテキストとして混入します
    for element in soup(["script", "style", "header", "footer", "nav"]):
        element.decompose()

    # get_text() でテキスト抽出
    # separator=" " を指定することで、タグの境界で単語がくっつくのを防ぎます
    # strip=True で前後の空白を削除します
    text = soup.get_text(separator=" ", strip=True)

    # 正規表現によるクレンジング
    # 改行やタブをスペースに置換
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # 連続するスペース（2つ以上）を1つにまとめる
    text = re.sub(r'\s{2,}', ' ', text)

    # 前後の最終トリミング
    return text.strip()


# --- 実行例 ---
sample_html = """
<html>
  <head><style>body {color: red;}</style></head>
  <body>
    <nav><ul><li>Home</li></ul></nav>
    <div id="main">
      <h1>タイトルの  例</h1>
      <p>これは第一段落です。<br>改行が含まれます。</p>
      <p>別の段落です。    空白が    多いです。</p>
    </div>
    <script>console.log('hello');</script>
  </body>
</html>
"""

cleaned_text = clean_html_text(sample_html)
print(cleaned_text)