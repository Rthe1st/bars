import unittest
import os
import cv2
import sys

from bars.play.input_methods import extract_from_image

class InputTestCase(unittest.TestCase):
    def test_extract_from_image(self):
        test_data = {
            'generated_barcode.png': b'5012093551425',
            'high_res_scan-1.jpg': b'5012093551425',
            'high_res_scan-2.jpg': b'5012093551029',
            'phone-1.jpeg': b'5012093551029',
            'phone-2.jpeg': b'5012093551029',
            'webcam-1.png': b'0634904031824',
        }
        for test_file, correct_barcode in test_data.items():
            with self.subTest(i=(test_file, correct_barcode)):
                image = cv2.imread(os.path.join('./tests/images', test_file))
                scan_info = extract_from_image(image)
                print(scan_info)
                self.assertIsNotNone(scan_info)
                self.assertEqual(len(scan_info), 1)
                self.assertEqual(scan_info[0].data, correct_barcode)
