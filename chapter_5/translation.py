! pip install argostranslate==1.11.0

import argostranslate.package
import argostranslate.translate

# 翻訳前と翻訳語の言語を指定
to_code = "en"
from_code = "ja"

# 翻訳に使用するモデルのパッケージのインデックスをアップデート
argostranslate.package.update_package_index()
# 使用可能なパッケージの取得
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, \
            available_packages
    )
)
# パッケージのインストール
argostranslate.package.install_from_path(package_to_install.download())

# --- 実行例 ---
translatedText = argostranslate.translate\
    .translate("所望のプロンプト", from_code, to_code)
print(translatedText)