from PIL import Image
import pyautogui
# pyautogui.mouseInfo()
im = pyautogui.screenshot()  # 截取整个屏幕
om = im.crop((220, 180, 315, 320))  # 根据截取的屏幕仅截取“带赞的手势图片”，可以用pyautogui.mouseInfo()获取图片的位置(左284,上416,右302,下438)
om.save("success.png")  # 将图片保存供pyautogui.locateOnScreen（）使用
