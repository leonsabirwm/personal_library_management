# importing the utility modules
import cv2
import time
import numpy as np
from pyzbar.pyzbar import decode
import crudOperations
from crudOperations import talk, get_command, add_book, lend_book, return_book,add_borrowing,omit_borrowing,display_book



def verify_qr(data):
    if data == "sabirthelibrarian":
        return True
    else:
        return False


def authentication():
    talk("Scan your id to get access")

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    scan_count = 1
    while scan_count:
        success, img = cam.read()
        cv2.imshow("result", img)
        cv2.waitKey(1)
        for barcode in decode(img):
            print('reading')
            my_data = barcode.data.decode("utf-8")
            if my_data:
                cam.release()
                cv2.destroyAllWindows()
                print(my_data)
                scan_count -= 1
                return verify_qr(my_data)


def greet():
    talk("Access Granted!!\n")
    talk("Hey welcome to Leo's library")
    talk("I can help you with adding\n,lending\n and enlisting a return")
    talk("Please speak up your choice")


authorized = True


def initializing():
    if authorized:
        # greet()
        command = get_command()
        if 'add' in command:
            add_book()
        elif 'lend' in command:
            lend_book()
        elif 'return' in command:
            return_book()
        if 'append' in command:
            add_borrowing()
        elif 'deduct' in command:
            omit_borrowing()
        elif 'display' in command:
            display_book()
        else:
            talk("Pardon...Choice again precisely")
            initializing()
    if not authorized:
        talk("Access Denied")


if __name__ == "__main__":
    initializing()
