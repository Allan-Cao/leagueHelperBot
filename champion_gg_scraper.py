import requests
from bs4 import BeautifulSoup

def get_synergy(adc, support, elo = None):
    try:
        data = requests.get(f'https://champion.gg/matchup/{adc}/{support}/synergy?league={elo}')
        soup = BeautifulSoup(data.text, "html.parser")
        win_percentage = float(soup.find("table", class_="table table-striped").find("td", class_="matchup-values-width").text[:-1])
        return win_percentage
    except:
        return None
