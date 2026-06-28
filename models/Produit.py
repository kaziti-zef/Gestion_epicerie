# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:10:03 2026

@author: KAZITI
"""

class Produit() : 
    def __init__(self,idP , nom  , quantite = None , prixUnitaire = None ,total = None ):
        self.nom = nom
        self.idP = idP
        self.total = total
        self.quantite = quantite
        self.prixUnitaire  = prixUnitaire
        
    def estQuantifiable(self):
        return self.quantite is not None
