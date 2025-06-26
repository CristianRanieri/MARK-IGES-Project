import unittest
import subprocess
import os
import sys
import pandas as pd


class BaseRepoCheckerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cls.script_path = os.path.join(current_dir, "cloning_check_script_test.py")  # Assicurati che il nome sia corretto
        cls.input_csv = os.path.abspath(cls.input_csv)
        cls.repos_path = os.path.abspath(cls.repos_path)

        assert os.path.isfile(cls.script_path), f"Script non trovato: {cls.script_path}"
        assert os.path.isfile(cls.input_csv), f"CSV non trovato: {cls.input_csv}"
        assert os.path.isdir(cls.repos_path), f"Cartella repos2 non trovata: {cls.repos_path}"

    def tearDown(self):
        for file in ["not_cloned_repos.csv", "effective_repos.csv"]:
            if os.path.exists(file):
                os.remove(file)

    def test_repo_checker_outputs(self):
        cmd = [
            sys.executable,
            self.script_path,
            "--input_file", self.input_csv,
            "--input_path", self.repos_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd= "C:/Users/Cristian/PycharmProjects/MARK-IGES-Project/MARK-Tool/MARK-Tool/Functional_Test/cloning_check_test"  # Imposta la working directory
        )

        print("\n===== STDOUT =====")
        print(result.stdout)
        print("===== STDERR =====")
        print(result.stderr)

        # Verifica file not_cloned_repos.csv
        self.assertTrue(os.path.exists("not_cloned_repos.csv"), "File not_cloned_repos.csv non trovato")
        expected_not_cloned = set(self.expected_not_cloned)

        if os.path.getsize("not_cloned_repos.csv") > 0:
            try:
                not_cloned_df = pd.read_csv("not_cloned_repos.csv")
                actual_not_cloned = set(not_cloned_df["ProjectName"])
            except pd.errors.EmptyDataError:
                actual_not_cloned = set()
        else:
            actual_not_cloned = set()

        self.assertFalse(expected_not_cloned - actual_not_cloned,
                         f"Repo mancanti in not_cloned_repos.csv: {expected_not_cloned - actual_not_cloned}")
        self.assertFalse(actual_not_cloned - expected_not_cloned,
                         f"Repo inattese in not_cloned_repos.csv: {actual_not_cloned - expected_not_cloned}")

        # Verifica file effective_repos.csv
        self.assertTrue(os.path.exists("effective_repos.csv"), "File effective_repos.csv non trovato")
        effective_df = pd.read_csv("effective_repos.csv")
        actual_effective = set(effective_df["ProjectName"])
        expected_effective = set(self.expected_effective)

        self.assertFalse(expected_effective - actual_effective,
                         f"Repo mancanti in effective_repos.csv: {expected_effective - actual_effective}")
        self.assertFalse(actual_effective - expected_effective,
                         f"Repo inattese in effective_repos.csv: {actual_effective - expected_effective}")


# Esempio test case 1
class TestRepoCheckerCase1(BaseRepoCheckerTest):
    input_csv = "C:/Users/Cristian/PycharmProjects/MARK-IGES-Project/MARK-Tool/MARK-Tool/Functional_Test/cloning_check_test/Test_input/input/applied_projects_1.csv"
    repos_path = "C:/Users/Cristian/PycharmProjects/MARK-IGES-Project/MARK-Tool/MARK-Tool/Functional_Test/cloning_check_test/Test_input/input/input_1/repos/repos2/"
    expected_effective = [
        "921kiyo/3d-dl",
        "aaronlam88/cmpe295",
        "abdullahselek/koolsla"
    ]
    expected_not_cloned = [
    ]

# Esempio test case 1
class TestRepoCheckerCase2(BaseRepoCheckerTest):
    input_csv = "C:/Users/Cristian/PycharmProjects/MARK-IGES-Project/MARK-Tool/MARK-Tool/Functional_Test/cloning_check_test/Test_input/input/applied_projects_2.csv"
    repos_path = "C:/Users/Cristian/PycharmProjects/MARK-IGES-Project/MARK-Tool/MARK-Tool/Functional_Test/cloning_check_test/Test_input/input/input_2/repos/repos2/"
    expected_effective = [
    ]
    expected_not_cloned = [
        "921kiyo/3d-dl",
        "aaronlam88/cmpe295",
        "abdullahselek/koolsla"
    ]


if __name__ == "__main__":
    unittest.main()
