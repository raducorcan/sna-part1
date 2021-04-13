import urllib3
import json
from bs4 import BeautifulSoup

urls = [
    'http://www.cdep.ro/pls/dic/legis_acte_parlam?cam=0&tip=1&an=2020',
    # 'http://www.cdep.ro/pls/dic/legis_acte_parlam?cam=0&tip=1&an=2019',
    # 'http://www.cdep.ro/pls/dic/legis_acte_parlam?cam=0&tip=1&an=2018',
    # 'http://www.cdep.ro/pls/dic/legis_acte_parlam?cam=0&tip=1&an=2017'
]

base_url = "http://www.cdep.ro/pls/proiecte"


def create_soup_from_url(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup


def crawl_approved_laws(urls, names_dict, edges):
    for url in urls:
        soup = create_soup_from_url(url)
        crawl_approved_laws_from_soup(soup, names_dict, edges)

    return list(map(lambda x: {"n1": x[0], "n2": x[1], "w": edges[x]}, edges.keys()))


def get_project_a(approval_a):
    approval_url = f'http://www.cdep.ro{approval_a["href"]}'
    # approval_url = f'http://www.cdep.ro/pls/legis/legis_pck.htp_act?ida=143039&frame=0'
    approval_url = approval_url[:-8]
    soup = create_soup_from_url(approval_url)
    return soup.find("a", {"target": "UPL"})


def crawl_approved_laws_from_soup(soup: BeautifulSoup, names_dict, edges):
    header = soup.find("tr", {"bgcolor": "#31639C"})
    approval_hyperlinks = header.parent.find_all("a")
    for approval_index, approval_a in enumerate(approval_hyperlinks):
        a = get_project_a(approval_a)
        href = a['href']
        law_project_url = f'http://www.cdep.ro{href.replace("2015", "")}'
        get_initiators(law_project_url, names_dict, edges)

        print(f"Processed {approval_index}/{len(approval_hyperlinks)}")


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


def crawl_party(names, party_dict):
    for query in names.keys():
        url = f'http://www.cdep.ro/pls/parlam/structura.mp?{query}'
        soup = create_soup_from_url(url)
        hyperlinks = soup.find_all("a")
        for a in hyperlinks:
            if 'structura.fp' in a['href']:
                party_dict[query] = a.string
                print(a.string)
                break


def save_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


#
#
# # data = crawl_data(urls, _names_dict, _edges)
# #
# # save_to_json(data, "edges.jsons")
# # save_to_json(_names_dict, "names.jsons")
#
def open_json(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data


# _names_dict = open_json('names.jsons')
# crawl_party(_names_dict, _party_dict)
# save_to_json(_party_dict, "parties.jsons")
_names_dict = {}
_party_dict = {}
_edges = {}
data = crawl_approved_laws(urls, _names_dict, _edges)

save_to_json(data, "edges_approved.jsons")
save_to_json(_names_dict, "names_approved.jsons")

# _names_dict = open_json('names_approved.jsons')
crawl_party(_names_dict, _party_dict)
save_to_json(_party_dict, "parties_approved.jsons")
