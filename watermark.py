
import sys
import cv2
import numpy
import os
# import requests
# import io
from PIL import Image, ImageDraw, ImageFont

 # truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
    # r = requests.get(truetype_url, allow_redirects=True)
font_path = 'AdobeSongStd-Light.otf' # "/System/Library/Fonts//Menlo.ttc"

def create_watermark(input_path, text, textSize):
    img = cv2.imread(input_path)
    # 判断是否是openCV图片类型
    if (isinstance(img, numpy.ndarray)):
        # 转化成PIL类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(font_path, size=textSize)
    # 绘制文本
    left = 100
    top = 100
    text = '仅用于华为招聘，请勿私自保存，2022-04-09'
    textColor = (168, 255, 103)
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV类型
    img2 = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
    # 保存图片
    output_path = resolve_output(input_path)
    cv2.imwrite(output_path, img2)
    cv2.imshow('img',img2)
    cv2.waitKey(0)
    # cv2.destoryAllWindows('img')

def add_water(input_path, text, fontsize):
    image = Image.open(input_path)
    # 字体文件
    fontsize = int(image.size[0] / 1800 * fontsize)
    print('image.size[0]:' + str(image.size[0]))
    print('fontsize: ' + str(fontsize))
    font = ImageFont.truetype(font_path, fontsize)

    mode = 'RGBA'
    # 添加背景
    new_img = Image.new(mode, (image.size[0] * 3, image.size[1] * 3), (255, 255, 255, 255))
    new_img.paste(image, image.size)
    # 添加水印
    font_len = len(text)
    rgba_image = new_img.convert(mode)
    text_overlay = Image.new(mode, rgba_image.size, (0, 0, 0, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    # 水印数量
    for i in range(0, rgba_image.size[0], font_len * 40 + 300):
        for j in range(0, rgba_image.size[1], 300):
            # print(f'i:{i}, j:{j}, text:{text}, font:{font}')
            image_draw.text((i, j), text, font=font, fill=(0, 0, 0, 50))
    # 水印文字角度
    text_overlay = text_overlay.rotate(45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    if image_with_text.mode in ("RGBA", "P"): 
        image_with_text = image_with_text.convert("RGB")

    output_path = resolve_output(input_path)    
    image_with_text.save(output_path)

def resolve_output(input_path):
    (output_dir, file_name) = os.path.split(input_path)
    output_dir = output_dir + '/out'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    (file_name, ext) = os.path.splitext(file_name)
    output_path = output_dir + '/' + file_name + '_wm' + ext
    print('output_path: ' + output_path)
    return output_path


def is_image(file):
    (_, ext) = os.path.splitext(file)
    return os.path.isfile and ext.lower().endswith(('.jpg', '.jpeg', '.png'))    

if __name__=='__main__':
    # create_watermark(sys.argv[1], sys.argv[2], 32)
    input_path = sys.argv[1]
    if len(sys.argv) < 3:
        text = '机密文档，请勿传阅'
    else:
        text = sys.argv[2]

    if os.path.isdir(input_path):
        dir = os.path.abspath(input_path)
        files = os.listdir(input_path)
        for file in files:
            if is_image(file):
                add_water(dir + '/' + file, text, 32)
    else:
        add_water(input_path, text, 32)