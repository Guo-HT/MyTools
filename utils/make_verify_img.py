# 生成网站登陆时4位验证码图片
import random
from io import BytesIO
import base64
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def get_random_char():
    char_all = [i for i in range(48, 58)] + [i for i in range(65, 91)]
    verify_code_list = [chr(random.choice(char_all)) for i in range(4)]
    return "".join(verify_code_list)


def get_random_color(low, high):
    return random.randint(low, high), random.randint(low, high), random.randint(low, high)


def get_verify_img():
    width, height = 180, 60
    verify_char = get_random_char()
    img = Image.new("RGB", (width, height), get_random_color(20, 100))
    font = ImageFont.truetype("/home/pi/Code/Django_proj/MyTools/static/font/STXINGKA/STXINGKA.ttf", 45)
    draw = ImageDraw.Draw(img)

    for i in range(4):
        top_blank = random.randint(5, 15)
        draw.text((45 * i + 5, top_blank), verify_char[i], font=font, fill=get_random_color(100, 200))

    for x in range(random.randint(200, 600)):
        x, y = random.randint(1, width - 1), random.randint(1, height - 1)
        draw.point((x, y), fill=get_random_color(50, 150))
    img = img.filter(ImageFilter.BLUR)
    # img.save("./verify.png")
    output_buffer = BytesIO()
    img.save(output_buffer, format="JPEG")
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str, verify_char

if __name__ == "__main__":
    get_verify_img()