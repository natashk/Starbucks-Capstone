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
#offers = pd.read_csv('../data/offers.csv')
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
    return render_template('home.html', ids=ids, graphJSON=graphJSON, offers=offers.to_dict('records'))


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
    data = pd.DataFrame(data={
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
        'age':[20],
        'became_member_on':[2015],
        'income':[20000],
        'F':[1],
        'M':[0],
        'O':[0],
        'no_gender':[0]
    })
    classification_result = model.predict_proba(data)[0]
    #if classification_result==1:
    #    classification_result = 'YES'
    #else:
    #    classification_result = 'NO'

    return render_template(
        'go.html',
        offer_id=offer_id,
        classification_result=classification_result,
        offers=offers.to_dict('records')
    )


def main():
    app.run(host='0.0.0.0', port=3001)


if __name__ == '__main__':
    main()