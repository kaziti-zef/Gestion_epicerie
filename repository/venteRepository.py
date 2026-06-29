# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:46:08 2026

@author: KAZITI
"""

# -*- coding: utf-8 -*-
import csv
import os

FICHIER_VENTES = "data/Ventes.csv"
ENTETE = ["idV", "idP", "quantite", "montantV", "dateV"]


class VenteRepository:

    def lireToutesLesVentes(self):
        if not os.path.exists(FICHIER_VENTES):
            return []
        with open(FICHIER_VENTES, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def ajouterVente(self, vente):
        nouveau = not os.path.exists(FICHIER_VENTES)
        with open(FICHIER_VENTES, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if nouveau:
                writer.writerow(ENTETE)
            writer.writerow([
                vente.idV,
                vente.idP,
                vente.quantite if vente.quantite is not None else "",
                vente.montantV,
                vente.dateV,
            ])

    def genererNouvelId(self):
        lignes = self.lireToutesLesVentes()
        nums = []
        for l in lignes:
            idV = l["idV"]
            if idV.startswith("V") and idV[1:].isdigit():
                nums.append(int(idV[1:]))
        prochain = max(nums, default=0) + 1
        return f"V{prochain}"