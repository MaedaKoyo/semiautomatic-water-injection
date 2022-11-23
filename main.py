from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
import japanize_kivy

import socket
import sys
import time
import datetime

datetime = datetime.datetime.now()    
minute = datetime.minute


class TextWidget(Widget):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ''

    def buttonClicked1(self):        #手動をクリック時
        # soclet
        PORT = 55555
        BUFSIZE = 4096
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect(("192.168.11.13",PORT))
        except:
            print("接続できません")
            sys.exit()

        flg = "1"
        client.sendall(flg.encode("UTF-8"))

        data = client.recv(BUFSIZE)
        print("サーバーからのメッセージ：")
        print(data.decode("UTF-8"))

        client.close()
        self.text = data.decode("UTF-8")


    def buttonClicked2(self):   #自動をクリック時
        # soclet
        PORT = 55555
        BUFSIZE = 4096
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect(("192.168.11.13",PORT))
        except:
            print("接続できません")
            sys.exit()
        flg = "2"
        client.sendall(flg.encode("UTF-8"))
        client.close()
        self.text = "自動注水中\n手動ボタンを押すと解除されます"



class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()

if __name__ == '__main__':
    MainApp().run()