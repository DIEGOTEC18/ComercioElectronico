import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta

# get stock info
# stock_info = msft.info
# print(stock_info)
# print(stock_info.get('currentPrice'))
# 'market'

# get historical market data
# hist = msft.history(period="max")

# show actions (dividends, splits)
# msft.actions

df_columns = ['stock', 'quantity', 'bought']
df = pd.read_csv('wallet.csv', index_col=False)
df_notes = pd.read_csv('wallet_notes.csv', index_col=False)
df_mmkt = pd.read_csv('wallet_mmkt.csv', index_col=False)
df_sold = pd.read_csv('sold.csv', index_col=False)

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn' Disable for debugging


def get_balance():
    funds = open('funds.txt', 'r')
    balance = float(funds.read())
    funds.close()
    return balance


def update_balance(new_balance):
    funds = open('funds.txt', 'w')
    funds.write(str(new_balance))
    funds.close()


def display_wallet():
    funds = open('funds.txt', 'r')
    balance = float(funds.read())
    funds.close()

    print()
    print("---")
    print(df)
    print()
    print("Your balance is: " + str(balance) + " USD")
    print()
    print("---")
    print()


def display_notes_wallet():
    print()
    print("---")
    print(df_notes)
    print("---")
    print()


def display_mmkt_wallet():
    print()
    print("---")
    print(df_mmkt)
    print("---")
    print()


def save_wallet():
    df.to_csv('wallet.csv', index=False)
    print("Wallet successfully saved!")


def save_notes_wallet():
    df_notes.to_csv('wallet_notes.csv', index=False)
    print("Notes wallet successfully saved!")


def save_mmkt_wallet():
    df_mmkt.to_csv('wallet_mmkt.csv', index=False)
    print("Money Market wallet successfully saved!")


run = True

print("Loading...")

while run:

    # Read and display wallet.

    print("Please select an option:")
    print("Buy - Sell - Wallet - Derivatives - MoneyMarket - PandL - Exit")
    x = input()

    if x == "Buy":
        print("Buy selected")
        print("Please introduce the shortname of the company you wish to buy stocks from:")
        user_input = input()

        print("Fetching stock info for " + user_input + "...")
        print()

        current_ticker = yf.Ticker(user_input)
        stock_info = current_ticker.info

        if stock_info.get('regularMarketPrice') is not None:

            current_price = stock_info.get('currentPrice')
            long_name = stock_info.get('longName')

            print("The current price for " + long_name + " is " + str(current_price) + " USD")
            print()
            print(stock_info)
            print()
            print("Do you wish to buy " + long_name + " stock at " + str(current_price) + " USD?")
            print("YES - NO")
            user_input2 = input()

            if user_input2 == "YES":
                print("How many shares do you wish to buy? ")
                shares_quantity = input()

                cost = int(shares_quantity) * current_price
                current_balance = get_balance()

                if cost <= current_balance:

                    today = date.today()
                    now = datetime.now()
                    current_date = today.strftime("%d/%m/%Y")
                    current_time = now.strftime("%H:%M:%S")

                    exists = False
                    index = -1

                    # update if exists:
                    for x in range(0, len(df)):
                        if str(df['stock'][x]) == str(user_input):
                            exists = True
                            index = x

                            break

                    if exists:

                        df['quantity'][index] = df['quantity'][index] + int(shares_quantity)
                        df['bought_price'][index] = ((df['bought_price'][index] + current_price) / 2)
                        df['date'][index] = current_date
                        df['hour'][index] = current_time
                        df['total_cost'][index] = df['total_cost'][index] + cost
                        df['profit-loss'][index] = df['profit-loss'][index] - cost
                        df['stocks_remaining'][index] = df['stocks_remaining'][index] + int(shares_quantity)

                    else:
                        new_row = {'stock': user_input, 'quantity': shares_quantity, 'bought_price': current_price,
                                'date': current_date, 'hour': current_time, 'total_cost': cost, 'quantity_sold': 0, 'sold_price': 0, 'total_sell': 0, 'profit-loss': (-1 * cost), 'date_sold': None, 'hour_sold': None, 'stocks_remaining': shares_quantity}
                        df = df.append(new_row, ignore_index=True)

                    print()
                    print(str(shares_quantity) + " shares of " + long_name + " stock bought successfully for " + str(cost))
                    print()
                    save_wallet()
                    update_balance(current_balance - cost)

                else:
                    print("Insufficient funds")

            elif user_input2 == "NO":
                print("Okey")
                print()

            else:
                print(user_input + " is not a valid option.")

        else:
            print()
            print("Error: " + user_input + " stock couldn't be found. Please verify the shortname.")
            print()

    elif x == "Sell":
        print("Sell selected")

        display_wallet()

        print("Please select the index of the stock you want to sell:")
        user_input = int(input())
        index = user_input

        row_data = df.iloc[index]

        print(row_data)

        stock_name = row_data.get('stock')
        quantity = row_data.get('quantity')
        bought_price = row_data.get('bought_price')
        bought_date = row_data.get('date')
        bought_hour = row_data.get('hour')

        print()
        print("You have " + str(quantity) + " shares of " + stock_name + " stock.")
        print("How many shares do you wish to sell?")
        user_input = input()
        sell_quantity = user_input

        while int(user_input) > quantity or int(user_input) <= 0:  # TODO Check for types here
            print()
            print(user_input + " is not a valid input.")
            print("How many shares do you wish to sell?")
            user_input = input()
            sell_quantity = user_input

        print()
        print("Fetching stock info for " + stock_name + "...")
        print()

        current_ticker = yf.Ticker(stock_name)
        stock_info = current_ticker.info

        current_price = stock_info.get('currentPrice')
        long_name = stock_info.get('longName')

        print("The current price for " + long_name + " is " + str(current_price) + " USD")
        print()
        print(stock_info)
        print()
        print("Are you sure you wish to sell " + user_input + " stock of " + long_name + " for " + str(current_price) + " USD?")
        print("YES - NO")
        user_input = input()

        if user_input == "YES":
            today = date.today()
            now = datetime.now()
            current_date = today.strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            current_balance = get_balance()
            cash = int(current_price) * int(sell_quantity)

            df['quantity_sold'][index] = int(sell_quantity)
            df['sold_price'][index] = current_price
            df['total_sell'][index] = cash
            df['profit-loss'][index] = (cash - df['total_cost'][index])
            df['date_sold'][index] = current_date
            df['hour_sold'][index] = current_time
            df['stocks_remaining'][index] = df['stocks_remaining'][index] - int(sell_quantity)

            save_wallet()

            update_balance(current_balance + cash)

            print()
            print("Stock successfully sold!")

    elif x == "Wallet":
        # TODO: Netting
        print("Wallet selected")

        print("Performing Netting:")


        display_wallet()

    elif x == "Derivatives":
        print("Derivatives selected")

        derivatives_section = True

        while derivatives_section:

            print("Please select an option:")
            print("Note - Wallet - Return")
            selection = input()

            if selection == "Note":

                print("\nPlease enter the initial (max) investment:")
                max_investment = int(input())

                print("\nPlease enter the minimum issue amount:")
                min_issue_amount = int(input())

                print("\nPlease enter the investment amount in USD:")
                investment_amount = int(input())

                while investment_amount > get_balance():
                    print("\nInsufficient funds. Please enter an amount lower than " + str(get_balance()) + ":")
                    investment_amount = int(input())

                print("\nPlease enter the issue currency shortcode (Ex. USD, MXN):")
                issue_currency = input()

                print("\nPlease enter the percentage of protected capital in decimal (Ex. 0.60 = 60%):")
                protected_capital = float(input())

                print("\nPlease enter the underlying asset type for the note (CURRENCY or STOCKS):")
                asset_type = input()

                while True:
                    if asset_type is not "CURRENCY" or asset_type is not "STOCKS":
                        break

                    print("\nOnly CURRENCY or STOCKS are accepted as underlying assets for the moment.")
                    print("Please enter the underlying asset type for the note (CURRENCY or STOCKS):")
                    asset_type = input()

                issue_ex_rate = 0
                underlying_asset = ""

                today = date.today()
                current_date = today.strftime("%Y-%m-%d")

                if asset_type == "CURRENCY":
                    print("\nPlease enter the currency shortcode (Ex. USD, MXN):")
                    underlying_asset = input()

                    ex_shortcode = ""
                    # Create exchange shortcode:
                    if issue_currency == "MXN" and underlying_asset == "USD":
                        ex_shortcode = "MXN=X"

                    else:
                        ex_shortcode = underlying_asset + issue_currency + "=X"

                    # Get currency data:
                    currency_data = yf.download(ex_shortcode, start=current_date, end=current_date)
                    issue_ex_rate = round(currency_data.get('Close')[0], 2)

                    print("\n" + ex_shortcode + " is " + str(issue_ex_rate) + " " + issue_currency + ".")

                else:
                    print("\nPlease enter the stock shortcode (Ex. MSFT, UBER):")
                    underlying_asset = input()

                    print("Fetching stock info for " + underlying_asset + "...")
                    print()

                    current_ticker = yf.Ticker(underlying_asset)
                    stock_info = current_ticker.info

                    if stock_info.get('regularMarketPrice') is not None:
                        current_price = stock_info.get('currentPrice')
                        long_name = stock_info.get('longName')

                    else:
                        print()
                        print("Error: " + underlying_asset + " stock couldn't be found. Please verify the shortname.")
                        print()

                        print("\nPlease enter the stock shortcode (Ex. MSFT, UBER):")
                        underlying_asset = input()

                        print("Fetching stock info for " + underlying_asset + "...")
                        print()

                        current_ticker = yf.Ticker(underlying_asset)
                        stock_info = current_ticker.info

                        while stock_info.get('regularMarketPrice') is None:
                            print()
                            print("Error: " + underlying_asset + " stock couldn't be found. Please verify the shortname.")
                            print()

                            print("\nPlease enter the stock shortcode (Ex. MSFT, UBER):")
                            underlying_asset = input()

                            print("Fetching stock info for " + underlying_asset + "...")
                            print()

                            current_ticker = yf.Ticker(underlying_asset)
                            stock_info = current_ticker.info

                    current_price = stock_info.get('currentPrice')
                    long_name = stock_info.get('longName')

                    print("The current price for " + long_name + " is " + str(current_price) + " USD")
                    print()
                    issue_ex_rate = current_price

                print("\nPlease enter the Note term in days (plazo):")
                term_days = int(input())

                period_of_observation = ""

                if 8 <= term_days < 30:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY - WEEKLY")
                    period_of_observation = input()

                elif 30 <= term_days < 90:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY - WEEKLY - MONTHLY")
                    period_of_observation = input()

                elif 90 <= term_days < 180:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY - WEEKLY - MONTHLY - QUARTERLY")
                    period_of_observation = input()

                elif 180 <= term_days < 360:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY - WEEKLY - MONTHLY - QUARTERLY - BIANNUAL")
                    period_of_observation = input()

                elif term_days >= 360:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY - WEEKLY - MONTHLY - QUARTERLY - BIANNUAL - YEARLY")
                    period_of_observation = input()

                else:
                    print("\nPlease enter one of the following periods of observation:")
                    print("DAILY")
                    period_of_observation = input()

                print("\nPlease enter the basis points to calculate the range:")
                bsp = int(input())
                min_range = issue_ex_rate - (bsp / 100)
                max_range = issue_ex_rate + (bsp / 100)

                if asset_type == "CURRENCY":
                    print("\nMin-range: " + str(min_range) + " " + issue_currency)
                    print("Max-range: " + str(max_range) + " " + issue_currency)

                else:
                    print("\nMin-range: " + str(min_range) + " USD")
                    print("Max-range: " + str(max_range) + " USD")

                print("\nPlease enter the max overall rate in decimal percentage (Ex. 0.60 = 60%):")
                max_overall_rate = float(input())

                print("\nPlease enter the max observation date rate in decimal percentage (Ex. 0.60 = 60%):")
                max_observation_date_rate = float(input())

                date_of_issue = today.strftime("%d/%m/%Y")
                exercise_or_expiry_date_d = today + timedelta(days=term_days)
                exercise_or_expiry_date = exercise_or_expiry_date_d.strftime("%d/%m/%Y")

                print("\nDate of issue: " + date_of_issue)
                print("Date of exercise or expiry: " + exercise_or_expiry_date)

                # Save to memory:
                new_row = {'max_investment': max_investment, 'min_issue_amount': min_issue_amount, 'investment_amount': investment_amount, 'issue_currency': issue_currency,
                          'protected_capital': protected_capital, 'asset_type': asset_type, 'underlying_asset': underlying_asset, 'issue_ex_rate': issue_ex_rate, 'term_days': term_days, 'period_of_observation': period_of_observation, 'min_range': min_range, 'max_range': max_range, 'max_overall_rate': max_overall_rate, 'max_observation_date_rate': max_observation_date_rate, 'date_of_issue': date_of_issue, 'exercise_or_expiry_date': exercise_or_expiry_date, 'status': "ACTIVE", "cumulative_rate": 0.0, "return": 0.0, "final_amount": 0.0}

                df_notes = df_notes.append(new_row, ignore_index=True)
                save_notes_wallet()

                update_balance(get_balance() - investment_amount)

                print("\nNote issued successfully!\nCheck your Derivatives Wallet for more info.\n\n")

            elif selection == "Wallet":
                # Check for expired notes:
                for x in range(0, len(df_notes)):

                    if df_notes['status'][x] == "ACTIVE":
                        exercise_or_expiry_date = datetime.strptime(df_notes['exercise_or_expiry_date'][x], "%d/%m/%Y").date()
                        today = date.today()

                        if exercise_or_expiry_date <= today:
                            print("\nThe note with underlying asset " + df_notes['underlying_asset'][x] + " issued in " + df_notes['date_of_issue'][x] + " expired in " + df_notes['exercise_or_expiry_date'][x])

                            # Calculate exercise:
                            observation_days = 0

                            if df_notes['period_of_observation'][x] == 'DAILY':
                                observation_days = 1

                            elif df_notes['period_of_observation'][x] == 'WEEKLY':
                                observation_days = 8

                            elif df_notes['period_of_observation'][x] == 'MONTHLY':
                                observation_days = 30

                            elif df_notes['period_of_observation'][x] == 'QUARTERLY':
                                observation_days = 90

                            elif df_notes['period_of_observation'][x] == 'BIANNUAL':
                                observation_days = 180

                            elif df_notes['period_of_observation'][x] == 'YEARLY':
                                observation_days = 360

                            else:
                                print("Period of observation is unknown")

                            current_date_observation = datetime.strptime(df_notes['date_of_issue'][x], "%d/%m/%Y").date()

                            cumulative_rate = 0.0

                            while current_date_observation < exercise_or_expiry_date:

                                current_date_observation_string = current_date_observation.strftime("%Y-%m-%d")
                                # print(current_date_observation_string)
                                # print(type(current_date_observation_string))

                                if df_notes['asset_type'][x] == "CURRENCY":

                                    ex_shortcode = ""
                                    # Create exchange shortcode:
                                    if str(df_notes['issue_currency'][x]) == "MXN" and str(df_notes['underlying_asset'][x]) == "USD":
                                        ex_shortcode = "MXN=X"

                                    else:
                                        ex_shortcode = df_notes['underlying_asset'][x] + df_notes['issue_currency'][x] + "=X"

                                    print(ex_shortcode)
                                    # Get currency data:
                                    currency_data = yf.download(ex_shortcode, start=current_date_observation_string, end=current_date_observation_string)
                                    current_price = 0.0

                                    if currency_data.empty:
                                        current_price = 0.0

                                    else:
                                        current_price = round(currency_data.get('Close')[0], 2)

                                    min_range = float(df_notes['min_range'][x])
                                    max_range = float(df_notes['max_range'][x])

                                    max_overall_rate = float(df_notes['max_overall_rate'][x])
                                    max_observation_date_rate = float(df_notes['max_observation_date_rate'][x])

                                    date_string = current_date_observation.strftime("%d/%m/%Y")

                                    print("--------------")

                                    if min_range <= current_price <= max_range and cumulative_rate < max_overall_rate:
                                        print(date_string + " | price: " + str(current_price) + " | enters" + " | rate: " + str(max_observation_date_rate))
                                        cumulative_rate = cumulative_rate + max_observation_date_rate
                                        print(str(cumulative_rate) + " of " + str(max_overall_rate))

                                    else:
                                        print(date_string + " |price: " + str(current_price) + " | no entry" + " | rate: 0.0")

                                else:
                                    stock_shortcode = df_notes['underlying_asset'][x]
                                    # print(current_date_observation_string)
                                    next_day = current_date_observation + timedelta(days=1)
                                    next_day_string = next_day.strftime("%Y-%m-%d")
                                    stock_data = yf.download(stock_shortcode, current_date_observation_string, next_day_string)
                                    current_price = 0.0

                                    # other_data = yf.download('AAPL', '2016-01-01', '2019-08-01')
                                    # print(other_data)

                                    if stock_data.empty:
                                        current_price = 0.0

                                    else:
                                        current_price = round(stock_data.get('Close')[0], 2)

                                    min_range = float(df_notes['min_range'][x])
                                    max_range = float(df_notes['max_range'][x])

                                    max_overall_rate = float(df_notes['max_overall_rate'][x])
                                    max_observation_date_rate = float(df_notes['max_observation_date_rate'][x])

                                    date_string = current_date_observation.strftime("%d/%m/%Y")

                                    print("--------------")

                                    if min_range <= current_price <= max_range and cumulative_rate < max_overall_rate:
                                        print(date_string + " | price: " + str(current_price) + " | enters" + " | rate: " + str(max_observation_date_rate))
                                        cumulative_rate = cumulative_rate + max_observation_date_rate
                                        print(str(cumulative_rate) + " of " + str(max_overall_rate))

                                    else:
                                        print(date_string + " |price: " + str(current_price) + " | no entry" + " | rate: 0.0")

                                current_date_observation = current_date_observation + timedelta(days=observation_days)

                            return_of_investment = float(df_notes['investment_amount'][x]) + (int(df_notes['investment_amount'][x]) * cumulative_rate)

                            print("\nInitial investment: " + str(df_notes['investment_amount'][x]))
                            print("\nOverall Rate: " + str(cumulative_rate))
                            print("Return: " + str((float(df_notes['investment_amount'][x]) * cumulative_rate)))
                            print("Final Amount: " + str(return_of_investment))
                            print("\nDo you wish to execute the note? (YES, NO)")
                            user_response = input()

                            if user_response == "YES" or user_response == "yes" or user_response == "Yes":
                                df_notes['cumulative_rate'][x] = cumulative_rate
                                df_notes['return'][x] = (float(df_notes['investment_amount'][x]) * cumulative_rate)
                                df_notes['final_amount'][x] = return_of_investment
                                df_notes['status'][x] = "EXECUTED"

                                save_notes_wallet()
                                update_balance(get_balance() + return_of_investment)
                                print("Balance: " + str(get_balance()))

                                print("\nNote executed.")

                            elif user_response == "NO" or user_response == "no" or user_response == "No":
                                df_notes['final_amount'][x] = df_notes['investment_amount'][x] * df_notes['protected_capital'][x]
                                df_notes['status'][x] = "EXPIRED"

                                save_notes_wallet()
                                update_balance(get_balance() + (df_notes['investment_amount'][x] * df_notes['protected_capital'][x]))
                                print("Balance: " + str(get_balance()))

                                print("\nNote expired.")

                            else:
                                print("\n" + user_response + " is not a valid answer. Ignored.")

                print("\nNotes Wallet:")
                display_notes_wallet()

            elif selection == "Return":
                derivatives_section = False

            else:
                print("Please select a valid option:")

    elif x == "MoneyMarket":
        print("Money Market selected")

        while True:

            print("\nPlease select one of the following options:")
            print("Bonds - Wallet - Return")
            user_selection = input()

            if user_selection == "Bonds":
                print("\nBonds selected:")
                print("\nPlease select one of the following bonds:")
                print("CETE - VARIABLE")
                bond_type = input()

                today = date.today()
                today_str = today.strftime("%Y-%m-%d")

                currency_data = yf.download("MXN=X", start=today_str, end=today_str)
                issue_ex_rate = round(currency_data.get('Close')[0], 2)

                if bond_type == "CETE":

                    date_of_issue = today.strftime("%d/%m/%Y")
                    due_date = None
                    rate = None

                    print("\nThe minimum investment is 1000 MXN (100 CETES)")
                    print("Please enter the initial investment in MXN:")
                    initial_investment_mxn = int(input())

                    while initial_investment_mxn < 1000:
                        print("\nThe minimum investment is 1000 MXN (100 CETES)")
                        print("Please enter the initial investment in MXN:")
                        initial_investment_mxn = int(input())

                    initial_investment_usd = (initial_investment_mxn / issue_ex_rate)

                    while initial_investment_usd > get_balance():
                        print("\nInsufficient funds: " + str(get_balance()) + "USD")
                        print("\nThe minimum investment is 1000 MXN (100 CETES)")
                        print("Please enter the initial investment in MXN:")
                        initial_investment_mxn = int(input())
                        initial_investment_usd = (initial_investment_mxn / issue_ex_rate)

                    print("\nPlease select one of the following periods of time: ")
                    print("28d - 91d - 182d - 364d")
                    period = input()
                    period_days = 0

                    while True:
                        if period == "28d" or period == "91d" or period == "182d" or period == "364d":
                            break

                        else:
                            print("\n" + str(period) + " is not a valid period.")
                            print("Please select one of the following periods of time: ")
                            print("28d - 91d - 182d - 364d")
                            period = input()

                    if period == "28d":
                        rate = 0.051
                        due_date_d = today + timedelta(days=28)
                        due_date = due_date_d.strftime("%d/%m/%Y")
                        period_days = 28

                        print("\nThe rate of a CETE bond for 28 days is 5.1% as of " + date_of_issue)

                    elif period == "91d":
                        rate = 0.055
                        due_date_d = today + timedelta(days=91)
                        due_date = due_date_d.strftime("%d/%m/%Y")
                        period_days = 91

                        print("\nThe rate of a CETE bond for 91 days is 5.5% as of " + date_of_issue)

                    elif period == "182d":
                        rate = 0.0586
                        due_date_d = today + timedelta(days=182)
                        due_date = due_date_d.strftime("%d/%m/%Y")
                        period_days = 182

                        print("\nThe rate of a CETE bond for 182 days is 5.86% as of " + date_of_issue)

                    elif period == "364d":
                        rate = 0.0656
                        due_date_d = today + timedelta(days=364)
                        due_date = due_date_d.strftime("%d/%m/%Y")
                        period_days = 164

                        print("\nThe rate of a CETE bond for 364 days is 6.56% as of " + date_of_issue)

                    else:
                        print("ERROR")

                    # Save to memory:
                    new_row = {'bond_type': bond_type, 'initial_investment_mxn': initial_investment_mxn, 'initial_investment_usd': initial_investment_usd,
                                   'rate': rate, 'period': period, 'period_days': period_days,
                                   'date_of_issue': date_of_issue, 'due_date': due_date,
                                   'status': "ACTIVE", 'return': 0.0, 'ISR': 0.0,
                                   'final_amount': 0.0}

                    df_mmkt = df_mmkt.append(new_row, ignore_index=True)
                    save_mmkt_wallet()

                    update_balance(get_balance() - initial_investment_usd)

                    print("\nBond successfully purchased! Check your Money Market Wallet for more info.")

                elif bond_type == "VARIABLE":
                    date_of_issue = today.strftime("%d/%m/%Y")
                    due_date = None
                    rate = None

                    print("\nPlease enter the initial investment in MXN:")
                    initial_investment_mxn = int(input())
                    initial_investment_usd = (initial_investment_mxn / issue_ex_rate)

                    while initial_investment_usd > get_balance():
                        print("\nInsufficient funds: " + str(get_balance()) + "USD")
                        print("\nThe minimum investment is 1000 MXN (100 CETES)")
                        print("Please enter the initial investment in MXN:")
                        initial_investment_mxn = int(input())
                        initial_investment_usd = (initial_investment_mxn / issue_ex_rate)

                    print("\nPlease enter the period in time in days:")
                    period_days = int(input())
                    period = (str(period_days) + "d")
                    due_date_d = today + timedelta(days=period_days)
                    due_date = due_date_d.strftime("%d/%m/%Y")

                    print("\nPlease enter the initial rate in decimals (Ex. 5.1% = 0.051):")
                    rate = float(input())

                    # Save to memory:
                    new_row = {'bond_type': bond_type, 'initial_investment_mxn': initial_investment_mxn,
                               'initial_investment_usd': initial_investment_usd,
                               'rate': rate, 'period': period, 'period_days': period_days,
                               'date_of_issue': date_of_issue, 'due_date': due_date,
                               'status': "ACTIVE", 'return': 0.0, 'ISR': 0.0,
                               'final_amount': 0.0}

                    df_mmkt = df_mmkt.append(new_row, ignore_index=True)
                    save_mmkt_wallet()

                    update_balance(get_balance() - initial_investment_usd)

                    print("\nBond successfully purchased! Check your Money Market Wallet for more info.")

            elif user_selection == "Wallet":
                print("\nBonds Wallet selected:")

                # Check for expired bonds and perform the Fixing:
                for x in range(0, len(df_mmkt)):

                    if df_mmkt['status'][x] == "ACTIVE":
                        due_date = datetime.strptime(df_mmkt['due_date'][x], "%d/%m/%Y").date()
                        today = date.today()

                        if due_date <= today:
                            print("\nYour " + df_mmkt['bond_type'][x] + " bond bought in " + df_mmkt['bond_type'][x] + " was due in " + df_mmkt['date_of_issue'][x])

                            print("\nPlease select one of the following options: ")
                            print("FullCollect - ProfitOnlyCollect - FullReinvest")
                            user_action = input()

                            while True:
                                if user_action == "FullCollect" or user_action == "ProfitOnlyCollect" or user_action == "FullReinvest":
                                    break

                                else:
                                    print("\n" + user_action + " is not a valid option.")
                                    print("Please select one of the following options: ")
                                    print("FullCollect - ProfitOnlyCollect - FullReinvest")
                                    user_action = input()

                            bond_type = df_mmkt['bond_type'][x]

                            if user_action == "FullCollect":
                                initial_investment_usd = df_mmkt['initial_investment_usd'][x]
                                rate = df_mmkt['rate'][x]
                                interests = initial_investment_usd * rate
                                isr = interests * 0.16
                                investment_return = interests - isr
                                final_amount = initial_investment_usd + investment_return

                                print("\n--------------")
                                print("Interests: " + str(interests) + " USD")
                                print("ISR: " + str(isr) + " USD")
                                print("Return: " + str(investment_return) + " USD")
                                print("Final amount: " + str(final_amount) + " USD")
                                print("--------------")

                                df_mmkt['status'][x] = "COLLECTED"
                                df_mmkt['return'][x] = investment_return
                                df_mmkt['ISR'][x] = isr
                                df_mmkt['final_amount'][x] = final_amount

                                save_mmkt_wallet()

                                update_balance(get_balance() + final_amount)

                                print(bond_type + " bond successfully collected. Check your Money Market wallet for more info.")

                            elif user_action == "ProfitOnlyCollect":
                                initial_investment_usd = df_mmkt['initial_investment_usd'][x]
                                rate = df_mmkt['rate'][x]
                                interests = initial_investment_usd * rate
                                isr = interests * 0.16
                                investment_return = interests - isr
                                final_amount = df_mmkt['final_amount'][x] + investment_return

                                print("\n--------------")
                                print("Interests: " + str(interests) + " USD")
                                print("ISR: " + str(isr) + " USD")
                                print("Return: " + str(investment_return) + " USD")
                                print("Final amount: " + str(final_amount) + " USD")
                                print("--------------")

                                df_mmkt['return'][x] = investment_return
                                df_mmkt['ISR'][x] = isr
                                df_mmkt['final_amount'][x] = final_amount

                                period_days = int(df_mmkt['period_days'][x])
                                new_due_date = due_date + timedelta(days=period_days)
                                new_due_date_str = new_due_date.strftime("%d/%m/%Y")
                                df_mmkt['due_date'][x] = new_due_date_str

                                if bond_type == "VARIABLE":
                                    print("\nPlease enter the new rate: ")
                                    new_rate = float(input())
                                    df_mmkt['rate'][x] = new_rate

                                save_mmkt_wallet()

                                update_balance(get_balance() + investment_return)

                                print(bond_type + " bond successfully collected and reinvested. Check your Money Market wallet for more info.")

                            elif user_action == "FullReinvest":
                                initial_investment_usd = df_mmkt['initial_investment_usd'][x]
                                rate = df_mmkt['rate'][x]
                                interests = initial_investment_usd * rate
                                isr = interests * 0.16
                                investment_return = interests - isr
                                final_amount = investment_return

                                print("\n--------------")
                                print("Interests: " + str(interests) + " USD")
                                print("ISR: " + str(isr) + " USD")
                                print("Return: " + str(investment_return) + " USD")
                                print("Final amount: " + str(final_amount) + " USD")
                                print("--------------")

                                df_mmkt['initial_investment_usd'][x] = initial_investment_usd + investment_return

                                today = date.today()
                                today_str = today.strftime("%Y-%m-%d")

                                currency_data = yf.download("MXN=X", start=today_str, end=today_str)
                                issue_ex_rate = round(currency_data.get('Close')[0], 2)

                                initial_investment_mxn = initial_investment_usd * issue_ex_rate
                                df_mmkt['initial_investment_mxn'][x] = initial_investment_mxn

                                period_days = int(df_mmkt['period_days'][x])
                                new_due_date = due_date + timedelta(days=period_days)
                                new_due_date_str = new_due_date.strftime("%d/%m/%Y")
                                df_mmkt['due_date'][x] = new_due_date_str

                                if bond_type == "VARIABLE":
                                    print("\nPlease enter the new rate: ")
                                    new_rate = float(input())
                                    df_mmkt['rate'][x] = new_rate

                                save_mmkt_wallet()

                                print(bond_type + " bond successfully collected and reinvested. Check your Money Market wallet for more info.")

                display_mmkt_wallet()

            elif user_selection == "Return":
                break

            else:
                print("Please select a valid option:")

    elif x == "PandL":
        print("\nGenerating report...")

        starting_funds = 70522.52

        stock_market = 0
        derivatives_market = 0
        money_market = 0

        profit_loss_overall = 0

        for x in range(0, len(df)):
            stock_market = stock_market + int(df['profit-loss'][x])

        for x in range(0, len(df_notes)):

            derivatives_market = derivatives_market + int(df_notes['final_amount'][x])

        for x in range(0, len(df_mmkt)):

            money_market = money_market + int(df_mmkt['final_amount'][x])

        profit_loss_overall = stock_market + derivatives_market + money_market

        print("\nP&L REPORT:")
        print("----------------")
        print("P&L Stock Market: " + str(stock_market) + " USD")
        print("P&L Derivatives Market: " + str(derivatives_market) + " USD")
        print("P&L Money Market: " + str(money_market) + " USD")
        print("\nP&L Overall: " + str(profit_loss_overall) + " USD")
        print("\nStarting Funds: " + str(starting_funds))
        print("Current Funds: " + str(get_balance()))
        print("----------------")

    elif x == "Exit":
        print("Exiting...")
        run = False

    else:
        print("Please select a valid option:")

