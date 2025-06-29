# create a python function that reads two cvs and with the same project name and join them in a new csv
import os.path
import pandas as pd


class Merge:
    def __init__(self, column_name, version):
        self.column_name = column_name
        self.result_name = 'result_analysis/result_' + column_name + '_' + str(version) + '.csv'

    def set_column_name_and_version(self,  column_name, version):
        self.column_name = column_name
        self.result_name = 'result_analysis/result_' + column_name + '_' + str(version) + '.csv'


# script che calcola diverse metriche: Accuracy, F-measure, Precisione e Recall(START)
    def get_false_positives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'No') & (df[f'Is_ML_{self.column_name}'] == 'Yes')]


    def get_false_negatives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'Yes') & (df[f'Is_ML_{self.column_name}'] == 'No')]


    def calc_true_positives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'Yes') & (df[f'Is_ML_{self.column_name}'] == 'Yes')].shape[0]


    def calc_false_positives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'No') & (df[f'Is_ML_{self.column_name}'] == 'Yes')].shape[0]


    def calc_true_negatives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'No') & (df[f'Is_ML_{self.column_name}'] == 'No')].shape[0]


    def calc_false_negatives(self, df):
        return df[(df[f'Is_Real_ML_{self.column_name}'] == 'Yes') & (df[f'Is_ML_{self.column_name}'] == 'No')].shape[0]


    def calc_performance_metrics(self, df):
        tp = self.calc_true_positives(df)
        fp = self.calc_false_positives(df)
        tn = self.calc_true_negatives(df)
        fn = self.calc_false_negatives(df)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        return precision, recall, f1, accuracy

# script che calcola diverse metriche: Accuracy, F-measure, Precisione e Recall(END)


# calcola le metriche di performance(precision, recall, F1, accuracy).
# salva i falsi positivi e i falsi negativi in file separati (false_positives.csv e false_negatives.csv).
# stampa le metriche di performance a console.
    def run(self):
        df_joint = pd.read_csv(self.result_name)
        df_joint.rename(columns={f'is ML {self.column_name.capitalize()}': f'Is_ML_{self.column_name}'}, inplace=True)

        precision, recall, f1, accuracy = self.calc_performance_metrics(df_joint)
        df_debug = self.get_false_positives(df_joint)
        df_debug.to_csv(f'verifying/{self.column_name}_false_positives.csv', index=False)
        df_debug = self.get_false_negatives(df_joint)
        df_debug.to_csv(f'verifying/{self.column_name}_false_negatives.csv', index=False)
        print(f"Analysis done for {self.column_name}. Results saved in {self.column_name}_verification.csv")
        print("Results:")
        print(f"Precision: {precision}, Recall: {recall}, F1: {f1}, Accuracy: {accuracy}")


if __name__ == "__main__":
    merge = Merge('producer', 3)
    merge.run()
    merge.set_column_name_and_version('consumer', 6)
    merge.run()