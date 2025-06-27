import git
import pandas as pd
from git import Repo
import shutil
import concurrent.futures
from threading import Lock
import os
import argparse

#TEST
def __search(row, lock, output_path, no_repos2=True):
    repo_full_name = row["ProjectName"]
    repo_url = f'https://github.com/{repo_full_name}.git'

    # Cloning path
    if no_repos2:
        clone_path = f'{output_path}/{repo_full_name}'
    else:
        clone_path = f'{output_path}/repos2/{repo_full_name}'

    try:
        print(f'cloning {repo_full_name}')
        Repo.clone_from(repo_url, clone_path, depth=1)
        print(f'cloned {repo_full_name}')
    except git.exc.GitError as e:
        print(f'error cloning  {repo_full_name}')
        with lock:
            with open('errors.csv', 'a', encoding='utf-8') as error_log:
                error = e.__str__().replace("'", "").replace("\n", "")
                str= f"{repo_full_name},{repo_url},'{error}'"
                error_log.write(str + '\n')
            return
    print(f'analyzed {repo_full_name}')
    print(f'saving {repo_full_name}')
    with lock:
        try:
            cloned_log = pd.read_csv('cloned_log.csv')
            cloned_log = cloned_log.append(row, ignore_index=True)
            cloned_log.to_csv('cloned_log.csv', index=False)
        except:
            print(f'error saving {repo_full_name}')
    print(f'saved {repo_full_name}')

    # Return top-level directory to optionally delete
    if no_repos2:
        return os.path.join(output_path, repo_full_name.split("/")[0])
    else:
        return os.path.join(output_path, "repos2", repo_full_name.split("/")[0])
#TEST


# def __search(row,lock,output_path):
#     repo_full_name = row["ProjectName"]
#     repo_url = f'https://github.com/{repo_full_name}.git'
#
#     try:
#         print(f'cloning {repo_full_name}')
#         Repo.clone_from(repo_url, f'{output_path}/repos2/{repo_full_name}', depth=1) #added depth to clone only the last version of the repo
#         print(f'cloned {repo_full_name}')
#     except git.exc.GitError as e:
#         print(f'error cloning  {repo_full_name}')
#         with lock:
#             with open('errors.csv', 'a', encoding='utf-8') as error_log:
#                 error = e.__str__().replace("'", "").replace("\n", "")
#                 str= f"{repo_full_name},{repo_url},'{error}'"
#                 error_log.write(str + '\n')
#             return
#     print(f'analyzed {repo_full_name}')
#     print(f'saving {repo_full_name}')
#     with lock:
#         try:
#             cloned_log = pd.read_csv('cloned_log.csv')
#             cloned_log = cloned_log.append(row, ignore_index=True)
#             cloned_log.to_csv('cloned_log.csv', index=False)
#         except:
#             print(f'error saving {repo_full_name}')
#     print(f'saved {repo_full_name}')
#     to_delete = "repos2/" + repo_full_name.split("/")[0]
#     return to_delete


def delete_repos(to_delete):
    shutil.rmtree(to_delete)
    print(f'deleted {to_delete}')


# def start_search(iterable,output_path, max_workers=None):
#     writer_lock = Lock()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         for repo in iterable:
#             _ = executor.submit(__search, repo, writer_lock, output_path)


# TEST
def start_search(iterable, output_path, no_repos2=True, max_workers=None):
    writer_lock = Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for repo in iterable:
            _ = executor.submit(__search, repo, writer_lock, output_path, no_repos2)


def main(input_file='Baseline_2nd_part.csv', output_path='', no_repos2=True):
    df = pd.read_csv(f'{input_file}', delimiter=",")
    df = df.head(50)

    if os.path.exists('cloned_log.csv'):
        cloned_log = pd.read_csv('cloned_log.csv', delimiter=",")
        df = df[~df['ProjectName'].isin(cloned_log['ProjectName'])]
        print(f"{len(df)} repositories left to clone (already filtered)")
    else:
        cloned_log = pd.DataFrame(columns=['ProjectName', 'repo_url', 'ml_libs', 'count'])
        cloned_log.to_csv('cloned_log.csv', index=False)

    print("Total repositories to process: " + str(len(df)))

    if no_repos2:
        os.makedirs(f'{output_path}', exist_ok=True)
    else:
        os.makedirs(f'{output_path}/repos2', exist_ok=True)

    iterable = [x for _, x in df.iterrows()]
    print(f'To analyze: {len(iterable)} repos')
    start_search(iterable, output_path, no_repos2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This component allows cloning GitHub repositories from a dataset of Python projects."
    )
    parser.add_argument("--input", type=str, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, help="Path to the output folder")
    parser.add_argument("--no-repos2", action="store_true", help="If set, repositories will be cloned directly into the output folder (no repos2/)")

    args = parser.parse_args()
    input_file = args.input
    output_path = args.output
    no_repos2 = args.no_repos2   # False se --no-repos2 NON è passato

    if input_file is None or output_path is None:
        print("Usage: python cloner.py --input <csv_file> --output <output_folder> [--no-repos2]")
        exit(1)

    main(input_file, output_path, no_repos2)
# TEST


# def main(input_file='Baseline_2nd_part.csv',output_path=''):
#     df = pd.read_csv(f'{input_file}', delimiter=",")
#     df = df.head(50)
#     if(os.path.exists('cloned_log.csv')):
#         cloned_log = pd.read_csv('cloned_log.csv', delimiter=",")
#         df = df[~df['ProjectName'].isin(cloned_log['ProjectName'])]
#         print(len(df))
#     else:
#         cloned_log = pd.DataFrame(columns=['ProjectName', 'repo_url','ml_libs','count'])
#         cloned_log.to_csv('cloned_log.csv', index=False)
#     print("The size of results is "+str(len(df)))
#
#     already_analyzed = None
#     error = None
#     os.makedirs(f'{output_path}/repos', exist_ok=True)
#
#     iterable = [x for y, x in df.iterrows()]
#     print(f'to analyze: {len(iterable)} repos')
#     start_search(iterable,output_path)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="This component allow to clone automatically Github Repositories from a dataset "
#                                                  "for Python projects")
#     parser.add_argument("--input", type=str, help="Path to the input folder")
#     parser.add_argument("--output", type=str, help="Path to the output folder")
#     args = parser.parse_args()
#     input = args.input
#     output = args.output
#     if input is None:
#         print("No input folder provided, use the command as follows: python cloner.py --input <input_folder> --output <output_folder>")
#         exit(1)
#     if output is None:
#         print("No output folder provided, use the command as follows: python cloner.py --input <input_folder> --output <output_folder>")
#         exit(1)
#     main(input,output)