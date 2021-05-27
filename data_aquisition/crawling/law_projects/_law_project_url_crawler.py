import logging

from data_aquisition.crawling.utils import create_soup_from_url


def _get_law_project_urls(year_url):
    logging.info(f"Getting law project urls from {year_url}")
    soup = create_soup_from_url(year_url)
    hyperlinks = soup.select(
        'body > table > tr > td:nth-child(2) > table:nth-child(2) > tr > td:nth-child(2) > p > p > table tr > td:nth-child(2) a')

    result = []
    for a_index, a in enumerate(hyperlinks):
        href = a['href']
        result.append(f'http://www.cdep.ro/pls/proiecte/{href}')

    return result


if __name__ == '__main__':
    all = _get_law_project_urls('http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anp=2021')
    approved = _get_law_project_urls('http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&anl=2021')
    denied = _get_law_project_urls('http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam=2&std=O&ans=2021')
