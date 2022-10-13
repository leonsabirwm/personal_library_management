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
from bson.objectid import ObjectId
import os
import json
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
from tabulate import tabulate

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
    os.remove('output.mp3')


def bangla_input(text):
    print(text)
    talk_bangla(text)
    return input()


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
borrowing_collection = db['borrowings']


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
    borrowed = False
    if book_lang == 'en':
        book_id = take_input("four-digit book id")
        book_name = take_input("book name")
        author_name = take_input("author's name")
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
    book = collection.find_one({"book_id": book_id})
    results = collection.update_one({"book_id": book_id}, {"$set": {"borrowed": person}})
    print(results.modified_count)
    if results.modified_count:
        book_person = book["book_name"]
        print(f'{book_person} has been lent to him {person}')
        talk(f'{book_person} has been lent to {person}')


def add_borrowing():
    results = borrowing_collection.find({})
    borrow_list = list(results)
    borrow_remaining = 5 - int(len(borrow_list))
    if borrow_remaining <= 0:
        talk("Sorry,Borrow limit exceeded")
    else:
        talk("Initializing the add borrowing process\n your borrowing limit is five and\n"
             f"you have got {borrow_remaining} borrowing remaining")
        talk('Mention the language of the respective book.\n')
        book_lang = take_input(" bn for bengali and en for english")


        if book_lang == 'en':
            lender_name = take_input("lender's name")
            book_name = take_input("Book name")
            author_name = take_input("Author name")
            book = {"lender_name": lender_name, "book_name": book_name, "author_name": author_name,"book_lang": book_lang}
            print(f"adding, {book_name} by ,{author_name},bought from {lender_name} , to the borrowing list")
            talk(f"adding {book_name} by {author_name},bought from {lender_name}to the borrowing list")
            result = borrowing_collection.insert_one(book)
            if result.acknowledged:
                print("Book added successfully")
                talk("Book added successfully")
        if book_lang == 'bn':
            lender_name = bangla_input("ধারদাতার নাম লিখুন")
            book_name = bangla_input("বইয়ের নাম লিখুন")
            author_name = bangla_input("লেখকের নাম লিখুন")
            book = {"lender_name": lender_name, "book_name": book_name, "author_name": author_name,"book_lang": book_lang}
            print(f"{author_name} কর্তৃক রচিত {book_name} বইটি গ্রন্থ ধারের তালিকায় লিপিবদ্ধ করা হচ্ছে ")
            talk_bangla(f"{author_name} কর্তৃক রচিত {book_name}, বইটি গ্রন্থ ধারের তালিকায় লিপিবদ্ধ করা হচ্ছে ")
            result = borrowing_collection.insert_one(book)
            if result.acknowledged:
                print("বইটি ধারের তালিকায় লিপিবদ্ধ করা হয়েছে")
                talk_bangla("বইটি ধারের তালিকায় লিপিবদ্ধ করা হয়েছে")


def omit_borrowing():
    results = borrowing_collection.find({})
    borrow_list = list(results)
    list_length = len(borrow_list)
    if list_length <= 0:
        print("Sorry, no borrowing in the list")
        talk("Sorry, no borrowing in the list")
    else:
        talk("Initializing borrowing deduction process, and printing your borrowing list below")
        table = []
        headers = ["index", "Object Id", "Lender", "Name", "Author"]
        for idx, book in enumerate(borrow_list):
            table_book = list(book.values())
            table.append(table_book)
        print(tabulate(table, headers, showindex="always"))
        book_index = int(take_input("a book's index to continue"))
        my_book = borrow_list[book_index]
        book_id = my_book["_id"]
        result = borrowing_collection.delete_one({'_id': book_id})
        if result.acknowledged:
            if my_book['book_lang'] == 'en':
                print(
                    f"{my_book['book_name']} borrowed from {my_book['lender_name']} deducted successfully from the borrowing list")
                talk(
                    f"{my_book['book_name']} borrowed from {my_book['lender_name']} deducted successfully from the borrowing list")
            if my_book['book_lang'] == 'bn':
                talk_bangla(f"{my_book['lender_name']} থেকে ধার নেওয়া {my_book['book_name']} বইটি ধারের তালিকা হতে বাদ দেওয়া হয়েছে")
                print(f"{my_book['lender_name']} থেকে ধার নেওয়া {my_book['book_name']} বইটি ধারের তালিকা হতে বাদ দেওয়া হয়েছে")


def display_book():
    print("Initializing book list displaying process,please speak up your choice:\n"
          "All books\n"
          "Bengali Books\n"
          "English Books\n"
          "Borrowed Books\n"
          "Lent Books")
    talk("Initializing book list displaying process,please speak up your choice:\n"
          "All books \n"
          "Bengali Books or"
          "English Books\n"
         "Borrowed Books or"
         "Lent Books")
    command = get_command()
    book_list = []
    if 'all' in command:
        results = collection.find({})
        book_list = list(results)
    elif 'bengali' in command:
        results = collection.find({"book_lang":'bn'})
        book_list = list(results)
    elif 'english' in command:
        results = collection.find({"book_lang": 'en'})
        book_list = list(results)
    elif 'borrowed' in command:
        results = borrowing_collection.find({})
        book_list = list(results)
    elif 'lent' in command:
        results = collection.find({'borrowed': {"$type": "string"}})
        book_list = list(results)
    else:
        talk("pardon,mention your demand again")
        display_book()
    table = []
    headers = ["index", "Name", "Author", "Language"]
    for idx,book in enumerate(book_list):
        print(book)
        del book['_id']
        del book['borrowed']
        del book['book_id']
        table_book = list(book.values())
        table.append(table_book)
    print(tabulate(table, headers, showindex="always"))

