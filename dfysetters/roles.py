class Person:
    def __init__(self, name) -> None:
        self.name = name


class Roles:
    def __init__(self) -> None:
        pass

    def get_all_roles(self):
        return {}


class SnrSpecialists(Roles):
    all_snr_specialists = []

    def __init__(self) -> None:
        pass
