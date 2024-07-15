from django.shortcuts import render
from django.http import HttpResponse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from .models import Dt


def index(request):
    return render(request, 'ticker/index.html')


def create_video(request):
    if request.method == 'POST':
        # Получаем данные из формы
        text_video = request.POST.get('text_video')

        # Сохранение запроса в базу данных
        video_request = Dt.objects.create(content=text_video)

        # Размеры видео (ширина x высота)
        width, height = 100, 100

        # Задаём параметры: адрес и имя файла, видеопоток с частотой 24 кадра в секунду
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_dir = os.path.join(base_dir, "ticker/static/videos")
        video_path = os.path.join(video_dir, "сто_на_сто_3_сек.mp4")
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

        # Начальные координаты для бегущей строки
        x, y = width, height // 2

        # Путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), 'static/fonts/ofont.ru_Times New Roman.ttf')
        if not os.path.exists(font_path):
            return HttpResponse(f"Font file not found: {font_path}", status=500)

        font = ImageFont.truetype(font_path, 20)

        for t in range(72):  # 3 секунды с частотой 24 кадра/сек
            # Создаем кадр с черным фоном
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Преобразуем кадр в изображение для Pillow
            pil_img = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_img)

            # Смещаем координаты по оси Х для эффекта бегущей строки
            # Подгоняем скорость бегущей строки под длину текста
            x -= len(text_video) / 7

            # Добавляем текст
            draw.text((x, y), text_video, font=font, fill=(255, 255, 255, 255))

            # Преобразуем изображение обратно в кадр OpenCV
            frame = np.array(pil_img)

            # Записываем кадр
            out.write(frame)

        # Закрываем видеопоток
        out.release()

        # Возвращаем видео как HTTP-ответ
        with open(video_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'inline; filename="сто_на_сто_3_сек.mp4"'
            return response

    return HttpResponse("Invalid request method", status=405)
