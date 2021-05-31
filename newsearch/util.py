# -*- coding: utf-8 -*-

import copy
import re

from dash.dependencies import Input, Output, State

from constants import valid_search_filters

"""
All utility functions for search.
"""

MAX_N_PATTERNS_PER_ENTITY = 10
MAX_N_CHARS_PER_PATTERN = 300


class ZumbiWebSearchError(BaseException):
    """
    An exception to be used for search app errors.

    Can also be used as a parent class for more specific exceptions.
    """

    pass


def get_search_field_callback_args(as_type="state", return_component="value"):
    """
    Return all available entity boxes as Inputs, Outputs, or States.

    Args:
        as_type (str): "state" for State, "input" for Input, or "output" for
            Output
        return_component (str): Either "value" for the value of the search
            box or n_submit for the number of times the search box has been
            hit.

    Returns:
        (list): The list of inputs, states, or outputs plotly dash dependency
            objects on the search page.
    """
    type_dict = {"state": State, "output": Output, "input": Input}
    t = type_dict[as_type]

    filters = []
    for f in valid_search_filters:
        filters.append(t("search-" + f + "-filters-input", return_component))
    return filters


def parse_search_box(search_text):
    """
    Parse the entity search text box

    Args:
        search_text (Str): The text in the search box, e.g.
            "material: PbTe, property: thermoelectric"

    Returns:
        entity_query (dict): The entity query in rester working context
        raw_text (str): The raw text to pass into the text field
    """
    if not search_text.strip():
        raise ZumbiWebSearchError("No text entered!")

    for f in valid_search_filters:
        if f in search_text.lower():
            redata = re.compile(re.escape(f), re.IGNORECASE)
            search_text = redata.sub(f, search_text)

    re_delimiters = "|".join(valid_search_filters)
    field_patterns = re.findall(f"({re_delimiters}):", search_text)

    if len(set(field_patterns)) < len(field_patterns):
        raise ZumbiWebSearchError("Redundant entity fields entered!")

    if not all([p in valid_search_filters for p in field_patterns]):
        raise ValueError(
            f"Regex'd a field (one of {field_patterns}) which is not a "
            f"valid search filter!"
        )

    if len(field_patterns) == 0:
        raise ZumbiWebSearchError("No valid entity fields entered!")

    entity_query = {}
    field_patterns.reverse()
    rtext = copy.deepcopy(search_text)
    for fp in field_patterns:
        query_pattern = re.findall(f"{fp}:.*", rtext)[0]
        rtext = rtext.replace(query_pattern, "")
        query_pattern = query_pattern.replace(f"{fp}:", "")
        query_patterns = [qt.strip() for qt in query_pattern.split(",")]
        query_patterns = [qt for qt in query_patterns if qt]
        entity_query[fp] = query_patterns

    if any(
        [len(v) > MAX_N_PATTERNS_PER_ENTITY for v in entity_query.values()]
    ):
        raise ZumbiWebSearchError

    for ent, query_patterns in entity_query.items():
        n_terms = len(query_patterns)
        if n_terms > MAX_N_PATTERNS_PER_ENTITY:
            raise ZumbiWebSearchError(
                f"Length of patterns for entity {ent} ({n_terms}) exceeds maximum for an entity {MAX_N_PATTERNS_PER_ENTITY}"
            )
        for pattern in query_patterns:
            n_chars = len(pattern)
            if n_chars > MAX_N_CHARS_PER_PATTERN:
                raise ZumbiWebSearchError(
                    f"Length of pattern {pattern} ({n_chars}) exceeds maximum for a pattern ({MAX_N_CHARS_PER_PATTERN})."
                )

    if "texto" in entity_query.keys():
        if not entity_query["texto"]:
            raw_text = None
        else:
            raw_text = entity_query.pop("texto")[0]
            if not raw_text.strip():  # remove empty strings
                raw_text = None
    else:
        raw_text = None

    n_entities = len(list(entity_query.values()))
    n_raw_text = 1 if raw_text else 0
    n_fields = n_entities + n_raw_text
    n_fields_entered = search_text.count(":")
    if n_fields != n_fields_entered:
        raise ZumbiWebSearchError(
            f"The number of parsed fields ({n_fields}) does not equal the number of entered fields ({n_fields_entered})!"
        )

    if not raw_text and not any([e_list for e_list in entity_query.values()]):
        raise ZumbiWebSearchError(
            f"No raw text or entities parsed for any of the entered fields: {list(entity_query.values())}"
        )

    if not entity_query and not raw_text:
        raise ZumbiWebSearchError("No raw text nor entity query parsed!")

    return entity_query, raw_text
