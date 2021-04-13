from data_aquisition.crawling.domain import RawInitiator, RawLawProject
from data_aquisition.crawling.utils import create_soup_from_url


def _get_law_project_from_url(law_project_url):
    print(f"Processing law project from '{law_project_url}'.")

    soup = create_soup_from_url(law_project_url)
    law_project_id, description = _get_law_project_id_and_description(soup)
    initiators = _get_law_project_initiators(soup)
    date = _get_law_project_creation_date(soup)
    return RawLawProject(law_project_id, description, initiators, date)


def _get_law_project_creation_date(soup):
    col1 = soup.find("td", string='- Camera Deputatilor:')
    col2 = col1.nextSibling
    return col2.string


def _get_law_project_id_and_description(soup):
    td = soup.select_one(
        'body > table tr > td:nth-child(2) > table:nth-child(2) tr > td:nth-child(2) > p:nth-child(2) > table tr td:nth-child(2)')
    children = td.children
    law_project_id = next(children)
    next(children)  # skip <br/> tag
    description = next(children)
    return law_project_id, description


def _get_law_project_initiators(soup):
    col1 = soup.find("td", string="Initiator:")
    hyperlinks = col1.parent.select("td:nth-child(2) a")

    initiators = []

    for a in hyperlinks:
        name = a.string.replace(u'\xa0', u' ')
        href = a["href"]
        url = f'http://www.cdep.ro{href}'

        initiators.append(RawInitiator(name, url))

    return initiators


if __name__ == '__main__':
    pl = _get_law_project_from_url('http://www.cdep.ro/pls/proiecte/upl_pck.proiect?cam=2&idp=18305')
    print(pl)
