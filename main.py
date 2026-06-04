import requests
from bs4 import BeautifulSoup
import pandas as pd

# Wikipedia URL
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Headers to avoid 403 error
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Get webpage
response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Print page title
if soup.title:
    print("Page Title:", soup.title.text)
else:
    print("Title not found")

# Find the S&P 500 companies table
table = soup.find("table", {"id": "constituents"})

# Get all rows
rows = table.find_all("tr")

print("Number of rows:", len(rows))

# Store data
companies = []

for row in rows[1:]:  # Skip header row
    cols = row.find_all("td")

    if len(cols) >= 8:
        symbol = cols[0].text.strip()
        company = cols[1].text.strip()
        sector = cols[2].text.strip()
        headquarters = cols[4].text.strip()

        companies.append([symbol, company, sector, headquarters])

print("Total companies extracted:", len(companies))

# Convert to DataFrame
df = pd.DataFrame(
    companies,
    columns=["Symbol", "Company", "Sector", "Headquarters"]
)

# Show first 5 rows
print("\nFirst 5 Companies:")
print(df.head())

# Save to CSV
df.to_csv("sp500_companie.csv", index=False)

print("\nCSV file created successfully!")
print("File saved as: sp500_companie.csv")