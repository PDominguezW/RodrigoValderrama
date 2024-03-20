import os
from flask import Flask, send_file
from flask_cors import CORS
from waitress import serve
from score_calculator import calculate_score
from utils import fill_and_clean_data, create_data_and_clean, validar_rut
from scrappers import run_scrappers
import zipfile
import traceback
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Get DB
load_dotenv()
mongo_url = os.environ['MONGODB_URL']
client = MongoClient(mongo_url)
db = client.Telefactor
users_collection = db.users

@app.route("/", methods=['GET'])
def welcome():
    return "Welcome to the Liquidez API!"

@app.route("/<user_id>/<rut>", methods=['GET'])
def root(user_id, rut):

    print("Program started")
    try:

        if not users_collection.find_one({"_id": ObjectId(user_id)}):
            return "User not found", 404
        
        # Format rut
        rut = rut.replace(".", "")

        if rut == "favicon.ico":
            return ""
        
        # Validate the rut
        if not validar_rut(rut):
            return "Rut invalido"
        
        print("Starting scrappers for rut: " + rut)

        # Run the main function with the provided parameter and wait until it's over
        run_scrappers(rut)

        print("Scrappers finished")
        print("Starting cleaning data")

        # Create a JSON response with the data of 'dealernet.json', 'experian.json', and 'equifax.json'.
        data = create_data_and_clean()

        # Format data
        data = fill_and_clean_data(data)

        print("Data cleaned")
        print("Starting score calculation")

        # Calculate the score
        file_name = calculate_score(rut, data)

        print("Score calculated")
        print("Starting zip creation")

        # Create a zip with the file of filename, and all the pfds in the pdf directory
        with zipfile.ZipFile('contents.zip', 'w') as zipObj:
            # Add file to zip
            zipObj.write(file_name)

            # Add files inside pdf directory to zip
            for folderName, subfolders, filenames in os.walk('respaldo'):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)

        print("Process finished")

        # Send the zip file
        return send_file('contents.zip', as_attachment=True)

    except Exception as e:
        # Return the error, with detail
        return traceback.format_exc()


if __name__ == "__main__":
    # Run Flask app
    serve(app,host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
