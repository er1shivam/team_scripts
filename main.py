import dfysetters.facebook_tracking as dfy
from constants import *
import pandas as pd


class RoleDict:
    def __init__(self, department, name) -> None:
        self.department = department
        self.name = name

    def getDictInfo(self):
        return dict(self)


jack = RoleDict("Pod Leads", "No_name")
tylee = RoleDict("Pod Leads", "Girls")
morgan = RoleDict("Snr Specialists", "Morgan")
isela = RoleDict("Snr Specialists", "Isela")
caycee = RoleDict("Snr Specialists", "Caycee")
pat = RoleDict("Snr Specialists", "Pat")
sean = RoleDict("Snr Specialists", "Sean")
kayla = RoleDict("Snr Specialists", "Kayla")
noela = RoleDict("Jnr Specialists", "Noela")
molly_c = RoleDict("Jnr Specialists", "Molly C")
zach = RoleDict("Jnr Specialists", "Zach")
julio = RoleDict("Jnr Specialists", "Julio")
ra_saan = RoleDict("Jnr Specialists", "Ra'Saan")
daniel = RoleDict("Jnr Specialists", "Daniel")
sonja = RoleDict("Jnr Specialists", "Sonja")
molly_n = RoleDict("Jnr Specialists", "Molly N")
suleyma = RoleDict("Setter", "Suleyma")
alex = RoleDict("Setter", "Alex")
amanda = RoleDict("Setter", "Amanda")
donnah = RoleDict("Setter", "Donnah")
liz = RoleDict("Setter", "Liz")
jelyn = RoleDict("Setter", "Jelyn")
monica = RoleDict("Setter", "Monica")
rachel = RoleDict("Setter", "Rachel")

print(jack.department)
