# PDF TO IMAGE CONVERSION
# Important libraries which have to be installed in windows.
# - Poppler. See: https://pypi.org/project/pdf2image/


# IMPORT LIBRARIES
import pdf2image
from PIL import Image, ImageChops
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

if __name__ == "__main__":
    original = "affuteuse_original.pdf"
    loaded = "affuteuse_loaded.pdf"
    pil_images_original = pdftopil(original)
    pil_images_loaded = pdftopil(loaded)

    assert len(pil_images_loaded) == len(pil_images_original), "Number of pages does not match"

    diffs = []
    for i in range(len(pil_images_original)):
        diff = ImageChops.difference(pil_images_original[i], pil_images_loaded[i])
        diff = ImageChops.invert(diff)
        #diff.show()
        diffs.append(diff)
    filename = "Difference"
    diffs[0].save(filename + ".pdf", save_all=True, append_images=diffs[1:])
