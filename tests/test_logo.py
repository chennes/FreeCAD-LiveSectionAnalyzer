"""The icon embedded in the macro must decode to a valid 96 x 96 PNG with a transparent corner.

Run:  python3 tests/test_logo.py      (needs Pillow)
"""
import base64
import io
import os
import re
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MACRO = os.path.join(HERE, "..", "macro", "LiveSectionAnalyzer.FCMacro")


class EmbeddedLogo(unittest.TestCase):
    def test_png_is_valid(self):
        src = open(MACRO, encoding="utf-8").read()
        m = re.search(r"_LOGO_PNG_B64 = \((.*?)\n\)\n", src, re.S)
        self.assertIsNotNone(m)
        data = base64.b64decode("".join(re.findall(r'"([A-Za-z0-9+/=]+)"', m.group(1))))
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        im = Image.open(io.BytesIO(data)).convert("RGBA")
        self.assertEqual(im.size, (96, 96))
        self.assertEqual(im.getpixel((0, 0))[3], 0)            # rounded corner is transparent
        self.assertEqual(im.getpixel((48, 48))[3], 255)        # centre is opaque
        self.assertLess(len(data), 20000)                      # keep the macro small

    def test_files_exist(self):
        for name in ("logo.png", "icon.png"):
            self.assertTrue(os.path.exists(os.path.join(HERE, "..", "docs", name)), name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
