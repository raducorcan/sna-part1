import logging

from data_aquisition.crawling.domain import RawLawProject
from data_aquisition.crawling.law_projects.crawler import get_all_law_projects, get_approved_law_projects, \
    get_denied_law_projects
from data_aquisition.interpreting.law_projects.interpreter import interpret_raw_file
from jsons.utils import save_to_json


def get_serializable_project_list(project_list):
    return list(map(RawLawProject.to_dict, project_list))


if __name__ == '__main__':
    logging.basicConfig(format='(%(asctime)s) - [%(levelname)s]: "%(message)s"', level=logging.INFO)

    # Crawling phase:
    years = [2021, 2020, 2019, 2018, 2017, 2016]

    for year in years:
        input_file = f'../data/raw/law_projects/all/deputies_{year}.json'
        output_file = f'../data/interpreted/law_projects/all/deputies_{year}.json'

        interpret_raw_file(input_file, output_file)



    for year in []:
        logging.info(f"--- Starting to proces year {year}: ---")

        # All law projects
        deputies_all_projects = get_all_law_projects(year, cam=2)
        # senators_all_projects = get_all_law_projects(year, cam=1)

        deputies_all_projects_json_serializable = get_serializable_project_list(deputies_all_projects)
        # senators_all_projects_json_serializable = get_serializable_project_list(senators_all_projects)

        save_to_json(deputies_all_projects_json_serializable, f'../data/raw/law_projects/all/deputies_{year}.json')
        # save_to_json(senators_all_projects_json_serializable, f'../data/raw/law_projects/all/senators_{year}.json')

        # Approved law projects
        # deputies_approved_projects = get_approved_law_projects(year, cam=2)
        # # senators_approved_projects = get_approved_law_projects(year, cam=1)
        #
        # deputies_approved_projects_json_serializable = get_serializable_project_list(deputies_approved_projects)
        # senators_approved_projects_json_serializable = get_serializable_project_list(senators_approved_projects)
        #
        # save_to_json(deputies_approved_projects_json_serializable, f'../data/raw/law_projects/approved/deputies_{year}.json')
        # save_to_json(senators_approved_projects_json_serializable, f'../data/raw/law_projects/approved/senators_{year}.json')
        #
        # # Denied law projects
        # deputies_denied_projects = get_denied_law_projects(year, cam=2)
        # senators_denied_projects = get_denied_law_projects(year, cam=1)
        #
        # deputies_denied_projects_json_serializable = get_serializable_project_list(deputies_denied_projects)
        # senators_denied_projects_json_serializable = get_serializable_project_list(senators_denied_projects)
        #
        # save_to_json(deputies_denied_projects_json_serializable, f'../data/raw/law_projects/denied/deputies_{year}.json')
        # save_to_json(senators_denied_projects_json_serializable, f'../data/raw/law_projects/denied/senators_{year}.json')

