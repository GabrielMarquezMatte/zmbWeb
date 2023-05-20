# -*- coding: utf-8 -*-

from dash import html

from app import display_app_html
from tests.util import VALID_PAGES, ZumbiWebBaseTest


"""
Tests for callbacks in the main app which are not tested elsewhere.
"""


class TestCoreAppCallbacks(ZumbiWebBaseTest):
    def test_display_app(self):
        f = display_app_html
        arg_combos = [(a,) for a in VALID_PAGES]
        valid_types = (str, dict, html.Div)
        for arg_combo in arg_combos:
            o = f(*arg_combo)
            self.assertTrue(isinstance(o, valid_types))
