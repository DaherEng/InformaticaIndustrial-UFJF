from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):
    """
    Classe do aplicativo
    """
    def build(self):
        """
        Método que gera o app
        """
        self._widget = MainWidget()
        return self._widget
    
if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly = True)
    MainApp().run()