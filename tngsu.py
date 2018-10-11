from csv import DictReader
import json

from flask import Flask
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型


from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


辭典 = 型音辭典(6)
with open('docker.csv') as sutian:
    for tsua in DictReader(sutian):
        try:
            詞物件 = 拆文分析器.建立詞物件(tsua['漢字'], tsua['羅馬字'])
            辭典.加詞(詞物件)
        except 解析錯誤:
            pass
語言模型 = KenLM語言模型('lm.arpa')


app = Flask(__name__)


@app.route("/<bun5ji7>")
def 標記(bun5ji7):
    漢字 = (
        拆文分析器.建立句物件(bun5ji7)
        .轉音(臺灣閩南語羅馬字拼音)
        .揣詞(拄好長度辭典揣詞, 辭典)
        .揀(語言模型揀集內組, 語言模型)
        .看型('', ' ')
    )
    return json.dumps(
        {'漢字': 漢字},
        indent=2, ensure_ascii=False, sort_keys=True
    )
