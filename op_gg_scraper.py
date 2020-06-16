import requests
from bs4 import BeautifulSoup


def get_skill_order(lane, name):
    """
    Gets skill order of specific champion and lane
    """
    data = requests.get("https://na.op.gg/champion/" +
                        name + "/statistics/" + lane)
    soup = BeautifulSoup(data.text, "html.parser")
    skills = soup.find("table", {"class": "champion-skill-build__table"})
    tbody = skills.find("tbody")
    tr = tbody.find_all("tr")[1]
    skill_table = []
    for td in tr.find_all("td"):
        if td.text.strip() == 'Q' or td.text.strip() == 'W' or td.text.strip() == 'R' or td.text.strip() == 'E':
            skill_table.append(td.text.strip())

    return skill_table

def get_runes(lane, name):
    """
    Gets the runes of specific champion and lane
    """
    rune_options = []
    data = requests.get("https://na.op.gg/champion/" +
                        name + "/statistics/" + lane)
    soup = BeautifulSoup(data.text, "html.parser")
    paths = soup.find_all('div', class_ = "champion-stats-summary-rune__name")
    rune_paths = ([path.text.split(' + ') for path in paths])
    active_runes = soup.find_all('div', class_ = ["perk-page__item perk-page__item--active",\
                                                  "perk-page__item perk-page__item--keystone perk-page__item--active"])
    # Determine the Primary/Secondary runes
    all_runes = []
    for runes in active_runes:
        all_runes.append(runes.find('img', alt=True)['alt'])

    # Determine the shards for each build
    all_shards = []
    active_shards = soup.find_all('div', class_ = "fragment__detail")
    for i in range(len(active_shards)):
        shard_option = active_shards[i].find_all('div', class_ = "fragment__row")
        _shard = []
        for j in range(len(shard_option)):
            for k in range(3):
                if ('class="active tip"' in str(shard_option[j].find_all('img')[k])):
                    _shard.append(k)

    # TODO: clean up data processing. op.gg seems always have 4 options but that could change
    # Formats data into a list of all runes
        if i in [0,1]:
            primary_path = [rune_paths[0][0],all_runes[(6*i):(4+(i*6))]]
            secondary_path = [rune_paths[0][1],all_runes[4+(6*i):(6+(i*6))]]
            rune_options.append([primary_path,secondary_path,_shard])
        else:
            primary_path = [rune_paths[1][0],all_runes[(6*i):(4+(i*6))]]
            secondary_path = [rune_paths[1][1],all_runes[4+(6*i):(6+(i*6))]]
            rune_options.append([primary_path,secondary_path,_shard])
    return(rune_options)

def get_build(lane, name):
    """
    Gets build for a champion in a specific lane
    """
    build = [
        ('starter_items_1', []),
        ('starter_items_2', []),
        ('build_1', []),
        ('build_2', []),
        ('build_3', []),
        ('build_4', []),
        ('build_5', []),
        ('boots_1', []),
        ('boots_2', []),
        ('boots_3', [])
    ]
    data = requests.get("https://na.op.gg/champion/" +
                        name + "/statistics/" + lane)
    soup = BeautifulSoup(data.text, "html.parser")
    table = soup.find_all("table", {"class": "champion-overview__table"})
    tbody = table[1].find("tbody")
    tr = tbody.find_all("tr", {"class": "champion-overview__row"})
    for i in range(0, 10):
        td = tr[i].find("td", {"class": "champion-overview__data"})
        ul = td.find("ul", {"class": "champion-stats__list"})
        li = ul.find_all("li")
        for j in li:
            try:
                mystr = j['title']
                start = mystr.find('>') + 1
                end = mystr.find('<', 1)
                build[i][1].append(mystr[start:end])
            except KeyError:
                pass
    return build
