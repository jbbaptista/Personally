import sqlite3
import datetime
import matplotlib.pyplot as plt
import numpy as np


def fetch_data(cursor, table_name, date_range):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    date_columns = [column for column in columns if column.startswith("date_") and column[5:] in date_range]
    cursor.execute(f"SELECT sector_id, sector_name, {', '.join(date_columns)} FROM {table_name}")
    return cursor.fetchall()


def calculate_growth_percentages(data, date_columns):
    growth = []
    for row in data:
        sector_id, sector_name, *values = row
        growth_percentages = [(values[i + 1] - values[i]) / values[i] * 100 if values[i] is not None and values[
            i + 1] is not None else None for i in range(len(values) - 1)]
        growth.append((sector_id, sector_name, *growth_percentages))
    return growth


def print_growth(growth_data, date_columns):
    for row in growth_data:
        sector_id, sector_name, *growth_percentages = row
        print(f"{sector_name} ({sector_id}):")
        for date, growth_percentage in zip(date_columns, growth_percentages):
            if growth_percentage is not None:
                print(f"{date}: {growth_percentage:.2f}%")
            else:
                print(f"{date}: N/A")
        print()


def calculate_avg_weekly_volume(data, date_columns):
    avg_weekly_volumes = []
    for row in data:
        sector_id, sector_name, *values = row
        avg_weekly_volume = sum([value for value in values if value is not None]) / len(values)
        avg_weekly_volumes.append((sector_id, sector_name, avg_weekly_volume))
    return avg_weekly_volumes


def calculate_volume_ratios(daily_volume_data, avg_weekly_volume_data, date_columns):
    volume_ratios = []
    for daily_row, avg_weekly_row in zip(daily_volume_data, avg_weekly_volume_data):
        sector_id, sector_name, *daily_values = daily_row
        _, _, avg_weekly_volume = avg_weekly_row
        ratios = [(daily_value / avg_weekly_volume) * 100 if daily_value is not None else None for daily_value in
                  daily_values]
        volume_ratios.append((sector_id, sector_name, *ratios))
    return volume_ratios


def print_volume_ratios(volume_ratio_data, date_columns):
    for row in volume_ratio_data:
        sector_id, sector_name, *volume_ratios = row
        print(f"{sector_name} ({sector_id}):")
        for date, volume_ratio in zip(date_columns, volume_ratios):
            if volume_ratio is not None:
                print(f"{date}: {volume_ratio:.2f}%")
            else:
                print(f"{date}: N/A")
        print()


# Connect to the SQLite database
conn = sqlite3.connect("crypto_sectors.db")
cursor = conn.cursor()

# Define the date range for daily and weekly data
today = datetime.date.today()
one_week_ago = today - datetime.timedelta(weeks=1)
date_range = [today - datetime.timedelta(days=i) for i in range(8)]
date_range_str = [date.strftime("%Y-%m-%d") for date in date_range]

# Fetch daily data and calculate growth percentages
market_cap_daily = fetch_data(cursor, "market_cap", date_range_str)
market_cap_growth = calculate_growth_percentages(market_cap_daily, date_range_str[1:])
print_growth(market_cap_growth, date_range_str[1:])

volume_daily = fetch_data(cursor, "daily_volume", date_range_str)
volume_growth = calculate_growth_percentages(volume_daily, date_range_str[1:])
print_growth(volume_growth, date_range_str[1:])

# Fetch weekly data and calculate growth percentages
weekly_date_range = [one_week_ago, today]
weekly_date_range_str = [date.strftime("%Y-%m-%d") for date in weekly_date_range]

market_cap_weekly = fetch_data(cursor, "market_cap", weekly_date_range_str)
market_cap_weekly_growth = calculate_growth_percentages(market_cap_weekly, weekly_date_range_str)
print_growth(market_cap_weekly_growth, weekly_date_range_str)

volume_weekly = fetch_data(cursor, "daily_volume", weekly_date_range_str)
volume_weekly_growth = calculate_growth_percentages(volume_weekly, weekly_date_range_str)
print_growth(volume_weekly_growth, weekly_date_range_str)

# Calculate average weekly volume and volume ratios
avg_weekly_volume = calculate_avg_weekly_volume(volume_weekly, weekly_date_range_str)
volume_ratios = calculate_volume_ratios(volume_daily, avg_weekly_volume, date_range_str[1:])
print_volume_ratios(volume_ratios, date_range_str[1:])

# Close the SQLite connection
conn.close()
