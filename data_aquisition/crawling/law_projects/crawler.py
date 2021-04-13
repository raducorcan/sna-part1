from data_aquisition.crawling.law_projects._law_project_data_crawler import _get_law_project_from_url
from data_aquisition.crawling.law_projects._law_project_url_crawler import _get_law_project_urls


def get_all_law_projects(year, cam=2):
    hrefs = _get_law_project_urls(f'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam={cam}&anp={year}')

    result = []
    for href in hrefs:
        result.append(_get_law_project_from_url(href))
    return result


def get_approved_law_projects(year, cam=2):
    hrefs = _get_law_project_urls(f'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam={cam}&anl={year}')

    result = []
    for href in hrefs:
        result.append(_get_law_project_from_url(href))
    return result


def get_denied_law_projects(year, cam=2):
    hrefs = _get_law_project_urls(f'http://www.cdep.ro/pls/proiecte/upl_pck.lista?cam={cam}&std=O&ans={year}')

    result = []
    for href in hrefs:
        result.append(_get_law_project_from_url(href))
    return result


if __name__ == '__main__':
    all = get_all_law_projects(2021)
    print(all)
