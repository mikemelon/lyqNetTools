import io
from PIL import Image

# 测试：将图片转为二进制数组对象(bytes)的两种方式。

im = Image.open(r'C:\Users\mikemelon2021\Pictures\啊啊啊.png')
# 第1种方式，无需使用图片文件，直接使用Image对象即可。
bytes_io = io.BytesIO()
im.save(bytes_io, format='PNG') # 直接将Image对象转换为二进制
image_bytes1 = bytes_io.getvalue()
print(image_bytes1)

# 第2种方式，需要有图片文件（提供文件路径）
with open(r'C:\Users\mikemelon2021\Pictures\啊啊啊.png', 'rb') as f:
    image_bytes2 = f.read()
    print(image_bytes2)

# im_show = Image.open(io.BytesIO(image_bytes1))
im_show = Image.open(io.BytesIO(image_bytes2))
im_show.show() # 较为奇怪的是，两种方式的二进制有细微区别，但都能显示同样的图像