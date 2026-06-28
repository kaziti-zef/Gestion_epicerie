# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:06:37 2026

@author: KAZITI
"""
import csv
from models.Produit import Produit 
import os
fichierProduits = "../data/Produits.csv"


class ProduitRepository : 
    
    def lireTous(self) :
        with open(fichierProduits, "r" , newline="" , encoding = "utf-8") as f:
           reader = csv.DictReader(f)
           return list(reader)
            
    def reecireTous(self , reader):
        with open(fichierProduits , "w" , newline = "" , encoding="utf-8" ) as f:
            writer = csv.writer(f)
            writer.writerow(["idP" , "nom" , "quantite" , "prixUnitaire" , "total"])
            print("lignesss----------")
            for ligne in reader:
                print(ligne)
                writer.writerow([ligne["idP"] , ligne["nom"] , ligne["quantite"] , ligne["prixUnitaire"] , ligne["total"]])
                
            
   
                
    def ajouterProduit(self , produit):
        print("dans repo")
        nouveau = not os.path.exists(fichierProduits)
        with open(fichierProduits , "a" , newline = "" , encoding= "utf-8") as f:
            writer = csv.writer(f)
            if nouveau : 
                print("1")
                writer.writerow(["idP" , "nom" , "quantite" , "prixUnitaire" , "total"])
            writer.writerow([produit.idP ,  produit.nom ,produit.quantite , produit.prixUnitaire , produit.total])
             
        
  
        
