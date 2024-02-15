from PIL import Image
import struct

# A4E05
# A4F22

# Data structure is Palette size
# Number of bytes for data structure is Palette size * 3 since each value is RGB
# Each part of the palette is indexed starting at 0x10


def create_image(width, height, imageData, palette):
    # Create a new blank image with the specified dimensions
    image = Image.new("RGB", (width, height))

    # Validate that the color array has enough colors for each pixel
    # num_pixels = width * height
    # if len(color_array) < num_pixels:
        # raise ValueError(f"Color array must have at least {num_pixels} colors.")

    paletteLen = len(palette)

    # Iterate through each pixel and assign the corresponding color
    for y in range(height):
        for x in range(width):
            # pixel_index = y * width + x
            # color = palette[colorId]
            # colorIndex = imageData[x][y] % paletteLen
            colorIndex = imageData[x][y] - 0x10
            c = palette[colorIndex]
            c = (min(int(c[0]*4), 255),min(int(c[1] * 4), 255),min(int(c[2]*4), 255))
            # print(f'color index: {colorIndex}')
            image.putpixel((x, y), c)

    return image

# Example usage:
if __name__ == "__main__":
    f = open('CELS3', 'rb')

    f.seek(0xA4E03)
    paletteLen = 0
    paletteData = []

    paletteLenRaw = struct.unpack("<h",f.read(2))[0]
    paletteLen = paletteLenRaw // 3

    for x in range(paletteLen):
        r = struct.unpack("b",f.read(1))[0]
        g = struct.unpack("b",f.read(1))[0]
        b = struct.unpack("b",f.read(1))[0]
        paletteData.append((r,g,b))

    for x in range(256 - paletteLen):
        paletteData.append((0,0,0))

    paletteSample = []
    paletteSample.append(range(64))
    paletteSample.append(range(64,128))
    paletteSample.append(range(128,192))
    paletteSample.append(range(192,256))

    generated_image = create_image(4, 64, paletteSample, paletteData)
    generated_image.save("palette.png")

    img1Offset = struct.unpack("<i",f.read(4))[0]

    # print(img1Offset)
    f.seek(img1Offset)

    bytesToRead = struct.unpack("b",f.read(1))[0]
    if bytesToRead == 0:
        print('bypassing, read value 0')

    imageDataLen = struct.unpack("<h",f.read(2))[0]

    # Specify image dimensions
    image_width = struct.unpack("<h",f.read(2))[0]
    image_height = struct.unpack("<h",f.read(2))[0]

    pyroImageData = f.read(imageDataLen - 4)

    print(f'Data len: {imageDataLen} | width: {image_width} | height: {image_height}')

    imageData = []

    for x in range(image_width):
        imageData.append(list(range(image_height)))

    x = 0
    y = 0
    i = 0

    while i < len(pyroImageData) - 2:

        if pyroImageData[i] & 0xF0 == 0x80:
            numColors = (pyroImageData[i] & 0xF) * 1
            i = i + 1
            # print(f'Draw {numColors} pixels')
            for ix in range(numColors):
                imageData[x][y] = pyroImageData[i+ix]
                y = y + 1
            i = i + (numColors)
        elif pyroImageData[i] & 0xF0 == 0xD0:
            numColors = (pyroImageData[i] & 0xF) + 16
            i = i + 1
            fillColor = pyroImageData[i]
            if numColors == 0:
                numColors = 3
            # print(f'Fill {numColors} pixels | orig {(pyroImageData[i-1] & 0xF)}')
            for ix in range(numColors):
                imageData[x][y] = fillColor
                # imageData[x][y] = 0
                y = y + 1
            i = i + 1
        elif pyroImageData[i] & 0xF0 == 0xC0:
            numColors = pyroImageData[i] & 0xF
            i = i + 1
            fillColor = pyroImageData[i]
            # print(f'Fill {numColors} pixels')
            for ix in range(numColors):
                imageData[x][y] = fillColor
                # imageData[x][y] = 0
                y = y + 1
            i = i + 1
        elif pyroImageData[i] & 0xF0 == 0xB0:
            numColors = 0x30 | (pyroImageData[i] & 0xF)
            i = i + 1
            # print(f'Draw {numColors} pixels')
            for ix in range(numColors):
                imageData[x][y] = pyroImageData[i+ix]
                # imageData[x][y] = 0
                y = y + 1
            i = i + (numColors)
        elif pyroImageData[i] & 0xF0 == 0xA0:
            numColors = 0x20 | (pyroImageData[i] & 0xF)
            i = i + 1
            # print(f'Draw {numColors} pixels')
            for ix in range(numColors):
                imageData[x][y] = pyroImageData[i+ix]
                # imageData[x][y] = 0
                y = y + 1
            i = i + (numColors)
        elif pyroImageData[i] & 0xF0 == 0x90:
            numColors = 0x10 | (pyroImageData[i] & 0xF)
            i = i + 1
            # print(f'Draw {numColors} pixels')
            for ix in range(numColors):
                imageData[x][y] = pyroImageData[i+ix]
                # imageData[x][y] = 0
                y = y + 1
            i = i + (numColors)
        elif pyroImageData[i] & 0xF0 == 0x40:
            # print(f'40 advance to next line {img1Offset+7+i} y: {y}')
            y = 0
            x = x + 1
            i = i + 1
        else:
            print (f'control error! {x}, {y}, {i} < {len(pyroImageData)} | {img1Offset + 7 + i}')
            exit()


    print(f'palette len: {paletteLen}')

    try:
        generated_image = create_image(image_width, image_height, imageData, paletteData)
        generated_image.save("output_image.png")
        print("Image created successfully! Saved as 'output_image.png'")
    except ValueError as e:
        print(f"Error: {e}")
