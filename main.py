import bs4, csv, datetime, time, pyppeteer, json
from requests_html import HTMLSession

import matplotlib.pyplot as plt

session = HTMLSession()
r = session.get("http://www.cboe.com/products/futures/vx-cboe-volatility-index-vix-futures")

dates, values = [], []

while True:

    try:
        r.html.render(timeout=30)
        print("Page successfully loaded")
    except pyppeteer.errors.TimeoutError:
        print("Could not load page, retrying in 30 seconds")
        time.sleep(30)

    data = r.html.find("#itemPlaceholderContainer1", first=True)
    dataSplit = data.text.split("\n")
    dataCut = []

    for i in dataSplit[8:]:
        dataCut.append(i)

    chunks = [dataCut[x:x+8] for x in range(0, len(dataCut), 8)]

    validLists = []

    for i in chunks:
        if not i[0][2].isdigit():
            validLists.append(i)

    for i in validLists:
        currentList = " ".join(i)
        print(currentList)
    
    time.sleep(300)
    print("Beginning again")

# try:
#     r.html.render(timeout=30)
#     print("Page successfully loaded")
# except pyppeteer.errors.TimeoutError:
#     print("Could not load page, retrying in 30 seconds")
#     time.sleep(30)

# data = r.html.find("#itemPlaceholderContainer1", first=True)
# dataSplit = data.text.split("\n")
# dataCut = []

# for i in dataSplit[8:]:
#     dataCut.append(i)

# chunks = [dataCut[x:x+8] for x in range(0, len(dataCut), 8)]

# validLists = []

# for i in chunks:
#     if not i[0][2].isdigit():
#         validLists.append(i)

# for i in validLists:
#     currentList = " ".join(i)
#     print(currentList)
# contango = dataSplit[:16]
# difference = dataSplit[16:]
# contango.insert(0, datetime.datetime.now())
# difference.insert(0, datetime.datetime.now())

# try:    
#     csv_file = open("vixData.csv", "a", newline="")
# except PermissionError:
#     print("Could not load file due to file being open, retrying in 5 minutes")
#     time.sleep(300)

# writer = csv.writer(csv_file)
# writer.writerow(contango)
# writer.writerow(difference)
# writer.writerow([])
# csv_file.close()
# print("Writing succesful")

# time.sleep(300)
# print("Beginning again")