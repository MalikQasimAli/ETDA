from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
matplotlib.rcParams['figure.figsize'] = [20, 10]
#import analyzer
#import et_data_handler
#import idt_fixation
#import ivt_fixation
#from python_scripts.Ivt_fix_class import Ivt_fix_class
from scipy.signal import butter, lfilter, freqz
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot
#from python_scripts.Utility_package import utility
import statistics
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error 
from scipy.signal import butter, filtfilt
from sklearn.metrics import roc_curve, auc
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import seaborn as sns
from .converter import pixels_to_degrees, pix2angle
import io

class Visuazlier:

  def show_transformation():
    #data = pd.read_csv("D:/Work/Framework_ET/Framework_ET/python_scripts/Utility_package/circle_transformation.csv") #circle,  
    # Try specifying the encoding explicitly
      file_path = "D:/Work/Framework_ET/Framework_ET/python_scripts/Utility_package/circle_transformation.csv"

          # Open the file with utf-8 encoding and errors='replace'
      with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
          # Read the content of the file
          file_content = file.read()

      # Use pd.read_csv on the file content
      data = pd.read_csv(io.StringIO(file_content))
      df=  data[['StimX','StimY','EtX','EtY','StimNormX','StimNormY']]

      fig = plt.figure(figsize=(15, 6))
      # Create a horizontal layout of two subplots
      

      plt.subplot(1, 3, 1)
      plt.scatter(data['StimX'], data['StimY'], label='Cartesian Coordinate Data', color='black', marker='x')

      # Set title
      plt.title('Cartesian Coordinate Data', color='black')

      # Set aspect ratio to 'equal' to ensure a square plot
      plt.gca().set_aspect('equal', adjustable='box')

      # Set symmetric limits for the x and y axes
      axes_limit = 4.5
      plt.xlim(-axes_limit, axes_limit)
      plt.ylim(-axes_limit, axes_limit)
      plt.xlabel('X-axis')
      plt.ylabel('Y-axis')

      # Display Cartesian coordinate grid centered at (0,0)
      plt.grid(True, which='both', linestyle='--', linewidth=0.2, color='gray', alpha=0.5)

      # Set spines positions
      plt.gca().spines['left'].set_position('zero')
      plt.gca().spines['right'].set_color('none')
      plt.gca().spines['bottom'].set_position('zero')
      plt.gca().spines['top'].set_color('none')

      # Remove ticks from the top and right edges
    # plt.gca().xaxis.set_ticks_position('bottom')
      plt.gca().yaxis.set_ticks_position('left')
      plt.text(0.5, -0.15, 'A', transform=plt.gca().transAxes, fontsize=16, fontweight='bold', va='top', ha='center')

      # Display legend
      #plt.legend()

      plt.subplot(1, 3, 2)
      plt.scatter(data['StimNormX'], data['StimNormY'], label='Normalized Coordinate Data', color='black', marker='x')
      plt.title('Normalized Coordinate Data', color='black')
      
      plt.grid(True, which='both', linestyle='--', linewidth=0.2, color='gray', alpha=0.5)
    # plt.legend()
      plt.text(0.5, -0.15, 'B', transform=plt.gca().transAxes, fontsize=16, fontweight='bold', va='top', ha='center')
      plt.xlabel('X-axis')
      plt.ylabel('Y-axis')

      plt.subplot(1, 3, 3)
      # Scatter plot for 'Target Data' with black 'x' markers
  

      # Scatter plot for 'Eye-tracking Data' with black 'o' markers
      filtered_x = data[data['EtY'] <= 1]
      #filtered_y = data[data['EtY'] <= 1]

    
      plt.scatter(filtered_x['EtX'], filtered_x['EtY'], label='Eye-tracking Data', color='gray', marker='o',alpha=0.7)
      plt.scatter(data['StimNormX'], data['StimNormY'], label='Target Data', color='black', marker='x')

      plt.title('Normalized Coordinate Data', color='black')
      #plt.xticks(np.arange(0, 1, 0.4))

      #plt.yticks(np.arange(0, 1, 0.4))
      # Add grid
      plt.grid(True, which='both', linestyle='--', linewidth=0.2, color='gray', alpha=0.5)
      plt.legend()
      plt.text(0.5, -0.15, 'C', transform=plt.gca().transAxes, fontsize=16, fontweight='bold', va='top', ha='center')
      plt.xlabel('X-axis')
      plt.ylabel('Y-axis')
      plt.tight_layout()  # Adjust layout to prevent overlapping 
      
      plt.savefig('transformation_img.png', dpi=400, bbox_inches='tight')
      plt.show()
  
  @staticmethod
  def show_heatmap_et_target(etx,ety,stmx,stmy):
      sns.kdeplot(x=etx, y=ety, cmap='viridis', fill=True, thresh=0, levels=100)
      plt.scatter(stmx,stmy,label='Target data')
      plt.title('Eye Tracking Heatmap (KDE)')
      plt.xlabel('X-axis')
      plt.ylabel('Y-axis')
    
      plt.legend()
      plt.show()

  @staticmethod
  def show_all_group(x,y,stem_X,stem_Y,time,et_velocity,stem_velocity):
            # Plot eye tracking data
          # Plot eye tracking data
      plt.subplot(4, 1, 1)
      plt.scatter(x, y, label='Eye Tracking Data', color='dodgerblue', marker='x')
      plt.scatter(stem_X, stem_Y, label='Target Data', color='firebrick', marker='o')
      plt.xlabel('Time (s)')
      plt.ylabel('Position')
      plt.title('Eye Tracking Data - Scatter plot')
      plt.grid(True)
      plt.legend()


      plt.subplot(4, 1, 2)
      plt.plot(time, x,  label='Eye X', color='skyblue',linewidth=2.0)
      plt.plot(time, y,  label='Eye Y', color='cornflowerblue',linewidth=2.0)
      plt.plot(time, stem_X,  label='Target X', color='red',linewidth=2.0)
      plt.plot(time, stem_Y,  label='Target Y', color='coral',linewidth=2.0)
      plt.xlabel('Time (s)')
      plt.ylabel('Position')
      plt.title('Eye Tracking Data - Line plot')
      plt.grid(True)
      plt.legend()

      # Plot of eye tracking velocity
      plt.subplot(4,1,3)
      #plt.plot(time_data[:-1], ET_instance.pix2angle(velocity), marker='x', label='Velocity', color='slategray',linewidth=2.0)
      plt.plot(time[:-1], pixels_to_degrees(et_velocity), marker='x', label='Velocity', color='slategray',linewidth=2.0)
      #plt.axhline(y=5, color='red', linestyle='--', label='Values > {}'.format(5))
      plt.xlabel('Time (s)')
      plt.ylabel('Velocity (°)')
      plt.title('Eye Tracking Velocity')
      plt.legend()
      plt.grid(True)

      #velocity of stimulus
      plt.subplot(4,1,4)
      plt.plot(time[:-1],  pixels_to_degrees(stem_velocity),  marker='x',  label='Velocity',color='gray',linewidth=2.0)
      plt.xlabel('Time (s)')
      plt.ylabel('Velocity (°)')
      plt.title('Target Velocity')
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.show()


  @staticmethod
  def show_plot_velocity(et_velocity,stim_velocity,time):
    


    #print(velocity)
      #vel2 = butter_lowpass_filter(stim_velocity, cutoff=2.7, fs=90, order=3) # FS is eye tracker frequncy and cutoff is frequcy to cut off.  Allows frequencies below the cutoff to pass through.
    #plt.xticks(time, velocity)
    plt.plot(time,et_velocity)
    plt.plot(time,stim_velocity)
    plt.legend(["Eye-tracking velocity after removing saccades", "Stimuli velocity"], loc ="lower right") 
  # plt.plot(time, label='time')
  #  plt.xlim(0, 2000)
  #  plt.hlines(ET.angle2pix(sac_min_thres), 0, 2000, colors='k', linestyles='dotted', label='Saccade min')
  #  plt.hlines(ET.angle2pix(fix_max_thres), 0, 2000, colors='k', linestyles='dashed', label='Fixation max')
  #  plt.legend(fontsize='xx-small', loc='upper right')
    plt.ylabel('Velocity (°/sec)')
    plt.xlabel('Time in seconds')
    plt.grid(True)
    plt.show()    

  @staticmethod
  def show_plot_gain(time,gain,rmse_value=0,thres=2):
        # Set the threshold
      pos_threshold = thres

      # Create a boolean mask for values greater than the threshold
      mask = gain > pos_threshold

      # Plot the data
      legend_label = 'Original Data - \n({:.2f}% values < {})'.format(rmse_value,pos_threshold)

      plt.plot(time, gain, label=legend_label)

      # Mark points where x-values are greater than the threshold
    # plt.scatter(time[mask], new_gain[mask], color='red', marker='o', label='Values > {}'.format(pos_threshold))
      plt.axhline(y=pos_threshold, color='red', linestyle='--', label='Values > {}'.format(pos_threshold))
      
      # Set labels and title
      plt.xlabel('Time in seconds')
      plt.ylabel('Velocity (°/sec)')
      plt.title('Smooth Pursuit Gain')
      plt.grid(True)
      # Add legend
      plt.legend()

      # Show the plot
      plt.show()


  @staticmethod
  def show_plot_accerlation(time,velocity, stim_velocity):
      # Define black and white-friendly colors
      line_color_eye = 'black'  # Use a shade of gray (e.g., 'black', '0.3', etc.)
      line_color_target = 'darkgray'  # Use a lighter shade for differentiation

                  # Calculate acceleration
      delta_time = np.diff(time)
      #eye tracking data
      et_delta_velocity = np.diff(velocity)
      et_acceleration = et_delta_velocity / delta_time
      # target/Stimuli data
      targt_delta_velocity = np.diff(stim_velocity)
      targt_acceleration = targt_delta_velocity / delta_time
        # Plot the velocity and acceleration
      plt.figure(figsize=(12, 6))

      plt.subplot(2, 1, 1)
      plt.plot(time, pixels_to_degrees(velocity), label='Eye movement Velocity', color=line_color_eye)
      plt.plot(time, pixels_to_degrees(stim_velocity), label='Target Velocity', color=line_color_target)
      plt.xlabel('Time (s)')
      plt.ylabel('Velocity (°)')
      plt.legend()

      plt.subplot(2, 1, 2)
      plt.plot(time[1:], et_acceleration, label='Acceleration', color=line_color_eye)
      plt.plot(time[1:], targt_acceleration, label='Target Acceleration', color=line_color_target)
      plt.xlabel('Time (s)')
      plt.ylabel('Acceleration (°/s$^2$)')
      plt.legend()

      plt.tight_layout()
      plt.savefig('acceleration.png', dpi=400, bbox_inches='tight')
      plt.show()


  @staticmethod
  def show_plot_rmse_gain(squared_diff_x,squared_diff_y,rmse):

    plt.figure(figsize=(10, 6))

    # Histogram for squared differences in x and y
    plt.subplot(2, 1, 1)
    plt.hist(squared_diff_x, bins=20, alpha=0.5, label='Squared Differences X', color='gray', edgecolor='black')
    plt.hist(squared_diff_y, bins=20, alpha=0.5, label='Squared Differences Y', color='lightgray', edgecolor='black')
    plt.xlabel('Squared Differences')
    plt.ylabel('Frequency')
    plt.legend()

    # Histogram for RMSE
    plt.subplot(2, 1, 2)
    plt.hist(rmse, bins=20, alpha=0.5, label='RMSE', color='darkgray', edgecolor='black')
    plt.xlabel('Root Mean Squared Error (RMSE)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig('rmse_eye_difference.png', dpi=400, bbox_inches='tight')
    plt.show()


  @staticmethod
  def show_plot_rmse_velocity(squared_diff_velocity,mse_velocity):
        # Histogram for squared differences in x and y
    plt.figure(figsize=(10, 6))

    # Histogram for squared differences in velocities
    plt.subplot(2, 1, 1)
    plt.hist(squared_diff_velocity, bins=20, alpha=0.5, label='Squared Differences Velocities', color='gray', edgecolor='black')
    plt.xlabel('Squared Differences')
    plt.ylabel('Frequency')
    plt.legend()

    # Histogram for RMSE in velocities
    plt.subplot(2, 1, 2)
    plt.hist(mse_velocity, bins=20, alpha=0.5, label='RMSE', color='darkgray', edgecolor='black')
    plt.xlabel('Root Mean Squared Error (RMSE)')
    plt.ylabel('Frequency')
    plt.legend()

    plt.tight_layout()
    plt.savefig('rmse_eye_velocity.png', dpi=400, bbox_inches='tight')
    plt.show()

  @staticmethod
   
    #plt.plot(x, "r", label='x-position')
    #plt.plot(y, "b", label='y-position')

    #plt.ylabel('Relative Position')
    #plt.legend(fontsize='xx-small', loc='upper right')
    #plt.show()
    # Creating plot with dataset_1
  # Plot eye tracking data
    
    plt.plot(time, x,  label='Eye Tracking X', marker='o')
    plt.plot(time, y, label='Eye Tracking Y',marker='o')

    # Plot target data
    plt.plot(time, stem_X, label='Target X', marker='x', color='red')
    plt.plot(time, stem_Y, label='Target Y', marker='x', color='blue')

    # Add labels and legend
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.title('Eye Tracking and Target Data Visualization')
    plt.axvline(x = line, color = 'b', label = 'Latency')
    plt.legend()
    plt.grid(True)
    plt.show()    


  @staticmethod
  def show_latency(velocity,stim_velocity,time,velocity_threshold,latency_start_time,latency_vel):

    plt.figure(figsize=(10, 5))

    plt.plot(time[1:]*1000, velocity, marker='x', linestyle='-', label='ET Velocity', color='black')
    plt.plot(time[1:]*1000, stim_velocity, marker='o', linestyle='-', label='Target Velocity', color='gray')
    plt.axhline(20, color='red', linestyle='--', label='Velocity Threshold')
    #plt.axvline(latency_start_time, color='green', linestyle='--', label='Latency Start')

    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (°)')
    plt.title('Latency')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the figure for inclusion in the research article
    plt.savefig('latency_image.png', dpi=400, bbox_inches='tight')

    # Show the plot
    plt.show()

  @staticmethod
  def show_scatter(x,y,time):
      plt.scatter(time, x, label='Eye Tracking Data', color='dodgerblue', marker='x')
      plt.scatter(time, y, label='Target Data', color='firebrick', marker='o')
      plt.xlabel('Time (s)')
      plt.ylabel('Position')
      plt.title('Eye Tracking Data - Scatter plot')
      plt.grid(True)
      plt.legend()
      plt.show()

  @staticmethod  
  def saccade_latency_distribution(saccade_onset):
      x_range = (0, 400)  # Replace start_value and end_value with your desired range
      plt.figure(figsize=(10, 5))
      # Create a histogram with a black and white theme
      plt.hist(saccade_onset, bins=10, color='white', edgecolor='black', range=x_range)
      plt.title('Saccade Latency')
      plt.xlabel('Saccade Latency (ms)')
      plt.ylabel('Count')

      # Customize the figure and axes background color
      plt.gca().set_facecolor('white')

      # Customize tick colors
      plt.tick_params(axis='x', colors='black')
      plt.tick_params(axis='y', colors='black')

      # Customize title and label colors
      plt.title('Saccade Latency', color='black')
      plt.xlabel('Saccade Latency (ms)', color='black')
      plt.ylabel('Count', color='black')
      plt.savefig('saccade_latency_image.png', dpi=400, bbox_inches='tight')

      plt.show()    