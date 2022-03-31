import pandas as pd
import plotly.graph_objects as go


# read in the json files
offers0 = pd.read_json('../data/portfolio.json', orient='records', lines=True)
users0 = pd.read_json('../data/profile.json', orient='records', lines=True)
#transactions0 = pd.read_json('../data/transcript.json', orient='records', lines=True)

#users = pd.read_csv('../data/users.csv')
transactions = pd.read_csv('../data/transactions.csv')

offers0['label'] = (offers0.index+1).astype(str) + '-' + offers0['offer_type']
df = transactions.merge(offers0, how='left', left_on='offer', right_on='id')
df = df.drop(columns=['id'])
df = df.merge(users0, how='left', left_on='person', right_on='id')
df = df.drop(columns=['id'])
df['became_member_on'] = df['became_member_on'].apply(lambda x: int(str(x)[:4]))

offer_received = df[df['event']=='offer received']
transaction = df[df['event']=='transaction']
offer_completed = df[df['event']=='offer completed']


df2 = pd.read_csv('../data/clean_data.csv')


def offers_distribution():
    # extract data needed for visuals
    offers = offer_received.groupby(by=['offer'])['person'].count().reset_index()
    offers = offers.merge(offers0[['id','label']], how='left', left_on='offer', right_on='id')

    offers_completed = offer_completed.groupby(by=['offer'])['person'].count().reset_index()
    offers_completed = offers_completed.merge(offers0[['id','label']], how='left', left_on='offer', right_on='id')

    plot_data = {
        'data': [
            go.Bar(
                x=offers['label'],
                y=offers['person'],
                name='Received'
            ),
            go.Bar(
                x=offers_completed['label'],
                y=offers_completed['person'],
                name='Completed'
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

    return plot_data


def offers_distribution2():
    # extract data needed for visuals
    offer_counts = df2.groupby(by=['offer'])['person'].count().reset_index()
    offers = offers0.reset_index()
    offers['index'] = offers['index'] + 1
    offers['label'] = offers['index'].astype(str) + '-' + offers['offer_type']
    offer_labels = offer_counts.merge(offers[['index','label']], how='left', left_on='offer', right_on='index')
    offer_labels.loc[offer_labels['offer']==0,'label'] = 'No offer'


    plot_data = {
        'data': [
            go.Bar(
                x=offer_labels['label'],
                y=offer_labels['person']
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

    return plot_data

def transactions_by_age():
    plot_data = {
        'data': [
            go.Histogram(
                x=transaction[transaction['gender']=='F']['age'],
                name='Female',
                xbins=dict(start=15, end=120, size=10)
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='M']['age'],
                name='Male'
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='O']['age'],
                name='Other'
            )
        ],
        'layout': {
            'title': 'Transactions by Age',
            'xaxis': {
                'title': "Age"
            },
            'yaxis': {
                'title': "Frequency",
                'automargin': 1,
            },
            'height': 500,
            'margin': {
                't': 50,
                'b': 150
            }

        }
    }

    return plot_data


def transactions_by_membership():
    plot_data = {
        'data': [
            go.Histogram(
                x=transaction[transaction['gender']=='F']['became_member_on'],
                name='Female'
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='M']['became_member_on'],
                name='Male'
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='O']['became_member_on'],
                name='Other'
            )
        ],
        'layout': {
            'title': 'Transactions by Year Became a Member',
            'xaxis': {
                'title': "Year Became a Member"
            },
            'yaxis': {
                'title': "Frequency",
                'automargin': 1,
            },
            'height': 500,
            'margin': {
                't': 50,
                'b': 150
            }

        }
    }

    return plot_data


def transactions_by_income():
    plot_data = {
        'data': [
            go.Histogram(
                x=transaction[transaction['gender']=='F']['income'],
                name='Female',
                xbins=dict(start=0, end=130000, size=10000)
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='M']['income'],
                name='Male'
            ),
            go.Histogram(
                x=transaction[transaction['gender']=='O']['income'],
                name='Other'
            )
        ],
        'layout': {
            'title': 'Transactions by Income',
            'xaxis': {
                'title': "Income"
            },
            'yaxis': {
                'title': "Frequency",
                'automargin': 1,
            },
            'height': 500,
            'margin': {
                't': 50,
                'b': 150
            }

        }
    }

    return plot_data


def income_age():
    plot_data = {
        'data': [
            go.Scatter(
                x=transaction[transaction['gender']=='F']['income'],
                y=transaction[transaction['gender']=='F']['age'],
                opacity=0.7,
                mode='markers',
                name='F'
            ),
            go.Scatter(
                x=transaction[transaction['gender']=='M']['income'],
                y=transaction[transaction['gender']=='M']['age'],
                opacity=0.7,
                mode='markers',
                name='M'
            ),
            go.Scattergl(
                x=transaction[transaction['gender']=='O']['income'],
                y=transaction[transaction['gender']=='O']['age'],
                opacity=0.7,
                mode='markers',
                name='O'
            )
        ],
        'layout': {
            'title': 'Income / Age Correlation',
            'xaxis': {
                'title': "Income"
            },
            'yaxis': {
                'title': "Age",
                'automargin': 1,
            },
            'height': 500,
            'margin': {
                't': 50,
                'b': 150
            }

        }
    }

    return plot_data
