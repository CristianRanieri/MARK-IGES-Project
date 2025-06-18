import os
import pandas as pd

#-------------------------------------------------------------------------------------------------------
# lo script:
# apre due csv oracle_producer.csv e oracle_consumer.csv.
# in entrambi aggiunge una colonna, rispettivamente Is_ML_Producer e Is_ML_Consumer.
# Lo script esamina le cartelle specificate (Producers_1, Producers_2, ecc. per i produttori e Consumers_1, Consumers_2, ecc. per i consumatori)
# Esamina per ogni nome di file presente nella cartella Producers_X se appare in oracle_producer.csv, in quel caso scrive 'Yes' nella colonna Is_ML_Producer altrimenti 'No'
# Esamina per ogni nome di file presente nella cartella Consumers_X se appare in oracle_consumer.csv, in quel caso scrive 'Yes' nella colonna Is_ML_Consumer altrimenti 'No'
# Per ogni cartella esaminata crea un file(come result_consumer_1.csv) dove salva il contenuto di 'oracle' con la nuova colonna aggiunta.
#-------------------------------------------------------------------------------------------------------

# Load the oracle.csv file
oracle_df = pd.read_csv("../oracle_producer.csv")

### First Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_producer"]].copy()

# Add the "is ML Producer" column
result_df["is ML Producer"] = "No"

# Path to the folder containing Producers_1 CSV files
producers_folder = "../../src/Producers/Producers_1"

# Check each .csv file in the Producers_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Producer"] = "Yes"

# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_producer_1.csv", index=False)


### Second Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_producer"]].copy()

# Add the "is ML Producer" column
result_df["is ML Producer"] = "No"

# Path to the folder containing Producers_1 CSV files
producers_folder = "../../src/Producers/Producers_2"

# Check each .csv file in the Producers_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Producer"] = "Yes"

# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_producer_2.csv", index=False)


# Load the oracle.csv file
oracle_df = pd.read_csv("../oracle_consumer.csv")

### First Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_consumer"]].copy()

# Add the "is ML Consumer" column
result_df["is ML Consumer"] = "No"

# Path to the folder containing Consumer_1 CSV files
producers_folder = "../../src/Consumers/Consumers_1"

# Check each .csv file in the Consumer_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Consumer"] = "Yes"

# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_consumer_1.csv", index=False)


### Second Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_consumer"]].copy()

# Add the "is ML Consumer" column
result_df["is ML Consumer"] = "No"

# Path to the folder containing Consumer_1 CSV files
producers_folder = "../../src/Consumers/Consumers_2"

# Check each .csv file in the Consumer_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Consumer"] = "Yes"

# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_consumer_2.csv", index=False)


### Third Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_consumer"]].copy()

# Add the "is ML Consumer" column
result_df["is ML Consumer"] = "No"

# Path to the folder containing CSV files
producers_folder = "../../src/Consumers/Consumers_3"

# Check each .csv file in the Producers_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Consumer"] = "Yes"

# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_consumer_3.csv", index=False)


### Fourth Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_consumer"]].copy()

# Add the "is ML Producer" column
result_df["is ML Consumer"] = "No"

# Path to the folder containing Producers_1 CSV files
producers_folder = "../../src/Consumers/Consumers_4"

# Check each .csv file in the Producers_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Consumer"] = "Yes"
# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_consumer_4.csv", index=False)

### Fifth Dataset ###
# Create a new dataframe with the required columns
result_df = oracle_df[["ProjectName", "Is_Real_ML_consumer"]].copy()

# Add the "is ML Producer" column
result_df["is ML Consumer"] = "No"

# Path to the folder containing Producers_1 CSV files
producers_folder = "../../src/Consumers/Consumers_5"

# Check each .csv file in the Producers_1 folder
for filename in os.listdir(producers_folder):
    if filename.endswith(".csv"):
        # Read the current CSV file
        file_path = os.path.join(producers_folder, filename)
        producer_df = pd.read_csv(file_path)

        # Check for matching ProjectName values
        matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
        result_df.loc[matching_projects, "is ML Consumer"] = "Yes"
# Save the resulting dataframe to a new CSV file
result_df.to_csv("result_consumer_5.csv", index=False)