import datetime
import logging
from typing import List

from data_aquisition.crawling.domain import RawLawProject
from data_aquisition.interpreting.domain import LawProject, Status, Initiator
from jsons.utils import load_from_json, save_to_json


def _extract_date(date_string):
    try:
        slash_index = date_string.index('/')
        stripped_date = date_string[slash_index + 1:]
        return datetime.datetime.strptime(stripped_date, '%d.%m.%Y').date()
    except Exception:
        return None


def _trim_spaces_colons(text: str):
    return text.strip(' :')


def _extract_party_from_key(key):
    # key = 'deputati - PNL:'
    # key = '- neafilitati:'
    minus_index = key.index('-')

    if minus_index == -1:
        logging.warning(f"Could not find minus index for key {key}")
    else:
        key = key[minus_index + 1:]

    return _trim_spaces_colons(key)


def _get_initiators(initiators_dict: dict):
    result = []

    for key in initiators_dict:
        party = _extract_party_from_key(key)
        raw_initiators = initiators_dict[key]
        initiators = list(map(lambda raw: Initiator(raw.href, raw.name, party), raw_initiators))
        result.extend(initiators)

    return result


def _get_interpreted_law_projects(raw_law_projects: List[RawLawProject], year, status):
    result = []
    for raw_law_proj in raw_law_projects:
        initiators = _get_initiators(raw_law_proj.initiators)

        senators_date = _extract_date(raw_law_proj.senators_date)
        deputies_date = _extract_date(raw_law_proj.deputies_date)

        result.append(LawProject(id=raw_law_proj.id,
                                 description=raw_law_proj.description,
                                 initiators=initiators,
                                 senators_date=senators_date,
                                 deputies_date=deputies_date,
                                 year=year,
                                 status=status,
                                 )
                      )

    return result


if __name__ == '__main__':
    raw_law_proj_dicts = load_from_json('../../../data/raw/law_projects/all/deputies_2021.json')
    raw_law_projs = list(map(RawLawProject.from_dict, raw_law_proj_dicts))
    law_projs = _get_interpreted_law_projects(raw_law_projs, 2021, Status.PENDING)

    law_projs_dicts = list(map(LawProject.to_dict, law_projs))
    save_to_json(law_projs_dicts, '../../../data/interpreted/law_projects/all/deputies_2021.json')

