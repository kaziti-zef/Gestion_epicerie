# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:22:03 2026

@author: KAZITI
"""
# -*- coding: utf-8 -*-
from models.Vente import Vente
from datetime import date


class VenteService:
    def __init__(self, repoV, produitService):
        self.repoV = repoV
        self.produitService = produitService

    def vendre(self, lignesFacture):
        """
        lignesFacture : liste de dicts
            { "idP": str, "quantite": float|None, "montantV": float }
        Retourne la liste des idV créés.
        """
        ids_crees = []
        today = date.today().strftime("%d-%m-%Y")
        for ligne in lignesFacture:
            p = self.produitService.chercherProduitId(ligne["idP"])
            if not p:
                raise ValueError(f"Produit {ligne['idP']} introuvable")
            idV = self.repoV.genererNouvelId()
            vente = Vente(
                idV=idV,
                idP=ligne["idP"],
                totalVente=ligne["montantV"],
                dateV=today,
                quantite=ligne.get("quantite"),
            )
            self.repoV.ajouterVente(vente)
            self.produitService.diminuerStock(ligne["idP"], ligne.get("quantite") or ligne["montantV"])
            ids_crees.append(idV)
        return ids_crees

    def lireToutesLesVentes(self):
        return self.repoV.lireToutesLesVentes()