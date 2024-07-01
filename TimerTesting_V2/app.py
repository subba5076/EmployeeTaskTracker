from flask import Flask, render_template, request, jsonify, send_file
import csv
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    data = request.json['rows']
    
    # Generate CSV file in memory
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Name', 'Task', 'Start Time', 'Elapsed Time'])
    
    for row in data:
        csv_writer.writerow([row['name'], row['task'], row['start_time'], row['elapsed_time']])
    
    output.seek(0)
    
    # Create a response object
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='report.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
