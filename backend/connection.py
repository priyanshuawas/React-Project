import requests
from bs4 import BeautifulSoup
import mysql.connector

# Define database connection details
db_host = "localhost"
db_user = "root"
db_password = "awasthipriyanshu"
db_name = "dummydata"

# Replace with the URL you want to scrape and desired element/attribute
url = "https://fnec.cornell.edu/for-participants/recipe-table/"
target_element = "table"
target_attribute = None  # Set to None if extracting from all table cells

# Connect to MariaDB
try:
    mydb = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

# Function to extract data from table cells
def extract_data(table_element):
    data = []
    if target_attribute:
        # Extract data based on specific attribute
        for row in table_element.find_all("tr"):
            row_data = [cell.get(target_attribute) for cell in row.find_all("td")]
            data.append(row_data)
    else:
        # Extract all text content from table cells
        for row in table_element.find_all("tr"):
            row_data = [cell.text.strip() for cell in row.find_all("td")]
            data.append(row_data)
    return data

# Scrape data
try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    table_element = soup.find(target_element)
    scraped_data = extract_data(table_element)
except Exception as e:
    print("Error scraping data:", e)
    exit()

# Prepare SQL query (modify table name and column names based on your table)
sql = "INSERT INTO your_table_name (column1, column2, ...) VALUES (%s, %s, ...)"
val = []
for row in scraped_data:
    val.append(tuple(row))

# Insert data into MariaDB
try:
    mycursor.executemany(sql, val)
    mydb.commit()
    print("Data inserted successfully!")
except mysql.connector.Error as err:
    print("Error inserting data:", err)

# Close the connection
finally:
    if mycursor is not None:
        mycursor.close()
    if mydb is not None:
        mydb.close()
