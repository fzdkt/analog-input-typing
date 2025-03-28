import pyautogui
import pyperclip
import pygetwindow as gw
import time
import random
from pypinyin import lazy_pinyin
from wubi_dict import wubi_dict

import unicodedata
import re


def is_chinese(char):
    if "CJK" in unicodedata.name(char):
        return True
    else:
        return False


# 激活目标窗口
def activate_target_window(window_title):
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        if win:
            win.activate()
            time.sleep(1)  # 等待窗口激活
            return True
        return False
    except IndexError:
        return False


# 切换至中文输入法（需要用户预先配置输入法快捷键）
def switch_to_chinese_ime():
    try:
        # 切换输入法
        pyautogui.keyDown("ctrl")
        pyautogui.press("~")
        pyautogui.keyUp("ctrl")
        time.sleep(0.8)  # 延长等待时间确保切换完成
    except Exception as e:
        print(f"输入法切换失败: {str(e)}")


def is_ascii(string):
    try:
        string.encode("ascii")
    except UnicodeEncodeError:
        return False
    else:
        return True


# 修改后的simulate_typing函数（core.py）
def simulate_typing(text, min_interval, max_interval):
    switch_to_chinese_ime()  # 确保输入法状态
    try:
        # 确保焦点在目标窗口
        pyautogui.click()  # 新增点击确保焦点
        time.sleep(0.5)

        # 打印调试信息
        print(f"[DEBUG] 开始输入内容，长度：{len(text)}")

        for char in text:
            print()

            if char.isdigit():
                # 处理字母数字
                print(f"输入数字: {char}")
                pyautogui.write(char, interval=random.uniform(0.05, 0.1))
                time.sleep(random.uniform(min_interval, max_interval))
            elif is_ascii(char):
                print(f"输入ASCII: {char}")
                pyautogui.keyDown("shift")
                time.sleep(0.08)
                pyautogui.typewrite(char)
                time.sleep(0.08)
                pyautogui.keyUp("shift")
                time.sleep(0.08)
                pyautogui.keyDown("shift")
                time.sleep(0.08)
                pyautogui.keyUp("shift")
                time.sleep(0.08)
                time.sleep(random.uniform(min_interval, max_interval))
            elif "\u4e00" <= char <= "\u9fff":
                # 中文处理
                print(f"输入中文: {char}")
                time.sleep(0.08)
                code = get_wubi_code(char)
                pyautogui.write(code, interval=0.08)
                time.sleep(0.2)
                pyautogui.keyDown("space")
                time.sleep(0.05)
                pyautogui.keyUp("space")
                # pyautogui.press('1')  # 通常第一个候选词
                time.sleep(random.uniform(0.2, 0.3))
                # # 输入拼音
                # pinyin = lazy_pinyin(char)
                # print(pinyin)
                # pyautogui.write(pinyin, interval=0.08)
                # lazy_pinyin(char)[0][0].lower()
                # time.sleep(0.2)  # 等待输入法响应

                # # 选择候选词
                
                # time.sleep(random.uniform(0.2, 0.3))

            else:
                # 符号处理优化
                print(f"输入其它符号: {char}")
                pyperclip.copy(char)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.08)

    except Exception as e:
        print(f"输入中断，错误信息: {str(e)}")
        import traceback

        traceback.print_exc()


# 获取五笔编码（带容错机制）
def get_wubi_code(char):
    code = wubi_dict.get(char, "")
    print(code)
    # 未找到编码时的处理方案
    if not code:
        print(f"警告：未找到字符 [{char}] 的五笔编码")
        # 使用拼音首字母（需安装pypinyin）
        # try:
        #     from pypinyin import lazy_pinyin

        #     return lazy_pinyin(char)[0][0].lower()
        # except:
        #     pass

        return "clip"  # 特殊标记

    return code.split(",")[0]
