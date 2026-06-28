# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:43:53 2026

@author: KAZITI
"""
import tkinter as tk
from models.Vente import Vente
class Factures(tk.Frame) : 
    def __init__(self , parent):
        self.ligne = 0
        self.btn = None
        self.ventes = []
        super().__init__(parent)
        tk.Label(self, text = "Facture").grid(row=0 , column=0)
        self.nouveauProduit()
        
    def placerBoutons(self):
        if self.btnAdd :
            print("détruit")
            self.btnAdd.destroy()
            self.btnPrint.destroy()
        self.btnAdd = tk.Button(self , 
                  text= "Ajouter", 
                  command= self.nouveauProduit
                  )
        self.btnPrint = tk.Button(self , 
                  text= "Imprimer", 
                  command= self.imprimer
                  )
        self.btnAdd.grid(row = self.ligne +1 , column= 2 ) 
        self.btnPrint.grid(row = self.ligne +2 , column= 2 ) 
  
    def nouveauProduit(self):
        tk.Entry(self ).grid(row= self.ligne + 1 , column=0)
        tk.Entry(self ).grid(row=self.ligne + 1 , column=1)
        tk.Entry(self ).grid(row=self.ligne + 1 , column=2)
        
        self.ligne +=1
        self.placerBoutons()
    
    def ajouterVente( idP, montantV , qte):
        ventes.append(Vente(idP = idP , montantV = montantV , quantite=qte))
        
        
        
        
        
        
        
        
        
        
        
        
        
        