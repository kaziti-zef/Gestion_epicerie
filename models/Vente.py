# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:02:36 2026

@author: KAZITI
"""

class Vente : 
    def __init__(self,   idP , totalVente , idV = None , dateV = None , quantite = None):
        self.idV = idV
        self.idP = idP
        self.quantite = quantite
        self.montantV = totalVente
        self.dateV = dateV 
        
        