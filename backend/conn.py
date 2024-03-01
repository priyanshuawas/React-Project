import requests
import mysql.connector
from bs4 import BeautifulSoup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="awasthipriyanshu",
    database="dummydata"
)
cursor = conn.cursor()
url = "https://fnec.cornell.edu/for-participants/recipe-table/"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table:
        header=[]
        data = []
        for row in table.find_all("tr"):
            for cell in row.find_all(["th"]):
                text = cell.get_text(strip=True)
                if ' ' in text:
                    text = f"`{text}`"
                header.append(text)
            row_data = []
            for cell in row.find_all(["td"]):
                text = cell.get_text(strip=True)
                row_data.append(text)
            if row_data:
                data.append(row_data)
    for items in data:
        query = "INSERT INTO `servey management system` ({}) VALUES ({})"
        query = query.format(', '.join(header), ', '.join(['%s'] * len(header)))
        cursor.execute(query, items)
        conn.commit()
    else:
        print("Table not found on the website.")
else:
    print(f"Error: Request failed with status code {response.status_code}")
print(soup.title,"header",header,"data",data)