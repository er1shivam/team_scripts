"""All roles
    TODO : Add verbose module documentation
"""

import pandas as pd


class Person:
    # TODO : Add class documentation

    def __init__(self, name) -> None:
        self.name = name

    
    def __repr__(self):
        return "Person({})".format(self.name)




class Roles():
    # TODO : Add class documentation
    def __init__(self) -> None:
        pass

    # TODO : Implement getting all members
    def get_members(self):
        pass

    # TODO : Implement getting all roles
    def get_all_roles(self):
        return {}


class SnrSpecialists(Roles):
    
    all_snr_specialists = []

    # TODO : Initialize class
    def __init__(self) -> None:
        pass

    # TODO: Implement and add documentation
    def parse_csv(self):
        df = pd.read_csv("db_people.csv", header=0)
        return df
    

    # TODO : Add documentation
    @classmethod
    def register_member(cls, snr_specialist_person: Person):
        if isinstance(snr_specialist_person, Person):
            cls.all_snr_specialists.append(snr_specialist_person)
        else:
            print("Please add SNRSpecialist of type Person")


    # TODO : Add documentation
    def register_all_members(self):
        df = self.parse_csv()
        for row in df.itertuples():
            if row.Role == "Snr Specialists":
                person = Person(row.Person)
                self.register_member(person)


    def get_members(self):
        return self.all_snr_specialists


class JnrSpecialists(Roles):
    pass


# TODO : Make the classes for other roles.
# class SnrSpecialists(Roles):
#     pass


# class SnrSpecialists(Roles):
#     pass