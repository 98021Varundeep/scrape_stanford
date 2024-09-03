import json
import httpx
from bs4 import BeautifulSoup

url = 'https://www.cs.stanford.edu/people-cs/faculty-name'

response = httpx.get(url, timeout=httpx.Timeout(30.0))
soup = BeautifulSoup(response.text, 'html.parser')

data = []

# Find all li elements (assuming faculty information is within li tags)
for li in soup.find_all('li'):
    name_tag = li.find('h3')
    if name_tag:
        name = name_tag.get_text(strip=True)
    else:
        continue

    title_tag = li.find('div', class_="views-field views-field-su-person-short-title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = 'N/A'

    link_tag = li.find('a', href=True)
    if link_tag:
        profile_link = 'https://www.cs.stanford.edu' + link_tag['href']
    else:
        profile_link = 'N/A'

    img = li.find('img', src=True)
    if img:
        img_path = 'https://www.cs.stanford.edu' + img['src']
    else:
        img_path = 'N/A'

    data.append({
        'name': name,
        'title': title,
        'profile_link': profile_link,
        'image': img_path
    })

# Print data (optional)
print(data)

# Write to JSON file
file_name = 'prof.json'
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
