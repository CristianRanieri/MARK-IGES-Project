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

        cls.input_file_exists = os.path.isfile(cls.csv_input_file)

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
        # Verifica se il file esiste
        if not os.path.isfile(self.csv_input_file):
            print(f"\nFile CSV non trovato: {self.csv_input_file}")
            is_empty_csv = True  # Considera il file come "vuoto" per il test
        else:
            with open(self.csv_input_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                is_empty_csv = len(lines) <= 1

        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "cloner", "cloner.py")),
            "--input", self.csv_input_file,
            "--output", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("\n===== STDOUT =====")
        print(result.stdout)
        print("===== STDERR =====")
        print(result.stderr)

        # Se il comando è terminato con errore, fallo fallire
        if result.returncode != 0:
            self.fail(f"Il comando cloner.py è terminato con errore, returncode={result.returncode}")

        self.repos_base_path = os.path.join(self.temp_output_dir, "repos2")

        if is_empty_csv:
            print(f"\nCSV '{self.csv_input_file}' vuoto o inesistente: verifico che nessuna repo sia stata clonata.")
            self.assertFalse(
                os.path.exists(self.repos_base_path),
                f"La cartella {self.repos_base_path} **non dovrebbe esistere** se il CSV è vuoto o mancante"
            )
            return  # Fine test per file vuoto o inesistente

        # Se arrivi qui significa che il CSV esiste ed è non vuoto
        print(f"\nContenuto di {self.repos_base_path}:")
        if os.path.exists(self.repos_base_path):
            print(os.listdir(self.repos_base_path))
        else:
            print("Cartella 'repos2' non trovata")

        self.assertTrue(os.path.isdir(self.repos_base_path), f"La cartella {self.repos_base_path} non esiste")

        if hasattr(self, "expected_cloned_repositories"):
            found = set()
            for owner in os.listdir(self.repos_base_path):
                owner_path = os.path.join(self.repos_base_path, owner)
                if os.path.isdir(owner_path):
                    for repo in os.listdir(owner_path):
                        repo_path = os.path.join(owner_path, repo)
                        if os.path.isdir(repo_path):
                            found.add(f"{owner}/{repo}")

            expected = set(self.expected_cloned_repositories)

            print(f"\nRepository clonate non corrispondono.\nAttese: {expected}\nTrovate: {found}")
            self.assertEqual(found, expected,
                             f"Repository clonate non corrispondono.\nAttese: {expected}\nTrovate: {found}")


# CL_0
class TestClonerCase0(BaseClonerTest):
    csv_input_file = "Test_input/input/input_non_esiste.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = {

    }

# CL_1
class TestClonerCase1(BaseClonerTest):
    csv_input_file = "Test_input/input/input_1.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = {
    }

# CL_2
class TestClonerCase2(BaseClonerTest):
    csv_input_file = "Test_input/input/input_2.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = [
        "921kiyo/3d-dl"
    ]

# CL_3
class TestClonerCase3(BaseClonerTest):
    csv_input_file = "Test_input/input/input_3.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = [
        "aaronlam88/cmpe295",
        "abdullahselek/koolsla",
        "abreheret/PixelAnnotationTool"
    ]


if __name__ == "__main__":
    unittest.main()
