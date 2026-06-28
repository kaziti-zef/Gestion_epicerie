# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:40:46 2026

@author: KAZITI
"""

import tkinter as tk
from Interfaces.facture import Factures

fenetre = tk.Tk()

fenetre.geometry("800x600")

factures = Factures(fenetre)
factures.pack()
fenetre.mainloop()

