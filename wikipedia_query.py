import requests
from bs4 import BeautifulSoup

url = "https://tr.wikipedia.org/wiki/Georg_Wilhelm_Friedrich_Hegel"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

liste2 = {
    'etkilendikleri': [],
    'etkiledikleri': [],
    'önemlifikirleri': [],
    'ilgialanlari' : []
}

table = soup.find("table", class_="infobox vcard")

for row in table.find_all("tr"):
    cells = row.find_all(['th', 'td'])
    row_data = [cell.get_text(strip=True) for cell in cells]
    if row_data[0][:14] == "Etkilendikleri":
        liste2['etkilendikleri'] = row_data[0][14:].split(',')
    elif row_data[0][:13] == "Etkiledikleri":
        liste2['etkiledikleri'] = row_data[0][13:].split(',')
    elif row_data[0] == "Önemli fikirleri":
        liste2['önemlifikirleri'] = row_data[1].split(',')
    elif row_data[0] == "İlgi alanları":
        liste2['ilgialanlari'] = row_data[1].split(',')

print("Etkilendikleri:", liste2['etkilendikleri'])
print("Etkiledikleri:", liste2['etkiledikleri'])
print("Önemli Fikirleri:", liste2['önemlifikirleri'])
print("İlgi Alanları:", liste2['ilgialanlari'])