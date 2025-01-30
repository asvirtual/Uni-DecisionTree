from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import LabelEncoder

import pandas as pd

import matplotlib.pyplot as plt

from sklearn.tree import plot_tree




# Define the dataset

categories = ["Weather", "TimeOfDay", "Temperature", "ActivityLevel", "OutdoorPreference", "Mood"]

outputs = ["Park", "Cafe", "Gym", "Relax"]



# Training data

training_data = [

    ["Sunny", "Morning", "Mild", "Medium", "Yes", "Happy", "Park"],

    ["Rainy", "Afternoon", "Cold", "Low", "No", "Tired", "Cafe"],

    ["Cloudy", "Evening", "Mild", "Medium", "Yes", "Neutral", "Gym"],

    ["Sunny", "Afternoon", "Hot", "High", "Yes", "Happy", "Park"],

    ["Rainy", "Morning", "Cold", "Low", "No", "Neutral", "Relax"],

    ["Cloudy", "Afternoon", "Mild", "Medium", "Yes", "Happy", "Park"],

    ["Sunny", "Evening", "Mild", "High", "Yes", "Neutral", "Gym"],

    ["Cloudy", "Morning", "Cold", "Low", "No", "Tired", "Relax"],

    ["Rainy", "Evening", "Cold", "Low", "No", "Tired", "Cafe"],

    ["Sunny", "Morning", "Hot", "Medium", "Yes", "Happy", "Park"],

    ["Rainy", "Afternoon", "Cold", "Medium", "No", "Neutral", "Cafe"],

]



# Convert data into a DataFrame

df = pd.DataFrame(training_data, columns=categories + ["Output"])



# Encode categorical variables

encoders = {col: LabelEncoder() for col in df.columns}

for col in df.columns:

    df[col] = encoders[col].fit_transform(df[col])



# Split features and target

X = df[categories]

y = df["Output"]



# Train decision tree

clf = DecisionTreeClassifier(criterion="entropy", random_state=0)

clf.fit(X, y)



# Convert the query using the same encoders

query = ["Sunny", "Evening", "Mild", "High", "Yes", "Happy"]

query_encoded = [encoders[col].transform([val])[0] for col, val in zip(categories, query)]



# Predict the output

predicted_output = encoders["Output"].inverse_transform(clf.predict([query_encoded]))[0]

print(predicted_output)


# Plot the decision tree

plt.figure(figsize=(12, 8))

plot_tree(clf, feature_names=categories, class_names=outputs, filled=True, rounded=True)

plt.show()