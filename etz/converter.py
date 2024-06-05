from math import atan2, degrees, isnan, sqrt
import math
import json
import os

class Converter:
    
    @staticmethod
    def json_file():
            # Get the path to the etz_json.json file
        json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'etz_json.json')

        # Load values from etz_json.json
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        return json_data

    @staticmethod
    def pixels_to_degrees(px):
        # Work in millimeters
    
        #print(px_distances)
        # Convert each pixel distance in the list to degrees
        
        # Get the path to the etz_json.json file
        
        json_data = Converter.json_file()
        # Extract values
        screen_values = json_data.get('screen_information', [])[0]

        pixels_per_mm = float(screen_values.get('pixels_per_mm', 0))
        mm_from_screen = float(screen_values.get('mm_from_screen', 0))
        
        degrees_list = []
        for px_distance in px:
            mm_distance = px_distance / pixels_per_mm

            # Trigonometry. Eye-to-screen is adjacent edge of triangle.
            # Subtended portion of the screen is the opposite edge.
            # Solve for angle using opp/adj = tangent(angle)
            tangent = mm_distance / mm_from_screen
            radian = math.atan(tangent)

            # Convert radians to degrees
            degree = math.degrees(radian)
            degrees_list.append(degree)
        
        return degrees_list

    @staticmethod
    def normalized_to_pixels(x,y):
        json_data = Converter.json_file()
        screen_values = json_data.get('screen_information', [])[0]
        # Extract values
        screen_width = float(screen_values.get('screen_width', 0))
        screen_height = float(screen_values.get('screen_height', 0))
        x= x*screen_width
        y=y*screen_height
        
        return [x,y]
    
    @staticmethod
    def cartesian_to_normalized(x,y):
        json_data = Converter.json_file()
        coordinate_data = json_data.get('cartesian_coordinate_to_norma', [])[0]

        Xwmin = float(coordinate_data.get('Xwmin', 0))
        Ywmin = float(coordinate_data.get('Ywmin', 0))
        Xwmax = float(coordinate_data.get('Xwmax', 0))
        Ywmax = float(coordinate_data.get('Ywmax', 0))
        
        Xvmin = float(coordinate_data.get('Xvmin', 0))
        Yvmin = float(coordinate_data.get('Yvmin', 0))
        Xvmax = float(coordinate_data.get('Xvmax', 0))
        Yvmax = float(coordinate_data.get('Yvmax', 0))
        
        sx=(Xvmax-Xvmin)/(Xwmax-Xwmin)
        sy=(Yvmax-Yvmin)/(Ywmax-Ywmin)
        
        xp=(x-Xwmin)*sx
        yp=(y-Ywmax)*sy
        
        return [xp,yp]

