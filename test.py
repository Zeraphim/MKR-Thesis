# import sys
# import pytesseract
# from difflib import SequenceMatcher as SQ

# try:
#     from PIL import Image
# except ImportError:
#     import Image

# raw_string = pytesseract.image_to_string("/Users/zeraphim/Desktop/aaa.png", lang="eng", config='--psm 7')  # eng or example_model

# print(raw_string)

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= r"gvision_auth.json"


def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    print(
                        "Word text: {} (confidence: {})".format(
                            word_text, word.confidence
                        )
                    )

                    for symbol in word.symbols:
                        print(
                            "\tSymbol: {} (confidence: {})".format(
                                symbol.text, symbol.confidence
                            )
                        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

# def detect_document(path):
#     """Detects document features in an image."""
#     from google.cloud import vision

#     client = vision.ImageAnnotatorClient()

#     with open(path, "rb") as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)

#     response = client.document_text_detection(image=image)

#     for page in response.full_text_annotation.pages:
#         for block in page.blocks:
#             for paragraph in block.paragraphs:
#                 for word in paragraph.words:
#                     word_text = "".join([symbol.text for symbol in word.symbols])
#                     print(word_text, end=' ')
#     print()  # Print a newline at the end

img_path = "/Users/zeraphim/Desktop/MKR-Thesis/demo_images/s1.png"

detect_document(img_path)