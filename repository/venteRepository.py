# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:46:08 2026

@author: KAZITI
"""

fichierVentes = "./data/Ventes.csv"
import csv
import os

class VenteRepository : 
    
    def lireToutesLesVentes(self): 
        with open(fichierVentes , "r" , newline = "" , encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
        
    def ajouterVente(self , vente) :
        nouveau =  "./data/Ventes.csv" 
        if not os.path.exists(nouveau):
            with open ( fichierVentes  , "w" , newline = ""  , encoding="utf-8" ) as f:
                writer = csv.writer(f)
                writer.writerow(["idV" , "idP" , "quantite" , "montantV" , "dateV"])
        with open(fichierVentes , "a" , newline = "" , encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([vente.idV , vente.idP , vente.quantite , vente.montantV])

                
            