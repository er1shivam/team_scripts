from datetime import datetime
import gspread
import pandas as pd


def sheets_setup():
    gc = gspread.oauth()
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
    )
    worksheet = sh.sheet1

    return worksheet


def create_dfs(worksheet):

    df = pd.DataFrame.from_dict(worksheet.get_all_records())
    df.set_index("Totals | Daily Average", inplace=True)
    df = df["Week Total"]

    pod_names = ["Girls SS", "No_name SS"]
    snr_specialist_names = ["Morgan SS", "Austin SS", "Caycee SS", "Isela SS", "Pat SS"]
    jnr_specialists_names = [
        "Kayla TC",
        "Kayla SS",
        "Julio TC",
        "Julio SS",
        "Sule TC",
        "Sule SS",
        "Noela TC",
        "Noela SS",
        "Molly TC",
        "Molly SS",
    ]
    setter_names = [
        "Donnah TC",
        "Liz TC",
        "Jelyn TC",
        "Jen TC",
        "Rachel TC",
        "Amanda TC",
    ]
    ops_names = ["Gussi Task", "Marl Task", "Roxan Task", "David Task"]

    return (
        pod_names,
        snr_specialist_names,
        jnr_specialists_names,
        setter_names,
        ops_names,
        df,
    )


def create_7d_total(worksheet):
    seven_day_total = {
        "Pods": [],
        "Snr Specialists": [],
        "Jnr Specialists": [],
        "Setters": [],
        "Ops": [],
    }

    (
        pod_names,
        snr_specialist_names,
        jnr_specialists_names,
        setter_names,
        ops_names,
        df,
    ) = create_dfs(worksheet)

    pod_df = df.loc[pod_names]
    snr_specialist_df = df.loc[snr_specialist_names]
    jnr_specialists_df = df.loc[jnr_specialists_names]
    setter_df = df.loc[setter_names]
    ops_df = df.loc[ops_names]

    seven_day_total["Pods"] = (
        pod_df.to_frame()
        .sort_values(by="Week Total", ascending=False)
        .to_dict()["Week Total"]
    )
    seven_day_total["Snr Specialists"] = (
        snr_specialist_df.to_frame()
        .sort_values(by="Week Total", ascending=False)
        .to_dict()["Week Total"]
    )
    seven_day_total["Jnr Specialists"] = (
        jnr_specialists_df.to_frame()
        .sort_values(by="Week Total", ascending=False)
        .to_dict()["Week Total"]
    )

    seven_day_total["Setters"] = (
        setter_df.to_frame()
        .sort_values(by="Week Total", ascending=False)
        .to_dict()["Week Total"]
    )
    seven_day_total["Ops"] = (
        ops_df.to_frame()
        .sort_values(by="Week Total", ascending=False)
        .to_dict()["Week Total"]
    )
    return seven_day_total, jnr_specialists_df


def fix_jnr_specialists(jnr_specialists_df, seven_day_total):

    mydf = jnr_specialists_df.to_frame()

    counts = {
        "Kayla Score": 0,
        "Julio Score": 0,
        "Sule Score": 0,
        "Noela Score": 0,
        "Molly Score": 0,
    }
    for index in mydf.index:
        ss_count = 0
        name = index.split()[0] + " Score"
        if "SS" in index:
            ss_count += mydf.loc[index]["Week Total"] * 5
            counts[name] = ss_count

    for index in mydf.index:
        name = index.split()[0] + " Score"
        if "TC" in index:
            counts[name] = mydf.loc[index]["Week Total"] + counts[name]

    seven_day_total["Jnr Specialists"] = counts

    return seven_day_total, counts


def leaderboard():
    worksheet = sheets_setup()
    seven_day_total_broken, jnr_specialists_df = create_7d_total(worksheet)
    seven_day_total, counts = fix_jnr_specialists(
        jnr_specialists_df, seven_day_total_broken
    )
    updated_df = pd.DataFrame.from_dict(seven_day_total)

    (
        pod_names,
        snr_specialist_names,
        jnr_specialists_names,
        setter_names,
        ops_names,
        df,
    ) = create_dfs(worksheet)
    pod_lead = updated_df[updated_df.index.isin(pod_names)]["Pods"]
    snr_spec = updated_df[updated_df.index.isin(snr_specialist_names)][
        "Snr Specialists"
    ]
    jnr_spec = updated_df[updated_df.index.isin(counts.keys())]["Jnr Specialists"]
    setter = updated_df[updated_df.index.isin(setter_names)]["Setters"]
    op = updated_df[updated_df.index.isin(ops_names)]["Ops"]

    return pd.concat([pod_lead, snr_spec, jnr_spec, setter, op])


if __name__ == "__main__":
    print(leaderboard())
