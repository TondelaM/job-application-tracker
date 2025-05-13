import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Suivi des candidatures")
        self.minsize(1200, 600)
        self._build_widgets()

    def _build_widgets(self):
        columns = (
            "date_cand", "entreprise", "titre_poste", "lieu", "type_poste",
            "heures_semaine", "salaire", "statut", "url", "plateforme",
            "date_entretien", "date_poste"
        )
        self.table = ttk.Treeview(self, columns=columns, show='headings')
        headings = {
            "titre_poste": "Titre Poste",
            "entreprise": "Entreprise",
            "lieu": "Lieu",
            "type_poste": "Type Poste",
            "salaire": "Salaire",
            "statut": "Statut",
            "heures_semaine": "Heures/Semaine",
            "url": "URL",
            "date_cand": "Date Candid.",
            "plateforme": "Plateforme",
            "date_entretien": "Date Entretien",
            "date_poste": "Date Prise Poste"
        }
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=100)
        self.table.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        form = ttk.Frame(self)
        labels = [
            ("Date candid.", 'date_entry'), ("Nom contact", 'contact_entry'),
            ("Titre poste", 'titre_entry'), ("Lieu", 'lieu_entry'),
            ("Type poste", 'type_cb'), ("Heures/Semaine", 'heures_entry'),
            ("URL", 'url_entry'), ("Salaire", 'salaire_entry'),
            ("Plateforme", 'plateforme_entry'), ("Entreprise", 'entr_entry'),
            ("Statut", 'statut_cb')
        ]
        for i, (text, attr) in enumerate(labels):
            ttk.Label(form, text=text).grid(row=i, column=0, sticky='w', pady=2)
            if attr.endswith('_cb'):
                setattr(self, attr, ttk.Combobox(form))
            else:
                entry_cls = ttk.Entry if attr.endswith('_entry') else DateEntry
                setattr(self, attr, entry_cls(form))
            getattr(self, attr).grid(row=i, column=1, pady=2)

        btns = ttk.Frame(form)
        self.add_btn    = ttk.Button(btns, text="Ajouter")
        self.update_btn = ttk.Button(btns, text="Modifier")
        self.delete_btn = ttk.Button(btns, text="Supprimer")
        self.add_btn.pack(side='left', padx=5)
        self.update_btn.pack(side='left', padx=5)
        self.delete_btn.pack(side='left', padx=5)
        btns.grid(row=len(labels), columnspan=2, pady=10)

        form.pack(side='right', fill='y', padx=10, pady=10)