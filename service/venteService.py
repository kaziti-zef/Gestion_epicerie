# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:22:03 2026

@author: KAZITI
"""

class VenteService :
    
    def __init__(self , repoV , produitService):
        self.repoV = repoV
        self.produitService = produitService 
        
    def vendre(self , repoV , ventes):
        for vente in ventes : 
            p = self.produitService.chercherProduitId(vente.idP)
            if not p:
                print("Produit non trouvé")
            else :
                if p.estQuantifiable():
                    self.produitService.diminuerStock(vente.idP , vente.quantite)
                else :
                    self.produitService.diminuerStock(vente.idP , vente.montantV)
                self.repoV.ajouterVente(vente)
    
    def lireToutesLesVentes(self):
        return self.repo.lireToutesLesVentes()
        
        