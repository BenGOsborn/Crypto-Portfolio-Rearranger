# Rearranges the users portfolio to the new assets based off of their old portfolio

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from binance import Client
import os
import json

# Steps
# 1. Get the previous percentages and compare them with the new ones
# 2. Seperate the ones that are decreasing in allocation vs the ones that are gaining in allocation
# 3. Remove the specified amount from the ones that are decreasing and then use this to fill up the ones that are increasing bit by bit


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    client = Client(api_key, api_secret)

    # Get the owned balances
    balances = client.get_account()["balances"]
    owned = {}
    assets = {}
    for balance in balances:
        asset = balance["asset"]
        ticker = asset + "BUSD" if asset != "BUSD" else asset + "USDT"
        asset_amount = float(balance["free"])

        # Calculate the USD invested in each token
        if float(asset_amount) > 0:
            price = float(client.get_avg_price(symbol=ticker)["price"])
            owned[asset] = price * asset_amount
            assets[asset] = asset_amount

    # Get the weighting of each asset in the portfolio
    total_invested = sum(x for x in owned.values())
    weights = {key: value / total_invested for key, value in owned.items()}

    # Load in the specified portfolio
    new_weights = json.load(open("portfolio.json"))

    # Now we want to go through and find the assets that we will be removing / adding and what we need to swap them out for
    rel_changes = {}

    for key, value in weights.items():
        rel_changes[key] = -value

    for key, value in new_weights.items():
        if key in rel_changes:
            rel_changes[key] += value
        else:
            rel_changes[key] = value

    changes = {key: value * total_invested for key,
               value in rel_changes.items()}
    changes = {key: changes[key]
               for key in sorted(changes, key=lambda x: changes[x])}

    # **** Now we will look at all of the negative ones and use them to fund pairs against the positve pairs until they run out (through some sort of stack mechanism ?)


# Run the program if the file is run directly
if __name__ == "__main__":
    main()
