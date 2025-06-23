import JsonFileManager
import csv
from Utils import Utils
import pandas as pd
from converter import Converter
from et_algo import ET_Algo
from visualizer import Visuazlier

class EtzLib:
       
    """
    Initilize.
    EtzLib = EtzLib()
    Parameters:
    - no paramter just intilize.
    """
       
        
    def __init__(self):
            self.json_manager = JsonFileManager()
            self.key_path = None

            #self.data = self.load_data()
            #self.csv_data = None



    def load_data_json(self):
            return self.json_manager.load_data()

    def save_data_json(self):
            self.json_manager.save_data(self.data)

    def get_value_json(self, key):
            return self.data.get(key)
        

    def set_value_json(self, key, value):
            self.data[key] = value
            # Save the data automatically whenever a value is set
            self.save_data()
        
    #this is for et file only if ET is seprate and task file is seprate. This will be used later for merging. This function will be called two time. one for et and one for task.
    def validate_csv_columns(self, csv_file_path,type):
        """
        Validate that all keys in eyetracking_data or task_data array exist in CSV columns based on the specified type.

        Parameters:
        - csv_file_path (str): The path to the CSV file.
        - type (str): The type of data to validate ("et", "task", or "all").

        Returns:
        - pd.DataFrame or None: The DataFrame if valid, None otherwise.
        # Example CSV and type
        csv_file_path = "path/to/your/file.csv"
        type = "all"  # Replace with "et", "task", or "all"

        # Validate and get DataFrame if valid
        df = my_library.validate_csv_columns(csv_file_path, type)

        if df is not None:
            print(f"CSV for {type} is valid.")
            print(df)
        else:
            print(f"CSV for {type} is not valid.")
        """
        self.key_path = type
        csv_data=Utils.load_csv(csv_file_path)
        if type == "et":
            key_path = "eyetracking_data"
        elif type == "task":
            key_path = "task_data"
        elif type == "all":
            key_path = "all_data"
        else:
            raise ValueError("Invalid type. Supported values are 'et', 'task', or 'all'.")

        json_keys = []
        if isinstance(key_path, list):
            for path in key_path:
                json_keys.extend(Utils.get_json_keys(self.json_manager, "data/your_json_file.json", path))
        else:
            json_keys = Utils.get_json_keys(self.json_manager, "data/your_json_file.json", key_path)

        csv_columns = csv_data[0].keys() if csv_data else []

        is_valid = all(key in csv_columns for key in json_keys)

        if is_valid:
            return pd.DataFrame(csv_data)
        else:
            return None

    
        

    def fill_gaps_with_formula(data):
        """
        fill missing data in et.

        Parameters:
        - et_data: eye-tracking data.
        Returns:
        - dataframe.
        """
        data = Utils.fill_gaps_with_formula(data)
        return data  
                 
    def merge_data(et_data, task_data):
        """
        Merge eye-tracking and task data.

        Parameters:
        - et_data: eye-tracking data.
        - task_data: Task data.

        Returns:
        - merged dataframe.
        """
        data=Utils.merge_data(et_data,task_data)
        return data
    
    def pixels_to_degrees(data):
        """
        convert pixels value to degrees.

        Parameters:
        - value.
        Returns:
        - value.
        """
        data=Converter.pixels_to_degrees(data)
        return data
    
    def normalized_to_pixels(x,y):
        """
        convert normalized value to pixels.

        Parameters:
        -x,y value.
        Returns:
        -x,y value.
        """
        [x,y]=Converter.normalized_to_pixels(x,y)
        return [x,y]
    
    def cartesian_to_normalized(x,y):
        """
        convert cartesian value to normalized.

        Parameters:
        - x,y value.
        Returns:
        -x,y value.
        """
        [x,y]=Converter.cartesian_to_normalized(x,y)
        return [x,y]   
    
    def apply_butter_worth_filter(x,y):
        """
        apply butterworth filter.

        Parameters:
        - x,y value.
        Returns:
        - x,y value.
        """
        [x,y] = ET_Algo.apply_butter_worth(x,y)
        return [x,y]
    
    
    def compute_velocity(x,y,time):
        velo = ET_Algo.compute_velocity(x,y,time)
       
        return velo
        
        
    def compute_gain_x_y_rmse(et_x,et_y,stim_x,stim_y):
        [squared_diff_x_,squared_diff_y,rmse] = ET_Algo.compute_gain_x_y_rmse(et_x,et_y,stim_x,stim_y)    
        return  [squared_diff_x_,squared_diff_y,rmse]
    
    
    def compute_velocity_gain_rmse(et_velocity,target_velocity):
        [squared_diff_velocity,mse_velocity] = ET_Algo.compute_velocity_gain_rmse(et_velocity,target_velocity)
        return  [squared_diff_velocity,mse_velocity]
    
    def compute_latency(et_velocity,time):
        [velocity_threshold,latency_start_time,latency_start] = ET_Algo.compute_latency(et_velocity,time)
        return [velocity_threshold,latency_start_time,latency_start]
    
    
    def compute_saccade_latency_onset(velocity,time):
        saccade_onset_times = ET_Algo.compute_saccade_latency_onset(velocity,time)
        return saccade_onset_times

    def fixation_stability(x,y):
        BCEA = ET_Algo.fixation_stability(x,y)
        return BCEA
    
    def calculate_smooth_pursuit_amplitude(eye_x, eye_y, target_x, target_y):
        amplitude = ET_Algo.calculate_smooth_pursuit_amplitude(eye_x, eye_y, target_x, target_y)
        return amplitude
    
    
    
    ########################################################################################################
    
    #####################################  Visualizations/Graphs  ############################################
    def show_plot_velocity(et_velocity,stim_velocity,time):
        Visuazlier.show_plot_velocity(et_velocity,stim_velocity,time)
        
    def show_plot_gain(time,gain,rmse_value=0,thres=2):
        Visuazlier.show_plot_gain(time,gain,rmse_value=0,thres=2)
        
    def show_plot_accerlation(time,velocity, stim_velocity):
        Visuazlier.show_plot_accerlation(time,velocity, stim_velocity)
        
    def show_plot_rmse_gain(squared_diff_x,squared_diff_y,rmse):
        Visuazlier.show_plot_rmse_gain(squared_diff_x,squared_diff_y,rmse)
    
    def show_plot_rmse_velocity(squared_diff_velocity,mse_velocity):
        Visuazlier.show_plot_rmse_velocity(squared_diff_velocity,mse_velocity)
        
    def plot_relative_position(x, y,time,stem_X,stem_Y,line):
        Visuazlier.plot_relative_position(x, y,time,stem_X,stem_Y,line):   
 # Example usage:







