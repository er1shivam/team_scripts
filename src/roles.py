"""This module takes in the csv of team member information and creates objects 
for each person to use for other functions
"""

import pandas as pd


class Person:
    """Creates the person object with the attributes needed"""

    def __init__(self, name, role) -> None:
        self.name = name
        self.role = role

    def __repr__(self) -> str:
        """Gives a summary of the attributes of the Person object

        Returns:
            str: Returns attributes of the person object
        """
        return f"Person (Name: {self.name} - Role: {self.role})"

    def __hash__(self):
        """This allows multiple classes to be added to the set all_team in a
        future function call

        Returns:
            hash: Hash of name and role of this instance
        """
        return hash((self.name, self.role))

    def __eq__(self, other):
        """Not fully sure why this works, but I will figure it out"""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.role == other.role


class Roles:
    """Registers and assigns Person object based on their role to the correct
    ist in role_dictionary"""

    all_team_members_in_company = set()

    def __init__(self) -> None:
        pass

    def getAllMembers(self):
        return self.all_members

    def listAllTeamMembersInCompany(self):
        return self.all_team_members_in_company

    def parse_csv_of_roles(self):
        """Uses csv as a database to pull through data for each team member

        Returns:
            dataframe: Returns two columns, name and role
        """
        df = pd.read_csv(
            "/Users/louisrae/Documents/dev/dfy_setters/src/db_people.csv"
        )
        return df

    def registerMember(self, team_member: Person):
        """Takes the Person object and assigns the attributes to the
        role dictionary and object to a list of all team_members

        Args:
            team_member (Person): Takes in Person object, defined above
        """
        self.all_team_members_in_company.add(team_member)

    def register_all_members(self):
        """Registers every member into dictionary and full list who
        is in database
        """
        for name, role in self.parse_csv_of_roles().values:
            person = Person(name, role)
            if role == "Pod Lead":
                PodLead().registerMember(person)
            elif role == "Snr Specialist":
                SnrSpecialist().registerMember(person)
            elif role == "Jnr Specialist":
                JnrSpecialist().registerMember(person)
            elif role == "Setter":
                Setter().registerMember(person)
            self.all_team_members_in_company.add(person)


class SnrSpecialist(Roles):

    all_members = set()

    def __init__(self) -> None:
        super().__init__()


class JnrSpecialist(Roles):

    all_members = set()

    def __init__(self) -> None:
        super().__init__()


class PodLead(Roles):

    all_members = set()

    def __init__(self) -> None:
        super().__init__()


class Setter(Roles):

    all_members = set()

    def __init__(self) -> None:
        super().__init__()
