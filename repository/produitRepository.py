# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:06:37 2026

@author: KAZITI
"""
# -*- coding: utf-8 -*-
import csv
import os
from models.Produit import Produit

FICHIER_PRODUITS = "data/Produits.csv"
ENTETE = ["idP", "nom", "quantite", "prixUnitaire", "total"]


class ProduitRepository:

    def lireTous(self):
        if not os.path.exists(FICHIER_PRODUITS):
            return []
        with open(FICHIER_PRODUITS, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def reecireTous(self, lignes):
        with open(FICHIER_PRODUITS, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ENTETE)
            writer.writeheader()
            for ligne in lignes:
                writer.writerow({
                    "idP":          ligne["idP"],
                    "nom":          ligne["nom"],
                    "quantite":     ligne["quantite"] if ligne["quantite"] is not None else "",
                    "prixUnitaire": ligne["prixUnitaire"] if ligne["prixUnitaire"] is not None else "",
                    "total":        ligne["total"] if ligne["total"] is not None else "",
                })

    def ajouterProduit(self, produit):
        nouveau = not os.path.exists(FICHIER_PRODUITS)
        with open(FICHIER_PRODUITS, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if nouveau:
                writer.writerow(ENTETE)
            writer.writerow([
                produit.idP,
                produit.nom,
                produit.quantite if produit.quantite is not None else "",
                produit.prixUnitaire if produit.prixUnitaire is not None else "",
                produit.total if produit.total is not None else "",
            ])

    def genererNouvelId(self):
        lignes = self.lireTous()
        nums = []
        for l in lignes:
            idP = l["idP"]
            if idP.startswith("PQ") and idP[2:].isdigit():
                nums.append(int(idP[2:]))
        prochain = max(nums, default=0) + 1
        return f"PQ{prochain}"