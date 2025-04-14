import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()

        if self._mese == 0:
            self._view.create_alert("Selezionare un mese!")
            self._view.update_page()
            return

        um_med = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.append(ft.Text("L'umidita media nel mese selezionato è:"))
        for u in um_med:
            self._view.lst_result.controls.append(ft.Text(f"{u[0]}: {u[1]}"))
        self._view.update_page()
    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()

        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return

        seq_ott, costo = self._model.get_sequenza_ottima(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for s in seq_ott:
            self._view.lst_result.controls.append(ft.Text(s))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

