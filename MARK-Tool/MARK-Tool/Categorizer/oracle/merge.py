# create a python function that reads two cvs and with the same project name and join them in a new csv
import os.path
import pandas as pd


# script che calcola diverse metriche: Accuracy, F-measure, Precisione e Recall(START)

def get_false_positives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'Yes')]


def get_false_negatives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'No')]


def calc_true_positives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'Yes')].shape[0]


def calc_false_positives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'Yes')].shape[0]


def calc_true_negatives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'No')].shape[0]


def calc_false_negatives(df, column_name):
    return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'No')].shape[0]


def calc_performance_metrics(df, column_name):
    tp = calc_true_positives(df, column_name)
    fp = calc_false_positives(df, column_name)
    tn = calc_true_negatives(df, column_name)
    fn = calc_false_negatives(df, column_name)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    return precision, recall, f1, accuracy

# script che calcola diverse metriche: Accuracy, F-measure, Precisione e Recall(END)


# effettua un unione di due csv(df_oracle e df_produced)
# cambia il nome della colonna Is ML X in Is_ML_X
# tutte le celle della colonna 'Is_ML_X' vuote(Nan) vengono riempite con 'No'
# salva un file con il segunti possibili nomi: producer_verification.csv o consumer_verification.csv


# def join(column_name, df_oracle, df_produced):
#     df_oracle = pd.read_csv(df_oracle)
#     df_produced = pd.read_csv(df_produced)
#     df_produced.rename(columns={f'Is ML {column_name}': f'Is_ML_{column_name}'}, inplace=True)
#     df_produced.drop_duplicates(subset=['ProjectName'], keep='first', inplace=True)
#     df_produced = df_produced[['ProjectName', f'Is_ML_{column_name}']]
#     df_joint = pd.merge(df_oracle, df_produced, on='ProjectName', how='left', validate='one_to_one')
#     # replace nan values with 'No'
#
#     df_joint[f'Is_ML_{column_name}'].fillna('No', inplace=True)
#
#     df_joint.to_csv(f'verifying/{column_name}_verification.csv', index=False)
#     return df_joint



# unisce i dataset due csv(df_oracle e df_produced).
# calcola le metriche di performance(precision, recall, F1, accuracy).
# salva i falsi positivi e i falsi negativi in file separati (false_positives.csv e false_negatives.csv).
# stampa le metriche di performance a console.
def reporting(oracle_name, column_name, base_output_path="../src/Producers/",
              analysis_path="Producers_2/results_first_step.csv", result_name=''):

    # df_joint = join(column_name, oracle_name, os.path.join(base_output_path, analysis_path))
    df_joint = pd.read_csv(result_name)
    df_joint.rename(columns={f'is ML {column_name.capitalize()}': f'Is_ML_{column_name}'}, inplace=True)

    precision, recall, f1, accuracy = calc_performance_metrics(df_joint, column_name)
    df_debug = get_false_positives(df_joint, column_name)
    df_debug.to_csv(f'verifying/{column_name}_false_positives.csv', index=False)
    df_debug = get_false_negatives(df_joint, column_name)
    df_debug.to_csv(f'verifying/{column_name}_false_negatives.csv', index=False)
    print(f"Analysis done for {column_name}. Results saved in {column_name}_verification.csv")
    print("Results:")
    print(f"Precision: {precision}, Recall: {recall}, F1: {f1}, Accuracy: {accuracy}")


def main():
    # non è stato creato un main(DA CAPIRE)
    base_output_path = "../src/Producers/"
    #analysis_path risultati dell'analisi du tutte le parole chiave di tutti i produttori in Producers_2
    analysis_path = "Producers_3/results_first_step.csv"
    column_name = 'producer'
    oracle_name = './oracle_producer_new.csv'
    result_name = 'result_analysis/result_producer_3.csv'

    reporting(oracle_name, column_name, base_output_path, analysis_path, result_name)


    base_output_path = "../src/Consumers/"
    analysis_path = "Consumers_6/results_consumer.csv"
    column_name = 'consumer'
    oracle_name = './oracle_consumer_new.csv'
    result_name = 'result_analysis/result_consumer_6.csv'

    reporting(oracle_name, column_name, base_output_path, analysis_path, result_name)


if __name__ == "__main__":
    main()