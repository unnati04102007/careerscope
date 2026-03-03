import pandas as pd
import os

def load_colleges_data():
    """
    Loads and cleans the college dataset.
    Returns a list of dictionaries.
    """
    # Adjust path relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'colleges.csv')
    
    if not os.path.exists(file_path):
        print(f"Dataset not found at: {file_path}")
        return []

    try:
        df = pd.read_csv(file_path)
        
        # Clean Data
        # 1. Handle Missing Values
        df = df.fillna({
            'Rating': 0,
            'Placement': 0,
            'Infrastructure': 0,
            'Academic': 0,
            'UG_fee': '0',
            'PG_fee': '0'
        })

        # 2. Convert Fees to Numeric
        # Remove commas and convert to int
        def clean_fee(fee):
            if isinstance(fee, str):
                fee = fee.replace(',', '').replace('--', '0')
                try:
                    return int(fee)
                except ValueError:
                    return 0
            return 0 if pd.isna(fee) else fee

        df['UG_fee'] = df['UG_fee'].apply(clean_fee)
        df['PG_fee'] = df['PG_fee'].apply(clean_fee)

        # 3. Clean Ratings/Scores (Ensure they are floats)
        cols_to_float = ['Rating', 'Placement', 'Infrastructure', 'Academic']
        for col in cols_to_float:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 4. Convert to Dictionary
        colleges = df.to_dict(orient='records')
        return colleges

    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []
