# functions for crud operations
from google_speech import Speech
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import speech_recognition as sr
import pyttsx3
import playsound
from gtts import gTTS
from pymongo import MongoClient
import os
import json
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("languages", 'hi')
engine.setProperty("voice", voices[2].id)
engine.setProperty("rate", 130)


def create_bar(number):
    my_num = number + number + number
    img = EAN13(my_num, writer=ImageWriter())
    img.save(f'barcodes/{number}' + "sabirB")



def talk(command):
    engine.say(command)
    engine.runAndWait()


def talk_bangla(text):
    language = 'bn'
    output = gTTS(text=text, lang=language, slow=False)
    output.save("output.mp3")
    playsound.playsound('output.mp3')


def get_command():
    try:
        with sr.Microphone() as source:

            print("listening")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language="en-IN")
            command = command.lower()
            print(command)
            return command


    except:
        print("Mic not found")


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
            if my_data:
                cam.release()
                cv2.destroyAllWindows()
                return my_data


"""
connect to the database
"""
client = MongoClient(
    "mongodb+srv://plibrary23:raNPCBW9Rrxayhcd@cluster0.tssrqjh.mongodb.net/?retryWrites=true&w=majority")
db = client['leosLibrary']
collection = db['books']


def take_input(text):
    print(f"insert {text}")
    talk(f"insert {text}")
    return input()

def add_book():
    print("Adding Books...hurray")
    talk("initializing adding process")
    talk('Mention the language of the respective book.\n'
         'insert bn for bengali and en for english')
    print('insert bn for bengali and en for english')
    book_lang = input()
    book_id = take_input("four-digit book id")
    book_name = take_input("book name")
    author_name = take_input("author's name")
    borrowed = False
    if book_lang == 'en':
        talk(f"Adding, {book_name}, by {author_name} ,in the book list")
        book = {"book_id": book_id, "book_name": book_name, "author_name": author_name, "book_lang": book_lang,
                "borrowed": borrowed}

        result = collection.insert_one(book)
        if result.acknowledged:
            print("Book added successfully")
            talk("Book added successfully")
            create_bar(book_id)
        else:
            print("Sorry,failed to add book")


def return_book():
    talk("initializing return enlisting process\n scan your book to proceed")
    raw_data = get_data()
    book_id = raw_data[0:4]
    book = collection.find_one({"book_id": book_id})
    book_name = book['book_name']
    borrower = book["borrowed"]
    author = book['author_name']
    results = collection.update_one({"book_id": book_id}, {"$set": {"borrowed": False}})
    print(results.modified_count)
    if results.modified_count:
        print(f'{borrower} returned {book_name}  by {author} ')
        talk(f'{borrower}, returned ,{book_name}  by ,{author} ')


def lend_book():
    talk("initializing lending process\n scan your book to proceed")
    raw_data = get_data()
    book_id = raw_data[0:4]
    person = take_input("borrower's name")
    book = collection.find_one({"book_id":book_id})
    results = collection.update_one({"book_id":book_id},{"$set": {"borrowed": person}})
    print(results.modified_count)
    if results.modified_count:
        book_person = book["book_name"]
        print(f'{book_person} has been lent to him {person}')
        talk(f'{book_person} has been lent to {person}')


"""talk("0022")
talk_bangla("")"""
"""text = 'আপনি কেমন আছেন'
language = 'bn'
output = gTTS(text=text, lang=language, slow=False)
output.save("output.mp3")
playsound.playsound("output.mp3")"""
