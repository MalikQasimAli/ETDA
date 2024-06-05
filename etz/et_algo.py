import math
import numpy as np
#from python_scripts import *
from scipy.signal import butter, filtfilt
from math import atan2, degrees, isnan, sqrt
from converter import Converter

class ET_Algo:
    
    @staticmethod
    def apply_butter_worth(x,y):
      # Butterworth filter parameters
        json_data = Converter.json_file()
        cutoff_frequency = int(json_data.get('bw_cuttoff_freq', 0))  # Cutoff frequency in Hz
        nyquist_frequency = 0.5 * 90  # Nyquist frequency is half of the sampling rate
        order = 4  # Filter order
            # Design Butterworth filter
        b, a = butter(N=order, Wn=cutoff_frequency/nyquist_frequency, btype='low')

        # Apply Butterworth filter using filtfilt
        x = filtfilt(b, a, x)
        y = filtfilt(b, a, y)

        return x,y
    
    
        """ Velocity calculation """
    @staticmethod    
    def euclidean_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    @staticmethod
    def compute_velocity(x,y,time):
        #distances_et = [ET_Algo.euclidean_distance(x[i-1], y[i-1], x[i], y[i]) for i in range(1, len(x))]
        #velocity = [distance / time[i] for i, distance in enumerate(distances_et)]
        #time_data=time[:-1]
        delta_t = np.diff(time)
        displacement = np.sqrt((np.diff(x))**2 + (np.diff(y))**2)

        velocity = displacement/delta_t
        return velocity

    """ END  Velocity calculation """

    @staticmethod
    def compute_gain_x_y_rmse(et_x,et_y,stim_x,stim_y):
        # type left, right, average.
        # Calculate squared differences
        # Get valid indices for eye tracking data
        # Apply valid indices to eye tracking data
        #x_valid = np.nan_to_num(x, nan=0)
        #y_valid = np.nan_to_num(y, nan=0)

        # Keep target data as is
        #target_x = np.array(target_x)
        #target_y = np.array(target_y)


        # Calculate squared differences and RMSE using valid eye tracking data
        squared_diff_x = (et_x - stim_x)**2
        squared_diff_y = (et_y - stim_y)**2
        
        rmse = np.sqrt(np.mean(squared_diff_x + squared_diff_y))
    

        # Convert squared differences and RMSE to degrees
       # squared_diff_x_deg = ET_instance.pix2angle(squared_diff_x)
       # squared_diff_y_deg = ET_instance.pix2angle(squared_diff_y)
       # rmse_deg = ET_instance.pix2angle(rmse)
    
        squared_diff_x_deg_nonan = squared_diff_x[~np.isnan(squared_diff_x)]
        squared_diff_y_deg_nonan = squared_diff_y[~np.isnan(squared_diff_y)]
        rmse_deg_nonan = rmse[~np.isnan(rmse)]

    # Graph_Visualizer.show_plot_rmse_gain(squared_diff_x_deg_nonan,squared_diff_y_deg_nonan,rmse_deg_nonan)
        return (squared_diff_x_deg_nonan,squared_diff_y_deg_nonan,rmse_deg_nonan)
    
    
    @staticmethod
    def compute_velocity_gain_rmse(et_velocity,target_velocity):
        # Assuming you have velocity data in lists
        #eye_tracking_velocity = et_velocity
        #target_velocity = target_velocity

        # Convert lists to NumPy arrays for easier calculations
        eye_tracking_velocity = np.array(et_velocity)
        target_velocity = np.array(target_velocity)

        # Calculate squared differences and MSE
        squared_diff_velocity = (eye_tracking_velocity - target_velocity)**2
        #mse_velocity = np.mean(squared_diff_velocity)
        mse_velocity = np.sqrt(np.mean(squared_diff_velocity))

        #mse_velocity=ET_instance.pix2angle(mse_velocity)
        #squared_diff_velocity=ET_instance.pix2angle(squared_diff_velocity)
        #eye_tracking_velocity=ET_instance.pix2angle(eye_tracking_velocity)
        #target_velocity=ET_instance.pix2angle(target_velocity)

        #Graph_Visualizer.show_plot_rmse_velocity(squared_diff_velocity,mse_velocity)
        return (squared_diff_velocity,mse_velocity)
    
    
    """ Calculate and show latency """
    @staticmethod    
    def compute_latency(et_velocity,time):
        
        # calculating latency using velocity threshold
        # Plot eye tracking data and velocity
        json_data = Converter.json_file()
        json_gaze_arr = json_data.get('gaze_metrics', [])[0]
        velocity_threshold = int(json_gaze_arr('latency_velocity_threshold', 0))
        #velocity_threshold=5
        # Set velocity threshold (adjust as needed)
        
    # Find the first point of velocity
        initial_velocity = et_velocity[0]
    
        latency_start = None
        latency_start_time = None

        # Iterate through the rest of the velocity points
        for i in range(1, len(et_velocity)):
            # Calculate the difference with the initial velocity
            velocity_difference = abs(et_velocity[i] - initial_velocity)

            # Check if the difference is greater or equal to the threshold
            if velocity_difference >= velocity_threshold:
                # Mark this point as latency start
                latency_start = et_velocity[i]
                latency_start_time = time[i]
           #     print('latency_start_time',latency_start_time)
                break  # Stop checking further points

        if latency_start_time is not None:
           # print(f'Latency Start: Time {latency_start_time}')
        # Graph_Visualizer.show_latency(velocity,stim_velocity,time,velocity_threshold,latency_start_time)
            return (velocity_threshold,latency_start_time,latency_start)
        
        else:
           # print('No latency detected.')
            return (velocity_threshold,latency_start_time,latency_start)
        
        
    @staticmethod    
    def compute_saccade_latency_onset(velocity,time):
        # Initialize saccade onset list
        saccade_onset_times  = []
        # Define thresholds
        
        json_data = Converter.json_file()
        json_gaze_arr = json_data.get('gaze_metrics', [])[0]
        velocity_threshold = int(json_gaze_arr('saccade_latency_velocity', 0)) 
       # velocity_threshold = 20  # in degrees per second
        time_threshold = int(json_gaze_arr('saccade_latency_time_threshold', 0)) 
       
        #time_threshold = 32  # in milliseconds

        velocity_bol=False
        time_bol=True
        start_time=0
        end_time=0
        # Iterate through the velocity and time lists
        for i in range(len(velocity)):
            # Check if velocity is greater than the threshold
            if velocity[i] >= velocity_threshold:
                velocity_bol=True
                if(time_bol):
                    start_time= time[i]
                    time_bol=False
            elif (velocity[i] < velocity_threshold):
                if(velocity_bol):
                    velocity_bol=False
                    time_bol=True
                    end_time=time[i]
                  #  print("end time",end_time)
                    total_time=end_time-start_time
                #  print("total time:",total_time)
                    if total_time >= time_threshold:
                        saccade_onset_times.append(total_time)

        return saccade_onset_times
    
    
    @staticmethod  
    def fixation_stability(x,y):

        sigma_H = np.std(x)
        sigma_V = np.std(y)
        rho = np.corrcoef(x, y)[0, 1]

        # Set a constant multiplier (you may need to adjust this based on your needs)
        k = 1.96

        # Calculate BCEA
        BCEA = k * np.pi * sigma_H * sigma_V * np.sqrt(1 - rho**2)

        #print(f"BCEA: {BCEA:.2f} arcminutes²")
        return BCEA
    
    @staticmethod  
    def calculate_smooth_pursuit_amplitude(eye_x, eye_y, target_x, target_y):
        # Calculate the deviation in x and y directions
        deviation_x = eye_x - target_x
        deviation_y = eye_y - target_y
        # Calculate the amplitude using the Pythagorean theorem
        amplitude = np.sqrt(deviation_x**2 + deviation_y**2)
        return amplitude  
    
    
    
    
    
    