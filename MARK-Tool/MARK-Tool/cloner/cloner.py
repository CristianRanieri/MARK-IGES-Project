import git
import pandas as pd
from git import Repo
import shutil
import concurrent.futures
from threading import Lock
import os
import argparse


class GitHubRepoCloner:
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path

    # TEST
    # def __search(self, row, lock, no_repos2=True):
    #     repo_full_name = row["ProjectName"]
    #     repo_url = f'https://github.com/{repo_full_name}.git'
    #
    #     # Cloning path
    #     if no_repos2:
    #         clone_path = f'{self.output_path}/{repo_full_name}'
    #     else:
    #         clone_path = f'{self.output_path}/repos2/{repo_full_name}'
    #
    #     try:
    #         print(f'cloning {repo_full_name}')
    #         Repo.clone_from(repo_url, clone_path, depth=1)
    #         print(f'cloned {repo_full_name}')
    #     except git.exc.GitError as e:
    #         print(f'error cloning  {repo_full_name}')
    #         with lock:
    #             with open('errors.csv', 'a', encoding='utf-8') as error_log:
    #                 error = e.__str__().replace("'", "").replace("\n", "")
    #                 str = f"{repo_full_name},{repo_url},'{error}'"
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
    #
    #     # Return top-level directory to optionally delete
    #     if no_repos2:
    #         return os.path.join(self.output_path, repo_full_name.split("/")[0])
    #     else:
    #         return os.path.join(self.output_path, "repos2", repo_full_name.split("/")[0])
    # TEST

    def __search(self, row, lock):
        repo_full_name = row["ProjectName"]
        repo_url = f'https://github.com/{repo_full_name}.git'

        try:
            print(f'cloning {repo_full_name}')
            Repo.clone_from(repo_url, f'{self.output_path}/repos2/{repo_full_name}', depth=1)
            print(f'cloned {repo_full_name}')
        except git.exc.GitError as e:
            print(f'error cloning  {repo_full_name}')
            with lock:
                with open('errors.csv', 'a', encoding='utf-8') as error_log:
                    error = e.__str__().replace("'", "").replace("\n", "")
                    str = f"{repo_full_name},{repo_url},'{error}'"
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

    def start_search(self, iterable, max_workers=None):
        writer_lock = Lock()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for repo in iterable:
                _ = executor.submit(self.__search, repo, writer_lock)

    # TEST
    # def start_search(self, iterable, no_repos2=True, max_workers=None):
    #     writer_lock = Lock()
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #         for repo in iterable:
    #             _ = executor.submit(self.__search, repo, writer_lock, no_repos2)
    # TEST

    def run(self):
        df = pd.read_csv(f'{self.input_file}', delimiter=",")
        df = df.head(50)
        if os.path.exists('cloned_log.csv'):
            cloned_log = pd.read_csv('cloned_log.csv', delimiter=",")
            df = df[~df['ProjectName'].isin(cloned_log['ProjectName'])]
            print(len(df))
        else:
            cloned_log = pd.DataFrame(columns=['ProjectName', 'repo_url', 'ml_libs', 'count'])
            cloned_log.to_csv('cloned_log.csv', index=False)

        print("The size of results is " + str(len(df)))
        os.makedirs(f'{self.output_path}/repos', exist_ok=True)
        iterable = [x for _, x in df.iterrows()]
        print(f'to analyze: {len(iterable)} repos')
        self.start_search(iterable)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This component allows to clone automatically Github Repositories from a dataset "
                                                 "for Python projects")
    parser.add_argument("--input", type=str, help="Path to the input folder")
    parser.add_argument("--output", type=str, help="Path to the output folder")
    args = parser.parse_args()
    input_file = args.input
    output_path = args.output
    if not input_file or not os.path.isfile(input_file):
        print(f"File di input non valido o inesistente: {input_file}")
        print("Usa il comando: python cloner.py --input <input_file.csv> --output <output_folder>")
        exit(0)

    if not output_path:
        print("Nessuna cartella di output specificata.")
        print("Usa il comando: python cloner.py --input <input_file.csv> --output <output_folder>")
        exit(0)

    cloner = GitHubRepoCloner(input_file, output_path)
    cloner.run()
