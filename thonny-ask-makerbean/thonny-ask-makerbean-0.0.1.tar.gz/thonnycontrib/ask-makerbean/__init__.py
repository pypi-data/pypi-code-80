import os
import sys
import datetime
import time
import platform
import requests
import pyperclip
from thonny import get_workbench, get_shell, ui_utils
from thonny.common import get_python_version_string
from thonny.ui_utils import CommonDialog
import tkinter as tk
import tkinter.font
from tkinter import ttk


class ShowUrlDialog(CommonDialog):
	def __init__(self, master, question_id):
		import webbrowser
		self.question_id = question_id

		super().__init__(master)

		main_frame = ttk.Frame(self)
		main_frame.grid(sticky=tk.NSEW, ipadx=15, ipady=15)
		main_frame.rowconfigure(0, weight=1)
		main_frame.columnconfigure(0, weight=1)

		self.title("提问")

		heading_font = tkinter.font.nametofont("TkHeadingFont").copy()
		heading_font.configure(size=19, weight="bold")
		heading_label = ttk.Label(
			main_frame, justify=tk.CENTER, text="问题链接", font=heading_font
		)
		heading_label.grid()

		url = f"https://makerbean.com/ask/get/{question_id}"
		url_font = tkinter.font.nametofont("TkDefaultFont").copy()
		url_font.configure(underline=1)
		url_label = ttk.Label(
			main_frame, text=url, style="Url.TLabel", cursor="hand2", font=url_font
		)
		url_label.grid()
		url_label.bind("<Button-1>", lambda _: webbrowser.open(url))

		self.copy = ttk.Button(main_frame, text="复制链接", command=self._copy, default="active")
		self.copy.grid(pady=(0, 15))
		self.copy.focus_set()

	def _copy(self, event=None):
		pyperclip.copy(f"https://makerbean.com/ask/get/{self.question_id}")

	def on_cancel(self):
		self.destroy()


class AskDialog(CommonDialog):
	def __init__(self, master):
		self.info = {}
		self.upload_done = False

		super().__init__(master)

		main_frame = ttk.Frame(self)
		main_frame.grid(sticky=tk.NSEW, ipadx=15, ipady=15)
		main_frame.rowconfigure(0, weight=1)
		main_frame.columnconfigure(0, weight=1)

		self.title("提问")
		# self.resizable(height=tk.TRUE, width=tk.FALSE)

		heading_font = tkinter.font.nametofont("TkHeadingFont").copy()
		heading_font.configure(size=19, weight="bold")
		heading_label = ttk.Label(
			main_frame, justify=tk.CENTER, text="向我们提问", font=heading_font
		)
		heading_label.grid()

		if platform.system() == "Linux":
			try:
				import distro

				system_desc = distro.name(True)
			except ImportError:
				system_desc = "Linux"

			if "32" not in system_desc and "64" not in system_desc:
				system_desc += " " + self.get_os_word_size_guess()
		else:
			system_desc = (
				platform.system() + " " + platform.release() + " " + self.get_os_word_size_guess()
			)

		self.info['platform'] = system_desc + "\n" + "Python " + get_python_version_string(maxsize=sys.maxsize)
		platform_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			text=self.info['platform'],
		)
		platform_label.grid(pady=20)

		label_font = tkinter.font.nametofont("TkDefaultFont").copy()
		label_font.configure(size=16, weight="bold")

		self.info['student_id'] = get_workbench().get_option('student_id', '')
		student_id_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			text="学号",
			font=label_font
		)
		student_id_label.grid(pady=16)
		self.student_id_input = ttk.Entry(main_frame)
		self.student_id_input.delete(0, "end")
		self.student_id_input.insert(0, self.info['student_id'])
		self.student_id_input.grid()

		self.info['code'] = self.get_code()
		code_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			text="代码",
			font=label_font
		)
		code_label.grid(pady=16)
		self.code_input = tk.Text(main_frame, height=5)
		self.code_input.delete(1.0, "end")
		self.code_input.insert(1.0, self.info['code'])
		self.code_input.grid()

		self.info['shell'] = self.get_shell()
		shell_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			text="终端信息",
			font=label_font
		)
		shell_label.grid(pady=16)
		self.shell_input = tk.Text(main_frame, height=5)
		self.shell_input.delete(1.0, "end")
		self.shell_input.insert(1.0, self.info['shell'])
		self.shell_input.grid()

		additional_content_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			text="补充内容",
			font=label_font
		)
		additional_content_label.grid(pady=16)
		self.additional_content_input = tk.Text(main_frame, height=5)
		self.additional_content_input.grid()

		status_font = tkinter.font.nametofont("TkDefaultFont").copy()
		status_font.configure(size=12)
		self.status_string = tk.StringVar()
		self.status_string.set("等待上传")
		self.status_label = ttk.Label(
			main_frame,
			justify=tk.CENTER,
			textvariable=self.status_string,
			font=status_font
		)
		self.status_label.grid(pady=14)
		self.submit_button = ttk.Button(main_frame, text="提交", command=self._submit, default="active")
		self.submit_button.grid(pady=(0, 15))
		self.submit_button.focus_set()

		# self.bind("<Return>", self._submit, True)
		# self.bind("<Escape>", self._submit, True)

	def get_code(self):
		current_editor = get_workbench().get_editor_notebook().get_current_editor()
		code = current_editor.get_text_widget().get("1.0", "end")
		return code

	def get_shell(self):
		current_shell = get_shell()
		return current_shell.text.get("1.0", "end")

	def upload_info(self):
		time.sleep(2)
		self.info['student_id'] = self.student_id_input.get()
		get_workbench().set_option('student_id', self.info['student_id'])
		self.info['additional_content'] = self.additional_content_input.get("1.0", "end")
		self.info['language'] = 'python'
		req = requests.post("https://makerbean.com/ask/upload/", data=self.info)
		result = req.json()
		if result['status'] == 0:
			self.upload_done = True
			question_id = result['question_id']
			ui_utils.show_dialog(ShowUrlDialog(get_workbench(), question_id))
			self.destroy()
		else:
			self.status_string.set("上传失败，请重试...")
			self.status_label.update_idletasks()

	def _submit(self, event=None):
		self.status_string.set("请稍等，正在上传，上传完成后会自动关闭...")
		self.status_label.update_idletasks()
		self.upload_info()

	def on_cancel(self):
		self.destroy()

	def get_os_word_size_guess(self):
		if "32" in platform.machine() and "64" not in platform.machine():
			return "(32-bit)"
		elif "64" in platform.machine() and "32" not in platform.machine():
			return "(64-bit)"
		else:
			return ""


def open_ask_makerbean_dialog():
	ui_utils.show_dialog(AskDialog(get_workbench()))


def load_plugin():
	get_workbench().add_command(
		command_id="ask_makerbean",
		menu_name="tools",
		image=os.path.join(os.path.dirname(__file__), "res", "ask.png"),
		command_label="Ask makerbean",
		caption="Ask makerbean",
		handler=open_ask_makerbean_dialog,
		include_in_toolbar=True
	)
