class Color:  # Класс для цвета с функцией трансформации RGB-схемы в LAB
    def __init__(self, hex_color):
        hex_color = hex_color.strip('#')
        self.red = int(hex_color[0:2], 16)
        self.green = int(hex_color[2:4], 16)
        self.blue = int(hex_color[4:], 16)

    def rgb_to_lab(self):
        input_color = (self.red, self.green, self.blue)
        num = 0
        rgb = [0, 0, 0]

        for value in input_color:
            value = float(value) / 255
            if value > 0.04045:
                value = ((value + 0.055) / 1.055) ** 2.4
            else:
                value = value / 12.92
            rgb[num] = value * 100
            num += 1

        xyz = [0, 0, 0, ]

        x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
        y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
        xyz[0] = round(x, 4)
        xyz[1] = round(y, 4)
        xyz[2] = round(z, 4)

        xyz[0] = float(xyz[0]) / 95.047
        xyz[1] = float(xyz[1]) / 100.0
        xyz[2] = float(xyz[2]) / 108.883

        num = 0
        for value in xyz:

            if value > 0.008856:
                value = value ** 0.3333333333333333
            else:
                value = (7.787 * value) + (16 / 116)

            xyz[num] = value
            num += 1

        lab = [0, 0, 0]

        l = (116 * xyz[1]) - 16
        a = 500 * (xyz[0] - xyz[1])
        b = 200 * (xyz[1] - xyz[2])

        lab[0] = round(l, 4)
        lab[1] = round(a, 4)
        lab[2] = round(b, 4)

        return lab


def calculation(name, input_color):  # вычисление "вектора" между двумя парами кортежей (r,g,b)
    color1 = Color(name)
    color2 = Color(input_color)
    x = color1.rgb_to_lab()
    y = color2.rgb_to_lab()
    distance = round(((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2) ** 0.5, 2)
    return distance

