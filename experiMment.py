"""import qrcode

def create_qr(text):
    img = qrcode.make(text)
    img.save(f'qrCodes/{text}.png')

create_qr("amm pata")"""
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://plibrary23:raNPCBW9Rrxayhcd@cluster0.tssrqjh.mongodb.net/?retryWrites=true&w=majority")
db = client['leosLibrary']
collection = db['books']
borrowing_collection = db['borrowings']
# results = borrowing_collection.find({})
results = collection.find({'borrowed':{"$type" : "string"}})

book_list = list(results)
print(book_list)
#
# for idx,book in enumerate(book_list):
#     print(idx,'----------',book)

