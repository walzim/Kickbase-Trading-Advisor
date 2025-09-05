from kickbase_api.league_data import get_activities, get_achievement_reward
import pandas as pd

def calc_manager_budgets(token, league_id, start_budget):

    data, login_bonus, achievement_bonus = get_activities(token, league_id)
    
    activities_df = pd.DataFrame(data)

    # calculate total login bonus given out and achievements
    total_login_bonus = sum(entry["data"]["bn"] for entry in login_bonus)
    print(f"Total login bonus given out: {total_login_bonus}")

    # calculate total achievement bonus given out
    total_achievement_bonus = 0
    for item in achievement_bonus:
        a_id = item["data"]["t"]
        achievement_reward = get_achievement_reward(token, league_id, a_id)
        total_achievement_bonus += achievement_reward
    print(f"Total achievement bonus given out: {total_achievement_bonus}")

    # TODO money for points
    
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

    budget_df = pd.DataFrame(list(budgets.items()), columns=["User", "Budget"]).sort_values("Budget", ascending=False)

    # Add login and achievement bonuses to all managers the same
    budget_df["Budget"] += (total_login_bonus + total_achievement_bonus)

    return budget_df