from data_aquisition.crawling.law_projects.crawler import get_all_law_projects
from jsons.utils import save_to_json

if __name__ == '__main__':
    # Crawling phase:
    years = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013]

    for year in years:
        deputies_all_projects = get_all_law_projects(year, cam=2)
        senators_all_projects = get_all_law_projects(year, cam=1)

        save_to_json(deputies_all_projects, f'../data/raw/law_projects/all/senators_{year}.json')
        save_to_json(senators_all_projects, f'../data/raw/law_projects/all/deputies_{year}.json')
