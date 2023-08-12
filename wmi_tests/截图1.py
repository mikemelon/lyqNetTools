import os
import sys
import argparse
import pyautogui

if __name__ == '__main__':
    temp_path = os.getenv('TEMP')
    # print(temp_path)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=False, help='文件名',default='screen_shot.png')
    parser.add_argument('-t', required=False, type=bool, help='是否保存到临时目录（true保存到临时目录，false(默认)保存到当前目录', default=False)

    args = parser.parse_args()
    if args.t:
        save_file = os.path.join(temp_path, args.f)
    else:
        save_file = args.f

    im = pyautogui.screenshot()
    im.save(save_file)