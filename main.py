# PDF TO IMAGE CONVERSION
# Important libraries which have to be installed in windows.
# - Poppler. See: https://pypi.org/project/pdf2image/


# IMPORT LIBRARIES
import pdf2image
from PIL import Image, ImageChops, ImageOps
import time

# DECLARE CONSTANTS
DPI = 300
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False


def pdftopil(pdf_path):
    # This method reads a pdf and converts it into a sequence of images
    # PDF_PATH sets the path to the PDF file
    # dpi parameter assists in adjusting the resolution of the image
    # output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
    # first_page parameter allows you to set a first page to be processed by pdftoppm
    # last_page parameter allows you to set a last page to be processed by pdftoppm
    # fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
    # thread_count parameter allows you to set how many thread will be used for conversion.
    # userpw parameter allows you to set a password to unlock the converted PDF
    # use_cropbox parameter allows you to use the crop box instead of the media box when converting
    # strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError

    poppler_path = r"Poppler\poppler-\bin"

    start_time = time.time()
    pil_images = pdf2image.convert_from_path(pdf_path, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE,
                                             last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD,
                                             use_cropbox=USE_CROPBOX, strict=STRICT, poppler_path=poppler_path)
    print("Time taken : " + str(time.time() - start_time))
    return pil_images

def difference(image1, image2):
    # features not in loaded
    diff1 = ImageChops.subtract(image1, image2)
    diff1 = ImageChops.invert(diff1)
    diff1 = ImageOps.colorize(diff1.convert("L"), black="red", white="white", )

    # elements in loaded, but not in original
    diff2 = ImageChops.subtract(image2, image1)
    diff2 = ImageChops.invert(diff2)
    diff2 = ImageOps.colorize(diff2.convert("L"), black="green", white="white")

    diff = ImageChops.add_modulo(diff1, diff2)
    # diff1.show()
    # diff2.show()
    # diff.show()

    return diff


if __name__ == "__main__":
    original = "affuteuse_original.pdf"
    loaded = "affuteuse_loaded.pdf"
    new_loaded = "affuteuse_new_loaded.pdf"
    pil_images_original = pdftopil(original)
    pil_images_loaded = pdftopil(loaded)
    pil_images_new_loaded = pdftopil(new_loaded)

    assert len(pil_images_loaded) == len(pil_images_original) == len(pil_images_new_loaded), "Number of pages does not match"

    diffs = []
    diffs2 = []
    for i in range(len(pil_images_original)):


        diff = difference(pil_images_original[i], pil_images_loaded[i])
        #diff.show()
        diffs.append(diff)

        diff2 = difference(pil_images_original[i], pil_images_new_loaded[i])
        diffs2.append(diff2)

    filename = "Difference"
    diffs[0].save(filename + ".pdf", save_all=True, append_images=diffs[1:])

    filename = "Difference2"
    diffs2[0].save(filename + ".pdf", save_all=True, append_images=diffs2[1:])
