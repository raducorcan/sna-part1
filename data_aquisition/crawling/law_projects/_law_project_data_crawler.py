from data_aquisition.crawling.domain import RawInitiator, RawLawProject
from data_aquisition.crawling.utils import create_soup_from_url
from jsons.utils import save_to_json


def _get_law_project_from_url(law_project_url):
    print(f"Processing law project from '{law_project_url}'.")

    soup = create_soup_from_url(law_project_url)

    try:
        law_project_id, description = _get_law_project_id_and_description(soup)
    except Exception as exc:
        law_project_id, description = '', ''
        print(f'Error while trying to extract law_project_id and description from {law_project_url}:{str(exc)}')

    try:
        initiators = _get_law_project_initiators(soup)
    except Exception as exc:
        initiators = []
        print(f'Error while trying to extract initiators from {law_project_url}:{str(exc)}')

    try:
        senators_date, deputies_date = _get_law_project_creation_date(soup)
    except Exception as exc:
        senators_date, deputies_date = '', ''
        print(f'Error while trying to extract date from {law_project_url}:{str(exc)}')

    return RawLawProject(law_project_id, description, initiators, senators_date, deputies_date)


def _get_law_project_creation_date(soup):
    senators_date, deputies_date = '', ''

    col1 = soup.find("td", string='- Senat:')
    if col1 is not None:
        col2 = col1.nextSibling
        senators_date = col2.string

    col1 = soup.find("td", string='- Camera Deputatilor:')
    if col1 is not None:
        col2 = col1.nextSibling
        deputies_date = col2.string

    return senators_date, deputies_date


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
    pl = _get_law_project_from_url('http://www.cdep.ro/pls/proiecte/upl_pck.proiect?cam=2&idp=15883')
    print(pl.to_dict())

