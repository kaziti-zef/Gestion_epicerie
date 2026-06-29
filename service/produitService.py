# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:59:32 2026

@author: KAZITI
"""
# -*- coding: utf-8 -*-
from models.Produit import Produit


class ProduitService:
    def __init__(self, repo):
        self.repo = repo

    # ---------- Lecture ----------
    def lireTous(self):
        return self.repo.lireTous()

    def chercherProduitId(self, idP):
        for el in self.lireTous():
            if el["idP"] == idP:
                return self._dictVersProduit(el)
        return None

    def chercherProduitParNom(self, nom):
        for el in self.lireTous():
            if el["nom"].lower() == nom.lower():
                return self._dictVersProduit(el)
        return None

    # ---------- Écriture ----------
    def ajouter(self, produit):
        produit.idP = self.repo.genererNouvelId()
        self.repo.ajouterProduit(produit)
        return produit.idP

    def modifierProduit(self, produit):
        lignes = self.lireTous()
        nouvelles = []
        for el in lignes:
            if el["idP"] == produit.idP:
                nouvelles.append({
                    "idP":          produit.idP,
                    "nom":          produit.nom,
                    "quantite":     produit.quantite if produit.quantite is not None else "",
                    "prixUnitaire": produit.prixUnitaire if produit.prixUnitaire is not None else "",
                    "total":        produit.total if produit.total is not None else "",
                })
            else:
                nouvelles.append(el)
        self.repo.reecireTous(nouvelles)

    def supprimerProduit(self, idP):
        lignes = self.lireTous()
        nouvelles = [el for el in lignes if el["idP"] != idP]
        self.repo.reecireTous(nouvelles)

    # ---------- Stock ----------
    def diminuerStock(self, idP, valeur):
        p = self.chercherProduitId(idP)
        if not p:
            return
        if p.estQuantifiable():
            p.quantite = (p.quantite or 0) - float(valeur)
        else:
            p.total = (p.total or 0) - float(valeur)
        self.modifierProduit(p)

    def augmenterStock(self, idP, valeur):
        p = self.chercherProduitId(idP)
        if not p:
            return
        if p.estQuantifiable():
            p.quantite = (p.quantite or 0) + float(valeur)
        else:
            p.total = (p.total or 0) + float(valeur)
        self.modifierProduit(p)

    # ---------- Utilitaire ----------
    def _dictVersProduit(self, el):
        return Produit(
            idP=el["idP"],
            nom=el["nom"],
            quantite=None if el["quantite"] == "" else float(el["quantite"]),
            prixUnitaire=None if el["prixUnitaire"] == "" else float(el["prixUnitaire"]),
            total=None if el["total"] == "" else float(el["total"]),
        )