import urllib3
import json
from bs4 import BeautifulSoup

urls = [
    'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anp=2020',
    # 'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anp=2019',
    # 'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anp=2018',
    # 'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anp=2017',
]

base_url = "http://www.cdep.ro/pls/proiecte"


def create_soup_from_url(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup


def crawl_data(urls, names_dict, edges):
    for url in urls:
        soup = create_soup_from_url(url)
        process_soup(soup, names_dict, edges)

    return list(map(lambda x: {"n1": x[0], "n2": x[1], "w": edges[x]}, edges.keys()))


def process_soup(soup: BeautifulSoup, names_dict, edges):
    hyperlinks = soup.select(
        'body > table > tr > td:nth-child(2) > table:nth-child(2) > tr > td:nth-child(2) > p > p > table tr > td:nth-child(2) a')
    for a_index, a in enumerate(hyperlinks):
        href = a['href']
        law_project_url = f'{base_url}/{href}'
        get_initiators(law_project_url, names_dict, edges)

        print(f"Processed {a_index}/{len(hyperlinks)}")


def get_initiators(law_project_url, names_dict, edges):
    soup = create_soup_from_url(law_project_url)
    col1 = soup.find("td", string="Initiator:")
    hyperlinks = col1.parent.select("td:nth-child(2) a")

    hrefs = []
    names = []
    print(f"Processing law {law_project_url} with {len(hyperlinks)} initiators.")
    for a in hyperlinks:
        name = a.string.replace(u'\xa0', u' ')

        index = a["href"].index("?")
        href = a["href"][index + 1:]

        names.append(name)
        if href in names_dict and names_dict[href] != name:
            print(f"!!! Name conflict !!! '{name}' vs '{names_dict[href]}'.")

        names_dict[href] = name

        hrefs.append(href)

    for i in range(len(hrefs)):
        for j in range(i + 1, len(hrefs)):
            dict_key = tuple(sorted([hrefs[i], hrefs[j]]))
            if dict_key not in edges:
                edges[dict_key] = 0
            edges[dict_key] += 1


def save_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


_names_dict = {}
_edges = {}
data = crawl_data(urls, _names_dict, _edges)

save_to_json(data, "edges.json")
save_to_json(_names_dict, "names.json")
