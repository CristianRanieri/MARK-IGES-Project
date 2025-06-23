import os
import argparse
from consumer_classifier_by_dict import MLConsumerAnalyzer
from producer_classifier_by_dict import MLProducerAnalyzer
# Resolve absolute paths dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))

def exec_analysis(input_path=os.path.join(script_dir, "../","../", "repos"),output_path=script_dir):
    # Resolve absolute paths dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script


    ######## ML-Model Producers ########
    input_folder = input_path
    output_base_folder = os.path.join(output_path, "Producers")
    output_folders = [
        os.path.join(output_base_folder, "Producers_Final")
    ]
    producer_dict_paths = [
        os.path.join(script_dir, "library_dictionary", "library_dict_producers_2.csv")
    ]

    # Ensure output folders exist
    for output_folder in output_folders:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Analyze the ML-Model Producer projects for each library dictionary and corresponding output folder
    for library_dict_path, output_folder in zip(producer_dict_paths, output_folders):
        # Initialize the analyzer with the respective output folder
        analyzer = MLProducerAnalyzer(output_folder=output_folder)

        # Check library dictionary path
        if not os.path.exists(library_dict_path):
            print(f"Error Producer: The library dictionary '{library_dict_path}' does not exist.")
            exit(1)

        # Ensure the input folder exists
        if not os.path.exists(input_folder):
            print(f"Error: The input folder '{input_folder}' does not exist.")
            exit(1)

        # Run the analysis
        print(f"Analyzing with library dictionary: {library_dict_path}")
        print(f"Results will be written to: {output_folder}")
        analyzer.analyze_projects_set_for_producers(input_folder, library_dict_path)



    ######## ML-Model Consumers ########
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    input_folder = input_path
    output_base_folder = os.path.join(output_path, "Consumers")
    output_folders = [
        os.path.join(output_base_folder, "Consumers_Final")
    ]
    consumer_dict_paths = [
        os.path.join(script_dir, "library_dictionary", "library_dict_consumers_2.csv")
    ]
    rules_3 = True
    rules_4 = True
    current_producer_dict_path = producer_dict_paths[0]
    current_consumer_dict_path = consumer_dict_paths[0]

    # Initialize the analyzer with the respective output folder
    analyzer = MLConsumerAnalyzer(output_folder=output_folders[0])

    # Check library dictionary path
    if not os.path.exists(current_consumer_dict_path):
        print(f"Error Consumer: The library dictionary '{current_consumer_dict_path}' does not exist.")
        exit(1)
    if not os.path.exists(current_producer_dict_path):
        print(f"Error Producer: The library dictionary '{current_producer_dict_path}' does not exist.")
        exit(1)

    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        exit(1)

    # Run the analysis
    print(f"Analyzing with library dictionary: {current_consumer_dict_path}")
    print(f"Results will be written to: {output_folders[0]}")
    print(f"Rules_3 is set to: {rules_3}")
    print(f"Rules_4 is set to: {rules_4}")
    analyzer.analyze_projects_set_for_consumers(input_folder, current_consumer_dict_path, current_producer_dict_path, rules_3, rules_4)


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser(description="Run ablation analysis for ML model producers and consumers.")
    parser.add_argument("--input_path", type=str, default=os.path.join(script_dir, "../", "../", "repos"),
                        help="Path to the input directory containing project repositories.")
    parser.add_argument("--output_path", type=str, default=script_dir,
                        help="Path to the output directory to store analysis results.")

    args = parser.parse_args()

    # Run ablation analysis with provided arguments
    print(f"Starting ablation analysis with input path: {args.input_path} and output path: {args.output_path}")
    exec_analysis(input_path=args.input_path, output_path=args.output_path)