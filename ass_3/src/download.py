import requests
from bs4 import BeautifulSoup
import random
import os
import pandas as pd
import yaml

#########################################################
# FUNCTION TO RETURN ALL CSV FILE NAMES FOR A GIVEN YEAR
#########################################################
def extract_csv_urls(base_url, year):                                   
    
    url = base_url + str(year) + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csv_urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.csv'):
            csv_urls.append(url + href)
    print("Returning all CSV file names from year ", year, "!")
    return csv_urls                                           # Used for sampling and finding the right files 

##########################################
# FUNCTION TO SAMPLE AND DOWNLOAD DATASET
##########################################
def download_dataset(n_loc, csv_urls, download_path):                   

    random_csv_urls = random.sample(csv_urls, n_loc)          # Samples n_loc files from the total list
    i=0
    filenames = []
    for csv_url in random_csv_urls:
        filename = os.path.join(download_path, csv_url.split('/')[-1])
        filenames.append(filename)
        print('Downloading file ', i+1,' : ', filename[-15:]) # -15 represents the last 15 characters of the path, i.e, the file name
        response = requests.get(csv_url)
        with open(filename, 'wb') as f:                       # Downloads the files to the download_path
            f.write(response.content)        
        i = i+1          
    return filenames                

########################################
# FUNCTION TO VALIDATE DOWNLOADED FILES
########################################
def validate_dataset(filenames):                                        

    valid_csv_files = []
    for filename in filenames:
        df = pd.read_csv(filename, dtype='unicode')                            # Read CSV
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
                    common_col_names.append(i)                # Averages make sense only with common column names
        
        for common_col in common_col_names:
            if df['Daily'+common_col].count()!=0 and df['Monthly'+common_col].count()!=0:       # Store only valid csv files
                print('The file ', filename[-15:], ' is valid with daily and monthly data existing for the column : ', common_col)
                valid_csv_files.append(filename)              # -15 represents the last 15 characters of the path, i.e, the file name
            else:
                print('The file ', filename[-15:], ' is invalid')
                os.remove(filename)                                                             # Delete the invlid csv files
                print('File ', filename[-15:], 'deleted')

    print('\nSampled ', len(filenames), 'files', )
    print('Number of valid files : ', len(valid_csv_files))
    return valid_csv_files

#########################################################################
#                          MAIN FUNCTION
#########################################################################
def main():
    params = yaml.safe_load(open("/home/laog/CS5830_Assignment_3/params.yaml"))["download"]
    
    year = params["year"]
    n_loc = params["n_loc"]
    base_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/'
    csv_download_path = '/home/laog/CS5830_Assignment_3/ass_3/data'    # Path for downloading CSVs
    all_csv_urls = extract_csv_urls(base_url, year)                                 

    num_of_valid_files = 0
    final_valid_files = []
    if not os.path.exists (csv_download_path) :                 # Creates the folder corresponding to the above path
        os.makedirs(csv_download_path)
        print('\nCreated data dir\n')

    sample_count = 0
    valid_count = 0
    while num_of_valid_files < n_loc:                           # Keep sampling till you get the required number of valid files
        
        sampled_files = download_dataset(n_loc, all_csv_urls, csv_download_path)
        valid_files = validate_dataset(sampled_files)
        sample_count+=len(sampled_files)
        valid_count+=len(valid_files)
        print('Totally sampled ',sample_count,'files so far')
        print('Total number of Valid files so far : ',valid_count,'\n')
        final_valid_files.append(valid_files)
        num_of_valid_files += len(valid_files)
    
    if num_of_valid_files > n_loc:                              # Don't consider any excess files; Ex: Say n_loc = 5, and you get 2 valid files per sampling, 
        excess_num_of_files = num_of_valid_files - n_loc        # then you end up with 6 valid files by the 3rd sampling. Don't consider the last file.
        print('Excess number of valid files : ', excess_num_of_files)
        print('Deleting excess files : ')
        for i in range(excess_num_of_files):
            excess_file = final_valid_files[n_loc+i]
            os.remove(csv_download_path + '/' + excess_file)                                                            
            print('File ', excess_file, 'deleted')
        final_valid_files = final_valid_files[:len(final_valid_files) - excess_num_of_files]

if __name__ == "__main__":
    main()