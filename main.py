import requests
from twilio.rest import Client
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACC_SID = os.getenv("TWILIO_ACC_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_MOBILE_NO = os.getenv("TWILIO_MOBILE_NO")
RECEIVER_MOBILE_NO = os.getenv("RECEIVER_MOBILE_NO")


BEST_PRICE = 13000.00

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

amazon_url_live = "https://www.amazon.in/Samsung-Convection-Microwave-MC28A5013AK-TL/dp/B09XBMXQ34/ref=sr_1_1_sspa?crid=BE2XITVX4LR9&dib=eyJ2IjoiMSJ9.7HX4kAufjO9Lj0BV0uxOsiq7nNny7aQIw8TVFK-E2RlajVPbhw8XSZGgHWmmMFEy87Wka7FHyTTQm7C_aLv-D65uPBXqpoh2hJbL6yJMNWlccqs1eAUOJtB1NbRkIWeN5uK2UrNZrIvne0Xt3l9vHGNuaQCswAron0Qe7fz9vI1E9x3Uw8256SGANKOIIsQLXqxhARf0f5EJE7BoUMgz6KTMe2NTQegxXU1nOoviXDw.NR3vBT8wUbYIjqsysIAkfpa-RXq4ar8dpJbzQqD-XPg&dib_tag=se&keywords=microwave&qid=1745736757&sprefix=microwav%2Caps%2C254&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
amazon_url_static = "https://appbrewery.github.io/instant_pot/"

response = requests.get(url=amazon_url_live , headers=headers)
amazon_html = response.text

soup = BeautifulSoup(amazon_html , "html.parser")

price_whole = soup.find(class_="a-price-whole").getText()
price_one = price_whole.split(',')[0]
price_two = price_whole.split(',')[1]

product_price = float(price_one + price_two)

product_title = soup.find(id="productTitle").getText().strip()


if product_price <= BEST_PRICE:

    msg_body = f"\nPrice Drop Alert!\n{product_title} is now ₹{product_price} only."
    #Not including the link as it might exceed the message length limit.

    client = Client(TWILIO_ACC_SID , TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_= TWILIO_MOBILE_NO,
        to= RECEIVER_MOBILE_NO,
        body= msg_body
    )
    print(message.body)

