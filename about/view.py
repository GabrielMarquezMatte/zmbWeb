# -*- coding: utf-8 -*-

from dash import dcc
from dash import html

from common import (
    common_body_style,
    common_header_style,
    common_info_box_html,
    common_stat_style,
    logo_html,
)
from constants import db_stats


"""
View html blocks for the about app.

Please do not define callback logic in this file.
"""


def app_view_html():
    """
    The entire app view (layout) for the about app.

    Returns:
        (dash_html_components.Div): The entire view for the about app.
    """
    introduction = introduction_html()

    return html.Div([introduction])


def introduction_html():
    """
    The introduction block.

    Returns:
        (dash_html_components.Div): The introduction html block.

    """
    logo = logo_html()
    introduction_subheader_txt = (
        "Um assistente virtual no combate à discriminação racial \n"
    )
    introduction_body_txt = (
        "Zumbi é uma iniciativa da Faculdade de Estudos Interdisciplinares (FACEI) "
        "da Pontifícia Universidade Católica de São Paulo (PUC-SP). "
        "O objetivo deste projeto é coletar publicações relevantes "
        "da mídia brasileira utilizando técnicas de Processamento de Linguagem Natural "
        "e extrair métricas que possam colaborar com a pesquisa e a "
        "formulação de políticas públicas sobre o racismo. "
        "Até o momento, nosso banco de dados contém "
    )

    introduction_body_txt2 = (
        "De tempos em tempos atualizamos nossa coleção com novas matérias "
        "jornalísticas sobre o racismo. Você pode ler mais sobre nossa "
        "pesquisa nas publicações listadas a seguir: "
    )

    publication_header_txt = "Publicações:"

    reference_1_txt = (
        "JANSEN, M. R., SILVA, J. O., LEMES, D. O.: A Discriminação Racial na Mídia Brasileira. "
        "**Em breve nas Revistas**. 2021"
    )

    reference_2_txt = (
        "SILVA, J. O., JANSEN, M. R., LEMES, D. O.: Um Modelo de Extração de Entidades Nomeadas para a Discriminação Racial no Brasil. "
        "**Em breve nas Revistas**. 2021"
    )

    why_use_header_txt = "Por quê usar o Zumbi?"
    why_use_body_txt = (
        "1. **É grátis**: Disponibilizamos o Zumbi gratuitamente a todos."
        "Disponibilizamos nosso modelo NLP em "
        "[Github](https://github.com/PUC-SP/zumbi) "
        "(incluindo o código-fonte para este site). "
        "Além disso, disponibilizamos uma API Python para buscas programáticas  "
        "em nosso banco de dados em  "
        "[Github](https://github.com/PUC-SP/zumbi).\n"
        "2. **Vai além do que a Google pode fazer**: "
        "O Zumbi vai além da busca por similaridade textual e usa "
        "contabiliza entidades especificamente treinadas na análise de "
        "milhares de matérias jornalísticas sobre a discriminação racial.\n "
        "3. **É (relativamente) rápido**: A cada dia ficamos mais rápidos! "
        "Estamos ativamente trabalhando em nossa infraestrutura para tornar o "
        "Zumbi mais rápido, mais preciso e mais informativo."
    )

    funding_header_txt = "Nossos patrocinadores"
    funding_body_txt = (
        "O Zumbi é uma iniciativa da FACEI na PUC-SP em busca de patrocinadores."
    )

    introduction_body_md = dcc.Markdown(introduction_body_txt)
    introduction_body_md2 = dcc.Markdown(introduction_body_txt2)
    why_use_body_md = dcc.Markdown(why_use_body_txt)
    reference_1_md = dcc.Markdown(reference_1_txt)
    reference_2_md = dcc.Markdown(reference_2_txt)
    funding_md = dcc.Markdown(funding_body_txt)

    introduction_subheader = html.Div(
        introduction_subheader_txt, className=common_header_style()
    )
    publication_header = html.Div(
        publication_header_txt, className=common_header_style()
    )
    introduction_body = html.Div(
        introduction_body_md, className=common_body_style()
    )
    introduction_body2 = html.Div(
        introduction_body_md2, className=common_body_style()
    )

    current_stats = current_stats_html()

    reference_1 = html.Div(reference_1_md, className=common_body_style())
    reference_2 = html.Div(reference_2_md, className=common_body_style())

    why_use_header = html.Div(
        why_use_header_txt, className=common_header_style()
    )
    why_use_body = html.Div(why_use_body_md, className=common_body_style())
    why_use_body_container = html.Div(
        why_use_body,
        className="has-margin-right-40 has-margin-left-40 has-margin-top-5 has-margin-bottom-5",
    )
    funding_header = html.Div(
        funding_header_txt, className=common_header_style()
    )
    funding_body = html.Div(funding_md, className=common_body_style())

    elements = [
        logo,
        introduction_subheader,
        introduction_body,
        current_stats,
        introduction_body2,
        publication_header,
        reference_1,
        reference_2,
        why_use_header,
        why_use_body_container,
        funding_header,
        funding_body,
    ]
    container = common_info_box_html(elements, id="about_id")
    return container


def current_stats_html():
    """
    WARNING: Do not edit this unless you know EXACTLY what you're doing.
    This block systematically defines elements used by clientside callbacks.
    Editing this without knowing how it works will likely result in javascript
    headaches.

    Get the html block for the current stats.

    Returns:
        (dash_html_components.Div): The html block for the current stats, including
            counting up animations.

    """
    label_map = {
        "materials": "entidades únicas",
        "entities": "entidades relacionadas",
        "abstracts": "matérias analisadas",
    }

    stats_columns = []

    # WARNING: don't mess with this section unless you know what you're doing!
    # The children of these divs needs to be ints for the javascript to
    # work correctly. Do NOT change the ids without changing the corresponding
    # javascript!
    # The ids currently are count-materials, count-abstracts, count-entities
    # The ids which it reads from are count-*-hidden-ref. The values it updates
    # are count-*. This is to prevent messing up quick reloads and double clicks
    for k, v in label_map.items():
        stat = html.Div(
            "{:,}".format(db_stats[k]),
            id=f"about-count-{k}-cs",
            className=f"is-size-4-desktop {common_stat_style()}",
        )
        stat_static_value = html.Div(
            "{:,}".format(db_stats[k]),
            id=f"about-count-{k}-hidden-ref-cs",
            className="is-hidden",
        )
        stat_descriptor = html.Div(
            f"{v}", className=f"is-size-6-desktop {common_stat_style()}"
        )
        stat_column = html.Div(
            [stat, stat_descriptor, stat_static_value],
            className="flex-column is-one-third",
        )
        stats_columns.append(stat_column)

    stats_columns = html.Div(
        stats_columns, className="columns is-centered is-desktop"
    )

    all_stats = html.Div(
        id="stats-container",
        children=stats_columns,
        className="container has-margin-top-30 has-margin-bottom-30",
    )

    return all_stats
