import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import *
import audio_translator
import Configclass
import os
import whisper

adt = audio_translator.audio_translator()
conf=Configclass.config
model = whisper.load_model("tiny")


def file_read():
    # ファイル選択ダイアログ表示
    file_path = filedialog.askopenfilename()
    if os.path.exists(file_path) != False:
        # ファイルが選択された場合
        return file_path
    else:
        # ファイル選択がキャンセルされた場合
        messagebox.showerror("エラー","ファイルが見つかりませんでした。")
        return None
    
def dir_read():
    dir_path=filedialog.askdirectory()
    if os.path.exists(dir_path) != False:
        # フォルダが選択された場合
        print("ファイル存在確認")
        conf.write_ini(dir_path)
        return True
    else:
        # フォルダ選択がキャンセルされた場合
        messagebox.showerror("エラー","フォルダを選択できませんでした。")
        return False




class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        # アプリのタイトル
        self.title("Audio_translator")
        # ウィンドウの初期サイズ
        self.geometry("500x320+0+0")
        
        self.drop_target_register(DND_FILES)
        
        self.dnd_bind('<<Drop>>',self.funcDragAndDrop)

        self.notebook=ttk.Notebook(
            self
        )
        
        self.tab1=tk.Frame(self.notebook)
        self.notebook.add(self.tab1,text="ホーム")
        self.tab2=tk.Frame(self.notebook)
        self.notebook.add(self.tab2,text="設定")
        self.notebook.pack(padx=10, pady=5,expand=True,fill='both')
        
        # テキスト表示ウィジェットの作成と配置
        self.text_widget = tk.Text(
            self.tab1,
            width=70,
            height=10,
            bg="#D0D0D0"
        )
        
        self.text_widget.pack(padx=10, pady=5,expand=True,fill='both')

        # 翻訳結果表示ウィジェットの作成と配置
        self.translation_widget = tk.Text(
            self.tab1,
            width=70,
            height=7,
            bg="#EFEFEF"
        )
        self.translation_widget.pack(padx=10, pady=0,expand=True,fill='both')
        
        # ホームの読み込みボタンと保存ボタンの作成と配置
        self.button_frame = tk.Frame(self.tab1)
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
        
        # 設定の読み込みボタンの作成と配置
        self.tab2_frame = tk.Frame(self.tab2)
        self.tab2_frame.pack(padx=10, pady=10)
        
        # 「保存フォルダ」ラベルの作成
        self.dirLabel=ttk.Label(
            self.tab2_frame,
            text="フォルダ参照＞＞"
        )
        self.dirLabel.pack(side=tk.LEFT)
        
        # 「フォルダ参照」エントリーの作成
        self.dir_Entry= ttk.Entry(
            self.tab2_frame,
            width=30
            )
        self.dir_Entry.pack(side=tk.LEFT)
        
        self.read_button2 = tk.Button(
            self.tab2_frame,
            text='参照',
            command=self.read_button_func2
        )
        self.read_button2.pack(side=tk.LEFT)
        self.entry_insert()
        # 結果とファイルパスを保存するための属性
        self.result = None
        self.file_path = None
        self.translated =None

    def entry_insert(self):
        self.dir_Entry.delete(tk.END)
        self.dir_Entry.insert(tk.END,conf.read_ini())
    
    def read_button_func(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        file_path = file_read()
        if file_path is None:
            return

        self.file_path = file_path  # ファイルパスを保存
        
        self.out_translation_func()
        
    def read_button_func2(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        if(dir_read()!=False):
            self.entry_insert()
        
        

    def out_translation_func(self):
        # 初期化
        self.translated=None
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
        self.out_translation_func() 
        
    def save_button_func(self):
        adt.txtout(self.result, self.file_path,self.translated)
        


# GUIアプリ生成
app = Application()
app.mainloop()
