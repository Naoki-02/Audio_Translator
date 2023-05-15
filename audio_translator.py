import whisper
import codecs
import os
from deep_translator import GoogleTranslator

model=whisper.load_model("tiny")

#result = model.transcribe("ファイル名")
path="english.mp3"

result = model.transcribe(path,fp16=False)
save=input()

#保存するかしないかの処理
if save == '1':
    #テキストファイルに出力し保存する
    with codecs.open('contents/'+os.path.splitext(os.path.basename(path))[0]+'.txt',mode='w',encoding='utf-8') as f:
        f.write(result["text"])
        print("保存しました。")

        
#日本語以外の場合翻訳して表示する
if result['language'] != 'ja':        
    translated=GoogleTranslator(source='auto',target='ja').translate(result['text'])
    print(translated)

print(result["text"])

