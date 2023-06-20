import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import *
import audio_translator
import os
import whisper

adt = audio_translator.audio_translator()
model = whisper.load_model("tiny")


def file_read():
    # ファイル選択ダイアログ表示
    file_path = filedialog.askopenfilename()
    print("ファイル名：" + file_path)
    if os.path.exists(file_path) != False:
        # ファイルが選択された場合
        print("ファイル存在確認")
        return file_path
    else:
        # ファイル選択がキャンセルされた場合
        messagebox.showerror("エラー","ファイルが見つかりませんでした")
        return None




class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        # アプリのタイトル
        self.title("Audio_translator")
        # ウィンドウの初期サイズ
        self.geometry("500x300+0+0")
        
        self.drop_target_register(DND_FILES)
        
        self.dnd_bind('<<Drop>>',self.funcDragAndDrop)

        # テキスト表示ウィジェットの作成と配置
        self.text_widget = tk.Text(
            self,
            width=70,
            height=10,
            bg="#D0D0D0"
        )
        
        self.text_widget.pack(padx=10, pady=5,expand=True,fill='both')

        # 翻訳結果表示ウィジェットの作成と配置
        self.translation_widget = tk.Text(
            self,
            width=70,
            height=7,
            bg="#EFEFEF"
        )
        self.translation_widget.pack(padx=10, pady=0,expand=True,fill='both')

        # 読み込みボタンと保存ボタンの作成と配置
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        self.read_button = tk.Button(
            self.button_frame,
            text='ファイル読み込み',
            command=self.read_button_func
        )
        self.read_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(
            self.button_frame,
            text='保存',
            command=self.save_button_func,
            state=tk.DISABLED  # 初期状態では非アクティブ
        )
        self.save_button.pack(side=tk.LEFT)

        # 結果とファイルパスを保存するための属性
        self.result = None
        self.file_path = None
        # self.translated =None

    def read_button_func(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        file_path = file_read()
        if file_path is None:
            return

        self.file_path = file_path  # ファイルパスを保存
        
        self.out_translation_func()
        
        

    def out_translation_func(self):
        # 初期化
        self.text_widget.delete("1.0", tk.END)
        self.translation_widget.delete("1.0", tk.END)

        result = adt.transcribe(model, self.file_path)
        self.result = result  # 結果を保存

        if result['language'] != 'ja':
            translated = adt.translate(result)
            self.translated=translated
            self.text_widget.insert(tk.END, result["text"])
            self.translation_widget.insert(tk.END, translated)
        else:
            self.text_widget.insert(tk.END, result["text"])
        # 保存ボタンをアクティブにする
        self.save_button.config(state=tk.ACTIVE)
        
    def funcDragAndDrop(self, e):
        self.file_path=e.data
        self.file_path=self.file_path.strip('{}')
        print("ファイル名:"+self.file_path)
        self.out_translation_func() 
        
    def save_button_func(self):
        adt.txtout(self.result, self.file_path)
        


# GUIアプリ生成
app = Application()
app.mainloop()
