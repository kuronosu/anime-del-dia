from bs4 import BeautifulSoup
import requests
import urllib3

def scraping():
    url = 'www.animeflv.net'
    rensponse = requests.get("https://" + url)
    soup = BeautifulSoup(rensponse.content, 'html.parser')
    anime = soup.find_all('div', {'class':'AnimeDia'})
    title = anime[0].find('span', {'class': 'Title'}).string#find('strong')
    image = 'https://' + url + anime[0].find('img')['src']
    image_name = image.split("/")[len(image.split("/"))-1]
    synp = anime[0].find('div', {'class': 'Synopsis',}).find('div', {'class': 'Description'}).string
    print(image_name)
    print(title)
    return anime

if __name__ == '__main__':
    scraping()
