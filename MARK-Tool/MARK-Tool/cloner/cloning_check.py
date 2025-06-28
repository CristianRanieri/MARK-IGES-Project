import os
import pandas as pd

class RepoChecker:
    def __init__(self, input_file='./applied_projects.csv', input_path='../repos/repos2/'):
        self.input_file = input_file
        self.input_path = input_path

    def check_cloned_repo(self, project_name):
        if os.path.exists(self.input_path + (project_name.split('/')[0])):
            if len(os.listdir(self.input_path + project_name.split('/')[0])) > 0:
                return True
            return False
        else:
            return False

    def get_not_cloned_list(self, df):
        not_cloned = []
        for index, row in df.iterrows():
            if not self.check_cloned_repo(row['ProjectName']):
                not_cloned.append(row)
        return not_cloned

    def get_cloned_list(self, df):
        cloned = []
        for index, row in df.iterrows():
            if self.check_cloned_repo(row['ProjectName']):
                cloned.append(row)
        return cloned

    def count_effective_repos(self):
        dirs = os.listdir(self.input_path)
        count = 0
        for dir in dirs:
            count += len(os.listdir(self.input_path + dir))
        return count

    def get_effective_repos(self):
        repos = pd.DataFrame(columns=['ProjectName', 'repo_path'])
        dirs = os.listdir(self.input_path)
        for dir in dirs:
            for repo in os.listdir(self.input_path + dir):
                repos = pd.concat([repos,
                    pd.DataFrame({'ProjectName': f'{dir}/{repo}',
                                  'repo_path': self.input_path + dir + '/' + repo}, index=[0])],
                    ignore_index=True)
        return repos

    def clean_log(self):
        if os.path.exists('not_cloned_repos.csv'):
            os.remove('not_cloned_repos.csv')

    def run(self):
        # Controlli su input
        if not os.path.isfile(self.input_file):
            print(f"Errore: il file di input '{self.input_file}' non esiste.")
            return

        if not os.path.isdir(self.input_path):
            print(f"Errore: la directory di input '{self.input_path}' non esiste.")
            return

        self.clean_log()
        df = pd.read_csv(f'{self.input_file}', delimiter=",")
        not_cloned = self.get_not_cloned_list(df)
        cloned = self.get_cloned_list(df)
        print(f'cloned: {len(cloned)} repos2')
        print(f'not cloned: {len(not_cloned)} repos2')
        not_cloned_df = pd.DataFrame(not_cloned)
        not_cloned_df.to_csv('not_cloned_repos.csv', index=False)
        print(f'effective repos: {self.count_effective_repos()}')
        effective_repos = self.get_effective_repos()
        effective_repos.to_csv('effective_repos.csv', index=False)

if __name__ == '__main__':
    checker = RepoChecker()
    checker.run()
