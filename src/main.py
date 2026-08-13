from PIL import Image

ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image_path, width=100):
    image = Image.open(image_path).convert("L")

    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.45)

    image = image.resize((width, height))

    pixels = image.load()

    ascii_lines = []

    for y in range(height):
        line = ""

        for x in range(width):
            pixel = pixels[x, y]

            index = pixel * (len(ASCII_CHARS) - 1) // 255
            line += ASCII_CHARS[index]

        ascii_lines.append(line)

    return ascii_lines


def create_svg(ascii_lines, output_path):
    char_width = 8
    char_height = 12

    width = len(ascii_lines[0]) * char_width
    height = len(ascii_lines) * char_height

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="black"/>',
    ]

    for y, line in enumerate(ascii_lines):
        escaped_line = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        svg_lines.append(
    f'<text x="0" y="{(y + 1) * char_height}" '
    f'font-family="monospace" font-size="12" '
    f'fill="white" opacity="0">'
    f'{escaped_line}'
    f'<animate '
    f'attributeName="opacity" '
    f'from="0" '
    f'to="1" '
    f'dur="2s" '
    f'begin="{y * 0.03}s" '
    f'repeatCount="indefinite" />'
    f'</text>'
)

    svg_lines.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(svg_lines))


ascii_lines = image_to_ascii("assets/profile.png")

create_svg(ascii_lines, "assets/ascii.svg")

print("SVG created successfully!")