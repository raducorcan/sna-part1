replace = {
    'ă': 'a',
    'â': 'a',
    'î': 'i',
    'ț': 't',
    'Ț': 'T',
    'ș': 's',
    'Ș': 'S',
    'á': 'a',
    'Á': 'A',
    'ó': 'o',
    'é': 'e',
    'Ő': 'O',
    'ő': 'o',
    'Ö': 'O',
    'ö': 'o',
    'ţ': 't',
    'ş': 's',
    'Ş': 'S',
    'Ţ': 'T',
}


def sanitize_string(s):
    for c in replace.keys():
        s = s.replace(c, replace[c])
    return s
