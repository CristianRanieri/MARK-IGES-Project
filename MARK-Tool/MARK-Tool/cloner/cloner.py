import git
import pandas as pd
from git import Repo
import shutil
import concurrent.futures
from threading import Lock
import os
import argparse

def __search(row, lock, output_path, use_repos2=True):
    repo_full_name = row["ProjectName"]
    repo_url = f'https://github.com/{repo_full_name}.git'

    # Cloning path
    if use_repos2:
        clone_path = f'{output_path}/repos2/{repo_full_name}'
    else:
        clone_path = f'{output_path}/{repo_full_name}'

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
    if use_repos2:
        return os.path.join(output_path, "repos2", repo_full_name.split("/")[0])
    else:
        return os.path.join(output_path, repo_full_name.split("/")[0])


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
#
#
# def delete_repos(to_delete):
#     shutil.rmtree(to_delete)
#     print(f'deleted {to_delete}')



def start_search(iterable,output_path, max_workers=None):
    writer_lock = Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for repo in iterable:
            _ = executor.submit(__search, repo, writer_lock, output_path)



def main(input_file='Baseline_2nd_part.csv',output_path=''):
    df = pd.read_csv(f'{input_file}', delimiter=",")
    df = df.head(50)
    if(os.path.exists('cloned_log.csv')):
        cloned_log = pd.read_csv('cloned_log.csv', delimiter=",")
        df = df[~df['ProjectName'].isin(cloned_log['ProjectName'])]
        print(len(df))
    else:
        cloned_log = pd.DataFrame(columns=['ProjectName', 'repo_url','ml_libs','count'])
        cloned_log.to_csv('cloned_log.csv', index=False)
    print("The size of results is "+str(len(df)))

    already_analyzed = None
    error = None
    os.makedirs(f'{output_path}/repos', exist_ok=True)

    iterable = [x for y, x in df.iterrows()]
    print(f'to analyze: {len(iterable)} repos')
    start_search(iterable,output_path)



#TEST SINGOLA REPO
def main_single_repo(repo_full_name, output_path):
    # Crea una finta riga come se venisse da un DataFrame
    row = pd.Series({"ProjectName": repo_full_name})

    # Se esiste un log dei progetti già clonati, salta quelli già presenti
    if os.path.exists('cloned_log.csv'):
        cloned_log = pd.read_csv('cloned_log.csv', delimiter=",")
        if repo_full_name in cloned_log['ProjectName'].values:
            print(f"{repo_full_name} è già stato clonato, salto.")
            return
    else:
        # Crea il file di log se non esiste
        cloned_log = pd.DataFrame(columns=['ProjectName', 'repo_url','ml_libs','count'])
        cloned_log.to_csv('cloned_log.csv', index=False)

    print(f"Clonazione di un singolo repo: {repo_full_name}")
    to_delete = __search(row, Lock(), output_path, use_repos2=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clona repository da GitHub.")
    parser.add_argument("--input", type=str, help="Percorso del file CSV oppure nome singolo repo (es: user/repo)")
    parser.add_argument("--output", type=str, help="Cartella di output")
    parser.add_argument("--single", action='store_true', help="Se indicato, --input sarà trattato come una singola repo")

    args = parser.parse_args()
    input = args.input
    output = args.output

    if input is None or output is None:
        print("Devi specificare sia --input che --output. Esempio:")
        print("python cloner.py --input user/repo --output path --single")
        exit(1)

    if args.single:
        main_single_repo(input, output)
    else:
        main(input, output)
#TEST SINGOLA REPO


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