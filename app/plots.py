import pandas as pd
import plotly.graph_objects as go


# read in the data
df = pd.read_csv('../data/combined.csv')

offer_received = df[df['event']=='offer received']
transaction = df[df['event']=='transaction']
offer_completed = df[df['event']=='offer completed']


def offers_distribution():
    """
    Distribution of received and completed offers
    OUTPUT:
        plot_data: dict, parameters for web plot 
    """
    # extract data needed for visuals
    received = offer_received.groupby(by=['offer_label'])['person'].count().reset_index()
    completed = offer_completed.groupby(by=['offer_label'])['person'].count().reset_index()

    plot_data = {
        'data': [
            go.Bar(
                x=received['offer_label'],
                y=received['person'],
                name='Received'
            ),
            go.Bar(
                x=completed['offer_label'],
                y=completed['person'],
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
                'title': "Count of Offers sent"
            }
        }
    }

    return plot_data


def transactions_by_age():
    """
    Distribution of transactions by age and gender
    OUTPUT:
        plot_data: dict, parameters for web plot 
    """
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
                'title': "Frequency"
            }
        }
    }

    return plot_data


def transactions_by_membership():
    """
    Distribution of transactions by membership year and gender
    OUTPUT:
        plot_data: dict, parameters for web plot 
    """
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
                'title': "Frequency"
            }
        }
    }

    return plot_data


def transactions_by_income():
    """
    Distribution of transactions by income and gender
    OUTPUT:
        plot_data: dict, parameters for web plot 
    """
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
                'title': "Frequency"
            }
        }
    }

    return plot_data


def income_age():
    """
    Correlation between income and age
    OUTPUT:
        plot_data: dict, parameters for web plot 
    """
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
                'title': "Age"
            }
        }
    }

    return plot_data
