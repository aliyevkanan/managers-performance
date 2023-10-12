from flask import Flask, render_template, Response, request
import datetime
import requests
import pandas as pd


app = Flask(__name__, template_folder="templates")


def get_data(update_from, update_to):
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={update_from}&end={update_to}&valcode=usd&sort=exchangedate&order=desc&json'
    response = requests.get(url)
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

        df.to_csv('usd_uah.csv', index=True)

        return Response(f"File - usd_uah was Downloaded")
    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
