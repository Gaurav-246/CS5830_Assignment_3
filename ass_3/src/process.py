import pandas as pd
import numpy as np
import sys
from os import listdir
import os

def compute_avg(csv_file, field_names):
    """
    Given a csv file and the required field names, 
    this function computes the monthly averages of the fields
    """
    df = pd.read_csv(csv_file, dtype="unicode")
    daily_field_names = ["Daily" + item for item in field_names]
    monthly_field_names = ["Monthly" + item for item in field_names]
    df = df[
        daily_field_names + monthly_field_names
    ]  # This DF contains just the required fields
    df = df.apply(
        pd.to_numeric, errors="coerce"
    )  # This DF changes string values of 'nan' to NaN

    avg_values_for_all_fields = []

    for i in range(len(field_names)):
        indices = [0]
        ground_truth_indices = df[monthly_field_names[i]][
            df[monthly_field_names[i]].notnull()
        ].index  # Indices of monthly GT values
        indices += [index for index in ground_truth_indices]
        avg_value_for_this_field = []

        for j in range(
            len(indices) - 1
        ):  # Computes monthly avg from previous month GT index to current month GT index
            avg_value_for_this_field.append(
                np.nanmean(df[daily_field_names][indices[j] : indices[j + 1]])
            )

        avg_values_for_all_fields.append(avg_value_for_this_field)

    return avg_values_for_all_fields


def main():
    data_dir_path = sys.argv[1]  # Read data from output of download stage
    prepared_dir_path = sys.argv[2]  # Read fields from output of prepare stage

    # Directory for output of this stage
    computed_dir_path = "/home/laog/CS5830_Assignment_3/ass_3/computed"

    if not os.path.exists(
        computed_dir_path
    ):  # Creates the folder corresponding to the above path
        os.makedirs(computed_dir_path)
        print("\nCreated computed dir")

    filenames = listdir(data_dir_path)  # Lists all csv files
    csv_files = [
        data_dir_path + filename for filename in filenames if filename.endswith(".csv")
    ]
    fields_file = prepared_dir_path + "list_of_fields.txt"

    with open(fields_file, "r") as file:
        lines = file.readlines()  # Read lines
        list_of_fields = []
        for line in lines:
            line = line.strip()[1:-1]  # Remove square brackets
            items = line.split(",")
            items = [
                item.strip().strip("'\"") for item in items
            ]  # Remove quotes and whitespace
            list_of_fields.append(items)

    computed_values = []
    for i in range(len(csv_files)):
        computed_values.append(compute_avg(csv_files[i], list_of_fields[i]))

    with open(computed_dir_path + "/" + "computed_values.txt", "w") as f:
        for line in computed_values:
            f.write(
                f"{line}\n"
            )  # Output the computed values as output to the evaluate stage
    print("Created computed_values.txt !\n")


if __name__ == "__main__":
    main()
