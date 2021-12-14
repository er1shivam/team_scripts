from dfy_tracking.dfysetters import Leaderboard
import gspread

gc = gspread.oauth()
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
)
worksheet = sh.sheet1

test1 = Leaderboard(gc, sh, worksheet)
print(test1.create_dfs())
dic, counts = test1.create_7d_total()

print(test1.leaderboard())
