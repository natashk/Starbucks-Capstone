import json
import plotly
import pandas as pd

from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar
from plotly.graph_objs import Box
import joblib
from sqlalchemy import create_engine


app = Flask(__name__)


# load data
offers = pd.read_json('../data/portfolio.json', orient='records', lines=True)
offers = offers.set_index('id').to_dict('index')

offers_clean = pd.read_csv('../data/offers.csv')
offers_clean = offers_clean.drop(columns=['Unnamed: 0'])

#users = pd.read_csv('../data/users.csv')
#transactions = pd.read_csv('../data/transactions.csv')
df = pd.read_csv('../data/clean_data.csv')

# load model
model = joblib.load('../model/model_rfc.pkl')


# index webpage displays visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    #offer_data = offers

    # extract data needed for visuals
    offer_counts = df.groupby(by=['offer'])['person'].count().reset_index()

    # create visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=offer_counts['offer'],
                    y=offer_counts['person']
                )
            ],

            'layout': {
                'title': 'Distribution of Offers',
                'xaxis': {
                    'title': "Offer",
                    'tickangle': 60,
                    'categoryorder':'total descending'
                },
                'yaxis': {
                    'title': "Count of Offers sent",
                    'automargin': 1,
                },
                'height': 500,
                'margin': {
                    't': 50,
                    'b': 150
                }

            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template(
        'home.html',
        ids=ids,
        graphJSON=graphJSON,
        offers=offers
    )


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input
    offer_id = request.args.get('offer_id', '')
    age = int(request.args.get('customer_age', '')) if request.args.get('customer_age', '')!='' else 118
    became_member_on = int(request.args.get('became_member_on', '')) if request.args.get('became_member_on', '')!='' else 0
    income = int(request.args.get('income', '0')) if request.args.get('income', '')!='' else 0
    gender = request.args.get('gender', 'no_gender')

#reward	difficulty	duration	mobile	social	web	email	bogo	discount	informational	age	became_member_on	income	F	M	O	no_gender
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
    predictions['0'] = {'prediction':round(result[1],2)}
    
    # predictions for each offer
    offer_cols = ['reward','difficulty','duration','mobile','social','web','email','bogo','discount','informational']
    for offer in offers_clean.to_dict('records'):
        for col in offer_cols:
            data_dict[col]=offer[col]
        
        data = pd.DataFrame(data=data_dict)
        result = model.predict_proba(data)[0]

        offer_data = offers[offer['orig_id']]
        offer_data['prediction'] = round(result[1],2)
        predictions[offer['id']] = offer_data


    return render_template(
        'go.html',
        offer_id=offer_id,
        age=age,
        became_member_on=became_member_on,
        income=income,
        gender=gender,
        result=predictions,
        offers=offers
    )


def main():
    app.run(host='0.0.0.0', port=3001)


if __name__ == '__main__':
    main()