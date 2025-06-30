import os
import pandas as pd

class ResultsAnalysis:
    def __init__(self, column_name, is_new ,version):
        self.column_name = column_name
        self.is_new = is_new
        self.version = version

    def set_column_name_and_is_new_and_version(self, column_name, is_new, version):
        self.column_name = column_name
        self.is_new = is_new
        self.version = version

    def run(self):
        # Load the oracle CSV file
        oracle_df = pd.read_csv(f"../oracle_{self.column_name}{'_new' if self.is_new else ''}.csv")

        # Create a new dataframe with the required columns
        result_df = oracle_df[["ProjectName", f"Is_Real_ML_{self.column_name}"]].copy()

        # Add the "is ML Producer" or "is ML Consumer" column
        result_df[f"is ML {self.column_name.capitalize()}"] = "No"

        # Path to the folder containing Producers or Consumers CSV files
        producers_folder = f"../../src/{self.column_name.capitalize()}s/{self.column_name.capitalize()}s_{self.version}"

        # Check each .csv file in the folder
        for filename in os.listdir(producers_folder):
            if filename.endswith(".csv"):
                # Read the current CSV file
                file_path = os.path.join(producers_folder, filename)
                producer_df = pd.read_csv(file_path)

                # Check for matching ProjectName values
                matching_projects = result_df["ProjectName"].isin(producer_df["ProjectName"])
                result_df.loc[matching_projects, f"is ML {self.column_name.capitalize()}"] = "Yes"

        # Save the resulting dataframe to a new CSV file
        result_df.to_csv(f"result_{self.column_name}_{self.version}.csv", index=False)


if __name__ == "__main__":
    results_analysis = ResultsAnalysis("producer",True,3)
    results_analysis.run()
    results_analysis.set_column_name_and_is_new_and_version("consumer", True, 6)
    results_analysis.run()