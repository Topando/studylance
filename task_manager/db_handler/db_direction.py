from bs4 import BeautifulSoup
import requests
from ..models import Direction
url = 'https://propostuplenie.ru/article/polnyj-perechen-specialnostej-i-napravlenij-podgotovki-vysshego-obrazovaniya/'


def direction_update():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    alltr = soup.findAll('tr')[1:]
    for tags in alltr:
        td = tags.findAll('td')
        if len(td) == 1:
            continue
        elif td[2].text.strip() != "Бакалавр":
            continue
        elif td[1].text.strip() == "":
            continue
        else:
            direction = Direction(direction=td[1].text.strip(), code=td[0].text.strip())
            try:
                direction.save()
            except Exception:
                print("ЛОХ")
