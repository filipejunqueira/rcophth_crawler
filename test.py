import requests
from bs4 import BeautifulSoup
import smtplib
import time

start = time.time()

URL = (
    "https://www.amazon.com.br/Placa-Geforce-Zotac-ZT-T20800D-10P-256Bits/dp/B07GR2NPM1/"
    "ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=RTX+2080ti&qid=1573926657&sr=8-1"
)

print("\nThis is the url:\n\n" + URL)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}

def check_price():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[2 : (len(price) - 3)].replace(".", ""))

    return converted_price

def send_mail(URL):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("filipemichelin@gmail.com", "ampobwounclkqsie")

    subject = "Price fell down! - this is a test though! :-)"
    body = "Check the link! :-): \n" + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("filipemichelin@gmail.com", "filipelqj@gmail.com", msg)
    print('Hey, email has been sent!')
    server.quit()

    return True

price = check_price()
target_price = 2599
if (price < target_price):
    send_mail(URL)


# while(True):
#     check_price()
#     time.sleep(60)

final_time = time.time() - start
print(f'it has taken {final_time} seconds')
