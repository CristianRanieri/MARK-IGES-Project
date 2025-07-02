# Replication Package README

## Overview

This replication package contains all the necessary 
files and scripts to reproduce the results and 
analyses presented in the paper 
"Into the ML-universe: An Improved Classification and 
Characterization of Machine-Learning Projects". 
The package is organized into several directories, 
each containing specific types of files such as 
datasets, scripts, and documentation.

## Contents


## 1. Execution Overview
 In the "ExecutionOverview" directory, we provide an overview description of the architecture of MARK.
- **execution.pdf** contains the whole process to replicate MARK.
- **KnowledgeBase.pdf** contains the steps to replicate the knowledge base.

## 2. Dataset
 In this folder, we provide the dataset used in the study.

- **Baseline.xlsx**: Baseline data collected from the preliminaries studies containing the whole set of ML-Applied and ML-Toolkit & Libraries projects.
- **Final_Dataset.csv**: The dataset containing the filtered project used in this study to perform the categorization and the characterization.

## 3. ML Projects

This folder contains the set of projects classified through the use of MARK. 
In detail, inside the folder there is a specific ".csv" file for each category of the project:
- ML-Model Producers
- ML-Model Consumers
- ML-Model Producers & Consumers
- ML-Toolkit & Libraries.


## 4. MARK-Tool
This folder contains the MARK tool and the instructions to execute it.


### Description

This repository contains a static analysis tool designed to classify machine learning (ML) projects into two categories: ML-Model Producers and ML-Model Consumers. The tool scans the project codebase to identify the nature of the ML activities being performed, helping developers and researchers understand the role of their project within the ML ecosystem.

- **ML-Model Producers**: Projects that focus on creating, training, and refining ML models.
- **ML-Model Consumers**: Projects that utilize pre-trained ML models to make predictions, perform data analysis, or integrate ML capabilities into applications.

### Features

- **Automated Classification**: Quickly classify ML projects based on static code analysis.
- **Comprehensive Reports**: Generate overview and detailed reports highlighting the key indicators used for classification.
- **Easy to Use**: Simple GUI for running the tool and generating reports.

### Output
- **ML-Model Producer** :

- Producer_Final : is the directory containing the final results of the analysis of the ML-Model Producer projects.



- **ML-Model Consumer** :

- Consumer_Final : is the directory containing the final results of the analysis of the ML-Model Consumer projects.

### Installation

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
   
### Specification


This script performs ablation analysis on ML model producers and consumers, analyzing project repositories using specific library dictionaries and generating output in structured folders.


For each component type:
- The script dynamically resolves paths for input directories, output directories, and library dictionaries.
- It analyzes repositories using `MLProducerAnalyzer` and `MLConsumerAnalyzer` classes from external modules.
- Results are stored in designated output folders with specific configurations applied for each iteration.

### Input and Output Folders

- **Input Path**: Base folder containing the project repositories to analyze.
- **Output Path**: Folder where results will be saved, categorized into `Producers` and `Consumers`.

The script creates subfolders for each analysis iteration and organizes results systematically.

### Usage

Run the gui_analysis.py module as follows:

```bash
python gui_analysis.py
```


### Output

The tool generates a report in the specified output directory containing the classification results and detailed analysis.
 1. **Overview Report**: Summary of the classification results.
 2. **Detailed Report**: For each project analyzed, the tool provides a breakdown of the training and inference APIs used for the classification.


## 5. Mark-Configuration Study

### Description

This repository contains a static analysis tool designed to classify machine learning (ML) projects into two categories: ML-Model Producers and ML-Model Consumers. The tool scans the project codebase to identify the nature of the ML activities being performed, helping developers and researchers understand the role of their project within the ML ecosystem.

- **ML-Model Producers**: Projects that focus on creating, training, and refining ML models.
- **ML-Model Consumers**: Projects that utilize pre-trained ML models to make predictions, perform data analysis, or integrate ML capabilities into applications.

### Features

- **Automated Classification**: Quickly classify ML projects based on static code analysis.
- **Comprehensive Reports**: Generate overview and detailed reports highlighting the key indicators used for classification.
- **Easy to Use**: Simple command-line interface for running the tool and generating reports.

### Configurations 
- **ML-Model Producer** :

- Producer_1 : Nguyen Dataset based Knowledge Base for the detection.
- Producer_2 : Our updated based Knowledge Base for the detection.

- **ML-Model Consumer** :

- Consumer_1 : Nguyen Dataset based Knowledge Base for the detection. Additional detection rules 3 and 4 are disabled
- Consumer_2 : Our updated based Knowledge Base for the detection. Additional detection rules 3 and 4 are disabled.
- Consumer_3 : Our updated based Knowledge Base for the detection.Additional detection rule 3 is enabled but rule 4 is disabled.
- Consumer_4 : Our updated based Knowledge Base for the detection.Additional detection rule 4 is enabled but rule 3 is disabled.
- Consumer_5 : Our updated based Knowledge Base for the detection.Additional detection rule 3 and 4 are enabled.



### Installation

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
   
### Specification


This script performs ablation analysis on ML model producers and consumers, analyzing project repositories using specific library dictionaries and generating output in structured folders.


For each component type:
- The script dynamically resolves paths for input directories, output directories, and library dictionaries.
- It analyzes repositories using `MLProducerAnalyzer` and `MLConsumerAnalyzer` classes from external modules.
- Results are stored in designated output folders with specific configurations applied for each iteration.

### Input and Output Folders

- **Input Path**: Base folder containing the project repositories to analyze.
- **Output Path**: Folder where results will be saved, categorized into `Producers` and `Consumers`.

The script creates subfolders for each analysis iteration and organizes results systematically.

### Usage

Run the script using Python, providing optional input and output paths as arguments:

```bash
python exec_ablation.py --input_path /path/to/input --output_path /path/to/output
```


### Output

The tool generates a report in the specified output directory containing the classification results and detailed analysis.
 1. **Overview Report**: Summary of the classification results.
 2. **Detailed Report**: For each project analyzed, the tool provides a breakdown of the training and inference APIs used for the classification.

## 6. Libraries API and Methods
This folder contains the set of libraries adopted and the knowledge base configurations adopted in this study.
In detail:
- **Nguyen_Knowledge_Base** folder contains the set of methods and libraries defined by Nguyen et al. in their study.
- **Our_Knowledge_Base** folder contains the set of methods and libraries defined by us in this study.


## 7. RQs

Contains directories and files related to different research questions (RQs) addressed in the study.

#### RQ1
The content is structured as follows:
- **Pipeline.xslx**: file containing the process for the knowledgebase extraction. 
  - Each step contains the list of the collected API keywords analyzed in this study with the related inter-rater assessment for inclusion and exclusion.
- **selected_projects.csv**: contains the sample selected for the validation.
- **RQ1.xlsx**: contains the data related to the process conducted for evaluating
the detection perforrmance of the tool.

#### RQ2
The content is structured as follows:
- **library_usage**: Directory containing the data related to the library usage analysis for ML-Model Consumers and ML-Model Producers.
  - **{consumers, producers}_libraries.csv**: contains the data related to the library usage analysis for ML-Model Consumers and ML-Model Producers.
  - **{consumers, producers}_libraries_count.csv**: contains the number of projects that uses a specific library.
  - **{consumers, producers}_libraries_treemap.pdf**: contains the treemap of the libraries used by the projects.
- **inputs**: contains the set of metrics adopted and used for the characterization of the projects through statistical tests. 
- **RQ2_test_results**: contains the results of the statistical tests applied.

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

## License
This project is licensed under the MIT License. See the LICENSE file for details.
