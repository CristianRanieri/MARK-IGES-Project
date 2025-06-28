import os
import argparse
from consumer_classifier_by_dict import MLConsumerAnalyzer
from producer_classifier_by_dict import MLProducerAnalyzer
from components.notebook_converter import NotebookConverter


class ExecAnalyzer:
    def __init__(self, input_path=None, output_path=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_dir = script_dir
        self.input_path = input_path or os.path.join(script_dir, "..", "..", "repos")
        self.output_path = output_path or script_dir

    def run(self):
        # Check input and output paths
        if not os.path.exists(self.input_path):
            print(f"Error: The input folder '{self.input_path}' does not exist.")
            exit(1)

        # --- ML-Model Producers ---
        output_base_folder = os.path.join(self.output_path, "Producers")
        output_folder_producers = os.path.join(output_base_folder, "Producers_Final")
        producer_dict_path = os.path.join(self.script_dir, "library_dictionary", "library_dict_producers_2.csv")

        os.makedirs(output_folder_producers, exist_ok=True)

        if not os.path.exists(producer_dict_path):
            print(f"Error Producer: The library dictionary '{producer_dict_path}' does not exist.")
            exit(1)

        print(f"Analyzing Producers with dictionary: {producer_dict_path}")
        print(f"Results will be written to: {output_folder_producers}")
        analyzer = MLProducerAnalyzer(output_folder=output_folder_producers)
        analyzer.analyze_projects_set_for_producers(self.input_path, producer_dict_path)

        # --- ML-Model Consumers ---
        output_base_folder = os.path.join(self.output_path, "Consumers")
        output_folder_consumers = os.path.join(output_base_folder, "Consumers_Final")
        consumer_dict_path = os.path.join(self.script_dir, "library_dictionary", "library_dict_consumers_2.csv")

        os.makedirs(output_folder_consumers, exist_ok=True)

        if not os.path.exists(consumer_dict_path):
            print(f"Error Consumer: The library dictionary '{consumer_dict_path}' does not exist.")
            exit(1)

        print(f"Analyzing Consumers with dictionary: {consumer_dict_path}")
        print(f"Results will be written to: {output_folder_consumers}")
        print("Rules_3 is set to: True")
        print("Rules_4 is set to: True")

        analyzer = MLConsumerAnalyzer(output_folder=output_folder_consumers)
        analyzer.analyze_projects_set_for_consumers(
            self.input_path,
            consumer_dict_path,
            producer_dict_path,
            rules_3=True,
            rules_4=True
        )


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Run ablation analysis for ML model producers and consumers.")
    parser.add_argument("--input_path", type=str, default=os.path.join(script_dir, "..", "..", "repos"),
                        help="Path to the input directory containing project repositories.")
    parser.add_argument("--output_path", type=str, default=script_dir,
                        help="Path to the output directory to store analysis results.")

    args = parser.parse_args()
    print(f"Starting ablation analysis with input path: {args.input_path} and output path: {args.output_path}")

    # Aggiunta esecuzione processo di conversione dei file . in .py
    converter = NotebookConverter()
    converter.run()

    analyzer = ExecAnalyzer(input_path=args.input_path, output_path=args.output_path)
    analyzer.run()
