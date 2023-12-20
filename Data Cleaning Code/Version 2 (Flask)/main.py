from flask import Flask, render_template, request
import pandas as pd
from Data_Cleaning_Code import Data_Cleaning
from flask import send_file
from io import BytesIO

app = Flask(__name__)

# Initialize final_df as None
final_df = None

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
    global final_df  # Access the global final_df variable
    if request.method == 'POST':
        file = request.files['file']
        sh_name = request.form['Sheet Name']
        col_name = request.form['SKU Column Name']
        dataframe = pd.read_excel(file, sheet_name=sh_name)
        final_df = Data_Cleaning(dataframe, col_name=col_name)
        #final_df = dataframe
    return render_template("display.html", dataframe = final_df)


@app.route('/download')
def download():
    global final_df
    if final_df is not None:
        excel_file = BytesIO()  # Create a BytesIO object to store the Excel file
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        
        excel_file.seek(0)  # Move the cursor to the beginning of the file
        return send_file(
            excel_file,
            as_attachment=True,
            download_name='cleaned_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        return "Data not available for download."



if __name__ == '__main__':
    app.run(debug=False)

