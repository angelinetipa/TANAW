import pandas as pd

FLEXIBLE_COLUMN_MAP = {
    "Region": ["region", "reg", "regional office"],
    "Division": ["division", "div", "school division"],
    "District": ["district", "school district"],
    "BEIS School ID": ["school id", "beis id", "beis_school_id", "schoolid"],
    "School Name": ["school name", "name of school", "schoolname"],
    "Street Address": ["street address", "address", "school address"],
    "Province": ["province"],
    "Municipality": ["municipality", "city/municipality", "city"],
    "Legislative District": ["legislative district", "leg district"],
    "Barangay": ["barangay", "brgy"],
    "Sector": ["sector"],
    "School Subclassification": ["school subclassification", "subclassification"],
    "School Type": ["school type", "type"],
    "Modified COC": ["modified coc", "mod coc", "coc"],
    "K Male": ["k male", "kindergarten male", "kmale"],
    "K Female": ["k female", "kindergarten female", "kfemale"],
    "G1 Male": ["g1 male", "grade 1 male", "grade1 male"],
    "G1 Female": ["g1 female", "grade 1 female", "grade1 female"],
    "G2 Male": ["g2 male", "grade 2 male", "grade2 male"],
    "G2 Female": ["g2 female", "grade 2 female", "grade2 female"],
    "G3 Male": ["g3 male", "grade 3 male", "grade3 male"],
    "G3 Female": ["g3 female", "grade 3 female", "grade3 female"],
    "G4 Male": ["g4 male", "grade 4 male", "grade4 male"],
    "G4 Female": ["g4 female", "grade 4 female", "grade4 female"],
    "G5 Male": ["g5 male", "grade 5 male", "grade5 male"],
    "G5 Female": ["g5 female", "grade 5 female", "grade5 female"],
    "G6 Male": ["g6 male", "grade 6 male", "grade6 male"],
    "G6 Female": ["g6 female", "grade 6 female", "grade6 female"],
    "Elem NG Male": ["elem ng male", "elementary ng male"],
    "Elem NG Female": ["elem ng female", "elementary ng female"],
    "G7 Male": ["g7 male", "grade 7 male", "grade7 male"],
    "G7 Female": ["g7 female", "grade 7 female", "grade7 female"],
    "G8 Male": ["g8 male", "grade 8 male", "grade8 male"],
    "G8 Female": ["g8 female", "grade 8 female", "grade8 female"],
    "G9 Male": ["g9 male", "grade 9 male", "grade9 male"],
    "G9 Female": ["g9 female", "grade 9 female", "grade9 female"],
    "G10 Male": ["g10 male", "grade 10 male", "grade10 male"],
    "G10 Female": ["g10 female", "grade 10 female", "grade10 female"],
    "JHS NG Male": ["jhs ng male", "junior hs ng male"],
    "JHS NG Female": ["jhs ng female", "junior hs ng female"],
    "G11 ACAD - ABM Male": ["g11 abm male", "grade 11 abm male"],
    "G11 ACAD - ABM Female": ["g11 abm female", "grade 11 abm female"],
    "G11 ACAD - HUMSS Male": ["g11 humss male", "grade 11 humss male"],
    "G11 ACAD - HUMSS Female": ["g11 humss female", "grade 11 humss female"],
    "G11 ACAD STEM Male": ["g11 stem male", "grade 11 stem male"],
    "G11 ACAD STEM Female": ["g11 stem female", "grade 11 stem female"],
    "G11 ACAD GAS Male": ["g11 gas male", "grade 11 gas male"],
    "G11 ACAD GAS Female": ["g11 gas female", "grade 11 gas female"],
    "G11 ACAD PBM Male": ["g11 pbm male", "grade 11 pbm male"],
    "G11 ACAD PBM Female": ["g11 pbm female", "grade 11 pbm female"],
    "G11 TVL Male": ["g11 tvl male", "grade 11 tvl male"],
    "G11 TVL Female": ["g11 tvl female", "grade 11 tvl female"],
    "G11 SPORTS Male": ["g11 sports male", "grade 11 sports male"],
    "G11 SPORTS Female": ["g11 sports female", "grade 11 sports female"],
    "G11 ARTS Male": ["g11 arts male", "grade 11 arts male"],
    "G11 ARTS Female": ["g11 arts female", "grade 11 arts female"],
    "G12 ACAD - ABM Male": ["g12 abm male", "grade 12 abm male"],
    "G12 ACAD - ABM Female": ["g12 abm female", "grade 12 abm female"],
    "G12 ACAD - HUMSS Male": ["g12 humss male", "grade 12 humss male"],
    "G12 ACAD - HUMSS Female": ["g12 humss female", "grade 12 humss female"],
    "G12 ACAD STEM Male": ["g12 stem male", "grade 12 stem male"],
    "G12 ACAD STEM Female": ["g12 stem female", "grade 12 stem female"],
    "G12 ACAD GAS Male": ["g12 gas male", "grade 12 gas male"],
    "G12 ACAD GAS Female": ["g12 gas female", "grade 12 gas female"],
    "G12 ACAD PBM Male": ["g12 pbm male", "grade 12 pbm male"],
    "G12 ACAD PBM Female": ["g12 pbm female", "grade 12 pbm female"],
    "G12 TVL Male": ["g12 tvl male", "grade 12 tvl male"],
    "G12 TVL Female": ["g12 tvl female", "grade 12 tvl female"],
    "G12 SPORTS Male": ["g12 sports male", "grade 12 sports male"],
    "G12 SPORTS Female": ["g12 sports female", "grade 12 sports female"],
    "G12 ARTS Male": ["g12 arts male", "grade 12 arts male"],
    "G12 ARTS Female": ["g12 arts female", "grade 12 arts female"],
}
def read_csv(filepath): 
    df = pd.read_csv(filepath, header=None)
    return df

def detect_header(df, max_scan_rows=10, verbose=False):
    # Detects and sets the correct header row in a DataFrame by scanning the first few rows.

    best_row_idx = None  # Index of the row that will be set as header
    max_valid_cells = 0  # Track the highest number of non-null values found

    # Loop through the first few rows to find the one with most non-null cells
    for i in range(min(len(df), max_scan_rows)):
        non_null_count = df.iloc[i].notnull().sum()  # Count non-null entries in the row
        # Update if this row has more non-null values than the previous best
        if non_null_count > max_valid_cells:
            max_valid_cells = non_null_count
            best_row_idx = i

    # Raise an error if no suitable header row was found
    if best_row_idx is None:
        raise ValueError("Could not detect header row.")
    if verbose:
        print(f"🧠 Best header row detected at index {best_row_idx}: {df.iloc[best_row_idx].tolist()}")

    # Set the best row as the header and drop all rows above it
    df.columns = [str(col) for col in df.iloc[best_row_idx]] # Set new header
    df = df.iloc[best_row_idx + 1:].reset_index(drop=True)  # Drop header row and above, reset index
    return df


def rename_columns(df, alias_map=FLEXIBLE_COLUMN_MAP, verbose=False):
    # Dictionary to store columns that need to be renamed
    renamed_cols = {}

    # Create a lowercase/stripped version of the column names for easier matching
    lower_cols = {str(col).lower().strip(): col for col in df.columns}

    # Loop through the alias map to find matches and rename accordingly
    for standard_col, aliases in alias_map.items():
        found = False  # Flag to track if a match is found for the current standard_col

        # Check each possible alias for the standard column
        for alias in aliases:
            alias_clean = alias.lower().strip()  # Clean alias for comparison

            # If alias is found in DataFrame columns
            if alias_clean in lower_cols:
                original_col = lower_cols[alias_clean]  # Get the actual column name from df
                renamed_cols[original_col] = standard_col  # Map original column to new standard name
                found = True
                break  # Stop checking other aliases once a match is found

        # If no match found and verbose is on, print a warning
        if not found and verbose:
            print(f"⚠️ Not found: '{standard_col}'")

    # Return DataFrame with columns renamed
    return df.rename(columns=renamed_cols)


def validate_columns(df, expected_cols, verbose=False):
    missing = [col for col in expected_cols if col not in df.columns]
    if missing and verbose:
        raise ValueError(f"Missing columns after renaming: {missing}")
       
