import pandas as pd
import os

def read_data_from_subfolders(base_dir):
    combined_data = pd.DataFrame()

    # Adjusted for 16 columns
    column_names = [
        'Elapsed Time', 'Level Name', 'User Track', 'empty', 'Player Body Position X', 
        'Player Body Position Y', 'Player Body Position Z', 'Player Body Rotation X', 
        'Player Body Rotation Y', 'Player Body Rotation Z', 'Player Body Rotation W',
        'Player Head Rotation X', 'Player Head Rotation Y', 'Player Head Rotation Z', 
        'Player Head Rotation W', 'Unknown'  # Added an 'Unknown' for the unidentified 16th column
    ]

    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path):
            for participant in os.listdir(category_path):
                participant_path = os.path.join(category_path, participant)
                if os.path.isdir(participant_path):
                    for condition in ['Immersive', 'Non-Immersive']:
                        condition_path = os.path.join(participant_path, condition)
                        if os.path.isdir(condition_path):
                            for data_file in os.listdir(condition_path):
                                file_path = os.path.join(condition_path, data_file)
                                if file_path.endswith('tracking-data.csv') and os.path.getsize(file_path) > 0:
                                    df = pd.read_csv(file_path, header=None)
                                    if df.shape[1] == 16:  # Now expecting 16 columns
                                        df.columns = column_names
                                        if 'empty' in df.columns:
                                            df.drop(columns=['empty'], errors='ignore', inplace=True)  # Assuming 'empty' is still not needed
                                        df['Category'] = category
                                        df['Participant'] = participant
                                        df['Condition'] = condition
                                        combined_data = pd.concat([combined_data, df], ignore_index=True)
                                    else:
                                        print(f"Column mismatch in file: {file_path}, found {df.shape[1]} columns, expected 16.")
                                else:
                                    print(f"Skipped empty or invalid file: {file_path}")

    return combined_data

base_directory = 'D:\\github\\Identification\\Data'
all_data = read_data_from_subfolders(base_directory)
if all_data.empty:
    print("No data loaded. DataFrame is empty.")
else:
    all_data.to_csv('combined_data.csv', index=False)
    print("DataFrame saved to combined_data.csv")
    print(all_data.head())
