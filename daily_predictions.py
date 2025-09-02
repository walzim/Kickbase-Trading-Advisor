from pipeline.predictions import live_data_predictions, join_current_market
from pipeline.preprocessing import preprocess_player_data, split_data
from pipeline.modeling import train_model, evaluate_model
from kickbase_api.user_management import login
from pipeline.data_handler import (
    create_player_data_table,
    check_if_data_reload_needed,
    save_player_data_to_db,
    load_player_data_from_db,
)
from IPython.display import display
from dotenv import load_dotenv
import os

competition_ids = [1]   # 1 = Bundesliga, 2 = 2. Bundesliga, 3 = La Liga
last_mv_values = 365    # in days, max 365
last_pfm_values = 50    # in matchdays, max idk

# TODO Add features like starting 11 probability, injuries, ...
features = [
    "p", "mv", "days_to_next", 
    "mv_change_1d", "mv_trend_1d", 
    "mv_change_3d", "mv_vol_3d",
    "mv_trend_7d", "market_divergence"
]

target = "mv_target_clipped" # or "mv_target"

# Load environment variables and login to kickbase
load_dotenv() 
USERNAME = os.getenv("KICK_USER")
PASSWORD = os.getenv("KICK_PASS")
token = login(USERNAME, PASSWORD)

# Data handling
create_player_data_table()
reload_data = check_if_data_reload_needed()
save_player_data_to_db(token, competition_ids, last_mv_values, last_pfm_values, reload_data)
player_df = load_player_data_from_db()
print("Data loaded from database.")

# Preprocess the data and spit the data
proc_player_df, today_df = preprocess_player_data(player_df)
X_train, X_test, y_train, y_test = split_data(proc_player_df, features, target)
print("Data preprocessed.")

# Train and evaluate the model
model = train_model(X_train, y_train)
signs_percent, rmse, mae, r2 = evaluate_model(model, X_test, y_test)
print(f"Model evaluation:\nSigns correct: {signs_percent:.2f}%\nRMSE: {rmse:.2f}\nMAE: {mae:.2f}\nR2: {r2:.2f}")

# Make live data predictions
live_predictions_df = live_data_predictions(today_df, model, features)

# Join with current available players on the market
bid_recommendations_df = join_current_market(token, live_predictions_df)
display(bid_recommendations_df)