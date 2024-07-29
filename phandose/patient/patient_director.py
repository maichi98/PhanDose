from .builders import PatientBuilder


class PatientDirector:

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> PatientBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: PatientBuilder):
        self._builder = builder

    def build(self):
        self._builder.build_dict_modalities()
        return self._builder.get_result()
