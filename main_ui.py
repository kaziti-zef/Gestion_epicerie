# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 04:31:45 2026

@author: KAZITI
"""

"""
Lancer l'application : python main_ui.py
(depuis le dossier Gestion_epicerie/)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from repository.produitRepository import ProduitRepository
from repository.venteRepository   import VenteRepository
from service.produitService        import ProduitService
from service.venteService          import VenteService
from Interfaces.app                import App

if __name__ == "__main__":
    produitRepo    = ProduitRepository()
    produitService = ProduitService(produitRepo)
    venteRepo      = VenteRepository()
    venteService   = VenteService(venteRepo, produitService)

    app = App(produitService, venteService, venteRepo)
    app.mainloop()