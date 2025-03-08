from PIL import Image

# Размер изображения
width, height = 1024, 1024

# Доступные цвета
colors = {
    "1": ("violet", (130, 5, 255)),  # Фиолетовый
    "2": ("yellow", (255, 170, 0))   # Желтый
}

# Выводим меню выбора
print("Выберите цвет градиента:")
for key, (name, _) in colors.items():
    print(f"{key} - {name}")

# Ввод пользователя
color_choice = input("Введите номер цвета: ").strip()

# Проверяем ввод
if color_choice not in colors:
    print("Ошибка: неправильный номер!")
    exit(1)

# Получаем выбранный цвет
color_name, base_color = colors[color_choice]
white = (255, 255, 255)

# Создание изображения
img = Image.new('RGB', (width, height))

for y in range(height):
    for x in range(width):
        factor = (x * y) / (width * height)
        r = int(base_color[0] * (1 - factor) + white[0] * factor)
        g = int(base_color[1] * (1 - factor) + white[1] * factor)
        b = int(base_color[2] * (1 - factor) + white[2] * factor)
        img.putpixel((x, y), (r, g, b))

# Сохранение изображения
filename = f'gradient-{color_name}.png'
img.save(filename)
print(f"Градиент сохранен как {filename}")
