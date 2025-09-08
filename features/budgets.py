from kickbase_api.league_data import get_activities, get_achievement_reward, get_managers, get_manager_performance
import pandas as pd

def calc_manager_budgets(token, league_id, league_start_date, start_budget):

    activities, login_bonus, achievement_bonus = get_activities(token, league_id, league_start_date)
    
    activities_df = pd.DataFrame(activities)

    # calculate total login bonus given out and achievements
    total_login_bonus = sum(entry["data"]["bn"] for entry in login_bonus)

    # calculate total achievement bonus given out
    total_achievement_bonus = 0
    for item in achievement_bonus:
        a_id = item["data"]["t"]
        achievement_reward = get_achievement_reward(token, league_id, a_id)
        total_achievement_bonus += achievement_reward

    # get all managers and their total points
    managers = get_managers(token, league_id)
    all_perfs = []
    for manager in managers:
        perf = get_manager_performance(token, league_id, manager[1], manager[0])
        all_perfs.append(perf)

    perf_df = pd.DataFrame(all_perfs)
    perf_df["point_bonus"] = perf_df["tp"] * 1000

    # get budgets through activities
    budgets = {}

    # get all managers
    users = set(activities_df["byr"].dropna().unique()).union(set(activities_df["slr"].dropna().unique()))
    for user in users:
        budgets[user] = start_budget

    # go through all activities and calculate budgets
    for _, row in activities_df.iterrows():
        byr, slr, trp = row["byr"], row["slr"], row["trp"]

        if pd.isna(byr) and pd.notna(slr):
            # Sell to the market
            budgets[slr] += trp
        elif pd.isna(slr) and pd.notna(byr):
            # Buy from the market
            budgets[byr] -= trp
        elif pd.notna(byr) and pd.notna(slr):
            # between two managers
            budgets[byr] -= trp
            budgets[slr] += trp

    budget_df = pd.DataFrame(list(budgets.items()), columns=["User", "Budget"])

    # add point bonus to budgets
    budget_df = budget_df.merge(perf_df[["name", "point_bonus"]], left_on="User", right_on="name", how="left").drop(columns=["name"])
    budget_df["Budget"] += budget_df["point_bonus"].fillna(0)
    budget_df = budget_df.drop(columns=["point_bonus"])
    budget_df = budget_df.sort_values("Budget", ascending=False).reset_index(drop=True)

    # Add login and achievement bonuses to all managers the same
    budget_df["Budget"] += (total_login_bonus + total_achievement_bonus)

    # convert to float for formatting
    budget_df["Budget"] = budget_df["Budget"].astype(float)

    return budget_df