import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def Month(x):
    """ 
    This function converts date to number
    Jan = 0, Fev = 1, etc
    """
    return  {
        "Jan" : 0,
        "Feb" : 1,
        "Mar" : 2,
        "Apr" : 3,
        "May" : 4,
        "June" : 5,
        "Jul" : 6,
        "Aug" : 7,
        "Sep" : 8,
        "Oct" : 9,
        "Nov" : 10,
        "Dec" : 11
    }[x]

def VisitorType(x):
    """ 
   Converts VisitorType, 0 (not returning) or 1 (returning)
    """
    return int(1) if x == "Returning_Visitor" else 0

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Load data in a data frame
    df = pd.read_csv(filename) 

    # Chane Months by Jan = 0, Fev = 1 etc
    df["Month"] = df["Month"].apply(Month)

    # Chenge Visitor type by New_visito or Other to 0 and Returning_visitor to 1
    df["VisitorType"] = df["VisitorType"].apply(VisitorType)
    df['VisitorType'].astype('int64')

    # Change weekend by False = 0 and True = 1
    df['Weekend'].astype('int64')

    # Change Revevue by False = 0 and True = 1
    df['Revenue'].astype('int64')
    
    # Start empty lists fro evidence and labels
    evidence = []
    labels = []

    # For each row and index in the data frame
    for index, rows in df.iterrows():
        # Create a list with the fow values
        rowlist = [
            rows.Administrative, 
            rows.Administrative_Duration, 
            rows.Informational, 
            rows.Informational_Duration, 
            rows.ProductRelated, 
            rows.ProductRelated_Duration, 
            rows.BounceRates,
            rows.ExitRates, 
            rows.PageValues, 
            rows.SpecialDay, 
            rows.Month, 
            rows.OperatingSystems, 
            rows.Browser,
            rows.Region, 
            rows.TrafficType, 
            rows.VisitorType, 
            rows.Weekend, 
        ]
        # Append that list to the evidence list
        evidence.append(rowlist)
        # Add the Revenue to the labels list
        labels.append(rows.Revenue)
    
    #Return the tuple (evidence, labels)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    report = classification_report(labels,predictions, digits = 4, output_dict = True)
    return report["True"]["precision"], report["False"]["precision"] # Returne (Sensitivity, specificity)


if __name__ == "__main__":
    main()
