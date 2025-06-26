import unittest
import subprocess
import os
import sys
import shutil
import stat


class BaseClonerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.csv_input_file = os.path.abspath(cls.csv_input_file)
        cls.temp_output_dir = os.path.abspath(cls.temp_output_dir)

        assert os.path.isfile(cls.csv_input_file), f"File CSV input non valido: {cls.csv_input_file}"
        assert os.path.isdir(cls.temp_output_dir), f"Output path non valido: {cls.temp_output_dir}"

        cls.repos_base_path = os.path.join(cls.temp_output_dir, "repos2")

    @staticmethod
    def handle_remove_readonly(func, path, exc):
        if isinstance(exc, PermissionError) and func in (os.rmdir, os.remove, os.unlink):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise exc

    def tearDown(self):
        if os.path.exists(self.repos_base_path):
            shutil.rmtree(self.repos_base_path, onexc=self.handle_remove_readonly)

    def test_cloner_expected_files(self):
        # Comando per eseguire cloner.py
        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "cloner", "cloner.py")),
            "--input", self.csv_input_file,
            "--output", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Debug output dello script
        print("\n===== STDOUT =====")
        print(result.stdout)
        print("===== STDERR =====")
        print(result.stderr)

        # Path previsto in base alla struttura: output/repos/repos2
        self.repos_base_path = os.path.join(self.temp_output_dir,"repos2")

        # Debug contenuto cartelle
        print(f"\nContenuto di {self.temp_output_dir}:")
        if os.path.exists(self.temp_output_dir):
            print(os.listdir(self.temp_output_dir))
        else:
            print("Cartella di output non trovata")

        repos_path = os.path.join(self.temp_output_dir, "repos")
        print(f"\nContenuto di {repos_path}:")
        if os.path.exists(repos_path):
            print(os.listdir(repos_path))
        else:
            print("Cartella 'repos' non trovata")

        print(f"\nContenuto di {self.repos_base_path}:")
        if os.path.exists(self.repos_base_path):
            print(os.listdir(self.repos_base_path))
        else:
            print("Cartella 'repos2' non trovata")

        # Verifica che la cartella esista
        self.assertTrue(os.path.isdir(self.repos_base_path), f"La cartella {self.repos_base_path} non esiste")

        # Verifica che tutte le repo attese siano presenti
        cloned_repos = os.listdir(self.repos_base_path)
        for owner, repo in self.expected_repo_map.items():
            owner_path = os.path.join(self.repos_base_path, owner)
            full_repo_path = os.path.join(owner_path, repo)

            self.assertTrue(os.path.isdir(full_repo_path), f"Directory non trovata: {full_repo_path}")

            # Verifica che la directory contenga almeno un file o cartella
            contents = os.listdir(full_repo_path)
            self.assertTrue(contents, f"La directory {full_repo_path} è vuota")


class TestClonerCase1(BaseClonerTest):
    csv_input_file = "Test_input/input/input_1.csv"
    temp_output_dir = "Test_input/output"
    expected_repo_map = {
        "921kiyo": "3d-dl",
        "aaronlam88": "cmpe295",
        "abdullahselek": "koolsla"
    }


class TestClonerCase2(BaseClonerTest):
    csv_input_file = "Test_input/repos_list_2.csv"
    temp_output_dir = "Test_output/output"
    expected_cloned_repositories = [
        "repoA",
        "repoB"
    ]


if __name__ == "__main__":
    unittest.main()
