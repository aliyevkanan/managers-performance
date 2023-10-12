from flask import Flask, render_template, Response, request
import datetime
import requests
import pandas as pd
from user_agent import generate_user_agent


app = Flask(__name__, template_folder="templates")


def get_data(update_from, update_to):
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={update_from}&end={update_to}&valcode=usd&sort=exchangedate&order=desc&json'
    headers = {'User-Agent': generate_user_agent()}
    response = requests.get(url, headers=headers)
    return response.json()

def proccess_data(response):
    data =  [{"date": day['exchangedate'], "rate": day['rate']} for day in response]
    return pd.DataFrame(data)

        
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        update_from =request.form.get("update_from") or  str(datetime.date.today())
        update_to = request.form.get("update_to") or str(datetime.date.today())

        update_to, update_from = update_to.replace("-", ""), update_from.replace("-", "")

        response = get_data(update_from, update_to)
        df = proccess_data(response)

        file_path = "csv_folder/" + "usd_uah.csv"
        df.to_csv(file_path, index=True)

        return Response(f"File - {file_path} was Downloaded")
    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
