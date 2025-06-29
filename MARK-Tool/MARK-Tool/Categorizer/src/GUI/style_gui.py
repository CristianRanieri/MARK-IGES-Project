
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def applica_stile(root):
    # Imposta il tema flatly
    root.style = ttk.Style(theme="flatly")

    # Imposta lo sfondo della finestra principale
    root.configure(background=root.style.colors.bg)

    # Configura il font e la dimensione del testo per Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Consolas", 11), rowheight=26)  # Font per righe e altezza riga  Segoe UI,Consolas, Lucida Console, Fira Code, JetBrains Mono
    style.configure("Treeview.Heading", font=("Consolas", 12, "bold"))  # Font per intestazioni

