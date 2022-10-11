"""import qrcode

def create_qr(text):
    img = qrcode.make(text)
    img.save(f'qrCodes/{text}.png')

create_qr("amm pata")"""

from barcode import EAN13
from barcode.writer import ImageWriter
#
#
def create_bar(number):
    my_num = number + number + number
    img = EAN13(my_num, writer=ImageWriter())
    img.save(f'barcodes/{number}' + "sabirB")

create_bar('7896')
import cv2
from pyzbar.pyzbar import decode

def get_data():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    scan_count = 1
    while scan_count:
        success, img = cam.read()
        cv2.imshow("result", img)
        cv2.waitKey(1)
        for barcode in decode(img):
            print('reading')
            my_data = barcode.data.decode("utf-8")
            return my_data

print(get_data())