from PIL import Image, ImageDraw, ImageFilter, ImageFont


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def get_poster(oig_img,poster_path):
    # 加载原始图像
    original_image = Image.open(oig_img)
    # 计算处理后的图像尺寸
    width, height = original_image.size
    processed_width = width
    processed_height = height - height // 6
    # 创建处理后的图像
    processed_image = Image.new("RGB", (processed_width, processed_height))
    # 复制原图的上半部分到处理后的图像的上半部分
    processed_image.paste(original_image.crop((0, height // 6, width, height)), (0, 0))
    # 缩小原图为圆形头像
    avatar_size = processed_width // 3
    avatar_image = original_image.resize((avatar_size, avatar_size)).convert("RGBA")
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    avatar_image.putalpha(mask)

    # 缩小原图为方形头像
    square_avatar_size = processed_width // 2
    square_avatar_image = original_image.resize((avatar_size, avatar_size)).convert("RGBA")
    square_avatar_image = square_avatar_image.crop((0, 0, avatar_size, avatar_size))

    # 创建虚化淡化的原图
    blurred_image_tmp = original_image.crop((0, height // 6, width, height - height // 4))
    blurred_image = blurred_image_tmp.filter(ImageFilter.GaussianBlur(radius=10))
    blurred_image = blurred_image.crop((0, 0, width, height))
    # 在淡化的图上放置文字
    text = "IT'S'HELP THE LUCK STICK"
    font = ImageFont.truetype("Arial.ttf", 42)  # 替换为合适的字体文件路径和字体大小
    draw = ImageDraw.Draw(blurred_image)
    text_width, text_height = textsize(text, font=font)
    text_position = ((processed_width - text_width) // 2 + 200, (processed_height) // 2 - 150)
    draw.text(text_position, text, fill=(79,79,79), font=font)
    # 创建最终的海报
    poster = Image.new("RGB", (width, height + height // 4))
    poster.paste(processed_image, (0, 0))
    poster.paste(blurred_image, (0, processed_height))
    # 在最终海报上放置头像
    poster.paste(avatar_image, (processed_width - avatar_size, processed_height - avatar_size // 2), avatar_image)
    poster.paste(square_avatar_image, (processed_width//16, processed_height+height // 16), square_avatar_image)

    # 显示或保存海报
    poster.show()
    poster.save(poster_path)

if __name__ == '__main__':
    get_poster("041.png", "poster.jpg")