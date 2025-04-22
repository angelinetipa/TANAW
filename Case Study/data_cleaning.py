import os
import pandas as pd
from datetime import datetime

def clean_data(df):
    # Create a directory named 'cleaned_files' in the current file's location
    cleaned_files_directory = os.path.join(os.path.dirname(__file__), 'cleaned_files')
    os.makedirs(cleaned_files_directory, exist_ok=True)

    # Convert applicable values to numeric; leave others unchanged
    df_cleaned = df.apply(pd.to_numeric, errors='ignore')

    # Dictionary to standardize common abbreviations and terms
    special_cases = {
        r'\bES\b': 'ELEMENTARY SCHOOL',
        'E/S': 'ELEMENTARY SCHOOL',
        r'\bELEM.\b': 'ELEMENTARY SCHOOL',
        r'\bNHS\b': 'NATIONAL HIGH SCHOOL',
        r'\bHS\b': 'HIGH SCHOOL',
        r'\bCES\b': 'CENTRAL ELEMENTARY SCHOOL',
        r'\bSCH.\b': 'SCHOOL',
        'Incorporated': 'INC.',
        r'\bMEM.\b': 'MEMORIAL',
        r'\bCS\b': 'CENTRAL SCHOOL',
        r'\bPS\b': 'PRIMARY SCHOOL',
        'P/S': 'PRIMARY SCHOOL',
        r'\bLC\b': 'LEARNING CENTER',
        'BARANGAY': 'BRGY. ',
        'POBLACION': 'POB. ',
        'STREET': 'ST. ',
        'BUILDING': 'BLDG. ',
        'BLOCK': 'BLK. ',
        'PUROK': 'PRK. ',
        'AVENUE': 'AVE. ',
        'ROAD': 'RD. ',
        'PACKAGE': 'PKG. ',
        'PHASE': 'PH. ',
        r'\s*,\s*': ', ',  # Replace extra spaces around commas
        r'\s{2,}': ' '     # Replace multiple spaces with a single space
    }

    # Columns to clean and format (remove symbols, standardize text)
    columns_to_format = [
        'Region', 'Division', 'District', 'BEIS School ID', 'School Name',
        'Street Address', 'Province', 'Municipality', 'Legislative District',
        'Barangay', 'Sector', 'School Subclassification', 'School Type', 'Modified COC']
    df_cleaned[columns_to_format] = df_cleaned[columns_to_format].astype(str).apply(
        lambda x: x.str.replace('#', '', regex=False)  # Remove '#' symbol
                    .str.replace(r'^[-:]', '', regex=True)  # Remove leading dashes or colons
                    .str.strip()  # Trim leading/trailing whitespace
                    .str.upper()  # Convert to uppercase
                    .replace(special_cases, regex=True)  # Apply standard replacements
    )

    # Replace invalid, missing, or junk values with 'UNKNOWN' for location-specific fields
    df_cleaned[columns_to_format] = (
        df_cleaned[columns_to_format]
        .replace(['N/A', 'N.A.', 'N / A', 'NA', 'NONE', 'NULL', 'NOT APPLICABLE', '', '0', '_', '=', '.', '-----'], pd.NA)
        .replace(r'^[\s\W_]+$', pd.NA, regex=True)  # Replace values that are just symbols or whitespace
        .fillna("UNKNOWN")
    )

    # Define non-enrollment-related columns (used to filter which ones contain actual enrollment data)
    non_enrollment_cols = [
        'Region', 'Division', 'District', 'BEIS School ID', 'School Name',
        'Street Address', 'Province', 'Municipality', 'Legislative District',
        'Barangay', 'Sector', 'School Subclassification', 'School Type', 'Modified COC'
    ]

    # Identify columns that likely contain enrollment numbers (i.e., not in the list above)
    enrollment_cols = [col for col in df_cleaned.columns if col not in non_enrollment_cols]
    max_threshold = 5000  # Max plausible number for enrollment counts

    # Filter out rows with unrealistic data:
    unrealistic_data = df_cleaned[(
        df_cleaned[enrollment_cols] < 0).any(axis=1) |            # Negative values
        (df_cleaned[enrollment_cols] % 1 != 0).any(axis=1) |      # Decimal values (should be whole numbers)
        (df_cleaned[enrollment_cols] > max_threshold).any(axis=1) # Extremely high numbers
    ]

    # Drop unrealistic rows from the cleaned DataFrame
    df_cleaned = df_cleaned.drop(unrealistic_data.index)

    # Generate filename with current timestamp
    cleaned_filename = f"Cleaned_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    cleaned_path = os.path.join(cleaned_files_directory, cleaned_filename)

    # Save cleaned data to CSV if it's a valid DataFrame
    if isinstance(df_cleaned, pd.DataFrame):
        df_cleaned.to_csv(cleaned_path, index=False)
        return cleaned_path  # Return the file path of the saved cleaned data
    else:
        raise ValueError("DataFrame was not cleaned properly.")
