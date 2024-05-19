import requests
from bs4 import BeautifulSoup
import sqlite3

with open("m.txt","r") as file:
    rows = file.readlines()
    list = [row.strip() for row in rows]
print(list)



conn = sqlite3.connect('philosophers.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS philosophers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        etkilendikleri TEXT,
        etkiledikleri TEXT,
        onemli_fikirleri TEXT,
        ilgi_alanlari TEXT
    )""")
conn.commit()
conn.close()


def insert_philosopher(name, etkilendikleri, etkiledikleri, onemli_fikirleri, ilgi_alanlari):
    conn = sqlite3.connect('philosophers.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO philosophers (name, etkilendikleri, etkiledikleri, onemli_fikirleri, ilgi_alanlari)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, ','.join(etkilendikleri), ','.join(etkiledikleri), ','.join(onemli_fikirleri), ','.join(ilgi_alanlari)))

    conn.commit()
    conn.close()

def listOfThePhilosopher(uurl):
    url = uurl
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

    insert_philosopher(url, liste2['etkilendikleri'], liste2['etkiledikleri'],
                       liste2['önemlifikirleri'], liste2['ilgialanlari'])

for i in list:
    listOfThePhilosopher(i)
# Örnek kullanım
insert_philosopher('Aristoteles', ['Platon'], ['Alexander the Great'], ['Formal logic', 'Empiricism'],
                   ['Metaphysics', 'Ethics'])


def get_philosopher(name):
    conn = sqlite3.connect('philosophers.db')
    c = conn.cursor()

    c.execute('SELECT * FROM philosophers WHERE name = ?', (name,))
    philosopher = c.fetchone()

    conn.close()

    if philosopher:
        return {
            'name': philosopher[0],
            'etkilendikleri': philosopher[1].split(','),
            'etkiledikleri': philosopher[2].split(','),
            'onemli_fikirleri': philosopher[,].split(','),
            'ilgi_alanlari': philosopher[5].split(',')
        }
    else:
        return None


print(get_philosopher('Aristoteles'))


"""Sür realizmi ustam zihnimin üstünden"""