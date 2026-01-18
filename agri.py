import pandas as pd

# Load data
df = pd.read_csv(r"C:\Users\BalaGomathi\Downloads\ICRISAT-District Level Data - ICRISAT-District Level Data.csv")

# Handle missing values: Fill NaN with 0 for areas/productions/yields (or drop if irrelevant)
df.fillna(0, inplace=True)

# Standardize units: Multiply areas/productions by 1000 to convert to actual ha/tons (if needed; check data)
area_cols = [col for col in df.columns if 'AREA' in col]
prod_cols = [col for col in df.columns if 'PRODUCTION' in col]
# df[area_cols] *= 1000  # Uncomment if in 1000 units

# Ensure consistency: Convert all to lowercase for names
df['State Name'] = df['State Name'].str.lower().str.title()
df['Dist Name'] = df['Dist Name'].str.lower().str.title()

# Save cleaned data
df.to_csv('cleaned_agri_data.csv', index=False)