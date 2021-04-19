from data_aquisition.crawling.domain import RawLawProject
from data_aquisition.interpreting.domain import LawProject, Status
from data_aquisition.interpreting.law_projects._law_project_data_interpreter import _get_interpreted_law_projects
from jsons.utils import load_from_json, save_to_json


def interpret_raw_file(input_file, output_file):
    raw_law_proj_dicts = load_from_json(input_file)
    raw_law_projs = list(map(RawLawProject.from_dict, raw_law_proj_dicts))
    law_projs = _get_interpreted_law_projects(raw_law_projs, 2021, Status.PENDING)

    law_projs_dicts = list(map(LawProject.to_dict, law_projs))
    save_to_json(law_projs_dicts, output_file)
