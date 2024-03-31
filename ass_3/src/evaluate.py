import numpy as np
import sys
import os
import json

def r2_score(y_true, y_pred):
    """
    Function to compute R2 score
    """
    numerator = np.sum((y_true - y_pred) ** 2)
    mean_true = np.mean(y_true)
    denominator = np.sum((y_true - mean_true) ** 2)
    return 1 - (numerator / denominator)

def main():
    prepared_dir_path = sys.argv[1]  # Reads ground truths from prepare stage
    computed_dir_path = sys.argv[2]  # Reads computed values from process stage

    # Directory for output of this stage
    evaluated_dir_path = "/home/laog/CS5830_Assignment_3/ass_3/evaluated"

    if not os.path.exists(
        evaluated_dir_path
    ):  # Creates the folder corresponding to the above path
        os.makedirs(evaluated_dir_path)
        print("\nCreated evaluated dir")

    gt_file = prepared_dir_path + "list_of_gt_values.txt"
    computed_file = computed_dir_path + "computed_values.txt"

    gt_values = []
    with open(gt_file, "r") as file:
        lines = file.readlines()
        for line in lines:  # Read the GT output
            line_values = json.loads(line)
            gt_values.append(line_values)

    computed_values = []
    with open(computed_file, "r") as file:
        lines = file.readlines()  # Read the computed output
        for line in lines:
            line_values = json.loads(line)
            computed_values.append(line_values)

    total_scores = []
    for i in range(len(computed_values)):
        csv_based_scores = []
        for j in range(len(computed_values[i])):  # Calculate R2 score between them
            field_wise_r2_score = r2_score(
                np.array(gt_values[i][j]), np.array(computed_values[i][j])
            )
            if field_wise_r2_score >= 0.9:
                print(
                    "Dataset is Consistent for File:",
                    i + 1,
                    ", Field :",
                    j + 1,
                    "with R2 score = %.3f" % field_wise_r2_score,
                )
            else:
                print(
                    "Dataset is Not Consistent for File:",
                    i + 1,
                    ", Field :",
                    j + 1,
                    "with R2 score = %.3f" % field_wise_r2_score,
                )
            csv_based_scores.append(field_wise_r2_score)
        total_scores.append(csv_based_scores)

    with open(evaluated_dir_path + "/" + "evaluation.txt", "w") as f:
        for line in total_scores:
            f.write(f"{line}\n")  # Output of Evaluate stage
    print("\nCreated evaluation.txt !")


if __name__ == "__main__":
    main()
