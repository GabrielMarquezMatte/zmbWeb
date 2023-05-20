# -*- coding: UTF-8 -*-

import pandas as pd

CODES_FILE = 'language/codes_ptBR.tsv'

def get_code_values(label, column) -> str:
    df = pd.read_csv(CODES_FILE, sep='\t')
    return df[df.code_id == label][column].values[0]

class BaseLabel:
    @staticmethod
    def api() -> str:
        raise NotImplementedError
    
    @staticmethod
    def web_label() -> str:
        raise NotImplementedError
    
    @staticmethod
    def examples() -> str:
        raise NotImplementedError
    
    @staticmethod
    def explanation() -> str:
        raise NotImplementedError
    
    @staticmethod
    def color() -> str:
        raise NotImplementedError

class ZmbLabels:

    class Source(BaseLabel):
        @staticmethod
        def api():
            return "sources"

        @staticmethod
        def web_label():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "purple"

    class People(BaseLabel):
        @staticmethod
        def api():
            return "people"

        @staticmethod
        def web_label():
            line = ZmbLabels.People.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.People.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.People.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "dark-red"

    class Educational(BaseLabel):
        @staticmethod
        def api():
            return "educational"

        @staticmethod
        def web_label():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "orange"


    class Private(BaseLabel):
        @staticmethod
        def api():
            return "private"

        @staticmethod
        def web_label():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "turq"


    class Public(BaseLabel):
        @staticmethod
        def api():
            return "public"

        @staticmethod
        def web_label():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "pink"

    class City(BaseLabel):
        @staticmethod
        def api():
            return "cities"

        @staticmethod
        def web_label():
            line = ZmbLabels.City.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.City.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.City.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "red"

    class State(BaseLabel):
        @staticmethod
        def api():
            return "states"

        @staticmethod
        def web_label():
            line = ZmbLabels.State.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.State.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.State.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "dark-blue"

    class Country(BaseLabel):
        @staticmethod
        def api():
            return "countries"

        @staticmethod
        def web_label():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "green"

    class Police(BaseLabel):
        @staticmethod
        def api():
            return "polices"

        @staticmethod
        def web_label():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "brown"

    class Work(BaseLabel):
        @staticmethod
        def api():
            return "works"

        @staticmethod
        def web_label():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "grey"

    class Movement(BaseLabel):
        @staticmethod
        def api():
            return "movements"

        @staticmethod
        def web_label():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "dark-green"

    class Political(BaseLabel):
        @staticmethod
        def api():
            return "political"

        @staticmethod
        def web_label():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "black"

    class Law(BaseLabel):
        @staticmethod
        def api():
            return "laws"

        @staticmethod
        def web_label():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "blue"

    class Media(BaseLabel):
        @staticmethod
        def api():
            return "media"

        @staticmethod
        def web_label():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "web_label")

        @staticmethod
        def examples():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "examples")

        @staticmethod
        def explanation():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "explanation")

        @staticmethod
        def color():
            return "light-blue"
        
    @staticmethod
    def all_classes() -> list[BaseLabel]:
        """
        Returns the classes of all labels
        """
        return [ \
            ZmbLabels.City,
            ZmbLabels.Country,
            ZmbLabels.State,
            ZmbLabels.Private,
            ZmbLabels.Educational,
            ZmbLabels.Public,
            ZmbLabels.Police,
            ZmbLabels.Law,
            ZmbLabels.People,
            ZmbLabels.Movement,
            ZmbLabels.Political,
            ZmbLabels.Work,
            ZmbLabels.Source,
        ]
    
    @staticmethod
    def web_lbl_2_api(wlbl:str):
        for class_ in ZmbLabels.all_classes():
            if (wlbl == class_.web_label()):
                return class_.api()
        raise ValueError(f"Invalid web label: {wlbl}")
    
    @staticmethod
    def valid_search_filters():
        return [class_.web_label() for class_ in ZmbLabels.all_classes()]
