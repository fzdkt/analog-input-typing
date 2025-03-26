import tkinter as tk
from tkinter import messagebox
import pyperclip
from core import activate_target_window, simulate_typing, switch_to_chinese_ime

from config import TARGET_WINDOW_TITLE, TYPE_INTERVAL, IME_SWITCH_DELAY


print("目标窗口标题:", TARGET_WINDOW_TITLE)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("作家助手打字模拟器")
        self.master.geometry("600x400")
        self.create_widgets()
        self.setup_ui()

    def create_widgets(self):
        # 文本输入框
        self.text_area = tk.Text(self.master, wrap=tk.WORD)
        self.text_area.pack(pady=10, fill=tk.BOTH, expand=True)

        # 按钮框架
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=5)

        # 粘贴按钮
        tk.Button(btn_frame, text="粘贴内容", command=self.paste_content).pack(
            side=tk.LEFT, padx=5
        )
        # 开始按钮
        tk.Button(btn_frame, text="开始模拟", command=self.start_simulation).pack(
            side=tk.LEFT, padx=5
        )
        # 退出按钮
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
        try:
            # if not hasattr(config, 'TARGET_WINDOW_TITLE'):
            if not hasattr(self.config, "TARGET_WINDOW_TITLE"):
                raise AttributeError("缺少必要配置项：TARGET_WINDOW_TITLE")
        except AttributeError as e:
            messagebox.showerror("配置错误", str(e))
            return
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "请输入或粘贴需要模拟输入的内容")
            return

        self.master.iconify()  # 最小化窗口
        print(self.config.TARGET_WINDOW_TITLE)

        # if not activate_target_window(config.TARGET_WINDOW_TITLE):
        if not activate_target_window(self.config.TARGET_WINDOW_TITLE):
            messagebox.showerror("错误", "未检测到作家助手窗口！")
            self.master.deiconify()
            return

        try:
            switch_to_chinese_ime()
            time.sleep(1)  # 等待输入法切换
            pyautogui.click()  # 确保光标在输入框
            simulate_typing(content, config.TYPE_INTERVAL)
        except Exception as e:
            messagebox.showerror("错误", f"输入中断: {str(e)}")
        finally:
            self.master.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
