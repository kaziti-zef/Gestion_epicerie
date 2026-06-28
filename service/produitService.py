# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:59:32 2026

@author: KAZITI
"""
from models.Produit import Produit
class ProduitService : 
    def __init__(self, repo):
        self.repo = repo
    
    def lireTous(self):
        return self.repo.lireTous()
        
    def ajouter(self , produit):
        print("ajout")
        self.repo.ajouterProduit(produit)
        
    def vendre(self, produit , valeur) :
        if produit.estQuantifiable():
            produit.quantite -= valeur
        else : 
            produit.total -= valeur
            
    def ajouterStock(self , produitId , valeur):
        produit = self.chercherProduitParId(produitId)
        if produit.estQuantifiable():
            produit.quantite += float( valeur )
        else : 
            produit.total += float( valeur )
            
            

    
    def augmenterStock(self ,idP,  surplus):
        p = self.repo.chercherProduitId(idP)
        if not p:
            print("produit non trouvé")
        else :
            if p.estQuantifiable() : 
                p.quantite += surplus
            else:
                p.total += surplus
            self.repo.modifierProduit(p)
    def diminuerStock(self ,idP ,  malus):
        p = self.chercherProduitId(idP)
        if not p:
            print("produit non trouvé")
        else :
            print("icii " ,type(p.quantite) )
            if p.estQuantifiable() : 
                p.quantite -= float(malus)
            else:
                p.total -= float(malus)
            self.modifierProduit(p) 
            
            
    def changerNom(self ,idP,  nouveauNom):
        p = self.chercherProduitId(idP)
        if not p:
            print("produit non trouvé")
        else :
            p.nom = nouveauNom
            self.repo.modifierProduit(p)
    def changerPrix(self , nouveauPrix):
        pass
    
    def chercherProduitId(self, idP): 
        dic = self.lireTous()
        for el  in dic :
            if(el["idP"] == idP ):
                produit = Produit(idP =  el["idP"] , nom = el["nom"]  , quantite =  None if el["quantite"] == "" else int(el["quantite"])  ,
                                  prixUnitaire = None if  el["prixUnitaire"]  == ""  else float(el["prixUnitaire"]) , total = None if el["total"] == "" else float(el["total"]) )
                return produit
        
        return False
    
    def supprimerProduit(self , idP):
        dic = self.lireTous()
        new = []
        for el in dic: 
            if el.idP != idP :
                new.append(el)
        
        self.repo.reecireTous(new)
    def chercherProduitParNom(self , nom):
        dic = self.lireTous()
        for el  in dic : 
            if(el.nom == nom):
                produit = Produit(idP =  el.idP , nom = el.nom , quantite = None if  el.quantite == ""  else int(el.quantite) , prixUnitaire = None if el.prixUnitaire == "" else float(el.prixUnitaire) , total = None if el.total == "" else float(el.total))
                return produit
    def modifierProduit(self , produit):
        reader = self.lireTous()
        new = []
        for el in reader: 
            if el["idP"] == produit.idP :
                new.append({"idP" : produit.idP , "nom" : produit.nom , "quantite" : produit.quantite , "prixUnitaire" : produit.prixUnitaire ,"total" : produit.total})
            else : 
                new.append(el)
        print(new)
        self.repo.reecireTous(new)    
            
        
    
 