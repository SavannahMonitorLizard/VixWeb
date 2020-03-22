import bs4, csv, datetime, time, pyppeteer
from requests_html import HTMLSession

session = HTMLSession()
r = session.get("http://www.vixcentral.com/")
try:
    r.html.render(timeout=30)
    print("Page successfully loaded")
except pyppeteer.errors.TimeoutError:
    print("Could not load page, please retry")

while True:

    try:
        r.html.render(timeout=30)
        print("Page successfully loaded")
    except pyppeteer.errors.TimeoutError:
        print("Could not load page, please retry")

    data = r.html.find("#basicTable", first=True)
    dataSplit = data.text.split("\n")
    contago = dataSplit[:16]
    difference = dataSplit[16:]
    contago.insert(0, datetime.datetime.now())
    difference.insert(0, datetime.datetime.now())

    try:    
        csv_file = open("vixData.csv", "a", newline="")
    except PermissionError:
        print("Could not load file due to file being open, retrying in 5 minutes")
        time.sleep(300)
        continue

    writer = csv.writer(csv_file)
    writer.writerow(contago)
    writer.writerow(difference)
    writer.writerow([])
    csv_file.close()
    print("Writing succesful")
    
    time.sleep(300)
    print("Beginning again")