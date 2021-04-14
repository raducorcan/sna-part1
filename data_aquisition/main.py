from data_aquisition.crawling.domain import RawLawProject
from data_aquisition.crawling.law_projects.crawler import get_all_law_projects
from jsons.utils import save_to_json


def get_serializable_project_list(project_list):
    return list(map(RawLawProject.to_dict, project_list))


if __name__ == '__main__':
    # Crawling phase:
    years = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013]

    for year in years:
        print(f"--- Starting to proces year {year}: ---")
        deputies_all_projects = get_all_law_projects(year, cam=2)
        senators_all_projects = get_all_law_projects(year, cam=1)

        deputies_all_projects_json_serializable = get_serializable_project_list(deputies_all_projects)
        senators_all_projects_json_serializable = get_serializable_project_list(senators_all_projects)

        save_to_json(deputies_all_projects_json_serializable, f'../data/raw/law_projects/all/senators_{year}.json')
        save_to_json(senators_all_projects_json_serializable, f'../data/raw/law_projects/all/deputies_{year}.json')
        print('\n')
