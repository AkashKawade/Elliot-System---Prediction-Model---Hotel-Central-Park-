import pandas as pd

# Load the Excel file
file_path = 'Client data\Central Park Hotel-20250116T104224Z-001\Central Park Hotel\CIAT plant\CIAT 1 jan-9 Aug 2024.xlsx'  # Replace with your actual file path

# Load all sheets into a dictionary of DataFrames
sheets_dict = pd.read_excel(file_path, sheet_name=None, skiprows=3)

# Initialize a list to store the combined data
combined_data = []

# Process each sheet
for sheet_name, df in sheets_dict.items():
    # Transpose the DataFrame
    df_transposed = df.transpose()

    # Use the first row as the header and keep the first row in the data
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed[1:].reset_index(drop=True)

    # Try to parse the sheet name as a date
    try:
        # Parse the sheet name as a date in the format 'Tue Dec 27 2022'
        parsed_date = pd.to_datetime(sheet_name, format='%a %b %d %Y', errors='coerce')
        if pd.isna(parsed_date):
            print(f"Could not parse date from sheet name: {sheet_name}")
            continue
        # Format the parsed date as dd/mm/yyyy
        formatted_date = parsed_date.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Error parsing date from sheet name '{sheet_name}': {e}")
        continue

    # Add the formatted date to the DataFrame
    df_transposed['Date'] = formatted_date

    # Reverse the data in all columns
    df_transposed = df_transposed.iloc[::-1].reset_index(drop=True)

    # Append the transposed DataFrame to the list
    combined_data.append(df_transposed)

# Combine all the data into a single DataFrame
combined_df = pd.concat(combined_data, ignore_index=True)


# Save the combined DataFrame to a CSV file
output_file_path = 'CCIAT 1 jan-9 Aug 2024_Combine_Data.csv'  # Replace with your desired output file path
combined_df.to_csv(output_file_path, index=False)

print("Combination complete. The new CSV file with reversed data in columns has been saved.")
