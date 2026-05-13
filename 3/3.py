from PIL import Image


# Загрузка координат из файла
def load_coords(filename):

    coords = []

    with open(filename, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if line != "":

                # Убираем скобки
                line = line.replace("(", "")
                line = line.replace(")", "")

                # Делим строку по запятой
                x, y = line.split(",")

                coords.append((int(x), int(y)))

    return coords

# 1.1 Декодирование из синего канала
def decode_blue(img_path, coords):

    img = Image.open(img_path).convert("RGB")

    pixels = img.load()

    text = ""

    for x, y in coords:

        r, g, b = pixels[x, y]

        # Каждый байт хранится в синем канале
        text += chr(b)

    return text


def encode_rg(img_path, text, coords, output="encoded.png"):

    img = Image.open(img_path).convert("RGB")

    pixels = img.load()

    data = text.encode("utf-8")

    print("Кодирование\n")

    for i in range(len(data)):
        
        x, y = coords[i]

        r, g, b = pixels[x, y]

        # Берем один байт текста
        byte = data[i]


        left_bits = byte >> 4
        right_bits = byte & 15


        new_r = (r & 240) | left_bits
        new_g = (g & 240) | right_bits

        # Записываем измененный пиксель
        pixels[x, y] = (new_r, new_g, b)

        # Информация для первого символа
        if i == 0:
            print(x,y)
            print("Первый байт текста:")
            print(byte)

            print("\nБиты первого байта:")
            print(bin(byte)[2:].zfill(8))

            print("\nИсходный пиксель:")
            print(f"R={r}, G={g}, B={b}")

            print("\nИзмененный пиксель:")
            print(f"R={new_r}, G={new_g}, B={b}")

            print()

    img.save(output)

    return output, len(data)


# Декодирование из R и G
def decode_rg(img_path, coords, length):

    img = Image.open(img_path).convert("RGB")

    pixels = img.load()

    data = []

    for i in range(length):

        x, y = coords[i]

        r, g, b = pixels[x, y]

        left_bits = r & 15
        right_bits = g & 15


        byte = (left_bits << 4) | right_bits

        data.append(byte)

    # Превращаем байты обратно в текст
    text = bytes(data).decode("utf-8")

    return text


# Главная программа
if __name__ == "__main__":

    image_name = "new34.png"

    keys_file = "keys34.txt"

    # Загружаем координаты
    coords = load_coords(keys_file)

    # 1.1 Декодирование

    blue_text = decode_blue(image_name, coords)

    print("Декодирование исходного изображения\n")

    print("Декодированный текст: ", blue_text)

    # 1.2 Кодирование

    secret = input("\nВведите текст: ")

    encoded_image, size = encode_rg(image_name, secret,coords)

    # Проверка декодирования

    decoded_text = decode_rg(encoded_image, coords, size)

    print("Декодированный текст: \n")

    print(decoded_text)