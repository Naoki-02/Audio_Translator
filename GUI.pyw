# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import filedialog
import audio_translator
import os
import whisper
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning)


adt=audio_translator.audio_translator()
model=whisper.load_model("tiny")
#txtfileを読み込むプログラム

def file_read():
    
    # ファイル選択ダイアログの表示
    file_path = filedialog.askopenfilename()
    print("ファイル名："+file_path)
    if os.path.exists(file_path) != False:
        # ファイルが選択された場合
        print("ファイル存在確認")
        return file_path
    else:
        # ファイル選択がキャンセルされた場合
        print("ファイルが見つかりません")
        return 0


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # アプリのタイトル
        self.title("ファイル読み込み")

        # テキスト表示キャンバスの作成と配置
        self.text_canvas = tk.Canvas(
            self,
            width=600,
            height=400,
            bg="#D0D0D0"
        )
        self.text_canvas.pack()

        # 読み込みボタンの作成と配置
        self.read_button = tk.Button(
            self,
            text='ファイル読み込み',
            command=self.read_button_func
        )
        self.read_button.pack()
        
        #保存ボタンの作成と配置
        self.save_button=tk.Button(
            self,
            text='保存',
            command=self.save_button_func,
            state=tk.DISABLED# 初期状態では非アクティブ
        )
        self.save_button.pack()
        # 結果とファイルパスを保存するための属性
        self.result=None
        self.file_path=None

    def read_button_func(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        file_path = file_read()
        if(file_path==0):
            return
           
        self.file_path=file_path # ファイルパスを保存
        
        result=adt.transcribe(model,file_path)
        self.result=result # 結果を保存
        
        if result['language'] != 'ja': 
            translated=adt.translate(result)
        

        # 読み込んだ結果を画面に描画
        self.text_canvas.create_text(300, 200, text=result["text"]+translated)

        # 保存ボタンをアクティブにする
        self.save_button.config(state=tk.ACTIVE)
    def save_button_func(self):
        adt.txtout(self.result,self.file_path)

# GUIアプリ生成
app = Application()
app.mainloop()
