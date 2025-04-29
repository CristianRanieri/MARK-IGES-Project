# MARK - Static Analysis Tool for Classifying ML Projects

**MARK** is a novel approach for the classification of machine learning projects. MARK is based on heuristics, built from a Knowledge
Base of APIs obtained on a filtered dataset.

## Description

This repository contains a static analysis tool designed to classify machine learning (ML) projects into two categories: ML-Model Producers and ML-Model Consumers. The tool scans the project codebase to identify the nature of the ML activities being performed, helping developers and researchers understand the role of their project within the ML ecosystem.

- **ML-Model Producers**: Projects that focus on creating, training, and refining ML models.
- **ML-Model Consumers**: Projects that utilize pre-trained ML models to make predictions, perform data analysis, or integrate ML capabilities into applications.

## Features

- **Automated Classification**: Quickly classify ML projects based on static code analysis.
- **Comprehensive Reports**: Generate overview and detailed reports highlighting the key indicators used for classification.
- **Easy to Use**: Simple command-line interface for running the tool and generating reports.

## Output
- **ML-Model Producer** :

- Producer_Final : is the directory containing the final results of the analysis of the ML-Model Producer projects.



- **ML-Model Consumer** :

- Consumer_Final : is the directory containing the final results of the analysis of the ML-Model Consumer projects.

## Installation

To install the static analysis tool, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ml-project-classifier.git
   cd ml-project-classifier
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
   
## Specification


This script performs ablation analysis on ML model producers and consumers, analyzing project repositories using specific library dictionaries and generating output in structured folders.


For each component type:
- The script dynamically resolves paths for input directories, output directories, and library dictionaries.
- It analyzes repositories using `MLProducerAnalyzer` and `MLConsumerAnalyzer` classes from external modules.
- Results are stored in designated output folders with specific configurations applied for each iteration.

### Input and Output Folders

- **Input Path**: Base folder containing the project repositories to analyze.
- **Output Path**: Folder where results will be saved, categorized into `Producers` and `Consumers`.

The script creates subfolders for each analysis iteration and organizes results systematically.

## Usage

Run the script using Python, providing optional input and output paths as arguments:

```bash
python exec_analysis.py --input_path /path/to/input --output_path /path/to/output
```


## Output

The tool generates a report in the specified output directory containing the classification results and detailed analysis.
 1. **Overview Report**: Summary of the classification results.
 2. **Detailed Report**: For each project analyzed, the tool provides a breakdown of the training and inference APIs used for the classification.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Extending the knowledge base of the tool by adding new ML libraries and APIs is a great way to contribute. You can also improve the classification algorithm or enhance the report generation process.

Please follow these steps:

1. Fork the repository.
2. Create a new branch:
      ```sh
    git checkout -b feature/yourfeature
    ```
   
3. Make your changes and commit them:
      ```sh
      git commit -m "Description of the feature"
    ```

4. Push to the branch:
      ```sh
      git push origin feature/yourfeature
    ```
5. Open a pull request.

