# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
import threading
import os

# Import du module principal
import MAIN
import Visualisation as Visu

class SimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur de Température de Surface")
        self.root.geometry("1100x650")
        
        # Variables stockant les coordonnées sélectionnées
        self.lat = None
        self.lon = None
        self.marker = None

        self.creer_interface()

    def creer_interface(self):
        # ---------- FRAME GAUCHE : LA CARTE ----------
        map_frame = tk.Frame(self.root)
        map_frame.pack(side="left", fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(map_frame, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(48.8566, 2.3522)  # Centré sur Paris par défaut
        self.map_widget.set_zoom(4)
        
        # Événement : Clic droit sur la carte pour définir les coordonnées
        self.map_widget.add_right_click_menu_command(
            label="Sélectionner ce point", 
            command=self.set_coordonnees, 
            pass_coords=True
        )

        # ---------- FRAME DROITE : LES CONTRÔLES ----------
        control_frame = tk.Frame(self.root, width=300, padx=20, pady=20, bg="#f0f0f0")
        control_frame.pack(side="right", fill="y")
        control_frame.pack_propagate(False) # Empêche le panneau de s'écraser

        # Titre
        tk.Label(control_frame, text="Paramètres", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        # Affichage Coordonnées
        self.lbl_coords = tk.Label(control_frame, text="📍 Aucune coordonnée\n(Faites un clic droit sur la carte)", font=("Helvetica", 10), bg="#f0f0f0", fg="black")
        self.lbl_coords.pack(pady=10)

        # Sélection de l'année
        tk.Label(control_frame, text="📅 Année de simulation :", font=("Helvetica", 11), bg="#f0f0f0").pack(pady=(20, 5))
        self.annee_var = tk.StringVar(value="2024")
        self.combo_annee = ttk.Combobox(control_frame, textvariable=self.annee_var, state="readonly", font=("Helvetica", 11))
        # Menu déroulant de 1850 à 2100
        self.combo_annee['values'] = [str(y) for y in range(1850, 2101)]#a changer si vous voulez plus d'années de simulation
        self.combo_annee.pack()

        # Bouton Lancer
        self.btn_lancer = tk.Button(control_frame, text="▶ Lancer la simulation", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.lancer_simulation)
        self.btn_lancer.pack(pady=40, fill="x")

        # Statut
        self.lbl_statut = tk.Label(control_frame, text="En attente de lancement...", font=("Helvetica", 10, "italic"), bg="#f0f0f0", fg="gray")
        self.lbl_statut.pack(side="bottom", pady=20)

    def set_coordonnees(self, coords):
        """Met à jour les coordonnées suite à un clic droit sur la carte."""
        self.lat, self.lon = coords
        self.lbl_coords.config(text=f"📍 Lat: {self.lat:.4f}°\n📍 Lon: {self.lon:.4f}°", fg="#0056b3")
        
        # Mettre à jour le marqueur visuel
        if self.marker:
            self.marker.delete()
        self.marker = self.map_widget.set_marker(self.lat, self.lon, text="Zone d'étude")

    def lancer_simulation(self):
        """Vérifie les inputs et lance le calcul dans un thread séparé."""
        if self.lat is None or self.lon is None:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un point sur la carte (clic droit).")
            return

        annee = int(self.annee_var.get())

        # Désactiver le bouton pour éviter les clics multiples
        self.btn_lancer.config(state="disabled", bg="#a5d6a7")
        self.lbl_statut.config(text="⏳ Simulation en cours...\nRegardez la console.", fg="blue")

        # Lancer le calcul en arrière-plan pour ne pas figer la fenêtre
        thread = threading.Thread(target=self.executer_calcul, args=(annee, self.lat, self.lon))
        thread.start()

    def executer_calcul(self, annee, lat, lon):
        """Fonction exécutée en arrière-plan."""
        try:
            # Appel des fonctions de ton MAIN.py
            T_point = MAIN.temp(annee, lat, lon)
            Visu.Visualiation(T_point, annee, lat, lon)
            
            # Revenir au thread principal pour mettre à jour l'interface
            self.root.after(0, self.fin_simulation, annee, lat, lon)
        except Exception as e:
            self.root.after(0, self.erreur_simulation, str(e))

    def fin_simulation(self, annee, lat, lon):
        """Restaure l'interface et prévient de la fin."""
        self.lbl_statut.config(text=f"✅ Simulation terminée !\n(Voir png et csv dans le dossier)", fg="green")
        self.btn_lancer.config(state="normal", bg="#4CAF50")
        messagebox.showinfo("Succès", f"Simulation pour {annee} aux coordonnées ({lat:.2f}, {lon:.2f}) terminée !\n\nLes fichiers graphiques et CSV ont été générés dans le dossier du script.")

    def erreur_simulation(self, erreur_msg):
        """Gère les éventuels crashs du backend."""
        self.lbl_statut.config(text="❌ Erreur durant le calcul", fg="red")
        self.btn_lancer.config(state="normal", bg="#4CAF50")
        messagebox.showerror("Erreur système", f"La simulation a échoué :\n\n{erreur_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()