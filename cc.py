import pyautogui
import pyperclip
import time
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import pandas as pd

class cc:
    def __init__(self, path) -> None:
        """
        :param path: 保存数据的excel文件路径
        """
        self.path = path


    def get_info(self):
        url = "http://www.example.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 这里需要找到正确的CSS选择器
        price_element = soup.select_one("复制你找到的CSS选择器(价格或其他数字)")
        date_element = soup.select_one("复制你找到的CSS选择器(日期或其他文字)")
        price = price_element.text if price_element else "未找到价格"
        date = date_element.text if date_element else "未找到日期"

        return price,date

    def save(self, price, date):
        df = pd.read_excel(self.path)
        new_data = pd.DataFrame({"日期": [date.strip()], "价格": [price.strip()]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(self.path, index=False)
        
    def get_msg(self, ifsave=False):
        price,date = self.get_info()
        if ifsave:
            self.save(price, date)
        
        # 自由拼接你需要发送的消息
        contents = date.strip() + "的价格为：" + price.strip()
        return contents

    def send(self, msg):
        # 复制需要发送的内容到粘贴板
        pyperclip.copy(msg)
        # 模拟键盘 ctrl + v 粘贴内容
        pyautogui.hotkey('ctrl', 'v')
        # 发送消息
        pyautogui.press('enter')

    def send_msg(self, friend, ifsave):
        # Ctrl + alt + w 打开微信
        pyautogui.hotkey('ctrl', 'alt', 'w')
        # 搜索好友
        pyautogui.hotkey('ctrl', 'f')
        # 复制好友昵称到粘贴板
        pyperclip.copy(friend)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 回车进入好友消息界面
        pyautogui.press('enter')

        msg = self.get_msg(ifsave)
        
        # 为防止发错对象，可将微信发送改为ctrl + enter，手动发送
        self.send(msg)


if __name__ == '__main__':
    # 这里改你需要发的群名
    friend_name = input("请输入发送对象：")
    bool = input("是否保存今日数据到excel?（是/否）")
    
    if bool == "是":
        path = input("请粘贴需要保存的路径:")
        robo = cc(path)
        robo.send_msg(friend_name,ifsave=True)
    else:
        robo = cc(path=None)
        robo.send_msg(friend_name,ifsave=False)
        
        
    