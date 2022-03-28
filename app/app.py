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
        offers=offers.to_dict('records')
    )


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input
    offer_id = request.args.get('offer_id', '')
    age = request.args.get('customer_age', '') 
    became_member_on = request.args.get('became_member_on', '') 
    income = request.args.get('income', '') 
    gender = request.args.get('gender', '') 

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
        'age':[40],
        'became_member_on':[2000],
        'income':[80000],
        'F':[0],
        'M':[1],
        'O':[0],
        'no_gender':[0]
    }
    # prediction with no offer
    data = pd.DataFrame(data_dict)
    result = model.predict_proba(data)[0]
    predictions[0] = round(result[1],2)
    
    # predictions for each offer
    offer_cols = ['reward','difficulty','duration','mobile','social','web','email','bogo','discount','informational']
    for offer in offers_clean.to_dict('records'):
        for col in offer_cols:
            data_dict[col]=offer[col]
        
        data_dict['age'] = [20]
        data_dict['became_member_on'] = [2015]
        data_dict['income'] = [20000]
        data_dict['F'] = [1]
        data_dict['M'] = [0]
        data_dict['O'] = [0]
        data_dict['no_gender'] = [0]

        data = pd.DataFrame(data=data_dict)
        result = model.predict_proba(data)[0]
        predictions[offer['id']] = round(result[1],2)


    return render_template(
        'go.html',
        offer_id=offer_id,
        result=predictions,
        offers=offers.to_dict('records')
    )


def main():
    app.run(host='0.0.0.0', port=3001)


if __name__ == '__main__':
    main()