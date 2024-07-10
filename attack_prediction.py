import pickle
import tensorflow as tf
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


model = tf.keras.models.load_model("models/GatedRecurrentUnit_model.h5")


with open(file="models/selected_features.pkl", mode="rb") as file:
    imp_cols = pickle.load(file=file)

with open(file="models/scaler.pkl", mode="rb") as file:
    scaler = pickle.load(file=file)


print(imp_cols)


class_labels = ['Benign', 'ddos', 'password', 'scanning']


def predict():

    filepath = 'in_folder/Test_Sample.csv'

    df = pd.read_csv(filepath)
    df.head()

    df_selected = df[imp_cols]
    df_selected.head()

    df_scaled = scaler.transform(df_selected.values)
    df_scaled = pd.DataFrame(df_scaled, columns=df_selected.columns)
    df_scaled

    prediction = model.predict(df_scaled.values)
    class_label = np.argmax(prediction)
    class_name = class_labels[class_label]
    probability = prediction[0][class_label]

    print(f"Class Label: {class_label}")
    print(f"Class Name: {class_name}")
    # print(f"Class probability: {probability:.3f}%")

    return class_name
