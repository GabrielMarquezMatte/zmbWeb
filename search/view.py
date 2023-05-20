# -*- coding: utf-8 -*-

from dash import dcc
from dash import html
from dash_elasticsearch_autosuggest import ESAutosuggest

from common import (
    common_null_warning_html,
    common_warning_html,
    logo_html,
)
from constants import (
    db_stats,
    elastic_host,
    elastic_pass,
    elastic_user,
    example_searches,
)
from zmb_labels import ZmbLabels

"""
View html blocks for the search app.

Please do not define callback logic in this file.
"""


def app_view_html():
    """
    The entire app view (layout) for the search app.

    Returns:
        (dash_html_components.Div): The entire view for the search app.
    """

    return html.Div(
        [
            logo_html(),
            search_bar_and_buttons_html(),
            guided_search_boxes_html(),
            subview_results_container_html(),
        ]
    )


def subview_results_container_html():
    """
    The placeholder html block for results. This is updated via callback.

    WARNING: for the loading animation to work correctly, it must be the direct
    parent of an html block which is being updated via callback.

    Args:
        None

    Returns:
        (dash_html_components.Div): The results container.

    """
    my_results_html = html.Div(id="search-results-container")
    wrapper = dcc.Loading(
        type="cube", children=my_results_html, className="msweb-fade-in"
    )
    return html.Div(wrapper)


def no_query_warning_html():
    """
    The html block when no query is entered and searched.

    Returns:
        (dash_html_components.Div): The html block when no query is entered.
    """
    null_txt = (
        f'Por favor digite um termo de busca e então clique em "Pesquisar" .'
    )
    return common_null_warning_html(null_txt)


def malformed_query_warning_html(bad_search_txt):
    """
    The html block when a query is malformed and searched.

    Args:
        bad_search_txt (str): The search text.

    Returns:
        (dash_html_components.Div): The html block when a malformed query is
            entered and searched.
    """
    warning_header_txt = f"Oops, we didn't understand that search."
    warning_body_txt = (
        f'\n Your search was: "{bad_search_txt}"\n. Try the format entity1: '
        f'value1, entity2: value2. For example: "person: George Floyd, '
        f'country: USA"'
    )
    return common_warning_html(warning_header_txt, warning_body_txt, "is-half")


def search_bar_and_buttons_html():
    """
    Get the html block for the search bar and Go and Example buttons.

    Returns:
        (dash_html_components.Div): The html block for the search bar and
            buttons
    """
    n_abstracts = "{:,}".format(db_stats["abstracts"])

    n_abstracts_hidden_ref = html.Span(
        id="search-count-abstracts-hidden-ref-cs",
        children=n_abstracts,
        className="is-hidden",
    )

    n_abstracts_link = dcc.Link(
        id="search-count-abstracts-cs",
        children=f"{n_abstracts}",
        href="/about",
        className="msweb-fade-in msweb-ubuntu",
    )

    label = html.Label(
        [
            "Pesquise ",
            n_abstracts_link,
            " matérias jornalísticas sobre a discriminação racial com IA",
        ],
        className="is-size-4-desktop has-margin-5",
    )
    label_container = html.Div(label, className="has-text-centered")

    search_bar = dcc.Input(
        placeholder=example_searches[-1],
        id="search-main-bar-input",
        className="input is-info is-medium",
        autoFocus=True,
    )

    sized = "is-size-7"
    tooltip_spans = [html.Span("Palavras-chave: ", className=sized)]
    for class_ in ZmbLabels.all_classes():
        color = class_.color()
        code = class_.web_label()
        tooltip_span = html.Span(
            code, className=f"msweb-is-{color}-txt {sized} has-text-weight-bold"
        )
        tooltip_spans.append(tooltip_span)
        tooltip_spans.append(html.Span(", "))

    tooltip_spans.pop(-1)

    search_bar_tooltip = html.Div(
        tooltip_spans, className=f"tooltip-text has-margin-0"
    )
    search_bar_html = html.Div(
        [label_container, search_bar, search_bar_tooltip],
        className="flex-column is-narrow tooltip",
    )

    go_button = html.Button(
        "Pesquisar",
        id="search-go-button",
        className="button is-info is-focused is-medium",
    )
    go_html = html.Div(
        go_button,
        className="flex-column is-narrow has-margin-left-10 has-margin-right-10",
    )

    example_search_button = html.Button(
        "Exemplo",
        id="search-example-button",
        className="button is-light is-focused is-medium",
    )
    example_search_html = html.Div(
        example_search_button,
        className="flex-column is-narrow has-margin-left-10 has-margin-right-10",
    )

    go_and_example_columns = html.Div(
        [go_html, example_search_html, n_abstracts_hidden_ref],
        className="columns is-centered has-margin-top-10 has-margin-bottom-20",
    )

    search_bar_centered = html.Div(
        search_bar_html, className="columns is-centered has-margin-bottom-10"
    )

    bar_and_go_container = html.Div(
        [search_bar_centered, go_and_example_columns], className="container"
    )

    example_search_container = hidden_ref_example_searches_html()
    bar_and_go_and_label_container = html.Div(
        [example_search_container, bar_and_go_container], className="container"
    )
    return bar_and_go_and_label_container


def hidden_ref_example_searches_html():
    """
    Get the hidden reference example search html. Used by callback to populate
    the search field.

    # todo: this can probably be written not as a hidden reference since it
    # todo: not updated via clientside callback anymore. The file can just
    # todo: be used in the same fashion as extract app random searches.

    Returns:
        (dash_html_components.Div): The html block for the hidden example
            search ref.

    """
    separator = " | "
    examples_as_string = [e + separator for e in example_searches]
    examples_hidden_ref = html.Span(
        id="search-examples-hidden-ref-cs",
        children=examples_as_string,
        className="is-hidden",
    )
    return examples_hidden_ref


def guided_search_boxes_html():
    """
    Get the html block for hidden guided search fields.

    Returns:
        (dash_html_components.Div): The html block for the hidden search fields.
    """
    hidden_container = html.Div(className="container")

    return hidden_container


def guided_search_box_elastic_html(class_):
    """
    Get the html block for a single filter boxes with ESAutosuggest.

    Args:
        field (str): The field type. Either a lowercase entity or "texto".
    """

    color = class_.color()
    common_entity_style = (
        f"msweb-is-{color}-txt is-size-5 has-text-weight-semibold"
    )

    code = class_.web_label()
    entity_txt = "{}:".format(code.capitalize())
    entity_name = html.Div(entity_txt, className=f"{common_entity_style}")

    tooltip_txt = class_.explanation()
    entity_label_tooltip = html.Div(
        tooltip_txt, className=f"tooltip-text is-size-7  has-margin-5"
    )

    # Autosuggest is styled by CSS react classnames ONLY!
    esas = ESAutosuggest(
        id="search-" + class_.api() + "-filters-input",
        fields=["original", "normalized"],
        endpoint=elastic_host + "/" + class_.explanation() + "/_search",
        defaultField="original",
        additionalField="normalized",
        placeholder=class_.examples(),
        authUser=elastic_user,
        authPass=elastic_pass,
        searchField="original.edgengram",
        sort=["_score"],
        suggestions=[],
        autoFocus=True,
        spellCheck=False,
    )
    esas = dcc.Input(id="search_" + class_.web_label() + "_filters_input")

    textbox = html.Div(
        [entity_name, esas, entity_label_tooltip],
        className="has-margin-right-10 has-margin-left-10 tooltip",
    )
    return textbox
