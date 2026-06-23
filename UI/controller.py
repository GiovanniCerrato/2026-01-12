import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno1 = None
        self._anno2 = None

    def fillDDAnni(self):
        allYears = self._model.getAllYears()
        for y in allYears:
            self._view._ddAnno1.options.append(ft.dropdown.Option(key=y,on_click = self._handleAnno1))
            self._view._ddAnno2.options.append(ft.dropdown.Option(key=y,on_click = self._handleAnno2))

    def _handleAnno1(self,e):
        self._anno1 = e.control.key
        print(self._anno1, type(self._anno1))

    def _handleAnno2(self,e):
        self._anno2 = e.control.key
        print(self._anno2, type(self._anno2))





    def handleCreaGrafo(self,e):
        if self._anno1 == None or self._anno2  == None or self._anno1>self._anno2:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare un range di anni valido!"))
            self._view.update_page()
            return
        self._model.buildGraph(self._anno1,self._anno2)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:",color="red"))
        nNodi,nArchi = self._model.getNumNodiArchi()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
        self._view._btnstampa.disabled = False
        self._view.update_page()
        return

    def handleDettagli(self, e):
        self._view.txt_result.clean()
        topTreArchi = self._model.topTreArchi()
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:",color="red"))
        for a in topTreArchi:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]} ({a[2]["weight"]} piloti condivisi)"))
        nCC = self._model.getNumCC()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nCC} componenti connesse",color="red"))
        compMax = self._model.getMaxCC()
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande: {len(compMax)} nodi",color="red"))
        for n,degree in compMax:
            self._view.txt_result.controls.append(ft.Text(f"{n} (grado= {degree})"))

        self._view.update_page()


        return

    def handleCerca(self, e):
        pass

