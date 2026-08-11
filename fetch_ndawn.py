import pandas as pd
from datetime import datetime
import os

# Official NDAWN live data stream URL (Current hourly/5-min observations)
URL = "https://nodak.edu"

try:
    # NDAWN API returns CSV text; skiprows handles the metadata headers if present
    df = pd.read_html("https://nodak.edu")[0]
    
    # Clean up column names by joining multi-index levels if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns]

    # Add a data fetch timestamp column
    df['Fetched_At_UTC'] = datetime.utcnow().isoformat()
    
    # Save the data to a file inside the repo
    # Option A: Overwrite a single file to keep it updated
    filename = "ndawn_latest_conditions.csv"
    
    # Option B (Alternative): Append or create unique history files if needed
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")

except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)
