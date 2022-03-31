import json
import pandas as pd

from flask import Flask
from flask import render_template, request
import joblib
import plotly

import plots

app = Flask(__name__)


# load data
offers_orig = pd.read_json('../data/portfolio.json', orient='records', lines=True)
offers_dict = offers_orig.set_index('id').to_dict('index')

offers_clean = pd.read_csv('../data/offers.csv')

# load model
model = joblib.load('../model/model_lr.pkl')


# index webpage displays visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    # create visuals
    graphs = [
        plots.offers_distribution(),
        #plots.offers_distribution2(),
        plots.transactions_by_age(),
        plots.transactions_by_membership(),
        plots.transactions_by_income(),
        #plots.income_age()
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template(
        'home.html',
        ids=ids,
        graphJSON=graphJSON
    )


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input
    age = int(request.args.get('customer_age', '')) if request.args.get('customer_age', '')!='' else 0
    became_member_on = int(request.args.get('became_member_on', '')) if request.args.get('became_member_on', '')!='' else 0
    income = int(request.args.get('income', '0')) if request.args.get('income', '')!='' else 0
    gender = request.args.get('gender', 'no_gender')

# reward	difficulty	duration
# mobile	social	web	email
# bogo	discount	informational
# age	became_member_on	income	F	M	O	no_gender
    # use model to predict classification for query
    predictions = {}
    data_dict = {
        'reward':[0],
        'difficulty':[0],
        'duration':[0],
        'mobile':[0],
        'social':[0],
        'web':[0],
        'email':[0],
        'bogo':[0],
        'discount':[0],
        'informational':[0],
        'age':[age],
        'became_member_on':[became_member_on],
        'income':[income],
        'F':[0],
        'M':[0],
        'O':[0],
        'no_gender':[0]
    }
    data_dict[gender] = [1]

    # prediction with no offer
    data = pd.DataFrame(data_dict)
    result = model.predict_proba(data)[0]
    predictions['0'] = {'offer_type':'no offer','prediction':round(result[1],2)}
    
    # predictions for each offer
    offer_cols = ['reward','difficulty','duration','mobile','social','web','email','bogo','discount','informational']
    for offer in offers_clean.to_dict('records'):
        for col in offer_cols:
            data_dict[col]=offer[col]
        
        data = pd.DataFrame(data=data_dict)
        result = model.predict_proba(data)[0]

        offer_data = offers_dict[offer['orig_id']]
        offer_data['prediction'] = round(result[1],2)
        predictions[offer['id']] = offer_data


    return render_template(
        'go.html',
        age=age,
        became_member_on=became_member_on,
        income=income,
        gender=gender,
        result=predictions
    )


def main():
    app.run(host='0.0.0.0', port=3001)


if __name__ == '__main__':
    main()