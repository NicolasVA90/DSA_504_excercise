# =============================================
# DSA 504: FINAL PROJECT
# Topic: NYC Traffic Crash Patterns & Borough Severity
# =============================================

# =============================================
# 1. CLEARLY STATED QUESTION:
# =============================================

# "Which NYC borough experiences the highest total volume of motor vehicle crashes, 
# and how do injuries and primary contributing factors distribute across boroughs?"

import glob
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================
# 2. DATA SOURCE & INGESTION (Using a smaller local subset for fast execution)
# =============================================

# Setting nrows=50000 loads a fast, manageable slice while keeping all columns intact
print("Locating local crash dataset...")
matching_files = glob.glob("Motor_Vehicle_Collisions*.csv")

if not matching_files:
    raise FileNotFoundError(
        "No matching CSV file found in the 'Final Project' folder!"
    )

file_path = matching_files[0]
print(f"Found file: {file_path}. Loading subset...")

df = pd.read_csv(file_path, nrows=50000, low_memory=False)
print(f"Dataset successfully loaded! Shape: {df.shape}")
df.head(3)

# =============================================
# # 3. DATA CLEANING & HYGIENE
# =============================================

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

# =============================================
# # 4. SQLITE DATABASE INTEGRATION
# =============================================

print("Loading data into SQLite database...")

# Create an in-memory SQLite connection (or connect to a local file database like 'crashes.db')
conn = sqlite3.connect("nyc_crashes.db")

# Write the DataFrame to a SQL table named 'crashes'
df.to_sql("crashes", conn, if_exists="replace", index=False)

print("Data successfully loaded into SQLite table 'crashes'!")

# =============================================
# # 5. SQL ANALYSIS & VISUALIZATION
# =============================================

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

# Plotting Total Crashes by Borough
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

# Save and show plot
plt.savefig("borough_crashes.png")
plt.show()

# Close database connection
conn.close()

# =============================================
# 6. AI-USE DISCLOSURE & REFLECTION
# =============================================
print(
    """
AI Disclosure:
- Artificial Intelligence (Gemini) was consulted as an assistive technical co-pilot 
  to structure the Pandas data cleaning pipeline, optimize SQLite aggregation syntax, 
  and refine Matplotlib/Seaborn visualization parameters.
- Rigorous Verification: All generated logic, query outputs, and visual plots were 
  manually reviewed, tested, executed, and interpreted by the author to ensure 
  technical precision and domain validity.
"""
)

