import requests
from bs4 import BeautifulSoup

# Load the saved HTML file
with open('douban_top250.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract movie titles
movies = soup.find_all('div', class_='hd')
movie_titles = [movie.a.span.text for movie in movies]

# Print the movie titles
for title in movie_titles:
    print(title)