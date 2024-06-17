import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'testingSomething.xlsx'  # Update this with your file path
df = pd.read_excel(file_path)

# Define the point allocations
mem_tech_points = {
    'Banner': 5,
    'Jsy': 15,
    'Jsy-Jsy': 18,
    'Rally Towel': 10,
    'Patch': 17,
    'Die Cut': 12,
    'MF Letter Patch': 20,
    'Net Cord': 20,
    'Jsy-Patch': 19,
    'Unknown': 5
}
rarity_points_ranges = {
    (1, 10): 30,
    (11, 50): 25,
    (51, 100): 20,
    (101, 200): 15,
    (201, 500): 10,
    (501, 1000): 5,
    (1001, float('inf')): 1
}
def get_rarity_points(numbered):
    for range_, points in rarity_points_ranges.items():
        if range_[0] <= numbered <= range_[1]:
            return points
    return 0

# Function to calculate points
def calculate_points(row):
    if row["#'d"] == 0 or pd.isna(row["#'d"]):
        auto_points = 30 if row['Auto'] == 1 else 0
        mem_tech_points_val = mem_tech_points.get(row['Mem/Tech'], mem_tech_points['Unknown'])
        rookie_points = 10 if row['Rookie'] == 1 else 0
        odd_points = 20*1/row['Odds']
        return auto_points  + mem_tech_points_val + odd_points + rookie_points
    auto_points = 20 if row['Auto'] == 1 else 0
    # odds_points = 10 if row['Odds'] > 0 else 0
    mem_tech_points_val = mem_tech_points.get(row['Mem/Tech'], mem_tech_points['Unknown'])
    
    
    rarity_points = get_rarity_points(row["#'d"])
    rookie_points = 10 if row['Rookie'] == 1 else 0
    return auto_points  + mem_tech_points_val + rarity_points + rookie_points

# Calculate total points for each row
df['Total Points'] = df.apply(calculate_points, axis=1)

# Define scaling factor
max_points = 80
max_price = 20
scaling_factor = max_price / max_points
base_value = 0.5

# Calculate predicted resale price
df['Predicted Resale Price'] = df['Total Points'] * scaling_factor + base_value

# Save the updated DataFrame to a new Excel file
output_file_path = 'testingSomething2.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Predicted resale prices have been saved to {output_file_path}")
