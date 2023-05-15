import whisper
import codecs
model=whisper.load_model("tiny")

#result = model.transcribe("ファイル名")
path="test.mp3"
result = model.transcribe(path,fp16=False)

with codecs.open('contents/test_w.txt',mode='w',encoding='utf-8') as f:
    f.write(result["text"])
    
print(result["text"])