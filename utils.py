from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle


def build_model(classifier, param_grid):
    '''
    INPUT:
    classifier - object, classifier
    parameters - dict, parameters for GridSearchCV

    OUTPUT:
    pipeline - machine learning pipeline, which will take in features as input
               and output classification results
    '''

    # text processing and model pipeline
    pipeline = Pipeline([
        ('clf', classifier)
    ])

    # create gridsearch object and return as final model pipeline
    pipeline = GridSearchCV(pipeline, param_grid=param_grid, scoring='f1')

    return pipeline


def evaluate_model(model, X_test, Y_test):
    '''
    INPUT:
    model - machine learning pipeline
    X_test - array of features
    Y_test - array of predictions
    OUTPUT:
    Reports:
        f1 score, precision, recall for each output of the dataset
        accuracy of the model
        the best parameters found using GridSearch
    '''

    y_pred = model.predict(X_test)
    print(classification_report(Y_test, y_pred))
    #print(f'Accuracy: {(y_pred==Y_test).mean()}')
    print("\nBest Parameters:", model.best_params_)


def save_model(model, model_filepath):
    '''
    INPUT:
    model - machine learning pipeline
    model_filepath - the filepath of the pickle file to save the model to
    OUTPUT:
    Saves the model as a pickle file
    '''

    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)

