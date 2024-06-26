import pandas as pd
import pickle

with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

unlabeled_data = pd.read_csv('Data_Set_2.csv')

selected_columns = unlabeled_data.iloc[1:, 1:12]

X = selected_columns.values

predictions = model.predict(X)
print(predictions)

actual_labels = unlabeled_data.iloc[1:, 13].values

accuracy = (predictions == actual_labels).mean()
print("Accuracy:", accuracy)