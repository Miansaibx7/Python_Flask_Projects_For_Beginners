import csv
import numpy as np
import matplotlib.pyplot as plt
import os

# First open a csv file

def analyze_marks(file_path, chart_path='static/average_chart.png'):
    try:
        with open (file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader) # Change the cvs file data into list

            if len(data) < 2:
                raise ValueError("CSV must have a header and at least one row of marks.")
            
            headers = data [0][1:]  # skip student name/id column
            marks_data = [list(map(float,row[1:])) for row in data[1:]]

            marks_array = np.array(marks_data)

#    NumPy calculations
             
            average = np.round(np.mean(marks_array,axis=0), 2)
            highest = np.max(marks_array, axis=0)
            lowest = np.min(marks_array,axis=0)

#    Generate bar chart for average marks

            plt.figure(figsize=(10,5))
            plt.bar(headers,average,color= 'skyblue')
            plt.xlabel("Subjects")
            plt.ylabel("Average Marks")
            plt.title("Average Marks per Subject")
            plt.tight_layout()

#    Save the chart

            if os.path.exists(chart_path):
                os.remove(chart_path)
            
            plt.savefig(chart_path)
            plt.close()

# Return function 
           
            return {
                "HeaderS" : headers,
                "Average" : average.tolist(),
                "Highest" : highest.tolist(),
                "Lowest"  : lowest.tolist(),
                "student_count" : len(marks_array),
                "Subject_count" : len(headers),
                "Chart_path" : chart_path
}
        
    except Exception as e:
        print ("Error Analyzing marks:",e)
        return None