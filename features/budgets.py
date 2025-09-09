from kickbase_api.user_management import get_budget, get_username
from kickbase_api.league_data import (
    get_activities,
    get_achievement_reward,
    get_managers,
    get_manager_performance,
    get_manager_info,
)
import pandas as pd

def calc_manager_budgets(token, league_id, league_start_date, start_budget):
    """
    Calculate manager budgets based on activities, bonuses, and team performance.
    """

    try:
        activities, login_bonus, achievement_bonus = get_activities(token, league_id, league_start_date)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch activities: {e}")

    activities_df = pd.DataFrame(activities)

    # Bonuses
    total_login_bonus = sum(entry.get("data", {}).get("bn", 0) for entry in login_bonus)

    total_achievement_bonus = 0
    for item in achievement_bonus:
        try:
            a_id = item.get("data", {}).get("t")
            if a_id is None:
                continue
            amount, reward = get_achievement_reward(token, league_id, a_id)
            total_achievement_bonus += amount * reward
        except Exception as e:
            # Skip broken achievement entry
            print(f"Warning: Failed to process achievement bonus {item}: {e}")

    # Manager performances
    try:
        managers = get_managers(token, league_id)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch managers: {e}")

    performances = []
    for manager in managers:
        try:
            manager_name, manager_id = manager
            info = get_manager_info(token, league_id, manager_id)
            team_value = info.get("tv", 0)

            perf = get_manager_performance(token, league_id, manager_id, manager_name)
            perf["Team Value"] = team_value
            performances.append(perf)
        except Exception as e:
            print(f"Warning: Skipping manager {manager}: {e}")

    perf_df = pd.DataFrame(performances)
    if not perf_df.empty:
        perf_df["point_bonus"] = perf_df["tp"].fillna(0) * 1000
        perf_df["Max Negative"] = (perf_df["Team Value"].fillna(0) * 0.33) * -1
    else:
        perf_df["name"] = []
        perf_df["point_bonus"] = []
        perf_df["Team Value"] = []
        perf_df["Max Negative"] = []

    # Initial budgets from activities
    budgets = {user: start_budget for user in set(activities_df["byr"].dropna().unique())
                                          .union(set(activities_df["slr"].dropna().unique()))}

    for _, row in activities_df.iterrows():
        byr, slr, trp = row.get("byr"), row.get("slr"), row.get("trp", 0)
        try:
            if pd.isna(byr) and pd.notna(slr):
                budgets[slr] += trp
            elif pd.isna(slr) and pd.notna(byr):
                budgets[byr] -= trp
            elif pd.notna(byr) and pd.notna(slr):
                budgets[byr] -= trp
                budgets[slr] += trp
        except KeyError as e:
            print(f"Warning: Skipping invalid activity row {row}: {e}")

    budget_df = pd.DataFrame(list(budgets.items()), columns=["User", "Budget"])

    # Merge performance bonuses
    budget_df = budget_df.merge(
        perf_df[["name", "point_bonus", "Team Value", "Max Negative"]],
        left_on="User",
        right_on="name",
        how="left"
    ).drop(columns=["name"], errors="ignore")

    budget_df["Budget"] = budget_df["Budget"] + budget_df["point_bonus"].fillna(0)
    budget_df.drop(columns=["point_bonus"], inplace=True, errors="ignore")
    budget_df.sort_values("Budget", ascending=False, inplace=True, ignore_index=True)

    # Add global bonuses (TODO better solution, as this estimation is not perfect)
    budget_df["Budget"] = budget_df["Budget"] + (total_login_bonus + total_achievement_bonus)

    # Sync with own actual budget
    try:
        own_budget = get_budget(token, league_id)
        own_username = get_username(token)
        mask = budget_df["User"] == own_username
        if not budget_df.loc[mask, "Budget"].eq(own_budget).all():
            budget_df.loc[mask, "Budget"] = own_budget
    except Exception as e:
        print(f"Warning: Could not sync own budget: {e}")

    # Calculate available budget
    budget_df["Available Budget"] = (budget_df["Max Negative"].fillna(0) - budget_df["Budget"]) * -1

    # Ensure consistent float format
    budget_df["Budget"] = budget_df["Budget"].astype(float)

    return budget_df