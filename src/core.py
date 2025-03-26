import pyautogui
import pygetwindow as gw
import time
import random
from pypinyin import lazy_pinyin

def activate_target_window(window_title):
    """激活目标窗口"""
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        if win:
            win.activate()
            time.sleep(1)  # 等待窗口激活
            return True
        return False
    except IndexError:
        return False

def switch_to_chinese_ime():
    """切换至中文输入法（需要用户预先配置输入法快捷键）"""
    pyautogui.hotkey('ctrl', 'shift')  # 常见输入法切换快捷键
    time.sleep(config.IME_SWITCH_DELAY)

def simulate_typing(text, interval_range):
    """模拟输入法打字"""
    for char in text:
        # 处理中文和特殊字符
        if '\u4e00' <= char <= '\u9fff':
            # 中文转拼音
            pinyin = lazy_pinyin(char)[0]
            pyautogui.write(pinyin, interval=random.uniform(0.05, 0.1))
            pyautogui.press('space')  # 选择候选词
        else:
            # 直接输入其他字符
            pyautogui.write(char, interval=random.uniform(*interval_range))
        
        # 添加随机输入间隔
        time.sleep(random.uniform(*interval_range))