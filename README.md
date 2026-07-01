# LLMによる情報抽出入門
## 〜日常のリアルなデータから価値ある情報を取り出す技術

本書のサンプルコードを格納しているリポジトリです。第5章・第6章・第7章・付録で紹介したコードを公開しています。

---

### 書籍情報

| 項目 | 内容 |
| :--- | :--- |
| **著者** | 中田百科，桐生佳介 著 |
| **定価** | 3,520円（本体3,200円＋税10%） |
| **発売日** | 2026年7月27日 |
| **判型** | B5変形 |
| **頁数** | 272ページ |
| **ISBN** | 978-4-297-15727-2 |
| **URL** | https://gihyo.jp/book/2026/978-4-297-15727-2 |

---
### ディレクトリ構成
```
chapter_5/
├── sample_date                          … 解析対象のデータが格納されたフォルダ
├── fixed-size-chunking.py               … 5-1-1 固定長チャンキング
├── extract-word.py                      … 5-1-1 Wordファイルからのテキスト抽出
├── extract-excel.py                     … 5-1-1 Excelファイルからのテキスト抽出
├── soup-cleansing.py                    … 5-1-2 HTMLタグのクレンジング
├── translation.py                       … 5-1-2 テキストの自動翻訳
└── tf-idf.py                            … 5-2-1 TF-IDFによる重要単語抽出

chapter_6/
├── sample_date                          … 解析対象のデータが格納されたフォルダ
├── batch-image-generation.py            … 6-1-1 画像バッチ処理
├── bounding-box.py                      … 6-1-2 バウンディングボックス描画
├── attention-map-generation.py          … 6-1-2 Grad-CAMによる注目領域の可視化
├── scaffolding.py                       … 6-1-2 Scaffolding
├── scaffolding-adaptive-color.py        … 6-1-2 配色を動的に決定するScaffolding
├── divide-image.py                      … 6-2-1 画像分割によるチャンキング
├── drawing-bounding-boxes.py            … 6-2-5 Geminiから出力されたバウンディングボックスの描画
├── make-binary-matrix.py                … 6-2-5 セマンティックセグメンテーションのバイナリ行列の生成
└── geometry-generation.py               … 6-2-6 数学の問題の図形の自動生成

chapter_7/
├── sample_date                          … 解析対象のデータが格納されたフォルダ
├── resampling.py                        … 7-1-1 音声データのリサンプリング
├── VAD-webrtcvad.py                     … 7-1-1 音声区間検出
├── fixed-size-chunking-token-speech.py  … 7-1-1 音声データのチャンキング
├── resampling-video.py                  … 7-2-1 動画データのリサンプリング
├── fixed-size-chunking-token-movie.py   … 7-2-1 動画データのチャンキング
├── telop.py                             … 7-2-2 テロップの自動挿入
└── narration.py                         … 7-2-2 ナレーションの自動挿入

appendix/
├── sample.py                            … A-1-1 Pythonの基本動作確認
├── numpy-test.py                        … A-1-1 Numpyのテスト
├── prepare-text-data.py                 … A-1-2 テキストファイルの作成
├── janome-test.py                       … A-1-2 形態素解析
├── pandas-test.py                       … A-1-2 単語の頻度分析
├── pillow-test.py                       … A-1-4 Pillowのテスト
├── opencv-test.py                       … A-1-5 Opencvのテスト
└── gemini-api-parameter-setting-test.py … A-2-4 APIによるGeminiの利用

```
### 利用方法
本書のコードはGoogle Colaboratory([https://colab.research.google.com/?hl=ja](https://colab.research.google.com/?hl=ja))環境での動作を想定しているPythonコードです。
#### 1. ソースのダウンロード
! git clone https://github.com/gihyo-book/llm_information_extraction_book.git

#### 2. 興味のある章へ移動（例：第5章の場合）
% cd llm_information_extraction_book/chapter_5

#### 3. 興味のあるコードの内容を確認
! cat tf-idf.py

#### 4. 実行
出力されたコードをコピーします。セルの左側にある三点リーダーから選択できます。  
新しいセルに貼り付けて実行ボタンを押下します。
