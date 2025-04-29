import os

import pandas as pd


def check_cloned_repo(path,project_name):
    if os.path.exists(path+ (project_name.split('/')[0])):
        #check if the folder contains really file or not
        if len(os.listdir(path+project_name.split('/')[0])) > 0:
            return True
        return False
    else:
        return False

def get_not_cloned_list(df,path):
    not_cloned = []
    for index, row in df.iterrows():
        if not check_cloned_repo(path,row['ProjectName']):
            not_cloned.append(row)
    return not_cloned

def get_cloned_list(df,path):
    cloned = []
    for index, row in df.iterrows():
        if check_cloned_repo(path,row['ProjectName']):
            cloned.append(row)
    return cloned

def count_effective_repos(path):
    dirs = os.listdir(path)
    count = 0
    for dir in dirs:
        count += len(os.listdir(path+dir))
    return count

def get_effective_repos(path):
    repos = pd.DataFrame(columns=['ProjectName', 'repo_path'])
    dirs = os.listdir(path)
    for dir in dirs:
        for repo in os.listdir(path+dir):
            repos = pd.concat([repos,pd.DataFrame({'ProjectName': f'{dir}/{repo}', 'repo_path': path+dir+'/'+repo}, index=[0])], ignore_index=True)
    return repos
def clean_log():
    if os.path.exists('not_cloned_repos.csv'):
        os.remove('not_cloned_repos.csv')

def main(input_file='./applied_projects.csv',input_path='../repos/repos/'):
    clean_log()
    df = pd.read_csv(f'{input_file}', delimiter=",")
    not_cloned = get_not_cloned_list(df,input_path)
    cloned = get_cloned_list(df,input_path)
    print(f'cloned: {len(cloned)} repos')
    print(f'not cloned: {len(not_cloned)} repos')
    not_cloned_df = pd.DataFrame(not_cloned)
    not_cloned_df.to_csv(f'not_cloned_repos.csv', index=False)
    print(f'effective repos: {count_effective_repos(input_path)}')
    effective_repos = get_effective_repos(input_path)
    effective_repos.to_csv(f'effective_repos.csv', index=False)

if __name__ == '__main__':
    main()


