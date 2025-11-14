# Islamist-Extremist Terrorism Statistics (RAND Database)

A simple Python tool that analyzes the **RAND Database of Worldwide Terrorism Incidents (1968–2009)** and shows:

- Total number of attacks attributed to known Islamist-extremist groups  
- Exact group names / individual perpetrators found in the data  
- Top years, countries and regions  
- Visual charts (saved as PNG)

> **Important disclaimer**  
> This project analyzes incidents committed by **extremist organizations**, not by Muslims in general. The vast majority of Muslims (over 99.9 %) condemn terrorism. Most victims of these attacks are themselves Muslim.

## Data source

[RAND Database of Worldwide Terrorism Incidents](https://www.rand.org/nsrd/projects/terrorism-incidents.html)  
Direct download: https://www.rand.org/nsrd/projects/terrorism-incidents/download.html  
File used: `RAND_Database_of_Worldwide_Terrorism_Incidents.csv` (≈40 000 incidents, 1968–2009)

## Features

- Automatic detection of the CSV file (no manual renaming needed)  
- Case-insensitive search for dozens of known Islamist-extremist groups  
- Lists **all matching group / individual names** with incident counts  
- Extracts year from the `Date` column (robust regex)  
- Simple region mapping (Middle East, South Asia, etc.)  
- Two clear charts (attacks per year + top countries)  
- Fully in English, ready to run

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/islamist-terrorism-rand-analysis.git
cd islamist-terrorism-rand-analysis

# 2. Download the data
#    Open the link above → click "Download" → unzip → 
#    place RAND_Database_of_Worldwide_Terrorism_Incidents.csv in this folder

# 3. Install dependencies
pip install pandas matplotlib

# 4. Run the script
python terrorism_rand_en.py
