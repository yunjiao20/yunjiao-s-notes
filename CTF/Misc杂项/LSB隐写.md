---
tags:
  - 2026/9/7
  - CTF
  - Python
---
LSB（Least Significant Bit 最低有效位）隐写

使用工具`stegsolve.jar`，下载
```sh
wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
```
运行使用
```sh
java -jar stegsolve.jar
```



或者，我写了一个python模块（实际就两个函数）来实现隐写和提取
```python
#!/bin/python

'''
用于实现RGB隐写和提取，提供了两个函数，允许你在png任意通道及其组合、二进制位
隐写和读取
'''


from PIL import Image
import math

def embed_message(img_path: str,
                  msg     : str,
                  channels: str,
                  output_path: str,
                  embed_position: int = -1) -> None:
    '''
    将信息嵌入到图像的信息中

    img_path: str  原始图片路径
    msg     : str  嵌入到秘密字符串（ASCII），utf-8可以使用base64
    channels: str  嵌入通道，只允许'R'/'G'/'B'三个字符的一个或多个，
                   RGB的顺序是字节插入像素信道的顺序
    output_path: str  输出图片路径
    embed_position: int = -1  嵌入位置，默认为 -1 (最低有效位LSB)，
                              应为一个负数
    '''
    # 检查通道信息
    channels = channels.lower()  # 小写方便后面处理
    if all([c in 'rgb' for c in channels]) is False:
        raise ValueError('argv \'channels\' must in \'RGB\' 参数channel是且只能是\'RGB\'中的一个或多个字符')
    channels = [dict(zip('rgb', range(3)))[c] for c in channels]    # rgb改为0、1、2下标，提高性能

    # 用于嵌入的函数
    def embed(byte: int, bit: str, ep = embed_position) -> int:
        '''嵌入信息'''
        bin_s = bin(byte)
        return eval(f'{bin_s[:ep]}{bit}{bin_s[ep:][1:]}')

    # 打开图像并转换为 RGB 模式
    # 请确保图片是标准的RGB三通道模式，而非RGBA等
    img = Image.open(img_path).convert('RGB')

    # 获取图片像素数据
    # list(img.getdata()) 返回一个列表，每一个元素是一个元组(R, G, B)
    #   如：[(128, 255, 0), ..., (25, 42, 9)]
    pixels = list(img.getdata())

    # 将嵌入信息msg转换为二进制字符串
    # format(..., '08b') 将其转换为 8 位二进制字符串
    bin_msg = ''.join([format(ord(char), '08b') for char in msg])

    # 检查图像容量是否足以插入文件
    if len(bin_msg) > (len(pixels) * len(channels)):
        # len(bin_msg) 插入的字节数
        # len(pixels) 像素数量
        # len(channels)使用多少个通道，即一个像素可以保存多少字节
        raise ValueError('image too small to keep message 图片太小，不足以嵌入所有信息')

    # 嵌入信息
    msg_index    = 0    # 嵌入信息bin_msg的索引
    pixels_index = 0    # 像素pixels的索引

    for pixel in pixels:
        r, g, b = pixel  # 各个信道的信息

        for channel in channels:  # 按输入信道channels的顺序向信道嵌入数据
            if msg_index >= len(bin_msg):  # 字符串插入完，不处理
                break
            #exec(f'{channel} = embed({channel}, bin_msg[msg_index])') # 如 r = embed(r)
            # !!!exec内无法修改修改变量（不指定作用域），且性能黑洞!!!这里改用if-elif-else
            if   channel == 0:
                r = embed(r, bin_msg[msg_index])
            elif channel == 1:
                g = embed(g, bin_msg[msg_index])
            else:
                b = embed(b, bin_msg[msg_index])

            msg_index += 1

        pixels[pixels_index] = (r, g, b)  # 修改成嵌入后的数据
        pixels_index += 1

    # 保存修改后的图像
    # 为了保留 LSB 信息，必须保存为无损格式如 PNG
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    new_img.save(output_path)
    print(f'信息已嵌入，新图片为 {output_path}')

    return output_path



def extract_message(image_path: str,
                    channels  : str,
                    extract_position: int = -1) -> list[str]:
    '''
    重图片中提取信息

    image_path: str  提取对象图片的地址
    channels  : str  提取的信道（'RGB'中的一个或多个，其顺序为每个像
                     素提取的信道顺序）
    extract_position: int = -1  每个信道数据的提取位置，应为负数。默认
                                为-1（最低有效位LSB）
    '''
    # 检查通道信息
    channels = channels.lower()  # 小写方便后面处理
    if all([c in 'rgb' for c in channels]) is False:
        raise ValueError('argv \'channels\' must in \'RGB\' 参数channels是且只能是\'RGB\'中的一个或多个字符')
    channels = [dict(zip('rgb', range(3)))[c] for c in channels]    # rgb改为0、1、2下标，提高性能

    # 打开图像并获取数据，注释详见函数embed_message
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())

    # 在字节中提取信息的方法
    def extract(byte: int, ep = extract_position) -> str:
        '''提取字节中extract_position处的信息'''
        return format(10, '08b')[ep]

    # 遍历像素提取信息
    bin_msg = ''
    for pixel in pixels:
        for channel in channels:  # 按输入信道channels的顺序提取信道信息
            bin_msg += extract(pixel[channel])

    # 二进制字符串转为ASCII字符
    ascii_s = ''
    for i in range(0, len(bin_msg), 8):
        # 每 8 位二进制转换为整数
        byte = bin_msg[i:i+8]

        ascii_s += chr(int(byte, 2))

    return ascii_s



if __name__ == '__main__':
    print('提供了用于嵌入和提取png图片LSB信息的功能，不支持直接运行')
    print('请使用其中包含的embed_message和extract_message函数')
```
