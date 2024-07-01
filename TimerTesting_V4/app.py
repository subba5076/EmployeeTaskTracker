from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import csv
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    data = request.json['rows']
    
    # Define the path for the CSV file
    csv_file_path = r'C:\Users\HP\Desktop\TimerTesting\csv\report.csv'
    
    # Generate CSV file
    with open(csv_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Name', 'Task', 'Start Time', 'Elapsed Time'])
        
        for row in data:
            csv_writer.writerow([row['name'], row['task'], row['start_time'], row['elapsed_time']])
    
    return send_file(
        csv_file_path,
        mimetype='text/csv',
        as_attachment=True,
        download_name='report.csv'
    )

@app.route('/visualize', methods=['POST'])
def visualize():
    # Path of the generated CSV file
    csv_file_path = r'C:/Users/HP/Desktop/TimerTesting/csv/report.csv'
    
    try:
        subprocess.run(['python', 'visualise.py', csv_file_path], check=True)
        return jsonify({"message": "Visualization created"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pie_charts')
def pie_charts():
    return send_file('pie_charts.html')

if __name__ == '__main__':
    app.run(debug=True)
