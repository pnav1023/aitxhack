from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file and file.filename.endswith('.csv'):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file)
        
        # Do something with the data, e.g., print it or process it
        print(df.head())  # Print the first few rows of the DataFrame
        
        # Redirect to the home page or another page
        return redirect(url_for('index'))
    
    return 'Invalid file type. Please upload a CSV file.'

if __name__ == '__main__':
    app.run(debug=True)
