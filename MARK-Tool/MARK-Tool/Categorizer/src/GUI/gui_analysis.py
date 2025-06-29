import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
from style_gui import applica_stile


class IGESAnalysisTool:
    def __init__(self, root):
        self.root = root
        applica_stile(root)
        self.root.title("IGES Analysis Tool")
        self.root.geometry("1000x600")

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.github_var = tk.StringVar()
        self.hovered_item_consumers = None
        self.hovered_item_producers = None

        self._build_gui()

    def _build_gui(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)
        self.tabs.bind("<Button-1>", self.close_tab_with_cross)

        self._build_tab_input()
        self._build_tab_output()

    def browse_generic_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=os.path.join(os.path.expanduser("~"), "Desktop"),
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            self.github_var.set(file_path)

    def select_input(self):
        folder = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser("~"), "Desktop"))
        if folder:
            self.input_var.set(folder)

    def select_output(self):
        folder = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser("~"), "Desktop"))
        if folder:
            self.output_var.set(folder)

    def _build_tab_input(self):
        self.tab_input = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_input, text="Input")

        frame1 = ttk.Frame(self.tab_input, padding=20)
        frame1.pack(fill='both', expand=True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=0)
        frame1.columnconfigure(2, weight=0)
        frame1.columnconfigure(3, weight=0)
        frame1.columnconfigure(4, weight=1)

        ttk.Label(frame1, text="Input Folder:").grid(row=0, column=1, sticky="e", pady=5)
        ttk.Entry(frame1, textvariable=self.input_var, width=70).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame1, text="Browse", command=self.select_input).grid(row=0, column=3, pady=5)

        ttk.Label(frame1, text="Output Folder:").grid(row=1, column=1, sticky="e", pady=5)
        ttk.Entry(frame1, textvariable=self.output_var, width=70).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(frame1, text="Browse", command=self.select_output).grid(row=1, column=3, pady=5)

        ttk.Label(frame1, text="GitHub Repo:").grid(row=2, column=1, sticky="e", pady=5)
        ttk.Entry(frame1, textvariable=self.github_var, width=70).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(frame1, text="Browse", command=self.browse_generic_file).grid(row=2, column=3, pady=5)

        ttk.Button(frame1, text="Start Analysis", command=self.esegui_script).grid(row=3, column=1, columnspan=3, pady=20)

    def _build_tab_output(self):
        self.tab_output = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_output, text="Output")

        frame2 = ttk.Frame(self.tab_output, padding=10)
        frame2.pack(fill='both', expand=True)

        frame_top = ttk.LabelFrame(frame2, text="Consumers", padding=5)
        frame_top.pack(side="top", fill="both", expand=True)

        frame_bottom = ttk.LabelFrame(frame2, text="Producers", padding=5)
        frame_bottom.pack(side="bottom", fill="both", expand=True)

        self.tree_consumers = ttk.Treeview(frame_top, columns=["File"], show="headings", height=10)
        self.tree_consumers.heading("File", text="CSV File")
        self.tree_consumers.pack(fill="both", expand=True)

        self.tree_producers = ttk.Treeview(frame_bottom, columns=["File"], show="headings", height=10)
        self.tree_producers.heading("File", text="CSV File")
        self.tree_producers.pack(fill="both", expand=True)

        style = ttk.Style()
        self.tree_consumers.tag_configure("hover", background="#e0e0ff")
        self.tree_producers.tag_configure("hover", background="#e0e0ff")

        self.tree_consumers.bind("<Motion>", self.on_motion_consumers)
        self.tree_consumers.bind("<Leave>", self.on_leave_consumers)
        self.tree_producers.bind("<Motion>", self.on_motion_producers)
        self.tree_producers.bind("<Leave>", self.on_leave_producers)

        self.tree_consumers.bind("<Double-1>", lambda e: self.apri_da_tree(self.tree_consumers, "Consumers"))
        self.tree_producers.bind("<Double-1>", lambda e: self.apri_da_tree(self.tree_producers, "Producers"))

    def esegui_script(self):
        input_path = self.input_var.get()
        output_path = self.output_var.get()
        github_repo = self.github_var.get().strip()

        if not input_path or not output_path:
            messagebox.showwarning("Warning", "Please select both input and output folders.")
            return

        try:
            if github_repo:
                # Verifica tipo file
                if not github_repo.lower().endswith(".csv"):
                    messagebox.showerror("Error", "The selected file is not a CSV file.")
                    return

                try:
                    with open(github_repo, newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        if len(rows) < 2:
                            messagebox.showerror("Error", "The CSV file is empty or contains only the header.")
                            return
                except Exception as e:
                    messagebox.showerror("CSV Read Error", f"Unable to read the CSV file: {e}")
                    return

                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
                cloner_path = os.path.join(base_path, "cloner", "cloner.py")

                comando_cloner = ['python', cloner_path, '--input', github_repo, '--output', input_path, '--no_repos2']
                result_clone = subprocess.run(comando_cloner, capture_output=True, text=True, encoding='latin-1')
                if result_clone.returncode != 0:
                    errore = result_clone.stderr or result_clone.stdout
                    messagebox.showerror("Repository Cloning Error", errore)
                    return

            comando = ['python', '../exec_analysis.py', '--input_path', input_path, '--output_path', output_path]
            result = subprocess.run(comando, capture_output=True, text=True, encoding='latin-1')
            if result.returncode == 0:
                messagebox.showinfo("Success", "Analysis completed successfully.")
                self.aggiorna_explorer(output_path)
                self.tabs.select(self.tab_output)
            else:
                errore = result.stderr or result.stdout
                messagebox.showerror("Script Error", errore)

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def aggiorna_explorer(self, output_path):
        self.tree_consumers.delete(*self.tree_consumers.get_children())
        self.tree_producers.delete(*self.tree_producers.get_children())

        path_c = os.path.join(output_path, "Consumers", "Consumers_Final")
        path_p = os.path.join(output_path, "Producers", "Producers_Final")

        if os.path.isdir(path_c):
            for fname in os.listdir(path_c):
                if fname.lower().endswith(".csv"):
                    self.tree_consumers.insert("", "end", values=[fname])

        if os.path.isdir(path_p):
            for fname in os.listdir(path_p):
                if fname.lower().endswith(".csv"):
                    self.tree_producers.insert("", "end", values=[fname])

    def apri_da_tree(self, treeview, tipo):
        sel = treeview.selection()
        if not sel:
            return
        fname = treeview.item(sel[0], "values")[0]
        base = self.output_var.get()

        if tipo == "Consumers":
            percorso = os.path.join(base, "Consumers", "Consumers_Final", fname)
        else:
            percorso = os.path.join(base, "Producers", "Producers_Final", fname)

        if os.path.isfile(percorso):
            self.crea_tab_csv(percorso)

    def crea_tab_csv(self, percorso):
        try:
            with open(percorso, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                righe = list(reader)
                if not righe:
                    messagebox.showwarning("Empty File", "The file is empty.")
                    return

                header = righe[0]
                dati = righe[1:]

                tab_name = os.path.basename(percorso)

                for i in range(self.tabs.index("end")):
                    if self.tabs.tab(i, "text") == tab_name:
                        self.tabs.select(i)
                        return

                new_tab = ttk.Frame(self.tabs)
                self.tabs.add(new_tab, text=tab_name)
                self.tabs.select(new_tab)

                top_bar = ttk.Frame(new_tab)
                top_bar.pack(fill="x", pady=2, padx=2)

                ttk.Label(top_bar, text=tab_name, font=("Segoe UI", 10, "bold")).pack(side="left")
                ttk.Button(top_bar, text="✕", width=3, command=lambda: self.tabs.forget(new_tab)).pack(side="right", padx=2)

                frame_table = ttk.Frame(new_tab)
                frame_table.pack(fill="both", expand=True)

                table = ttk.Treeview(frame_table, columns=header, show="headings")
                table.pack(side="left", fill="both", expand=True)

                scrollbar_v = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
                scrollbar_v.pack(side="right", fill="y")
                table.configure(yscrollcommand=scrollbar_v.set)

                scrollbar_h = ttk.Scrollbar(new_tab, orient="horizontal", command=table.xview)
                scrollbar_h.pack(side="bottom", fill="x")
                table.configure(xscrollcommand=scrollbar_h.set)

                for col in header:
                    table.heading(col, text=col)
                    table.column(col, width=120, anchor="w")

                for row in dati:
                    table.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("CSV Opening Error", str(e))

    def close_tab_with_cross(self, event):
        x, y = event.x, event.y

        for index in range(self.tabs.index("end")):
            bbox = self.tabs.bbox(index)
            if not bbox:
                continue
            x1, y1, width, height = bbox

            if x1 <= x <= x1 + width and y1 <= y <= y1 + height:
                tab_text = self.tabs.tab(index, "text")
                if tab_text and tab_text.endswith("✕"):
                    approx_char_width = 7
                    text_len = len(tab_text)
                    close_x_start = x1 + (text_len - 2) * approx_char_width

                    if x >= close_x_start:
                        self.tabs.forget(index)
                        return

    def on_motion_consumers(self, event):
        row_id = self.tree_consumers.identify_row(event.y)
        if row_id != self.hovered_item_consumers:
            if self.hovered_item_consumers is not None:
                self.tree_consumers.item(self.hovered_item_consumers, tags=())
            if row_id:
                self.tree_consumers.item(row_id, tags=("hover",))
            self.hovered_item_consumers = row_id

    def on_leave_consumers(self, event):
        if self.hovered_item_consumers is not None:
            self.tree_consumers.item(self.hovered_item_consumers, tags=())
            self.hovered_item_consumers = None

    def on_motion_producers(self, event):
        row_id = self.tree_producers.identify_row(event.y)
        if row_id != self.hovered_item_producers:
            if self.hovered_item_producers is not None:
                self.tree_producers.item(self.hovered_item_producers, tags=())
            if row_id:
                self.tree_producers.item(row_id, tags=("hover",))
            self.hovered_item_producers = row_id

    def on_leave_producers(self, event):
        if self.hovered_item_producers is not None:
            self.tree_producers.item(self.hovered_item_producers, tags=())
            self.hovered_item_producers = None


if __name__ == "__main__":
    root = tk.Tk()
    app = IGESAnalysisTool(root)
    root.mainloop()
