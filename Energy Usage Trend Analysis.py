#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display  # For rendering HTML tables in Jupyter

# Load your dataset
data = pd.read_csv('CCIAT 1 jan-9 Aug 2024_Combine_Data.csv', parse_dates=[['Date', 'Description']])
data.rename(columns={'Date_Description': 'DateTime'}, inplace=True)

# Add useful columns for filtering
data['Date'] = data['DateTime'].dt.date  # Extract date
data['YearMonth'] = data['DateTime'].dt.to_period('M')  # Extract year-month

# Calculate non-cumulative kWh difference
data['kWh_Difference'] = data['kWh'].diff().fillna(0)  # Calculate differenceChiller Pump Feb 01 2022_to Dec 31 2022_Combine_Data.
data.loc[data['kWh_Difference'] < 0, 'kWh_Difference'] = 0  # Handle negative differences

# Function to filter data and calculate totals
def filter_usage(data, choice_type, choice_value):
    if choice_type == 'date':
        # Filter by specific date
        filtered_data = data[data['Date'] == pd.to_datetime(choice_value).date()]
        print(f"Energy usage for {choice_value}:")
    elif choice_type == 'month':
        # Filter by specific month
        filtered_data = data[data['YearMonth'] == pd.to_datetime(choice_value).to_period('M')]
        print(f"Energy usage for {choice_value}:")
    else:
        print("Invalid choice_type! Use 'date' or 'month'.")
        return

    # Sort the filtered data by DateTime to ensure it is in chronological order
    filtered_data = filtered_data.sort_values(by='DateTime')

    # Calculate totals using non-cumulative kWh_Difference
    total_kw = filtered_data['kW (Total)'].sum()
    total_kwh = filtered_data['kWh_Difference'].sum()
    avg_pf = filtered_data['Avg PF'].mean()

    print(f"\nTotal Energy Usage:")
    print(f"- Total kW (Total): {total_kw:.2f}")
    print(f"- Total kWh (Difference): {total_kwh:.2f}")
    print(f"- Average Power Factor (Avg PF): {avg_pf:.2f}")

    # Display detailed results in a scrollable table
    daily_summary = filtered_data[['DateTime', 'kW (Total)', 'kWh', 'kWh_Difference', 'Avg PF']].copy()
    print("\nDetailed Data:")
    styled_table = daily_summary.style.set_table_attributes("style='display:inline-block; overflow:auto; height:400px;'")                                        .set_table_styles([
                                           {'selector': 'th', 'props': [('font-size', '12px')]},
                                           {'selector': 'td', 'props': [('font-size', '12px')]},
                                       ])
    display(styled_table)  # Display scrollable table in Jupyter Notebook

    # Plot the results with time for the selected specific date or month
    plt.figure(figsize=(14, 7))
    plt.plot(filtered_data['DateTime'], filtered_data['kW (Total)'], label='kW (Total)', color='blue', linewidth=2)
    plt.plot(filtered_data['DateTime'], filtered_data['kWh_Difference'], label='kWh (Difference)', color='orange', linewidth=2)

    # Format the x-axis for clearer date labeling
    if choice_type == 'month':
        # Show every day of the month
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # Show major ticks for each day in the month
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))  # Show day-month-year format
    else:
        # If it's a daily plot, set intervals based on time
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Show time as HH:MM
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Set tick intervals to every 1 hour

    # Auto-format x-axis labels for better readability
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

    # Set plot title and labels
    plt.title(f"Energy Usage for {choice_value}", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Energy", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# Function to take user input for date or month
def get_user_input():
    choice_type = input("Enter the type of filter ('date' or 'month'): ").strip().lower()
    
    if choice_type == 'date':
        choice_value = input("Enter the specific date (in format YYYY-MM-DD): ").strip()
    elif choice_type == 'month':
        choice_value = input("Enter the specific month (in format YYYY-MM): ").strip()
    else:
        print("Invalid choice. Please enter 'date' or 'month'.")
        return
    
    filter_usage(data, choice_type, choice_value)

# Example: Get user input for filtering
get_user_input()


# In[ ]:




