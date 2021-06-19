import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def get_currency_gold():

	url = "https://altin.doviz.com/"
	result = requests.get(url)
	contents = BeautifulSoup(result.text, "html.parser")

	gold_ounce_s = contents.find("td", {"data-socket-key":"ons", "data-socket-attr":"s"}).text.replace("$","")
	gold_ounce_b = contents.find("td", {"data-socket-key":"ons", "data-socket-attr":"b"}).text.replace("$","")

	gold_24_s = contents.find("td", {"data-socket-key":"gram-altin", "data-socket-attr":"s"}).text
	gold_24_b = contents.find("td", {"data-socket-key":"gram-altin", "data-socket-attr":"b"}).text

	gold_22_s = contents.find("td", {"data-socket-key":"22-ayar-bilezik", "data-socket-attr":"s"}).text
	gold_22_b = contents.find("td", {"data-socket-key":"22-ayar-bilezik", "data-socket-attr":"b"}).text


	gold_18_s = contents.find("td", {"data-socket-key":"18-ayar-altin", "data-socket-attr":"s"}).text
	gold_18_b = contents.find("td", {"data-socket-key":"18-ayar-altin", "data-socket-attr":"b"}).text

	gold_14_s = contents.find("td", {"data-socket-key":"14-ayar-altin", "data-socket-attr":"s"}).text
	gold_14_b = contents.find("td", {"data-socket-key":"14-ayar-altin", "data-socket-attr":"b"}).text

	gold_8 = Decimal(contents.find("td", {"data-socket-key":"gram-altin", "data-socket-attr":"s"}).text.replace(",",".")) * Decimal(0.333)

	dolar = contents.find("span", {"data-socket-key":"USD"}).text
	euro = contents.find("span", {"data-socket-key":"EUR"}).text

	value = {
	"dolar":dolar,
	"euro":euro,
	"gold_ounce_s":gold_ounce_s,
	"gold_ounce_b":gold_ounce_b,
	"gold_24_s":gold_24_s,
	"gold_24_b":gold_24_b,
	"gold_22_s":gold_22_s,
	"gold_22_b":gold_22_b,
	"gold_18_s":gold_18_s,
	"gold_18_b":gold_18_b,
	"gold_14_s":gold_14_s,
	"gold_14_b":gold_14_b,
	"gold_8":gold_8
	}

	return value

	
def get_price_doral():

	url = "https://altin.doviz.com/"
	result = requests.get(url)
	contents = BeautifulSoup(result.text, "html.parser")

	dolar = contents.find("span", {"data-socket-key":"USD"}).text.replace(",", ".")
	return dolar


def get_price_gold():

	url = "https://altin.doviz.com/"
	result = requests.get(url)
	contents = BeautifulSoup(result.text, "html.parser")

	gold_24_s = contents.find("td", {"data-socket-key":"gram-altin", "data-socket-attr":"s"}).text.replace(",", ".")
	return gold_24_s
