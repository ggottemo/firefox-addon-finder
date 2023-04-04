# Description: This script searches for Firefox versions of Chrome extensions
import requests
from bs4 import BeautifulSoup


# Insert html containing the table of extensions
html = """
 
"""

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Extract the extension names and Chrome Store URLs
extensions = []
for row in soup.find_all('tr'):
    link = row.find('a')
    if link and 'chrome.google.com/webstore' in link['href']:
        extensions.append({
            'name': link.text,
            'chrome_url': link['href']
        })

# Search for Firefox versions
firefox_search_base_url = "https://www.google.com/search?q=site%3Aaddons.mozilla.org+"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Open the output file for writing
with open('firefox_addons.txt', 'w') as file:
    for extension in extensions:
        query = firefox_search_base_url + extension['name']
        print(f"Searching Firefox version for {extension['name']}...")

        # Send the search request
        response = requests.get(query, headers=headers)
        search_soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first search result
        search_result = search_soup.find('div', class_='tF2Cxc')

        if search_result:
            firefox_url = search_result.find('a', href=True)['href']
            print(f"Found Firefox version for {extension['name']}: {firefox_url}")
            # Write to the output file
            file.write(f"{extension['name']} - {firefox_url}\n")
        else:
            print(f"No Firefox version found for {extension['name']}")
            file.write(f"{extension['name']} - Not found\n")