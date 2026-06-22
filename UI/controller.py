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
        pass

    def handleDettagli(self, e):
        pass

    def handleCerca(self, e):
        pass

