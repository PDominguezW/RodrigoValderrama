import os
from flask import Flask, send_file
from waitress import serve
from score_calculator import calculate_score
from utils import fill_and_clean_data, create_data_and_clean, validar_rut
from scrappers import run_scrappers

# Create the Flask app
app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return "Welcome to the Liquidez API!"

@app.route("/<rut>", methods=['GET'])
def root(rut):

    # Format rut
    rut = rut.replace(".", "")

    if rut == "favicon.ico":
        return ""
    
    # Validate the rut
    if not validar_rut(rut):
        return "Rut invalido"

    # Run the main function with the provided parameter and wait until it's over
    run_scrappers(rut)

    # Create a JSON response with the data of 'dealernet.json', 'experian.json', and 'equifax.json'.
    data = create_data_and_clean()

    # Format data
    data = fill_and_clean_data(data)

    # Calculate the score
    file_name = calculate_score(rut, data)

    return send_file(file_name, as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    # Run Flask app
    serve(app,host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
