import numpy as np
import sys
import os
import json

def r2_score(y_true, y_pred):
    numerator = np.sum((y_true - y_pred)**2)
    mean_true = np.mean(y_true)
    denominator = np.sum((y_true-mean_true)**2)
    return 1 - (numerator/denominator)

def main():
    prepared_dir_path = sys.argv[1]
    computed_dir_path = sys.argv[2]
    evaluated_dir_path = '/home/laog/CS5830_Assignment_3/ass_3/evaluated'

    if not os.path.exists(evaluated_dir_path) :           # Creates the folder corresponding to the above path
        os.makedirs(evaluated_dir_path)
        print('\nCreated evaluated dir')
    
    gt_file = prepared_dir_path + 'list_of_gt_values.txt'
    computed_file = computed_dir_path + 'computed_values.txt'

    gt_values = []
    with open(gt_file, 'r') as file:                        
        lines = file.readlines()
        for line in lines:
            line_values = json.loads(line)
            gt_values.append(line_values)

    computed_values = []
    with open(computed_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_values = json.loads(line)
            computed_values.append(line_values)
    
    total_scores = []
    for i in range(len(computed_values)):
        csv_based_scores = []
        for j in range(len(computed_values[i])):
            field_wise_r2_score = r2_score(np.array(gt_values[i][j]), np.array(computed_values[i][j]))
            csv_based_scores.append(field_wise_r2_score)
        total_scores.append(csv_based_scores)
    
    with open(evaluated_dir_path + '/' + 'evaluation.txt','w') as f:
        for line in total_scores:
            f.write(f"{line}\n")
    print('\nCreated evaluation.txt !')

if __name__ == "__main__":
    main()