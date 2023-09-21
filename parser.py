import requests
from bs4 import BeautifulSoup
import csv

url_list = [
	#url products
]

csv_product = "product_info.csv"
csv_file = open(csv_product, "a", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)

csv_writer.writerow([]) # write your columns name

for url in url_list:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        part_name = soup.find("h2", class_="bold").get_text(strip=True)

        values = []

        for span_element in soup.find_all("span", class_="text-gray-light"):
            value = span_element.get_text(strip=True)
            values.append(value)

        if len(values) >= 4:
            part_number = values[0]
            vehicle_model = values[1]
            availability = values[2]
            manufacture = values[3]
        else:
            part_number = "N/A"
            vehicle_model = "N/A"
            availability = "N/A"
            manufacture = "N/A"

        listed_price_element = soup.find("", _="") #write (div,id,h5,h2 or ...) afet . write (class, id or ...)
        listed_price = listed_price_element.find_next("", _="") if listed_price_element else "N/A"

        your_price_element = soup.find("", _="") #write (div,id,h5,h2 or ...) afet . write (class, id or ...)
        your_price = your_price_element.get_text(strip=True) if your_price_element else "N/A"

        shipping_weight_element = soup.find("", _="") #write (div,id,h5,h2 or ...) afet . write (class, id or ...)
        shipping_weight = shipping_weight_element.find_next("", class_="") if shipping_weight_element else "N/A"

        try:
            img = soup.find("a", class_="carousel-thumbnail").find("img")["src"]
            img = img.replace("", "") #write what you need to delete in img adress
            img_urls = "" + img #paste the url
        except (AttributeError, KeyError):
            img_urls = "N/A"

        csv_writer.writerow([]) # # write your columns name again

    else:
        print(f"Didn't get data wtih {url}")

csv_file.close()
print("Done!")
