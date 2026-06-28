# -*- coding: utf-8 -*-

from repository.produitRepository import ProduitRepository
from repository.venteRepository import VenteRepository
from models.Produit import Produit
from models.Vente import Vente
from service.produitService import ProduitService
from service.venteService import VenteService
import csv
produitRepository = ProduitRepository()
produitService = ProduitService(produitRepository)

venteRepo = VenteRepository()
venteService= VenteService(venteRepo, produitService)

ventes=  []
v1 = Vente("v1" ,"PQ1" ,  1200 , quantite=3  , dateV = "25-06-2026")
v2 = Vente("v2" , "PQ2" , 1000 ,"25-06-2026")
ventes.append(v1)
ventes.append(v2)
 
# Ecriture de la facture 
f =  open("data/Factures/facture1.txt" , "w")
f.write("**********************Facture*******************\n")

for vente in ventes:
    produit = produitService.chercherProduitId(vente.idP)
    if not produit : 
        break
    else : 
        f.write(produit.nom , "\t",  vente.quantite , produit.prixUnitaire , vente.montantV  , "\n")




venteService.vendre(venteRepo, ventes)