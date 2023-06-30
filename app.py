from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# example from the website docs
# use it to understand how I did it
@app.route("/docs", methods=["GET"])
def docs():
    url = "https://api.exchangerate.host/latest?base=USD"
    response = requests.get(url)
    data = response.json()

    print(data)
    return data


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            amount = request.form["amount"]
            amount = float(amount)
            convert_from = request.form["convert_from"]
            convert_to = request.form["convert_to"]

            url = "https://api.exchangerate.host/latest?symbols=USD,GBP"
            response = requests.get(url).json()

            Exchange_rate = response["Realtime Currency Exchange Rate"]

            Exchange_rate = float(Exchange_rate)  # inorder to display in decimals
            # multiplying the exchange rate by the amount
            result = Exchange_rate * amount

            convert_from_code = response["From_Currency Code"]
            convert_from_name = response["From_Currency Name"]
            convert_to_code = response["To_Currency Code"]
            convert_to_name = response["To_Currency Name"]
            updated_time = response["Refreshed"]
            return render_template(
                "home.html",
                result=round(result, 2),
                amount=amount,
                convert_from_codes=convert_from_code,
                convert_from_name=convert_from_name,
                convert_to_code=convert_to_code,
                convert_to_name=convert_to_name,
                updated_time=updated_time,
            )
        # if the request failed
        except Exception as e:
            return f"<h1> Bad Request : {e} </h1>"

    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
