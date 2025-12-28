import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df_raw = pd.read_csv(r"C:\Users\BalaGomathi\Desktop\GUVI\cleaned_agri_data.csv")

# Convert wide format to long format
crops = {
    'Rice': ['RICE AREA (1000 ha)', 'RICE PRODUCTION (1000 tons)', 'RICE YIELD (Kg per ha)'],
    'Wheat': ['WHEAT AREA (1000 ha)', 'WHEAT PRODUCTION (1000 tons)', 'WHEAT YIELD (Kg per ha)'],
    'Maize': ['MAIZE AREA (1000 ha)', 'MAIZE PRODUCTION (1000 tons)', 'MAIZE YIELD (Kg per ha)'],
    'Cotton': ['COTTON AREA (1000 ha)', 'COTTON PRODUCTION (1000 tons)', 'COTTON YIELD (Kg per ha)'],
    'Groundnut': ['GROUNDNUT AREA (1000 ha)', 'GROUNDNUT PRODUCTION (1000 tons)', 'GROUNDNUT YIELD (Kg per ha)'],
    'Sugarcane': ['SUGARCANE AREA (1000 ha)', 'SUGARCANE PRODUCTION (1000 tons)', 'SUGARCANE YIELD (Kg per ha)'],
    'Soybean': ['SOYABEAN AREA (1000 ha)', 'SOYABEAN PRODUCTION (1000 tons)', 'SOYABEAN YIELD (Kg per ha)'],
    'Sunflower': ['SUNFLOWER AREA (1000 ha)', 'SUNFLOWER PRODUCTION (1000 tons)', 'SUNFLOWER YIELD (Kg per ha)'],
    'Sesamum': ['SESAMUM AREA (1000 ha)', 'SESAMUM PRODUCTION (1000 tons)', 'SESAMUM YIELD (Kg per ha)'],
}

# Create long format dataframe
data_list = []
for crop, cols in crops.items():
    if all(c in df_raw.columns for c in cols):
        temp = df_raw[['Dist Code', 'Year', 'State Code', 'State Name', 'Dist Name'] + cols].copy()
        temp.columns = ['Dist Code', 'Year', 'State Code', 'State_Name', 'District_Name', 'Area', 'Production', 'Yield']
        temp['Crop'] = crop
        temp['Crop_Year'] = temp['Year']
        data_list.append(temp)

df = pd.concat(data_list, ignore_index=True)
df = df[['Crop_Year', 'State_Name', 'District_Name', 'Crop', 'Area', 'Production', 'Yield']]
df = df.dropna(subset=['Production', 'Area'])
df = df[(df['Area'] > 0) & (df['Production'] > 0)]

print("Generating 10 CSV files for Power BI...")

# Query 1: Top 7 Rice Producing States
rice_df = df[df['Crop'] == 'Rice']
rice_prod = rice_df.groupby('State_Name')['Production'].sum().nlargest(7).reset_index()
rice_prod.columns = ['State_Name', 'Total_Production']
rice_prod.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_1_Top7_Rice_States.csv', index=False)
print("✓ Query 1: Top 7 Rice Producing States")

# Query 2: Top 5 Wheat Producing States
wheat_df = df[df['Crop'] == 'Wheat']
wheat_prod = wheat_df.groupby('State_Name')['Production'].sum().nlargest(5).reset_index()
wheat_prod.columns = ['State_Name', 'Total_Production']
wheat_prod.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_2_Top5_Wheat_States.csv', index=False)
print("✓ Query 2: Top 5 Wheat Producing States")

# Query 3: Year-wise Trend of Rice Production (Top 3 States)
top3_rice_states = rice_df.groupby('State_Name')['Production'].sum().nlargest(3).index
rice_yearly = rice_df[rice_df['State_Name'].isin(top3_rice_states)].groupby(['Crop_Year', 'State_Name'])['Production'].sum().reset_index()
rice_yearly.columns = ['Year', 'State_Name', 'Production']
rice_yearly.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_3_Rice_Yearly_Top3_States.csv', index=False)
print("✓ Query 3: Year-wise Rice Production Trend (Top 3 States)")

# Query 4: Top 5 Districts by Wheat Production Growth (Last 5 Years)
recent_years = sorted(wheat_df['Crop_Year'].unique())[-5:]
wheat_recent = wheat_df[wheat_df['Crop_Year'].isin(recent_years)]
wheat_district_yearly = wheat_recent.groupby(['District_Name', 'Crop_Year'])['Production'].sum().unstack(fill_value=0)
growth = ((wheat_district_yearly.iloc[:, -1] - wheat_district_yearly.iloc[:, 0]) / wheat_district_yearly.iloc[:, 0] * 100).nlargest(5).reset_index()
growth.columns = ['District_Name', 'Growth_Rate_Percentage']
growth.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_4_Top5_Wheat_District_Growth.csv', index=False)
print("✓ Query 4: Top 5 Districts by Wheat Production Growth (Last 5 Years)")

# Query 5: States with Highest Growth in Oilseed Production
oilseeds = ['Groundnut', 'Soybean', 'Sunflower', 'Sesamum']
oilseed_df = df[df['Crop'].isin(oilseeds)]
oilseed_yearly = oilseed_df.groupby(['State_Name', 'Crop_Year'])['Production'].sum().unstack(fill_value=0)
recent_oilseed_years = oilseed_yearly.columns[-5:]
oilseed_growth = ((oilseed_yearly[recent_oilseed_years[-1]] - oilseed_yearly[recent_oilseed_years[0]]) / oilseed_yearly[recent_oilseed_years[0]] * 100).nlargest(5).reset_index()
oilseed_growth.columns = ['State_Name', 'Growth_Rate_Percentage']
oilseed_growth.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_5_Top5_Oilseed_Growth_States.csv', index=False)
print("✓ Query 5: Top 5 States by Oilseed Production Growth")

# Query 6: Yearly Production Growth of Cotton (Top 5 States)
cotton_df = df[df['Crop'] == 'Cotton']
top5_cotton_states = cotton_df.groupby('State_Name')['Production'].sum().nlargest(5).index
cotton_yearly = cotton_df[cotton_df['State_Name'].isin(top5_cotton_states)].groupby(['Crop_Year', 'State_Name'])['Production'].sum().reset_index()
cotton_yearly.columns = ['Year', 'State_Name', 'Production']
cotton_yearly.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_6_Cotton_Yearly_Top5_States.csv', index=False)
print("✓ Query 6: Yearly Cotton Production (Top 5 States)")

# Query 7: Districts with Highest Groundnut Production in 2017
groundnut_2017 = df[(df['Crop'] == 'Groundnut') & (df['Crop_Year'] == 2017)].groupby('District_Name')['Production'].sum().nlargest(10).reset_index()
groundnut_2017.columns = ['District_Name', 'Production']
groundnut_2017.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_7_Top10_Groundnut_Districts_2017.csv', index=False)
print("✓ Query 7: Top 10 Districts for Groundnut Production (2017)")

# Query 8: Average Maize Yield by State
maize_df = df[df['Crop'] == 'Maize'].copy()
maize_df['Yield'] = maize_df['Production'] / maize_df['Area']
maize_yield = maize_df.groupby('State_Name')['Yield'].mean().sort_values(ascending=False).reset_index()
maize_yield.columns = ['State_Name', 'Average_Yield']
maize_yield.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_8_Maize_Average_Yield_by_State.csv', index=False)
print("✓ Query 8: Average Maize Yield by State")

# Query 9: Total Area Cultivated for Oilseeds by State
oilseed_area = oilseed_df.groupby('State_Name')['Area'].sum().sort_values(ascending=False).reset_index()
oilseed_area.columns = ['State_Name', 'Total_Area']
oilseed_area.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_9_Oilseed_Total_Area_by_State.csv', index=False)
print("✓ Query 9: Total Area Cultivated for Oilseeds by State")

# Query 10: Top 10 Districts by Rice Yield
rice_df_yield = rice_df.copy()
rice_df_yield['Yield'] = rice_df_yield['Production'] / rice_df_yield['Area']
top_rice_yield = rice_df_yield.groupby('District_Name')['Yield'].mean().nlargest(10).reset_index()
top_rice_yield.columns = ['District_Name', 'Average_Yield']
top_rice_yield.to_csv(r'C:\Users\BalaGomathi\Desktop\GUVI\Query_10_Top10_Rice_Yield_Districts.csv', index=False)
print("✓ Query 10: Top 10 Districts by Rice Yield")

print("\n✅ All 10 CSV files generated successfully in C:\\Users\\BalaGomathi\\Desktop\\GUVI\\")
