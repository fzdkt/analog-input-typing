# import os
# os.environ['PYTHONWARNINGS'] = 'ignore' 
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning)
import tkinter as tk
from tkinter import messagebox
import pyperclip
import time  # 新增时间模块
import pyautogui  # 新增自动化模块
from core import simulate_typing  # 移除不需要的依赖
from config import TYPE_INTERVAL  # 仅保留必要配置


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("通用打字模拟器")
        self.master.geometry("600x400")
        self.create_widgets()
        self.setup_ui()

    def create_widgets(self):
        # 文本输入框
        self.text_area = tk.Text(self.master, wrap=tk.WORD)
        self.text_area.pack(pady=10, fill=tk.BOTH, expand=True)

        # 新增设置框架
        settings_frame = tk.Frame(self.master)
        settings_frame.pack(pady=5)

        # 输入间隔设置
        tk.Label(settings_frame, text="输入间隔(秒):").pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(settings_frame, width=6)
        self.interval_entry.insert(0, str(TYPE_INTERVAL))
        self.interval_entry.pack(side=tk.LEFT, padx=5)

        # 按钮框架
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="粘贴内容", command=self.paste_content).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="开始模拟", command=self.start_simulation).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="退出程序", command=self.master.quit).pack(
            side=tk.RIGHT, padx=5
        )

    def setup_ui(self):
        # 创建右键菜单
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="粘贴", command=self.paste_content)
        self.text_area.bind("<Button-3>", self.show_context_menu)

    def paste_content(self):
        try:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, pyperclip.paste())
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败: {str(e)}")

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def start_simulation(self):
        content = self.text_area.get(1.0, tk.END).strip()
        # print("内容：", content)
        if not content:
            messagebox.showwarning("警告", "请输入或粘贴需要模拟输入的内容")
            return

        try:
            # 获取用户自定义间隔时间
            interval = float(self.interval_entry.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入有效的正数间隔时间")
            return
        # print("间隔：", interval)

        # 显示倒计时弹窗
        countdown_window = tk.Toplevel()
        countdown_window.title("准备输入")
        tk.Label(countdown_window, text="请在2秒内将光标定位到输入位置").pack(
            padx=20, pady=10
        )
        tk.Label(countdown_window, text="2", font=("Arial", 24)).pack()
        countdown_window.update()

        # 倒计时动画
        for i in range(2, 0, -1):
            time.sleep(1)
            countdown_window.children["!label2"].config(text=str(i))
            countdown_window.update()

        countdown_window.destroy()  # 关闭倒计时窗口
        time.sleep(0.5)  # 额外缓冲时间
        pyautogui.click()  # 点击确保焦点

        if interval <= 0.01:  # 防止间隔过小
            messagebox.showerror("错误", "间隔时间不能小于0.01秒")
            return

        try:
            # 直接在当前光标位置开始输入
            simulate_typing(content, interval * 0.8, interval * 1.2)  # 添加20%波动范其妙sh围
        except Exception as e:
            messagebox.showerror("错误", f"输入中断: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
