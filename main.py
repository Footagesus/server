from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/api/pixelate', methods=['POST'])
def pixelate():
    data = request.json
    image_url = data.get('image_url')
    pixel_size = data.get('pixel_size', 10)
    
    # Проверяем, если передана ссылка на изображение
    if not image_url:
        return jsonify({'error': 'Image URL not provided'}), 400
    
    # Загружаем изображение по ссылке
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Пикселизация изображения
    img = img.resize(
        (img.size[0] // pixel_size, img.size[1] // pixel_size),
        Image.NEAREST
    )
    img = img.resize(
        (img.size[0] * pixel_size, img.size[1] * pixel_size),
        Image.NEAREST
    )
    
    # Преобразуем изображение в список пикселей
    pixels = list(img.getdata())
    pixel_array = []
    width, height = img.size
    for y in range(height):
        row = []
        for x in range(width):
            row.append(pixels[y * width + x][:3])  # Берем RGB
        pixel_array.append(row)
    
    return jsonify(pixel_array)

if __name__ == '__main__':
    app.run(debug=True)
