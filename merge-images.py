from PIL import Image
import sys


def merge_images(file1, file2, file3, file4):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    image3 = Image.open(file3)
    image4 = Image.open(file4)

    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size

    result_width = max(width1, width3) + max(width2, width4)
    result_height = max(height1, height2) + max(height3, height4)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.paste(im=image3, box=(0, height1))
    result.paste(im=image4, box=(width1,height2))
    return result

mergedImage = merge_images(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
mergedImage.save(sys.argv[1])
