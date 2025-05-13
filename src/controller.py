from model import init_db, Session, Candidature, Statut, TypePoste
from view import MainView
from datetime import datetime

class AppController:
    def __init__(self):
        init_db()
        self.session = Session()
        self.view    = MainView()
        self._populate_choices()
        self._bind_events()
        self._load_data()

    def _populate_choices(self):
        self.view.statut_cb['values']    = [s.value for s in Statut]
        self.view.statut_cb.current(0)
        self.view.type_cb['values']      = [t.value for t in TypePoste]
        self.view.type_cb.current(0)

    def _bind_events(self):
        self.view.add_btn   .configure(command=self.on_add)
        self.view.update_btn.configure(command=self.on_update)
        self.view.delete_btn.configure(command=self.on_delete)
        self.view.table.bind("<<TreeviewSelect>>", self.on_select)

    def _load_data(self):
        for cand in Candidature.query_all(self.session):
            self._insert_row(cand)

    def _insert_row(self, cand):
        self.view.table.insert("", "end", iid=cand.id, values=(
            cand.date_candidature, cand.entreprise, cand.titre_poste, cand.lieu,
            cand.type_poste.value, cand.heures_semaine or '', cand.salaire or '',
            cand.statut.value, cand.url, cand.plateforme,
            cand.date_entretien or '', cand.date_prise_poste or ''
        ))

    def on_add(self):
        data = {
            'date_candidature': self.view.date_entry.get_date(),
            'nom_contact'     : self.view.contact_entry.get(),
            'titre_poste'     : self.view.titre_entry.get(),
            'lieu'            : self.view.lieu_entry.get(),
            'type_poste'      : TypePoste(self.view.type_cb.get()),
            'heures_semaine'  : float(self.view.heures_entry.get() or 0),
            'url'             : self.view.url_entry.get(),
            'salaire'         : float(self.view.salaire_entry.get() or 0),
            'plateforme'      : self.view.plateforme_entry.get(),
            'entreprise'      : self.view.entr_entry.get(),
            'statut'          : Statut(self.view.statut_cb.get()),
        }
        cand = Candidature(**data)
        cand.save(self.session)
        self._insert_row(cand)

    def on_update(self):
        sel = self.view.table.selection()
        if not sel: return
        cand = self.session.query(Candidature).get(int(sel[0]))
        cand.nom_contact       = self.view.contact_entry.get()
        cand.titre_poste       = self.view.titre_entry.get()
        cand.lieu              = self.view.lieu_entry.get()
        cand.type_poste        = TypePoste(self.view.type_cb.get())
        cand.heures_semaine    = float(self.view.heures_entry.get() or 0)
        cand.url               = self.view.url_entry.get()
        cand.salaire           = float(self.view.salaire_entry.get() or 0)
        cand.plateforme        = self.view.plateforme_entry.get()
        cand.entreprise        = self.view.entr_entry.get()
        cand.statut            = Statut(self.view.statut_cb.get())
        self.session.commit()
        self.view.table.item(cand.id, values=(
            cand.date_candidature, cand.entreprise, cand.titre_poste, cand.lieu,
            cand.type_poste.value, cand.heures_semaine or '', cand.salaire or '',
            cand.statut.value, cand.url, cand.plateforme,
            cand.date_entretien or '', cand.date_prise_poste or ''
        ))

    def on_delete(self):
        sel = self.view.table.selection()
        if not sel: return
        cand = self.session.query(Candidature).get(int(sel[0]))
        if messagebox.askyesno("Confirmer", "Supprimer cette candidature ?"):
            cand.delete(self.session)
            self.view.table.delete(cand.id)

    def on_select(self, event):
        sel = self.view.table.selection()
        if not sel: return
        cand = self.session.query(Candidature).get(int(sel[0]))
        self.view.date_entry.set_date(cand.date_candidature)
        self.view.contact_entry.delete(0, 'end'); self.view.contact_entry.insert(0, cand.nom_contact or '')
        self.view.titre_entry.delete(0, 'end'); self.view.titre_entry.insert(0, cand.titre_poste or '')
        self.view.lieu_entry.delete(0, 'end'); self.view.lieu_entry.insert(0, cand.lieu or '')
        self.view.type_cb.set(cand.type_poste.value)
        self.view.heures_entry.delete(0, 'end'); self.view.heures_entry.insert(0, cand.heures_semaine or '')
        self.view.url_entry.delete(0, 'end'); self.view.url_entry.insert(0, cand.url or '')
        self.view.salaire_entry.delete(0, 'end'); self.view.salaire_entry.insert(0, cand.salaire or '')
        self.view.plateforme_entry.delete(0, 'end'); self.view.plateforme_entry.insert(0, cand.plateforme or '')
        self.view.entr_entry.delete(0, 'end'); self.view.entr_entry.insert(0, cand.entreprise)
        self.view.statut_cb.set(cand.statut.value)

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    AppController().run()