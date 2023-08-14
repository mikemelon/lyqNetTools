from pynput.mouse import Controller, Button

mouse = Controller()

print(f'当前鼠标位置：{mouse.position}')


# mouse.position = (100, 100)
mouse.move(100, 100)

print(f'当前鼠标位置：{mouse.position}')

# press + release 相当于一次单击
mouse.press(Button.right)
mouse.release(Button.right)

mouse.click(Button.right, 2)