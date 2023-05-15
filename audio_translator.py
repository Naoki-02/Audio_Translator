import whisper

model=whisper.load_model("base")

#result = model.transcribe("ファイル名")

result = model.transcribe("test.mp3",fp16=False)

print(result["text"])