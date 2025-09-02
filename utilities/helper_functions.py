def adjust_trading_day():
    # Due to the market updates at 22:00, we have to
    # move the data after 22:00 into the training pot
    # and move the prediction day already one up.
    # e.g. 29.08 21:30 --> prediction day 29.08
    # e.g. 29.08 22:30 --> prediction day 30.08
    pass