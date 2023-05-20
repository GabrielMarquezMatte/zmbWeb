# -*- coding: utf-8 -*-

from dash import dcc
from dash import html

from common import (
    common_body_style,
    common_header_style,
    common_info_box_html,
    common_title_style,
    divider_html,
)
from constants import db_stats


"""
View html blocks for the journal app.

Please do not define callback logic in this file.
"""


def app_view_html():
    """
    The entire app view (layout) for the journal app.

    Returns:
        (dash_html_components.Div): The entire view for the journal app.
    """
    journals = journal_info_html()

    return html.Div([journals])


def journal_info_html():
    """
    Get the html block for journal info.

    Returns:
        (dash_html_components.Div): The html block for journal info and
            dropdown.
    """
    journals = db_stats["journals"]
    n_journals = "{:,}".format(len(journals))

    journal_info_header_txt = "Mídias no Zumbi"
    journal_info_subheader_txt = (
        f"Pesquise entre {n_journals} mídias jornalísticas"
    )
    journals_info_body_txt = (
        f"Neste momento o Zumbi conta com "
        f"{n_journals} matérias jornalísticas. Você pode pesquisar quais "
        f"mídias que processamos pelo menos uma matéria utilizando "
        f"o campo de busca a seguir."
    )

    journal_info_header = html.Div(
        journal_info_header_txt, className=common_title_style()
    )
    journal_info_subheader = html.Div(
        journal_info_subheader_txt, className=common_header_style()
    )
    journal_info_body = html.Div(
        journals_info_body_txt, className=common_body_style()
    )

    jkeys = [{"label": v, "value": str(i)} for i, v in enumerate(journals)]
    dropdown = dcc.Dropdown(
        placeholder="Pesquise sua mídia favorita...",
        options=jkeys,
        className="is-size-6 has-margin-bottom-50",
        clearable=False,
        multi=True,
        optionHeight=25,
    )
    dropdown_label = html.Div(
        "Pesquise nossa coleção", className=common_header_style()
    )

    hr_dropdown = divider_html()

    elements = [
        journal_info_header,
        journal_info_subheader,
        journal_info_body,
        hr_dropdown,
        dropdown_label,
        dropdown,
    ]

    container = common_info_box_html(elements, id="journals")
    return container
