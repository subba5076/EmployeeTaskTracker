import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from io import BytesIO
import base64

def create_individual_pie_charts(csv_file):
    # Dictionary to store data grouped by individual
    data = defaultdict(list)

    # Read CSV and populate data dictionary
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            name = row[0].strip()
            task = row[1].strip()
            elapsed_time = float(row[3].strip())

            data[name].append((task, elapsed_time))

    # List to store base64 encoded pie chart images
    charts = []

    # Generate pie charts for each individual
    for name, tasks in data.items():
        tasks.sort(key=lambda x: x[1], reverse=True)  # Sort tasks by elapsed time (descending)

        task_names = [task[0] for task in tasks]
        elapsed_times = [task[1] for task in tasks]

        # Create pie chart with smaller size
        plt.figure(figsize=(4, 3))  # Adjust the figsize here for smaller charts
        plt.pie(elapsed_times, labels=task_names, autopct='%1.1f%%', startangle=140)
        plt.title(f'Task Distribution for {name}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save pie chart to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        charts.append(base64.b64encode(img.getvalue()).decode())
        plt.close()

    # Generate HTML page with embedded pie charts
    html_content = '<html><head><title>Pie Charts</title></head><body style="text-align:center;">'
    for chart in charts:
        html_content += f'<img src="data:image/png;base64,{chart}" style="margin: 10px;"/>'
    html_content += '</body></html>'

    # Write HTML content to a file
    with open('pie_charts.html', 'w') as html_file:
        html_file.write(html_content)

# Example usage:
if __name__ == "__main__":
    csv_file = "c:\\Users\\HP\\Downloads\\report (2).csv"  # Replace with your CSV file path
    create_individual_pie_charts(csv_file)
