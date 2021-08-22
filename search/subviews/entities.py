# -*- coding: utf-8 -*-

import dash_html_components as html

from constants import entity_color_map, rester
from search.common import (
    big_label_and_disclaimer_html,
    common_results_container_style,
    no_results_html,
)

"""
Functions for defining the results container when entity results are desired.

Please do not define callback logic in this file.
"""

# Maximum number of rows shown for each entity table. 10 usually looks good.
MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10

# Maximum number of columns to fit on the screen
MAX_N_COLUMNS = 3

big_label_and_disclaimer = big_label_and_disclaimer_html("entities")
entities_no_results_html = no_results_html(pre_label=big_label_and_disclaimer)

db2front_ent_types = {
    "PER": "pes",
    "MED": "mid",
    "EDU": "educ",
    "ORG": "com",
    "GOV": "gov",
    "CITY": "cid",
    "CTRY": "pais",
    "POL": "pol",
    "WRK": "obra",
    "MOV": "mov",
    "text": "texto"
}

def entities_results_html(entity_query, raw_text):
    """
    Get the html block for entities results from the Rester-compatible
    entity query and text.

    Args:
        entity_query (dict): The entity query, in Rester-compatible format.
        raw_text (str, None): Any raw text to search for.

    Returns:
        (dash_html_components.Div): The entities results html block.

    """
    results = rester.entities_search(
        entity_query, text=raw_text, top_k=MAX_N_ROWS_FOR_EACH_ENTITY_TABLE
    )
    # It seems that results should
    if results is None or not any([v for v in results.values()]):
        return entities_no_results_html
    else:
        all_tables = all_score_tables_html(results)
        all_tables_container = html.Div(
            children=[big_label_and_disclaimer, all_tables],
            className=common_results_container_style(),
        )
        return all_tables_container


def all_score_tables_html(results_dict):
    """
    Get all the score tables for all entity types as an html block.

    Args:
        results_dict (dict): The result dictionary directly from the Rester.

    Returns:
       (dash_html_components.Div): The entity table as an html block.
    """
    columns_classes = "columns is-desktop is-centered"

    half = "is-half"
    third = "is-one-third"

    div_rows, div_elems = [], []

    k = 0 # an entity type counter
    for entity_type in results_dict.keys():
        k += 1

        front_ent_type = db2front_ent_types.get(entity_type)
        div_elems.append(
            single_entity_score_table_html( results_dict[entity_type], front_ent_type, third )
        )

        is_k_div_by_3 = k % 3 == 0

        # If k is not divisible by 3 and is not the last element,
        # then continue populating div_elems
        if (k != len(results_dict) and not is_k_div_by_3):
            continue

        div_rows.append(html.Div(div_elems, className=columns_classes))

        if (is_k_div_by_3):
            div_elems = []

    return html.Div(div_rows)

def single_entity_score_table_html(most_common, entity_type, width):
    """
    Get the html block for a single entity's score table.

    Args:
        most_common ([str]): The most common entities of this type.
        entity_type (str): The entity type (e.g., "pessoa")
        width (the width of the table in terms of the table container). Valid
            widths are specified according to bulma column widths, e.g.,
            "is-half".

    Returns:
        (dash_html_components.Div): A single entity table html block.
    """
    n_results = len(most_common)

    formatted_n_results = min(n_results, MAX_N_ROWS_FOR_EACH_ENTITY_TABLE)
    if formatted_n_results == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE:
        table_label = f"Top {formatted_n_results} entidades"
    else:
        table_label = f"Todas as {formatted_n_results} entidades"

    color = entity_color_map[entity_type.lower()]
    header_entity_type = html.Span(
        f"{entity_type}", className=f"msweb-has-{color}-txt"
    )
    header_table_label = html.Span(f": {table_label}")

    header_entity_type = html.Th([header_entity_type, header_table_label])
    header_score = html.Th("Cont")
    header = html.Tr([header_entity_type, header_score])

    rows = [None] * n_results

    row_number = 0
    for dic in most_common:
        ent, count = dic['name'], dic['count']
        entity = html.Td(ent, className="has-width-50")
        count = html.Td("{:.2f}".format(count), className="has-width-50")
        rows[row_number] = html.Tr([entity, count])
        row_number += 1
        if row_number == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE - 1:
            break
    table = html.Table(
        [header] + rows,
        className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped",
    )
    return html.Div(table, className=f"column {width}")
