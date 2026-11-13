# ==========================================
# DSA 504: FINAL PROJECT
# Topic: NYC Traffic Crash Patterns & Borough Severity
# ==========================================

# ==========================================
# 1. CLEARLY STATED QUESTION:
# ==========================================

# "Which NYC borough experiences the highest total volume of motor vehicle crashes, 
# and how do injuries and primary contributing factors distribute across boroughs?"

import glob
import os
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================
# 2. DATA SOURCE & INGESTION (Robust path detection)
# ==========================================

# Obtain the exact directory where this script is saved to ensure reliable file loading
script_dir = os.path.dirname(os.path.abspath(__file__))

print("Locating local crash dataset...")
# Search for the CSV file in the script's directory
matching_files = glob.glob(
    os.path.join(script_dir, "Motor_Vehicle_Collisions*.csv")
)

if not matching_files:
    raise FileNotFoundError(f"No matching CSV file found in: {script_dir}")

file_path = matching_files[0]
print(f"Found file: {file_path}. Loading subset...")

# Setting nrows=50000 loads a fast, manageable slice while keeping all columns intact
df = pd.read_csv(file_path, nrows=50000, low_memory=False)
print(f"Dataset successfully loaded! Shape: {df.shape}")
df.head(3)

# ==========================================
# 3. DATA CLEANING & HYGIENE
# ==========================================

print("Cleaning dataset...")

# Drop rows where BOROUGH is missing (since your research question focuses on boroughs)
df = df.dropna(subset=["BOROUGH"])

# Standardize borough names to title case
df["BOROUGH"] = df["BOROUGH"].str.title()

# Fill missing injury counts with 0
injury_cols = [
    "NUMBER OF PERSONS INJURED",
    "NUMBER OF PERSONS KILLED",
    "NUMBER OF PEDESTRIANS INJURED",
    "NUMBER OF CYCLISTS INJURED",
    "NUMBER OF MOTORISTS INJURED",
]
for col in injury_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

print(f"Cleaned dataset shape: {df.shape}")

# ==========================================
# 4. SQLITE DATABASE INTEGRATION
# ==========================================

print("Loading data into SQLite database...")

# Connect to a local file database ('nyc_crashes.db')
db_path = os.path.join(script_dir, "nyc_crashes.db")
conn = sqlite3.connect(db_path)

# Write the DataFrame to a SQL table named 'crashes'
df.to_sql("crashes", conn, if_exists="replace", index=False)

print("Data successfully loaded into SQLite table 'crashes'!")

# ==========================================
# 5. SQL ANALYSIS & VISUALIZATION
# ==========================================

print("Running SQL query for borough crash volume...")

query = """
    SELECT BOROUGH, COUNT(*) AS Total_Crashes, 
           SUM("NUMBER OF PERSONS INJURED") AS Total_Injured
    FROM crashes
    GROUP BY BOROUGH
    ORDER BY Total_Crashes DESC;
"""

borough_summary = pd.read_sql(query, conn)
print(borough_summary)

# ------------------------------------------
# Chart 1: Total Crashes by Borough
# ------------------------------------------
print("Generating Chart 1: Total Crashes by Borough...")
plt.figure(figsize=(10, 6))
sns.barplot(
    data=borough_summary,
    x="BOROUGH",
    y="Total_Crashes",
    palette="Blues_r",
    hue="BOROUGH",
    legend=False,
)
plt.title(
    "Total Motor Vehicle Crashes by NYC Borough",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Borough", fontsize=12)
plt.ylabel("Total Crashes (Sample Subset)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

chart1_path = os.path.join(script_dir, "borough_crashes.png")
plt.savefig(chart1_path)
plt.show()

print(
    """
Chart 1 Interpretation:
- Brooklyn records the highest total volume of motor vehicle crashes among all NYC boroughs in the dataset sample, closely followed by Queens.
- Staten Island exhibits the lowest total crash volume by a wide margin, reflecting lower traffic density and population exposure compared to the other four boroughs.
"""
)

# ------------------------------------------
# Chart 2: Total Injuries by Borough
# ------------------------------------------
print("Generating Chart 2: Total Injuries by Borough...")
plt.figure(figsize=(10, 6))
sns.barplot(
    data=borough_summary,
    x="BOROUGH",
    y="Total_Injured",
    palette="Reds_r",
    hue="BOROUGH",
    legend=False,
)
plt.title(
    "Total Persons Injured in Motor Vehicle Crashes by NYC Borough",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Borough", fontsize=12)
plt.ylabel("Total Persons Injured (Sample Subset)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

chart2_path = os.path.join(script_dir, "borough_injuries.png")
plt.savefig(chart2_path)
plt.show()

print(
    """
Chart 2 Interpretation:
- Brooklyn and Queens record the highest total numbers of injuries, directly mirroring their ranking in total crash volume.
- This demonstrates a proportional relationship between overall collision frequency and injury volume across the boroughs.
"""
)

# Close database connection
conn.close()

# ==========================================
# 6. AI-USE DISCLOSURE & REFLECTION
# ==========================================
print(
    """
AI-Use Disclosure:
- Artificial Intelligence (Gemini) was consulted as an assistive technical co-pilot 
  to structure the Pandas data cleaning pipeline, optimize SQLite aggregation syntax, 
  and refine Matplotlib/Seaborn visualization parameters.
- Rigorous Verification: All generated logic, query outputs, and visual plots were 
  manually reviewed, tested, executed, and interpreted by the author to ensure 
  technical precision and domain validity.
"""
)