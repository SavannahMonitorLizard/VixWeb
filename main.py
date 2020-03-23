import bs4, csv, datetime, time, pyppeteer, json
from requests_html import HTMLSession

import matplotlib.pyplot as plt

session = HTMLSession()
r = session.get("http://www.vixcentral.com/")

dates, values = [], []

while True:

    try:
        r.html.render(timeout=30)
        print("Page successfully loaded")
    except pyppeteer.errors.TimeoutError:
        print("Could not load page, retrying in 30 seconds")
        time.sleep(30)
        continue

    data = r.html.find("#basicTable", first=True)
    dataSplit = data.text.split("\n")
    contango = dataSplit[:16]
    difference = dataSplit[16:]
    contango.insert(0, datetime.datetime.now())
    difference.insert(0, datetime.datetime.now())

    try:    
        csv_file = open("vixData.csv", "a", newline="")
    except PermissionError:
        print("Could not load file due to file being open, retrying in 5 minutes")
        time.sleep(300)
        continue

    writer = csv.writer(csv_file)
    writer.writerow(contango)
    writer.writerow(difference)
    writer.writerow([])
    csv_file.close()
    print("Writing succesful")

    with open("values_dates.json") as load_file:
        values_dates = json.load(load_file)
    values = values_dates["values"]
    dates = values_dates["dates"]
    values.append(contango[3])
    dates.append(datetime.datetime.now().strftime("%a, %b %d, %Y, %H:%M:%S"))
    values_dates = {}
    values_dates.setdefault("values", values)
    values_dates.setdefault("dates", dates)
    print(values_dates)
    with open("values_dates.json", "w") as dump_file:
        json.dump(values_dates, dump_file)
    
    plt.plot(dates, values, "-o")
    plt.savefig("vixGraph.png")
    
    time.sleep(300)
    print("Beginning again")