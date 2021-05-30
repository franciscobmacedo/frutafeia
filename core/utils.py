from core.enum import ESTADO_CHOICES, MEDIDA_CHOICES, TIPO_PRODUTO_CHOICES


def get_choice_value(choice_str, choices):
    choice_nr = [
        t[0] for t in choices if t[1].lower().strip() == choice_str.lower().strip()
    ]
    if not choice_nr:
        return None
    return choice_nr[0]


def get_estado(estado_str):
    return get_choice_value(estado_str, ESTADO_CHOICES)


def get_tipo_produto(tipo_str):
    return get_choice_value(tipo_str, TIPO_PRODUTO_CHOICES)


def get_medida(medida_str):
    if isinstance(medida_str, str):
        medida_str = medida_str.lower().capitalize()
        return get_choice_value(medida_str, MEDIDA_CHOICES)
    else:
        return None
