import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{Nedges}"))

        self._view.update_page()

    def handleDettagli(self, e):
        top3Archi = self._model.getTop3Archi()
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore: ", color="red"))

        for arco in top3Archi:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0].constructorRef} -> {arco[1].constructorRef} ({arco[2]['weight']} piloti condivisi)"))

        numComp, largest, details = self._model.getConnectedComponents()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numComp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(largest)} nodi): ", color="red"))

        for l in largest:
            self._view.txt_result.controls.append(ft.Text(f"{l}"))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decresente:", color="red"))

        for d in details:
            self._view.txt_result.controls.append(ft.Text(f"{d}"))
        self._view.update_page()

    def handleCerca(self, e):
        K = self._view._txtInK.value
        if K == "":
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un valore intero per K", color="red"))
            self._view.update_page()
            return

        try:
            K = int(K)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un valore intero per K", color="red"))
            self._view.update_page()
            return

        best_path, bestscore = self._model.getListaCostruttoriOttima(K)
        if best_path is None:
            self._view.txt_result.controls.append(ft.Text(f"Non ci sono abbastanza componenti connesse distinte", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Lista di costruttori con minor scarto di età dei veterani:", color="red"))
        for c in best_path:
            self._view.txt_result.controls.append(ft.Text(f"{c.constructorRef} ({c.name}) - Pilota più vecchio nato il: {c.oldest_driver_dob}"))

        self._view.txt_result.controls.append(ft.Text(f"Scarto di età dei veterani (in giorni): {bestscore}"))
        youngest_veteran = min(best_path, key=lambda x: x.oldest_driver_dob)
        oldest_veteran = max(best_path, key=lambda x: x.oldest_driver_dob)
        self._view.txt_result.controls.append(ft.Text(f"Costruttore con il veterano più giovane: {youngest_veteran.constructorRef} ({youngest_veteran.oldest_driver_dob})"))
        self._view.txt_result.controls.append(ft.Text(f"Costruttore con il veterano più vecchio: {oldest_veteran.constructorRef} ({oldest_veteran.oldest_driver_dob})"))
        self._view.update_page()

    def fillDDYear(self):
        years = self._model.getYears()
        years.sort(reverse=True)
        for year in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(year))
            self._view._ddAnno2.options.append(ft.dropdown.Option(year))
        self._view.update_page()