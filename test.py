import sys
import pytesseract
from difflib import SequenceMatcher as SQ

try:
    from PIL import Image
except ImportError:
    import Image

# lang = sys.argv[1]

# img_path = 'data/validation/0.tif'
img_path = '0.tif'
img = Image.open(img_path)
raw_text = pytesseract.image_to_string(
    img, lang="example_model", config='--psm 7')  # eng or example_model
target = "The computers are becoming sentient,"
percent_coincidence = round(SQ(None, target, raw_text).ratio() * 100, 2)

print("Output: {}\nPercent coincidence: {}%".format(
    raw_text, percent_coincidence))
