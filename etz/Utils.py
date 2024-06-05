import os
import csv
import numpy as np
from converter import Converter

class Utils:
    
    @staticmethod
    def get_json_keys(json_manager, json_file_path, key_path):
        """
        Get the keys from the JSON file based on the specified key path.

        Parameters:
        - json_manager (JsonFileManager): An instance of JsonFileManager.
        - json_file_path (str): The path to the JSON file.
        - key_path (str): The path to the keys in the JSON file.

        Returns:
        - list: A list of keys from the JSON file.
        """
        json_data = json_manager.load_data_from_file(json_file_path)

        keys = json_data
        for key in key_path.split('.'):
            keys = keys.get(key, {})
            if not keys:
                break

        return list(keys.keys())
    
    
    @staticmethod
    def fill_gaps_with_formula(df):
        # Identify the rows where x is 0
        columns_to_process = ['left_x', 'left_y']
        json_data = Converter.json_file()
        json_gap_arr = json_data.get('fill_missing_gap', [])[0]
        json_gap = int(json_gap_arr('max_gap_lenght', 0))
        
        for column_name in columns_to_process:
            # Identify the rows where the specified column is 0
            zero_rows = df[column_name] == 0

            # Create a mask for the first and last consecutive zeros
            first_zero = zero_rows & ~zero_rows.shift(fill_value=False)
            last_zero = zero_rows & ~zero_rows.shift(-1, fill_value=False)

            # Find the indices of the first and last consecutive zeros
            first_zero_indices = first_zero.index[first_zero]
            last_zero_indices = last_zero.index[last_zero]
           
          
            # Loop through consecutive zero groups
            for first_index, last_index in zip(first_zero_indices, last_zero_indices):
                total_time = df.loc[last_index, 'timestamp'] - df.loc[first_index, 'timestamp']

                if total_time < json_gap: 
                    # Fill the gap using the provided formula
                    t1, x1 = df.loc[first_index, ['timestamp', column_name]]
                    t2, x2 = df.loc[last_index, ['timestamp', column_name]]
                    df.loc[first_index + 1:last_index, column_name] = x1 + (df.loc[first_index + 1:last_index, 'timestamp'] - t1) / (t2 - t1) * (x2 - x1)

        return df

    
    @staticmethod
    def load_csv(csv_file_path):
        """
        Load data from a CSV file.

        Parameters:
        - csv_file_path (str): The path to the CSV file.
        -csv_file_path = "path/to/your/file.csv"
        -my_library.load_csv(csv_file_path)



        Returns:
        - list: A list of dictionaries representing the CSV data.
        """
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_data = list(csv_reader)
        return csv_data 
    
    @staticmethod
    def merge_data(et_data,task_data):
        
        cdf=task_data[['task_x','task_y','timestamp']]
        
        #interpolation. task data ---> et data
        interpolated_values_x = np.interp(et_data['timestamp'], cdf['timestamp'], cdf['task_x'])
        interpolated_values_y = np.interp(et_data['timestamp'], cdf['timestamp'], cdf['task_y'])
        et_data['task_x'] = interpolated_values_x
        et_data['task_y'] = interpolated_values_y
        
        return et_data
        