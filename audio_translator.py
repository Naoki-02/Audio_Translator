import codecs
import os
from deep_translator import GoogleTranslator

class audio_translator:
    
    #result = model.transcribe("ファイル名")
    path="english.mp3"

    def txtout(self,result,path):
        #テキストファイルに出力し保存する
            with codecs.open('contents/'+os.path.splitext(os.path.basename(path))[0]+'.txt',mode='w',encoding='utf-8') as f:
                f.write(result["text"])
                print("保存しました。")

    def translate(self,result):
        #日本語以外の場合翻訳して表示する
            translated=GoogleTranslator(source='auto',target='ja').translate(result['text'])
            return translated

        

    def transcribe(self,model,path):
        result = model.transcribe(path)
        return result