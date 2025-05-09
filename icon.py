from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Создаем изображение 256x256 пикселей
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Рисуем круг
    circle_color = (47, 79, 79)  # Тёмный серо-зелёный
    draw.ellipse([20, 20, size-20, size-20], fill=circle_color)
    
    # Рисуем цифру "1"
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    text_color = (236, 240, 241)  # Светло-серый
    draw.text((size//2-30, size//2-60), "1", font=font, fill=text_color)
    
    # Сохраняем как .ico в нескольких размерах
    image.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    
    return 'icon.ico'

if __name__ == "__main__":
    create_icon() 