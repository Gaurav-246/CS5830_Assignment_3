import pandas as pd
import sys
from os import listdir
import os

def valid_fields(csv_file):
    df = pd.read_csv(csv_file, dtype='unicode')
    daily_col_names = []
    monthly_col_names = []
    for column_name in df.columns:
        if 'Daily' in column_name:
            daily_col_names.append(column_name[5:])       # Store Column names with Daily data
        if 'Monthly' in column_name:
            monthly_col_names.append(column_name[7:])     # Store Column names with Monthly data

    common_col_names = []
    for i in daily_col_names:
        for j in monthly_col_names:
            if i==j:                                      # Store common column names b/w daily and monthly
                common_col_names.append(i)                # A field is valid only if it is present in both 'Daily' and 'Monthly' columns
    print('Common Column names for file',csv_file[-15:],' found are : ', common_col_names)
    return common_col_names

def ground_truth(csv_file, field_names):
    df = pd.read_csv(csv_file, dtype='unicode')           
    gt_values = []
    for field in field_names:
        non_null_values = df[field].notnull()             # Finds the required values
        ground_truth_value = df[field][non_null_values].to_numpy()    # Converting from pandas DataFrame to numpy array
        gt_values.append(ground_truth_value)
    print('Ground Truth values extracted for file',csv_file[-15:],' !')
    return gt_values                                      # Returns a list of GTs for each validfield name

def main():
    data_dir_path = sys.argv[1]
    filenames = listdir(data_dir_path)                    # Lists all csv files
    csv_files = [data_dir_path + filename for filename in filenames if filename.endswith(".csv")]

    prepared_dir_path = '/home/laog/CS5830_Assignment_3/ass_3/prepared'

    if not os.path.exists(prepared_dir_path) :           # Creates the folder corresponding to the above path
        os.makedirs(prepared_dir_path)
        print('\nCreated prepared dir\n')

    list_of_valid_fields = []
    list_of_gt_values = []
    for csv_file in csv_files:
        common_field_names = valid_fields(csv_file)
        list_of_valid_fields.append(common_field_names)   # Get list of fields   
        list_of_gt_values.append(ground_truth(csv_file, ['Monthly'+item for item in common_field_names]))
    
    with open(prepared_dir_path + '/' + 'list_of_fields.txt','w') as f:
        for line in list_of_valid_fields:
            f.write(f"{line}\n")
    print('\nCreated list_of_fields.txt !')

    with open(prepared_dir_path + '/' + 'list_of_gt_values.txt','w') as f:
        for line in list_of_gt_values:
            f.write(f"{line}\n")
    print('Created list_of_gt_values.txt !\n')

if __name__ == "__main__":
    main()