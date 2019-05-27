from bars.play import barcodes
import time
from pyzbar import pyzbar
import cv2

def extract_from_image(scan_image, debug=False):
    # we use global thresholding
    # consider adaptive thresholding
    # https://stackoverflow.com/questions/38166197/barcode-pre-processing-for-zbar
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    # https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html?highlight=adaptivethreshold
    for threshold in range(50,200, 5):

        transformed_image = cv2.cvtColor(scan_image,cv2.COLOR_RGB2GRAY)
        cv2.threshold(transformed_image,threshold,255,cv2.THRESH_BINARY)
        #transformed_image = cv2.adaptiveThreshold(transformed_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #   cv2.THRESH_BINARY,7,3)
        
        scan_info = pyzbar.decode(transformed_image)
        
        if debug:
            print(threshold)
            cv2.imwrite('threshold_{}.png'.format(threshold),  transformed_image)

        if len(scan_info) != 0:
            return scan_info
    return None

def from_webcam(debug=True):

    video_capture = cv2.VideoCapture(0)

    ret, scan_image = video_capture.read()

    if debug:
        cv2.imwrite('view.png',  scan_image)

    scan_info = extract_from_image(scan_image)

    if scan_info is not None:
        cv2.imwrite('last_successful_Scan.png', scan_image)

    time.sleep(0.5)

    keep_looping = True
    return scan_info, keep_looping

def from_image(file_location):
    scan_image = cv2.imread(file_location)
    scan_info = extract_from_image(scan_image)
    if scan_info is None:
        print('No barcodes detected')

    keep_looping = False

    return scan_info, keep_looping

def file_monitoring(input_file):
    """
    Used ot simulate continuous input (like a webcam would give)
    Monitor a file and re-fire scanning whenever it changes
    """
    return None, False