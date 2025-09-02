<h1 align="center">KickAdvisor</h1>
<div align="justify"> <p> <strong>Kickbase Trading Advisor:</strong> A helper for the fantasy football game <a href="https://www.kickbase.com" target="_blank" rel="noopener">Kickbase</a>, built to predict next-day player market value movements. Each day, you’ll receive an email with predicted market value changes for all players currently on your league’s transfer market. This project uses the community <a href="https://kevinskyba.github.io/kickbase-api-doc/index.html" target="_blank" rel="noopener">Kickbase API</a> by <a href="https://github.com/kevinskyba" target="_blank" rel="noopener">kevinskyba</a>, big shoutout! 

</p> </div> <h2 align="center">What does the tool do?</h2> 
<ol> 
<li> <strong>Data Collection:</strong> Retrieves historical data from the API, including up to a year of player market values and performance stats (e.g., points scored, minutes played), plus more. </li>
<li> <strong>Feature Engineering:</strong> Adds derived metrics not directly available from the API, such as market value trend, volatility, market divergence, and others. </li>
<li> <strong>Model Training:</strong> Trains a machine learning model (Random Forest Regressor) to learn patterns between these features and next-day market value changes. </li>
<li> <strong>Daily Recommendations:</strong> Compares predicted changes with players currently listed on your league’s market and sends you the results via email every day. </li> 
</ol>

TODO:
- How to use the tool? (GitHub Actions, Secrets, Setup etc)
- Future Work and possible limitations
