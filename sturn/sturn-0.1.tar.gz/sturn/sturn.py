import pyautogui

def turn(side):
	if side == "right":
		pyautogui.hotkey('ctrl', 'alt', 'right')
	elif side == "left":
		pyautogui.hotkey('ctrl', 'alt', 'left')
	elif side == "up":
		pyautogui.hotkey('ctrl', 'alt', 'up')
	elif side == "down":
		pyautogui.hotkey('ctrl', 'alt', 'down')