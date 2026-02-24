"""Views - Capa de presentación"""
from .main_window import MainWindow
from .vocabulario_view import VocabularioView
from .practica_view import PracticaView
from .generic_table_view import GenericTableView
from .caligrafia_view import CaligrafiaView
from .numeros_view import NumerosView
from .gramatica_view import GramaticaView, ConjugacionView
from .estadisticas_view import EstadisticasView

__all__ = ['MainWindow', 'VocabularioView', 'PracticaView', 'GenericTableView', 
           'CaligrafiaView', 'NumerosView', 'GramaticaView', 'ConjugacionView', 'EstadisticasView']
