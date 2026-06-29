# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 04:33:27 2026

@author: KAZITI
"""

# -*- coding: utf-8 -*-
"""
Point d'entrée de l'interface graphique.
Lance depuis la racine du projet : python -m Interfaces.app
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import os, sys

# ─── Couleurs & constantes ───────────────────────────────────────────────────
BG         = "#F5F6FA"
SIDEBAR_BG = "#1E2A3A"
ACCENT     = "#3A86FF"
ACCENT2    = "#48BFE3"
DANGER     = "#EF233C"
SUCCESS    = "#06D6A0"
TEXT_DARK  = "#1E2A3A"
TEXT_LIGHT = "#FFFFFF"
TEXT_MUTED = "#8D99AE"
CARD_BG    = "#FFFFFF"
BORDER     = "#E2E8F0"
ROW_ALT    = "#F0F4FF"

NAV_ITEMS = [
    ("🧾", "Nouvelle Facture"),
    ("📦", "Produits"),
    ("📊", "Ventes"),
]


# ─── Styles globaux ──────────────────────────────────────────────────────────
def appliquer_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame",       background=BG)
    style.configure("Card.TFrame",  background=CARD_BG, relief="flat")
    style.configure("TLabel",       background=BG, foreground=TEXT_DARK, font=("Segoe UI", 10))
    style.configure("Title.TLabel", background=BG, foreground=TEXT_DARK, font=("Segoe UI", 18, "bold"))
    style.configure("Sub.TLabel",   background=BG, foreground=TEXT_MUTED, font=("Segoe UI", 10))
    style.configure("Card.TLabel",  background=CARD_BG, foreground=TEXT_DARK, font=("Segoe UI", 10))

    style.configure("Accent.TButton",
        background=ACCENT, foreground=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"), borderwidth=0,
        focusthickness=0, padding=(14, 8))
    style.map("Accent.TButton",
        background=[("active", "#2563EB"), ("pressed", "#1D4ED8")])

    style.configure("Danger.TButton",
        background=DANGER, foreground=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"), borderwidth=0,
        focusthickness=0, padding=(14, 8))
    style.map("Danger.TButton",
        background=[("active", "#C1121F")])

    style.configure("Success.TButton",
        background=SUCCESS, foreground=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"), borderwidth=0,
        focusthickness=0, padding=(14, 8))
    style.map("Success.TButton",
        background=[("active", "#05A37A")])

    style.configure("Ghost.TButton",
        background=BG, foreground=ACCENT,
        font=("Segoe UI", 10), borderwidth=1,
        relief="solid", padding=(10, 6))
    style.map("Ghost.TButton",
        background=[("active", ROW_ALT)])

    style.configure("TEntry",
        fieldbackground=CARD_BG, foreground=TEXT_DARK,
        borderwidth=1, relief="solid",
        font=("Segoe UI", 10), padding=6)

    style.configure("TCombobox",
        fieldbackground=CARD_BG, foreground=TEXT_DARK,
        borderwidth=1, selectbackground=ACCENT,
        font=("Segoe UI", 10), padding=6)
    style.map("TCombobox",
        fieldbackground=[("readonly", CARD_BG)])

    style.configure("Treeview",
        background=CARD_BG, foreground=TEXT_DARK,
        rowheight=30, fieldbackground=CARD_BG,
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
        background=SIDEBAR_BG, foreground=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
    style.map("Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", TEXT_LIGHT)])

    style.configure("TSeparator", background=BORDER)
    style.configure("TScrollbar",
        background=BORDER, troughcolor=BG,
        borderwidth=0, arrowcolor=TEXT_MUTED)


# ─── Application principale ──────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self, produitService, venteService, venteRepo):
        super().__init__()
        self.produitService = produitService
        self.venteService   = venteService
        self.venteRepo      = venteRepo

        self.title("Épicerie Manager")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(bg=SIDEBAR_BG)
        appliquer_styles(self)

        self._build_ui()
        self._nav_select(0)

    def _build_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / titre
        tk.Label(self.sidebar, text="🛒", bg=SIDEBAR_BG, fg=TEXT_LIGHT,
                 font=("Segoe UI", 28)).pack(pady=(28, 4))
        tk.Label(self.sidebar, text="Épicerie", bg=SIDEBAR_BG, fg=TEXT_LIGHT,
                 font=("Segoe UI", 13, "bold")).pack()
        tk.Label(self.sidebar, text="Manager", bg=SIDEBAR_BG, fg=ACCENT2,
                 font=("Segoe UI", 11)).pack(pady=(0, 24))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16)

        # Boutons nav
        self._nav_buttons = []
        for i, (icone, label) in enumerate(NAV_ITEMS):
            btn = tk.Button(
                self.sidebar,
                text=f"  {icone}  {label}",
                anchor="w",
                bg=SIDEBAR_BG,
                fg="#BDC7D5",
                activebackground="#2D3E50",
                activeforeground=TEXT_LIGHT,
                font=("Segoe UI", 11),
                borderwidth=0,
                cursor="hand2",
                pady=12,
                command=lambda idx=i: self._nav_select(idx)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._nav_buttons.append(btn)

        # Bas de sidebar
        tk.Label(self.sidebar, text="v1.0", bg=SIDEBAR_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(side="bottom", pady=12)

        # Zone principale
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        # Pages
        self._pages = {}
        for PageClass, key in [
            (PageFacture,  "facture"),
            (PageProduits, "produits"),
            (PageVentes,   "ventes"),
        ]:
            frame = PageClass(self.main, self)
            frame.place(relwidth=1, relheight=1)
            self._pages[key] = frame

    def _nav_select(self, idx):
        keys = ["facture", "produits", "ventes"]
        for i, btn in enumerate(self._nav_buttons):
            if i == idx:
                btn.configure(bg="#2D3E50", fg=TEXT_LIGHT, font=("Segoe UI", 11, "bold"))
            else:
                btn.configure(bg=SIDEBAR_BG, fg="#BDC7D5", font=("Segoe UI", 11))
        page = self._pages[keys[idx]]
        page.lift()
        if hasattr(page, "on_show"):
            page.on_show()


# ─── Composants utilitaires ──────────────────────────────────────────────────
def card(parent, **kwargs):
    f = tk.Frame(parent, bg=CARD_BG, bd=0, **kwargs)
    f.configure(highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER)
    return f


def label_champ(parent, texte, row, col=0, bg=CARD_BG):
    tk.Label(parent, text=texte, bg=bg, fg=TEXT_MUTED,
             font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", padx=(12, 4), pady=(10, 0))


# ─── PAGE FACTURE ─────────────────────────────────────────────────────────────
class PageFacture(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.lignes = []          # liste de LigneFacture
        self._build()

    def _build(self):
        # En-tête
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=32, pady=(24, 0))
        tk.Label(hdr, text="Nouvelle Facture", bg=BG, fg=TEXT_DARK,
                 font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Button(hdr, text="🖨  Imprimer / Valider", style="Success.TButton",
                   command=self._imprimer).pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=32, pady=12)

        # Scrollable zone lignes
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=32)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.lignes_frame = tk.Frame(canvas, bg=BG)

        self.lignes_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.lignes_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # En-têtes colonnes
        hdrs = ["Produit", "Prix unitaire", "Quantité", "Montant", "Total", ""]
        cols = [280, 120, 100, 120, 100, 40]
        for i, (h, w) in enumerate(zip(hdrs, cols)):
            tk.Label(self.lignes_frame, text=h, bg=BG, fg=TEXT_MUTED,
                     font=("Segoe UI", 9, "bold"), width=w//8, anchor="w"
                     ).grid(row=0, column=i, padx=4, pady=(0, 4), sticky="w")

        # Pied : total + bouton ajouter
        pied = tk.Frame(self, bg=BG)
        pied.pack(fill="x", padx=32, pady=16)
        ttk.Button(pied, text="＋  Ajouter une ligne", style="Ghost.TButton",
                   command=self._ajouter_ligne).pack(side="left")

        total_frame = card(pied)
        total_frame.pack(side="right")
        tk.Label(total_frame, text="TOTAL À PAYER", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(padx=20, pady=(10, 0))
        self.lbl_total = tk.Label(total_frame, text="0 FCFA", bg=CARD_BG, fg=ACCENT,
                                  font=("Segoe UI", 22, "bold"))
        self.lbl_total.pack(padx=20, pady=(0, 10))

        self._ajouter_ligne()

    def on_show(self):
        for ligne in self.lignes:
            ligne.rafraichir_produits()

    def _ajouter_ligne(self):
        row = len(self.lignes) + 1
        ligne = LigneFacture(self.lignes_frame, self, row)
        self.lignes.append(ligne)

    def maj_total(self):
        total = sum(l.get_total() for l in self.lignes)
        self.lbl_total.configure(text=f"{total:,.0f} FCFA".replace(",", " "))

    def _imprimer(self):
        lignes_valides = []
        for l in self.lignes:
            d = l.get_data()
            if d:
                lignes_valides.append(d)

        if not lignes_valides:
            messagebox.showwarning("Facture vide", "Ajoutez au moins un produit.")
            return

        try:
            ids = self.app.venteService.vendre(lignes_valides)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        # Générer fichier texte
        os.makedirs("data/Factures", exist_ok=True)
        num = len(os.listdir("data/Factures")) + 1
        chemin = f"data/Factures/facture_{num:03d}.txt"
        total_global = sum(l["montantV"] for l in lignes_valides)

        with open(chemin, "w", encoding="utf-8") as f:
            f.write("=" * 52 + "\n")
            f.write("            ÉPICERIE MANAGER\n")
            f.write("=" * 52 + "\n")
            from datetime import date
            f.write(f"  Facture n°{num:03d}   Date : {date.today().strftime('%d/%m/%Y')}\n")
            f.write("-" * 52 + "\n")
            f.write(f"{'Produit':<22}{'Qté':>6}{'P.U':>10}{'Total':>12}\n")
            f.write("-" * 52 + "\n")
            for d in lignes_valides:
                p = self.app.produitService.chercherProduitId(d["idP"])
                nom = p.nom if p else d["idP"]
                qte = f"{d['quantite']:.0f}" if d.get("quantite") else "-"
                pu  = f"{p.prixUnitaire:.0f}" if (p and p.prixUnitaire) else "-"
                f.write(f"  {nom:<20}{qte:>6}{pu:>10}{d['montantV']:>10.0f} F\n")
            f.write("=" * 52 + "\n")
            f.write(f"{'TOTAL':>40}  {total_global:>8.0f} F\n")
            f.write("=" * 52 + "\n")
            f.write("        Merci pour votre confiance !\n")

        messagebox.showinfo("Succès",
            f"Vente enregistrée ✅\nFacture sauvegardée : {chemin}")

        # Réinitialiser
        for w in self.lignes_frame.winfo_children():
            if int(w.grid_info().get("row", 0)) > 0:
                w.destroy()
        self.lignes.clear()
        self._ajouter_ligne()
        self.maj_total()


class LigneFacture(tk.Frame):
    def __init__(self, parent, page, row):
        super().__init__(parent, bg=BG)
        self.page = page
        self.row  = row
        self._total_val = 0.0
        self._produit = None

        produits = self._charger_produits()
        noms = [p.nom for p in produits]
        self._produits_map = {p.nom: p for p in produits}

        # Combobox produit
        self.var_produit = tk.StringVar()
        self.combo = ttk.Combobox(parent, textvariable=self.var_produit,
                                   values=noms, width=32, font=("Segoe UI", 10))
        self.combo.grid(row=row, column=0, padx=4, pady=3, sticky="w")
        self.combo.bind("<<ComboboxSelected>>", self._on_select)
        self.combo.bind("<Return>", self._on_select)
        self.combo.bind("<FocusOut>", self._on_select)

        # Champs dynamiques (initialement masqués)
        self.var_pu      = tk.StringVar(value="")
        self.var_qte     = tk.StringVar()
        self.var_montant = tk.StringVar()
        self.var_total   = tk.StringVar(value="0")

        self.ent_pu      = ttk.Entry(parent, textvariable=self.var_pu,    width=14, state="readonly")
        self.ent_qte     = ttk.Entry(parent, textvariable=self.var_qte,   width=12)
        self.ent_montant = ttk.Entry(parent, textvariable=self.var_montant, width=14)
        self.lbl_total   = tk.Label(parent, textvariable=self.var_total, bg=BG,
                                    fg=SUCCESS, font=("Segoe UI", 11, "bold"), width=12, anchor="w")

        self.ent_pu.grid(     row=row, column=1, padx=4, pady=3)
        self.ent_qte.grid(    row=row, column=2, padx=4, pady=3)
        self.ent_montant.grid(row=row, column=3, padx=4, pady=3)
        self.lbl_total.grid(  row=row, column=4, padx=4, pady=3)

        self.ent_qte.bind("<KeyRelease>", self._calc_total)
        self.ent_montant.bind("<KeyRelease>", self._calc_total)

        # Bouton supprimer
        btn_del = tk.Button(parent, text="✕", bg=BG, fg=DANGER,
                            font=("Segoe UI", 11, "bold"), borderwidth=0,
                            cursor="hand2", command=self._supprimer)
        btn_del.grid(row=row, column=5, padx=4)

        # Masquer par défaut
        self._mode = None
        self._cacher_champs()

    def _charger_produits(self):
        from service.produitService import ProduitService
        dicts = self.page.app.produitService.lireTous()
        return [self.page.app.produitService._dictVersProduit(d) for d in dicts]

    def rafraichir_produits(self):
        produits = self._charger_produits()
        noms = [p.nom for p in produits]
        self._produits_map = {p.nom: p for p in produits}
        self.combo["values"] = noms

    def _on_select(self, event=None):
        nom = self.var_produit.get().strip()
        p   = self._produits_map.get(nom)
        if not p:
            p = self.page.app.produitService.chercherProduitParNom(nom)
            if p:
                self._produits_map[nom] = p
        self._produit = p
        if not p:
            self._cacher_champs()
            return
        if p.estQuantifiable():
            self._mode_quantifiable(p)
        else:
            self._mode_montant()

    def _mode_quantifiable(self, p):
        self._mode = "qte"
        pu = p.prixUnitaire or 0
        self.var_pu.set(f"{pu:.0f}")
        self.var_qte.set("")
        self.var_montant.set("")
        self.var_total.set("0")
        self.ent_pu.grid()
        self.ent_qte.grid()
        self.ent_montant.grid_remove()
        self.lbl_total.grid()

    def _mode_montant(self):
        self._mode = "montant"
        self.var_pu.set("")
        self.var_qte.set("")
        self.var_montant.set("")
        self.var_total.set("0")
        self.ent_pu.grid_remove()
        self.ent_qte.grid_remove()
        self.ent_montant.grid()
        self.lbl_total.grid()

    def _cacher_champs(self):
        self._mode = None
        self.ent_pu.grid_remove()
        self.ent_qte.grid_remove()
        self.ent_montant.grid_remove()
        self.lbl_total.grid_remove()

    def _calc_total(self, event=None):
        try:
            if self._mode == "qte":
                qte = float(self.var_qte.get() or 0)
                pu  = float(self.var_pu.get()  or 0)
                t   = qte * pu
            elif self._mode == "montant":
                t = float(self.var_montant.get() or 0)
            else:
                t = 0
            self._total_val = t
            self.var_total.set(f"{t:,.0f} F".replace(",", " "))
        except ValueError:
            self._total_val = 0
        self.page.maj_total()

    def _supprimer(self):
        # Détruire tous les widgets de cette ligne dans la grille parente
        parent = self.combo.master
        for w in parent.grid_slaves(row=self.row):
            w.destroy()
        self.page.lignes.remove(self)
        self.page.maj_total()

    def get_total(self):
        return self._total_val

    def get_data(self):
        if not self._produit:
            return None
        try:
            if self._mode == "qte":
                qte = float(self.var_qte.get())
                pu  = float(self.var_pu.get())
                return {"idP": self._produit.idP, "quantite": qte, "montantV": qte * pu}
            elif self._mode == "montant":
                montant = float(self.var_montant.get())
                return {"idP": self._produit.idP, "quantite": None, "montantV": montant}
        except ValueError:
            return None


# ─── PAGE PRODUITS ────────────────────────────────────────────────────────────
class PageProduits(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # En-tête
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=32, pady=(24, 0))
        tk.Label(hdr, text="Gestion des Produits", bg=BG, fg=TEXT_DARK,
                 font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Button(hdr, text="＋  Nouveau produit", style="Accent.TButton",
                   command=self._ouvrir_form).pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=32, pady=12)

        # Barre de recherche
        search_frame = tk.Frame(self, bg=BG)
        search_frame.pack(fill="x", padx=32, pady=(0, 10))
        tk.Label(search_frame, text="🔍", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 12)).pack(side="left")
        self.var_search = tk.StringVar()
        self.var_search.trace("w", lambda *_: self._filtrer())
        ttk.Entry(search_frame, textvariable=self.var_search, width=40).pack(side="left", padx=6)

        # Tableau
        cols = ("ID", "Nom", "Type", "Quantité / Stock", "Prix unitaire")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", selectmode="browse")
        largeurs = [70, 200, 100, 140, 130]
        for c, w in zip(cols, largeurs):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        self.tree.tag_configure("alt", background=ROW_ALT)
        self.tree.pack(fill="both", expand=True, padx=32)

        # Barre d'actions
        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=32, pady=12)
        ttk.Button(actions, text="✏  Modifier",   style="Ghost.TButton",  command=self._modifier).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="🗑  Supprimer",  style="Danger.TButton", command=self._supprimer).pack(side="left")

        self._charger()

    def on_show(self):
        self._charger()

    def _charger(self, filtre=""):
        for r in self.tree.get_children():
            self.tree.delete(r)
        data = self.app.produitService.lireTous()
        for i, el in enumerate(data):
            nom = el["nom"].lower()
            if filtre and filtre not in nom:
                continue
            est_qte  = el["quantite"] != ""
            type_p   = "Quantifiable" if est_qte else "Montant"
            stock    = el["quantite"] if est_qte else f"{el['total']} F"
            pu       = el["prixUnitaire"] if est_qte else "-"
            tag = "alt" if i % 2 else ""
            self.tree.insert("", "end", iid=el["idP"],
                             values=(el["idP"], el["nom"], type_p, stock, pu), tags=(tag,))

    def _filtrer(self):
        self._charger(self.var_search.get().lower())

    def _ouvrir_form(self, produit=None):
        FormProduit(self, self.app, produit, callback=self._charger)

    def _modifier(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionnez un produit.")
            return
        idP = sel[0]
        p = self.app.produitService.chercherProduitId(idP)
        self._ouvrir_form(produit=p)

    def _supprimer(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionnez un produit.")
            return
        if messagebox.askyesno("Confirmer", "Supprimer ce produit ?"):
            self.app.produitService.supprimerProduit(sel[0])
            self._charger()


class FormProduit(tk.Toplevel):
    def __init__(self, parent, app, produit=None, callback=None):
        super().__init__(parent)
        self.app      = app
        self.produit  = produit
        self.callback = callback
        self.title("Modifier produit" if produit else "Nouveau produit")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()
        self._build()

    def _build(self):
        titre = "Modifier" if self.produit else "Nouveau Produit"
        tk.Label(self, text=titre, bg=BG, fg=TEXT_DARK,
                 font=("Segoe UI", 16, "bold")).pack(pady=(20, 8))
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        body = card(self)
        body.pack(fill="both", expand=True, padx=20, pady=12)

        tk.Label(body, text="Nom du produit", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 0))
        self.var_nom = tk.StringVar(value=self.produit.nom if self.produit else "")
        ttk.Entry(body, textvariable=self.var_nom, width=32).grid(row=1, column=0, padx=16, pady=(2, 8), sticky="w")

        tk.Label(body, text="Type de produit", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=16)
        self.var_type = tk.StringVar()
        frame_radio = tk.Frame(body, bg=CARD_BG)
        frame_radio.grid(row=3, column=0, padx=16, pady=(2, 8), sticky="w")
        tk.Radiobutton(frame_radio, text="Quantifiable (ex: riz, sucre…)", variable=self.var_type,
                       value="qte", bg=CARD_BG, fg=TEXT_DARK, activebackground=CARD_BG,
                       command=self._maj_champs).pack(anchor="w")
        tk.Radiobutton(frame_radio, text="En vrac / montant fixe (ex: tomates)", variable=self.var_type,
                       value="montant", bg=CARD_BG, fg=TEXT_DARK, activebackground=CARD_BG,
                       command=self._maj_champs).pack(anchor="w")

        if self.produit:
            self.var_type.set("qte" if self.produit.estQuantifiable() else "montant")
        else:
            self.var_type.set("qte")

        # Champs dynamiques
        self.frame_qte = tk.Frame(body, bg=CARD_BG)
        self.frame_qte.grid(row=4, column=0, padx=16, pady=(0, 8), sticky="w")
        tk.Label(self.frame_qte, text="Quantité initiale", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(self.frame_qte, text="Prix unitaire (FCFA)", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", padx=(16, 0))
        self.var_qte = tk.StringVar(value=str(int(self.produit.quantite)) if (self.produit and self.produit.quantite) else "")
        self.var_pu  = tk.StringVar(value=str(int(self.produit.prixUnitaire)) if (self.produit and self.produit.prixUnitaire) else "")
        ttk.Entry(self.frame_qte, textvariable=self.var_qte, width=14).grid(row=1, column=0, pady=(2, 0))
        ttk.Entry(self.frame_qte, textvariable=self.var_pu,  width=14).grid(row=1, column=1, pady=(2, 0), padx=(16, 0))

        self.frame_total = tk.Frame(body, bg=CARD_BG)
        self.frame_total.grid(row=4, column=0, padx=16, pady=(0, 8), sticky="w")
        tk.Label(self.frame_total, text="Stock total (FCFA)", bg=CARD_BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.var_total = tk.StringVar(value=str(int(self.produit.total)) if (self.produit and self.produit.total) else "")
        ttk.Entry(self.frame_total, textvariable=self.var_total, width=28).grid(row=1, column=0, pady=(2, 0))

        self._maj_champs()

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Annuler", style="Ghost.TButton",
                   command=self.destroy).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="Enregistrer", style="Accent.TButton",
                   command=self._enregistrer).pack(side="left")

    def _maj_champs(self):
        if self.var_type.get() == "qte":
            self.frame_qte.lift()
            self.frame_total.lower()
        else:
            self.frame_total.lift()
            self.frame_qte.lower()

    def _enregistrer(self):
        from models.Produit import Produit
        nom = self.var_nom.get().strip()
        if not nom:
            messagebox.showwarning("Champ manquant", "Le nom est obligatoire.")
            return
        try:
            if self.var_type.get() == "qte":
                qte = float(self.var_qte.get())
                pu  = float(self.var_pu.get())
                p   = Produit(idP=self.produit.idP if self.produit else "",
                              nom=nom, quantite=qte, prixUnitaire=pu, total=None)
            else:
                total = float(self.var_total.get())
                p     = Produit(idP=self.produit.idP if self.produit else "",
                                nom=nom, quantite=None, prixUnitaire=None, total=total)
        except ValueError:
            messagebox.showwarning("Valeur invalide", "Vérifiez les champs numériques.")
            return

        if self.produit:
            self.app.produitService.modifierProduit(p)
        else:
            self.app.produitService.ajouter(p)

        if self.callback:
            self.callback()
        self.destroy()


# ─── PAGE VENTES ──────────────────────────────────────────────────────────────
class PageVentes(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app  = app
        self._all = []
        self._build()

    def _build(self):
        # En-tête
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=32, pady=(24, 0))
        tk.Label(hdr, text="Historique des Ventes", bg=BG, fg=TEXT_DARK,
                 font=("Segoe UI", 20, "bold")).pack(side="left")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=32, pady=12)

        # Filtres / tris
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=32, pady=(0, 10))

        tk.Label(ctrl, text="🔍", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 12)).pack(side="left")
        self.var_search = tk.StringVar()
        self.var_search.trace("w", lambda *_: self._afficher())
        ttk.Entry(ctrl, textvariable=self.var_search, width=24).pack(side="left", padx=6)

        tk.Label(ctrl, text="Trier par :", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(side="left", padx=(16, 4))
        self.var_tri = tk.StringVar(value="Date (récent)")
        tris = ["Date (récent)", "Date (ancien)", "Montant (↓)", "Montant (↑)", "Produit (A→Z)", "Plus vendus"]
        ttk.Combobox(ctrl, textvariable=self.var_tri, values=tris, state="readonly", width=18).pack(side="left")
        self.var_tri.trace("w", lambda *_: self._afficher())

        # KPIs
        self.kpi_frame = tk.Frame(self, bg=BG)
        self.kpi_frame.pack(fill="x", padx=32, pady=(0, 12))

        # Tableau
        cols = ("N°", "Date", "Produit", "Quantité", "Montant")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", selectmode="browse")
        largeurs = [60, 110, 220, 100, 130]
        for c, w in zip(cols, largeurs):
            self.tree.heading(c, text=c,
                command=lambda _c=c: self._tri_colonne(_c))
            self.tree.column(c, width=w, anchor="center")
        self.tree.tag_configure("alt", background=ROW_ALT)

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(32, 0))
        scroll.pack(side="right", fill="y", padx=(0, 16))

    def on_show(self):
        self._charger()

    def _charger(self):
        raw = self.app.venteService.lireToutesLesVentes()
        self._all = []
        for el in raw:
            p = self.app.produitService.chercherProduitId(el["idP"])
            nom = p.nom if p else el["idP"]
            self._all.append({
                "idV":     el["idV"],
                "dateV":   el["dateV"] or "-",
                "nom":     nom,
                "idP":     el["idP"],
                "quantite": el["quantite"] or "-",
                "montant": float(el["montantV"]) if el["montantV"] else 0,
            })
        self._maj_kpi()
        self._afficher()

    def _maj_kpi(self):
        for w in self.kpi_frame.winfo_children():
            w.destroy()

        total_ca = sum(v["montant"] for v in self._all)
        nb       = len(self._all)

        # Produit le plus vendu
        from collections import Counter
        cnt = Counter(v["nom"] for v in self._all)
        top = cnt.most_common(1)[0][0] if cnt else "-"

        kpis = [
            ("💰 CA Total", f"{total_ca:,.0f} F".replace(",", " ")),
            ("🧾 Nb Ventes", str(nb)),
            ("🏆 Top Produit", top),
        ]
        for titre, val in kpis:
            c = card(self.kpi_frame)
            c.pack(side="left", padx=(0, 12), pady=4, ipady=6, ipadx=16)
            tk.Label(c, text=titre, bg=CARD_BG, fg=TEXT_MUTED,
                     font=("Segoe UI", 9, "bold")).pack(padx=12, pady=(8, 0))
            tk.Label(c, text=val, bg=CARD_BG, fg=TEXT_DARK,
                     font=("Segoe UI", 14, "bold")).pack(padx=12, pady=(0, 8))

    def _afficher(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        filtre = self.var_search.get().lower()
        data   = [v for v in self._all if filtre in v["nom"].lower() or filtre in v["dateV"]]

        tri = self.var_tri.get()
        if tri == "Date (récent)":
            data = sorted(data, key=lambda v: v["dateV"], reverse=True)
        elif tri == "Date (ancien)":
            data = sorted(data, key=lambda v: v["dateV"])
        elif tri == "Montant (↓)":
            data = sorted(data, key=lambda v: v["montant"], reverse=True)
        elif tri == "Montant (↑)":
            data = sorted(data, key=lambda v: v["montant"])
        elif tri == "Produit (A→Z)":
            data = sorted(data, key=lambda v: v["nom"])
        elif tri == "Plus vendus":
            from collections import Counter
            cnt = Counter(v["nom"] for v in data)
            data = sorted(data, key=lambda v: cnt[v["nom"]], reverse=True)

        for i, v in enumerate(data):
            tag = "alt" if i % 2 else ""
            qte = v["quantite"] if v["quantite"] != "" else "-"
            self.tree.insert("", "end",
                values=(v["idV"], v["dateV"], v["nom"], qte,
                        f"{v['montant']:,.0f} F".replace(",", " ")),
                tags=(tag,))

    def _tri_colonne(self, col):
        mapping = {
            "Date":    "Date (récent)",
            "Montant": "Montant (↓)",
            "Produit": "Produit (A→Z)",
        }
        if col in mapping:
            self.var_tri.set(mapping[col])