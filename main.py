# terrorism_rand_en.py
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob
import re
from datetime import datetime

# -------------------------------------------------
# 1. Find and load the RAND CSV file
# -------------------------------------------------
patterns = [
    'RAND_Database_of_Worldwide_Terrorism_Incidents.csv',
    'rdwti.csv',
    'terrorism-incidents*.csv',
    'rand_terrorism*.csv'
]

csv_file = None
for p in patterns:
    matches = glob.glob(p)
    if matches:
        csv_file = matches[0]
        break

if csv_file is None:
    print("ERROR: RAND CSV file not found in the current folder.")
    print("Download it from https://www.rand.org/nsrd/projects/terrorism-incidents/download.html")
    print("and place the file (e.g. RAND_Database_of_Worldwide_Terrorism_Incidents.csv) here.")
    sys.exit(1)

try:
    df = pd.read_csv(csv_file, encoding='latin-1', low_memory=False)
    print(f"Data loaded from: {csv_file}")
    print(f"Total incidents: {len(df):,}")
    print("Columns:", list(df.columns))
except Exception as e:
    print(f"Failed to read {csv_file}: {e}")
    sys.exit(1)

# -------------------------------------------------
# 2. List of known Islamist-extremist groups
# -------------------------------------------------
islamist_groups = [
    'Taliban', 'Islamic State', 'ISIL', 'ISIS',
    'Al-Qaida', 'Al Qaeda', 'AQAP', 'AQIM',
    'Boko Haram', 'Al-Shabaab', 'Hamas',
    'Hezbollah', 'Hizballah', 'Lashkar-e-Taiba', 'LeT',
    'Jaish-e-Mohammed', 'JEM', 'Abu Sayyaf',
    'Jemaah Islamiyah', 'Jemaah Islamiyyah',
    'Islamic Jihad', 'Harakat ul-Mujahidin',
    'Jaishe-Mohammad'
]

# -------------------------------------------------
# 3. Filter rows that mention any of the groups
# -------------------------------------------------
pattern = '|'.join(islamist_groups)
mask = df['Perpetrator'].astype(str).str.contains(pattern, case=False, na=False, regex=True)
df_filtered = df[mask].copy()

# -------------------------------------------------
# 4. Extract year from the Date column
# -------------------------------------------------
def extract_year(date_str):
    if pd.isna(date_str):
        return None
    txt = str(date_str).strip()
    # Look for a 4-digit year (19xx or 20xx)
    m = re.search(r'\b(19|20)\d{2}\b', txt)
    return int(m.group(0)) if m else None

df_filtered['year'] = df_filtered['Date'].apply(extract_year)
df_filtered = df_filtered[df_filtered['year'] >= 1970].copy()

if df_filtered.empty:
    print("\nWARNING: No incidents matched the group list.")
    print("Top 20 Perpetrators in the whole dataset (for debugging):")
    print(df['Perpetrator'].value_counts().head(20))
    sys.exit(1)

# -------------------------------------------------
# 5. Show which groups / names were actually found
# -------------------------------------------------
found_perpetrators = (
    df_filtered['Perpetrator']
    .astype(str)
    .str.strip()
    .value_counts()
    .head(30)                     # limit to 30 most frequent
)
print("\nGroups / Individual names that matched the filter (top 30):")
for name, cnt in found_perpetrators.items():
    print(f"  • {name}  →  {cnt:,} incident(s)")

# -------------------------------------------------
# 6. Basic statistics
# -------------------------------------------------
total_attacks = len(df_filtered)
print(f"\nTotal attacks attributed to the listed groups (1970-2009): {total_attacks:,}")
print(f"Percentage of all incidents in the database: {total_attacks/len(df)*100:.2f}%")

# ----- by year -----
yearly = df_filtered.groupby('year').size()
print("\nTop 10 years by number of attacks:")
print(yearly.nlargest(10).to_string())

# ----- by country -----
country = df_filtered['Country'].value_counts()
print("\nTop 10 countries by number of attacks:")
print(country.head(10).to_string())

# ----- simple region mapping (optional) -----
region_map = {
    'Iraq':'Middle East', 'Lebanon':'Middle East', 'Israel':'Middle East',
    'Syria':'Middle East', 'Afghanistan':'South Asia', 'Pakistan':'South Asia',
    'India':'South Asia', 'Nigeria':'Sub-Saharan Africa',
    'Somalia':'Sub-Saharan Africa', 'Philippines':'Southeast Asia',
    'Indonesia':'Southeast Asia'
}
df_filtered['region'] = df_filtered['Country'].map(region_map).fillna('Other')
region = df_filtered['region'].value_counts()
print("\nTop 5 regions (simple mapping):")
print(region.head().to_string())

# -------------------------------------------------
# 7. Plotting
# -------------------------------------------------
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Year line chart
yearly.plot(ax=ax1, kind='line', marker='o', linewidth=2, color='tab:red')
ax1.set_title('Attacks by Islamist-extremist groups per year (1970-2009)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of attacks')
ax1.grid(True, alpha=0.3)

# Country bar chart (top 10)
country.head(10).plot(ax=ax2, kind='bar', color='tab:blue', edgecolor='navy')
ax2.set_title('Top 10 countries')
ax2.set_xlabel('Country')
ax2.set_ylabel('Number of attacks')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('terrorism_rand_en.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nChart saved as 'terrorism_rand_en.png'")
print("\nSource: RAND Database of Worldwide Terrorism Incidents (1968-2009)")
print("Note: These numbers refer to extremist groups, not to Muslims in general.")