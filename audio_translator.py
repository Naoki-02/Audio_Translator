import codecs
import os
import Configclass
from deep_translator import GoogleTranslator
from tkinter import messagebox
class audio_translator:
    

    def txtout(self,result,path,trans):
        #テキストファイルに出力し保存する
        try:
            Dir_path=Configclass.config.read_ini()
            with codecs.open(Dir_path+"/"+os.path.splitext(os.path.basename(path))[0]+'.txt',mode='w',encoding='utf-8') as f:
                f.write(result["text"])
                if(trans != None):
                    f.write('\n\n'+trans)
                messagebox.showinfo("確認","保存しました")
        except OSError:
            messagebox.showerror("エラー","ファイルを開けませんでした。")

    def translate(self,result):
        #日本語以外の場合翻訳して表示する
            translated=GoogleTranslator(source='auto',target='ja').translate(result['text'])
            return translated

        

    def transcribe(self,model,path):
        result = model.transcribe(path)
        return result