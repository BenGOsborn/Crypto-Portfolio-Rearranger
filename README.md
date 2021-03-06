# [Crypto Portfolio Rearranger](https://crypto-portfolio-rearranger.herokuapp.com)

## WHEN USING THIS SCRIPT, YOU TAKE THE CHANCE IT LOSING YOU MONEY. DO NOT USE CODE THAT YOU DO NOT UNDERSTAND. I AM NOT RESPONSIBLE FOR ANY MONEY YOU MAY LOSE.

## An API that automatically rearranges your Binance portfolio with minimal trades.

### Description
This script allows you to reallocate the weightings of each asset in your Binance portfolio with a few lines of work. Save yourself hours of time manually calculating the amount of each token you will have to buy and sell from your current portfolio to achieve the portfolio you desire.

### Requirements
- Python==3.8
- Pipenv==2021.5.29

### Instructions
**Local version**
1. Make a new ```.env``` file in ```src``` and inside of it specify your Binance ```API_KEY=``` and ```API_SECRET=```
2. Make a new ```portfolio.json``` file in ```src``` and inside of it specify your desired new portfolio assets and weightings e.g. 
```json
{
    "BNB": 0.4,
    "ETH": 0.4,
    "SOL": 0.2
}
```
3. Within the ```src``` directory, run the commands ```pipenv install``` and ```pipenv run python local.py```

**API version**

Send a ```POST``` request to the [API](https://crypto-portfolio-rearranger.herokuapp.com)'s ```/rearrange``` route with the following ```JSON``` body *(an example can be seen below)*

- ```api_key```: your Binance API key
- ```api_secret```: your Binance API secret key
- ```portfolio```: a key value ```JSON``` object containing key value pairs of the ticker of each asset you wish to add to your portfolio with its weighting percentage
```json
{
	"api_key": "abCdEf124...",
	"api_secret": "123Ef40cv...",
	"portfolio": {
		"SOL": 40,
		"BNB": 20,
		"LINK": 40
	}
}
```