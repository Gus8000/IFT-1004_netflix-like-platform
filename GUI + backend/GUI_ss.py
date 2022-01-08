import tkinter
from tkinter import Tk, Button, Label, Entry, Frame, ttk, messagebox, scrolledtext, Canvas, Text
import tkinter as threading
from utilisateur import *
from mediatheque import *
from PIL import Image, ImageTk
import tkinter as tk, threading
import imageio
from tkvideo import tkvideo
import glob

theme = 'dark'

class DoubleScrolledFrame: # Code copié depuis https://gist.github.com/novel-yet-trivial/2841b7b640bba48928200ff979204115
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = ttk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = ttk.Scrollbar(self.outer, orient=tk.HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion=(0, 0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units")
        elif event.num == 5 or event.delta < 0:
            func(1, "units")

    def __str__(self):
        return str(self.outer)
        
class FenetreDeBase(Tk):                                # classe mère, toutes les classes de fenêtres héritent d'elle donc toutes les classes de fenêtres peuvent s'appeler les unes les autres,
    def __init__(self, titre):                          #   sert juste à ce que la fenêtre d'accueil se base sur Tk (pour initialisation) et puisse appeler les autres fenêtres
        super().__init__()
        self.title(titre)

    def ouvrir_inscription(self, evenement=None):
        self.destroy()
        fenetre_inscription = UlFlixInscription("Inscription")              # création de la fenetre d'inscription à partir de classe ULFlixInscription
        fenetre_inscription.mainloop()

    def ouvrir_connexion(self, evenement=None):
        self.destroy()
        fenetre_login = ULFlixConnexion("Connexion")                             # création de la fenetre de connexion à partir de classe ULFlixLogin
        fenetre_login.mainloop()

    def ouvrir_tableau_des_films(self, evenement=None):
        self.destroy()
        fenetre_tableau = ULFlixTableauDeBord("Tableau de bord ULFlix", utilisateur)           # création de la fenetre du tableau des films à partir de classe ULFlixLogin OU ULFlixInscription
        fenetre_tableau.mainloop()

    def ouvrir_accueil_light(self, evenement=None):
        self.destroy()
        global theme
        theme = 'light'
        fenetre_accueil_light = ULFlixAccueilLight("Bienvenue sur ULFlix - Light")
        fenetre_accueil_light.mainloop()

    def ouvrir_accueil_dark(self, evenement=None):
        self.destroy()
        global theme
        theme = 'dark'
        fenetre_accueil_dark = ULFlixAccueilDark("Bienvenue sur ULFlix - Dark")
        fenetre_accueil_dark.mainloop()

    def show_info(self, movie_id, evenement=None):
        fenetre_info_du_show = InfoDuShow(movie_id)  # création de la fenetre de connexion à partir de classe ULFlixLogin
        fenetre_info_du_show.mainloop()

    def quit(self):
        self.destroy()

    def show_video(self, movie_id, evenement=None):
        self.destroy()

        root = Tk()
        my_label = Label(root)
        my_label.pack()
        player = tkvideo(f"./videos/{movie_id}.mp4", my_label, loop = 1, size = (1280,720))   # Fonctionne mais pas de son
        player.play()
        root.mainloop()

    def get_color_background(self):
        global theme
        if theme == "dark":
            bg = "black"
        elif theme == "light":
            bg = "white"
        return bg

    def get_color_foreground(self):
        global theme
        if theme == "dark":
            fg = "white"
        elif theme == "light":
            fg = "black"
        return fg

class ULFlixAccueilDark(FenetreDeBase):
    def __init__(self, titre):
        super().__init__(titre)

        self.title(titre)          # ici, self = une fenêtre de la classe de fenêtre d'accueil
        background = self.get_color_background()
        foreground = self.get_color_foreground()

        self.cadre_accueil = Frame(self, background=background, padx=46, pady=45)

        self.geometry("1250x590")
        self.resizable(True,True)

        global logo_accueil
        logo = Image.open("bouton-rouge.jpg")
        logo = logo.resize((100, 100))
        logo_accueil = ImageTk.PhotoImage(logo)
        self.logo = Label(self.cadre_accueil, image=logo_accueil)
        self.accueil_light_label = Label(self.cadre_accueil, text="Changez pour le thème clair!", background=background, foreground= foreground,
                                           font="Times 13 bold", cursor="spider")
        self.accueil_light_label.bind("<Button-1>", self.ouvrir_accueil_light)
        self.titre_accueil_label = Label(self.cadre_accueil, text = "Bienvenue sur ULFlix", foreground= "red", font= "Castellar 65 bold", pady=70,
                                 background=background)
        self.inscription_accueil_label = Label(self.cadre_accueil, text = "Créer un compte", background= background,
                                         foreground= "red", bd="10", font="Times 24 bold", cursor="spider")
        self.inscription_accueil_label.bind("<Button-1>", self.ouvrir_inscription)
        self.connexion_accueil_label = Label(self.cadre_accueil, text="Ouvrir une session", background= background,
                                        foreground= "red", font="Times 24 bold", cursor="spider")
        self.connexion_accueil_label.bind("<Button-1>", self.ouvrir_connexion)

        self.logo.grid(row=0, column=0, columnspan=2)
        self.accueil_light_label.grid(row=3, column=0,columnspan=2)
        self.titre_accueil_label.grid(row=1, column=0, columnspan=2)
        self.inscription_accueil_label.grid(row=2, column=0, pady=40)
        self.connexion_accueil_label.grid(row=2 , column=1, pady=40)

        self.cadre_accueil.grid(row=0, column=0)

class ULFlixAccueilLight(FenetreDeBase):
    def __init__(self, titre):
        super().__init__(titre)

        self.title(titre)  # ici, self = une fenêtre de la classe de fenêtre d'accueil
        background = self.get_color_background()
        foreground = self.get_color_foreground()

        self.cadre_accueil = Frame(self, background=background, padx=46, pady=45)

        self.geometry("1250x590")
        self.resizable(True, True)

        global logo_accueil
        logo = Image.open("bouton-rouge.jpg")
        logo = logo.resize((100, 100))
        logo_accueil = ImageTk.PhotoImage(logo)
        self.logo = Label(self.cadre_accueil, image=logo_accueil, background=background)
        self.accueil_dark_label = Label(self.cadre_accueil, text="Changez pour le thème sombre!",
                                        background=background, foreground=foreground,
                                        font="Times 12 bold", cursor="spider")
        self.accueil_dark_label.bind("<Button-1>", self.ouvrir_accueil_dark)
        self.titre_accueil_label = Label(self.cadre_accueil, text="Bienvenue sur ULFlix", foreground="red",
                                         font="Castellar 65 bold", pady=70,
                                         background=background)
        self.inscription_accueil_label = Label(self.cadre_accueil, text="Créer un compte", background=background,
                                               foreground="red", bd="10", font="Times 24 bold", cursor="spider")
        self.inscription_accueil_label.bind("<Button-1>", self.ouvrir_inscription)
        self.connexion_accueil_label = Label(self.cadre_accueil, text="Ouvrir une session", background=background,
                                             foreground="red", font="Times 24 bold", cursor="spider")
        self.connexion_accueil_label.bind("<Button-1>", self.ouvrir_connexion)

        self.logo.grid(row=0, column=0, columnspan=2)
        self.accueil_dark_label.grid(row=3, column=0,columnspan=2)
        self.titre_accueil_label.grid(row=1, column=0, columnspan=2)
        self.inscription_accueil_label.grid(row=2, column=0, pady=40)
        self.connexion_accueil_label.grid(row=2, column=1, pady=40)

        self.cadre_accueil.grid(row=0, column=0)


class UlFlixInscription(FenetreDeBase):
    def __init__(self, titre):
        super().__init__(titre)

        self.title(titre)                            # ici, self = une fenêtre de la classe de fenêtre d'inscription, créée lorsque la fenêtre d'accueil appelle la fonction ouvrir_inscription
                                                     #     OU lorsque l'utilisateur clique sur not_yet_member_label_connexion dans la fenêtre de connexion
        background = self.get_color_background()
        foreground = self.get_color_foreground()

        self.cadre_inscription = Frame(self, bg=background, padx=30, pady=30)

        self.titre_inscription_label = Label(self.cadre_inscription, text="Créez votre compte dès maintenant!", font="Times 30 bold", foreground="red",
                            background=background, padx=20, pady=10)
        self.nom_inscription_label = Label(self.cadre_inscription, text="Nom: ",foreground="red", background=background, font="Times 18 bold", pady= 12, padx=20)
        self.email_inscription_label = Label(self.cadre_inscription, text="Email: ",foreground="red", background=background, font="Times 18 bold",pady= 12, padx=20)
        self.password_inscription_label = Label(self.cadre_inscription, text="Mot de passe: ",foreground="red", background=background, font="Times 18 bold",pady= 12, padx=20)
        self.age_inscription_label = Label(self.cadre_inscription, text="Âge: ", foreground="red", background=background, font="Times 18 bold", pady= 12, padx=20)
        self.pays_inscription_label = Label(self.cadre_inscription, text="Pays: " , foreground="red", background=background, font="Times 18 bold",pady= 12, padx=20)
        self.abonnement_inscription_label = Label(self.cadre_inscription, text="Abonnement: ", foreground="red", background=background, font="Times 18 bold", pady= 12, padx=20)
        self.abonnement_warning_inscription_label = Label(self.cadre_inscription, text="( 1 = abonnement régional et 2 = abonnement international )", font="Times 12 bold", foreground=foreground, background=background)
        self.nom_inscription_entry = Entry(self.cadre_inscription)
        self.email_inscription_entry = Entry(self.cadre_inscription)
        self.password_inscription_entry = Entry(self.cadre_inscription)
        liste_annee = []
        for i in range(1, 100):
            liste_annee.append(i)
        self.age_combo_inscription = ttk.Combobox(self.cadre_inscription,values= liste_annee)
        with open('countries.txt') as f:
            list_of_countries = [ligne.strip() for ligne in f]
        self.pays_combo_inscription = ttk.Combobox(self.cadre_inscription, values=list_of_countries)
        self.abonnement_combo_inscription = ttk.Combobox(self.cadre_inscription, values=["1", "2"])
        self.inscription_label = Label(self.cadre_inscription, text="S'inscrire!", background=background,
                                         foreground="red", padx=30,
                                         font="Times 18 bold", cursor="spider")
        self.inscription_label.bind("<Button-1>", self.gerer_inscription)
        self.already_member_label_inscription = Label(self.cadre_inscription,
                                                      text="Déjà membre? Cliquez ici pour vous connecter!", background=background,
                                                      foreground=foreground, cursor="spider", pady=12)
        self.already_member_label_inscription.bind("<Button-1>", self.ouvrir_connexion)

        self.titre_inscription_label.grid(row=0, column=0, columnspan=2)
        self.nom_inscription_label.grid(row=1, column=0)
        self.email_inscription_label.grid(row=2, column=0)
        self.password_inscription_label.grid(row=3, column=0)
        self.age_inscription_label.grid(row=4, column=0)
        self.pays_inscription_label.grid(row=5, column=0)
        self.abonnement_inscription_label.grid(row=6, column=0)
        self.abonnement_warning_inscription_label.grid(row=7, column=0)
        self.nom_inscription_entry.grid(row=1, column=1)
        self.email_inscription_entry.grid(row=2, column=1)
        self.password_inscription_entry.grid(row=3, column=1)
        self.age_combo_inscription.grid(row=4, column=1)
        self.pays_combo_inscription.grid(row=5, column=1)
        self.abonnement_combo_inscription.grid(row=6, column=1)
        self.inscription_label.grid(row=10, column=0, columnspan=2, pady=40)
        self.already_member_label_inscription.grid(row=11, column=0, columnspan=2)

        self.cadre_inscription.grid(row=0, column=0)

    def gerer_inscription(self, event=None):                                        # fonction appelée par la fenêtre d'inscription et qui inscrit l'utilisateur (processus d'inscription)
        global utilisateur
        annuaire_utilisateur = AnnuaireUtilisateur("ulflix-utilisateurs.txt")
        try:
            utilisateur = annuaire_utilisateur.inscrire(self.nom_inscription_entry.get(),
                                                        self.email_inscription_entry.get(),
                                                        self.password_inscription_entry.get(),
                                                        self.age_combo_inscription.get(),
                                                        self.pays_combo_inscription.get(),
                                                        self.abonnement_combo_inscription.get(),
                                                        )
        except ErreurInscription as e:
            messagebox.showerror("Erreur d'inscription", e, parent=self)
        else:
            self.ouvrir_tableau_des_films()                                            #   juste à placer les classes d'exceptions dans le module d'exceptions et ensuite les importer

class ULFlixConnexion(FenetreDeBase):
    def __init__(self, titre):
        super().__init__(titre)

        self.title(titre)                            # ici, self = une fenêtre de la classe de fenêtre de connexion, créée lorsque la fenêtre d'accueil appelle la fonction ouvrir_connection

        background = self.get_color_background()
        foreground = self.get_color_foreground()

        self.cadre_connexion = Frame(self, background=background, padx=20, pady=20)

        self.titre_connexion_label = Label(self.cadre_connexion, text="Content de vous revoir", font="Times 30 bold",
                                           foreground="red", background=background)
        self.email_connexion_label = Label(self.cadre_connexion, text="Email: ", font="Times 18 bold", foreground="red",
                                           bg=background)
        self.password_connexion_label = Label(self.cadre_connexion, text="Mot de passe: ", font="Times 18 bold",
                                              foreground="red", bg=background)
        self.email_connexion_entry = Entry(self.cadre_connexion)
        self.password_connexion_entry = Entry(self.cadre_connexion,show= "*")
        self.connexion_label = Label(self.cadre_connexion, text="Se connecter", background=background,
                                                 font="Times 18 bold", foreground="red", cursor="spider")
        self.connexion_label.bind("<Button-1>", self.gerer_connexion)
        self.not_yet_member_connexion_label = Label(self.cadre_connexion, text="Pas encore de compte? Cliquez ici pour en créer un!",
                                                    bg=background,
                               foreground=foreground, cursor= "spider")
        self.not_yet_member_connexion_label.bind("<Button-1>", self.ouvrir_inscription)

        self.titre_connexion_label.grid(row=0, column=0, columnspan=2, pady=20)
        self.email_connexion_label.grid(row=1, column=0, pady=12)
        self.password_connexion_label.grid(row=2, column=0, pady=12)
        self.email_connexion_entry.grid(row=1, column=1)
        self.password_connexion_entry.grid(row=2, column=1)
        self.connexion_label.grid(row=3, column=0, columnspan=2, pady=30)
        self.not_yet_member_connexion_label.grid(row=4, column=0, columnspan=2)

        self.cadre_connexion.grid(row=0, column=0)

    def gerer_connexion(self, evenement=None):                                                          # fonction appelée par la fenêtre de connexion et qui authentifie l'utilisateur (processus connexion)
        global utilisateur
        annuaire_utilisateur = AnnuaireUtilisateur("ulflix-utilisateurs.txt")
        try:
            utilisateur = annuaire_utilisateur.authentifier(self.email_connexion_entry.get(), self.password_connexion_entry.get())
        except ErreurAuthentifier as e:
            messagebox.showerror("Erreur d'authentification", e, parent=self)
        else:
            self.ouvrir_tableau_des_films()

class ULFlixTableauDeBord(FenetreDeBase):
    def __init__(self, titre, utilisateur):
        super().__init__(titre)

        self.__videos_dossier = "./videos"
        self.__images_dossier = "./images"
        self.width = 1000
        self.height = 600
        self.height_movie = 150

        self.utilisateur = utilisateur                     # ici, self = une fenêtre de la classe de fenêtre du tableau des films, créée lorsque la fenêtre de connexion appelle la
        self.title(titre)                                  # fonction gerer_connexion et qu'aucune exception n'est levée OU lorsqu'un utilisateur s'inscrit via la fenêtre d'inscription

        fichier_des_shows = "ulflix.txt"

        mediatheque = Mediatheque(fichier_des_shows)

        selection_ids = mediatheque.filtrer_ids_sur_age(self.utilisateur.age)
        if self.utilisateur.abonnement == 1:
            temp = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("pays", self.utilisateur.pays)
            selection_ids = list(set(selection_ids).intersection(temp))

        mediatheque.reduire_liste_des_shows(selection_ids)

        print(f"Salut {self.utilisateur.nom.title()}! Tu as accès à {len(mediatheque)} films et séries télés.")

        movies_by_filter = {}

        movie_classes = ["Action & Adventure", "Comedies", "Dramas", "Sci-Fi & Fantasy", "Thrillers", "Horror Movies"]
        for movie_class in movie_classes:
            movies_by_filter[movie_class] = (
                mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("categories", movie_class))

        movie_types = ["TV Show"]
        for movie_type in movie_types:
            movies_by_filter[movie_type] = (
                mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("type", movie_type))

        self.geometry(f"{self.width}x{self.height}")
        self.titre_tableau_label = Label(self, text= f'Bienvenue {self.utilisateur.nom}',foreground= "red", font= "Castellar 24 bold").grid(row=0,column=0, columnspan=2)

        self.photos = []
        self.current_row = 1

        self.main_scroll = DoubleScrolledFrame(self, width=self.width-50, height=self.height-50, 
                borderwidth=2, relief=tk.SUNKEN, background="light gray")
        self.main_scroll.grid(row=1, column=1)

        for filter_ in movies_by_filter:
            Label(self.main_scroll, text=filter_, font="bold", fg="red").grid(row=self.current_row, column=1)
            self.current_row += 1

            movies = movies_by_filter[filter_]
            images = self.afficher_image_selon_selection_ids(movies)

            frame = DoubleScrolledFrame(self.main_scroll, width=self.width-50, height=self.height_movie, 
                borderwidth=2, relief=tk.SUNKEN, background="light gray")
            frame.grid(column=1, row=self.current_row, sticky='nsew')
            self.current_row += 1

            for i, image in enumerate(images):
                if i <=100:                                                                                     # Étant donné la quantité de photos (6953), nous avons limité
                    self.displayImg(frame, image, 1, i+1)                                                       # le téléchargement à 100 shows par catégories.

    def displayImg(self, frame, img_path, row, column):
            image_path = f"{self.__images_dossier}/{img_path}"
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)  # keep references!
            newPhoto_label = Label(frame, image=photo)
            newPhoto_label.grid(row=row, column=column)
            newPhoto_label.bind('<Button-1>', lambda event, movie_id=img_path.split('.')[0]: 
                            self.description_ou_trailer(movie_id))

    def afficher_image_selon_selection_ids(self, selection_ids):
        dirlist = os.listdir(self.__images_dossier)
        list_image_ids = []
        for image in dirlist:
            if os.path.splitext(image)[0] in selection_ids:
                list_image_ids.append(image)
        return list_image_ids

    def afficher_description_show(self, show):
        show = show.strip("'")
        with open("ulflix.txt", encoding="utf-8") as o:
            for line in o:
                if line.startswith(show):
                    print(line)

    def description_ou_trailer(self, movie_id):

        def ouvrir_tableau_apres_quit():
            root.destroy()
            self.ouvrir_tableau_des_films()

        background = self.get_color_background()
        foreground = self.get_color_foreground()

        root = Tk()
        root.geometry("400x250")
        fram = Frame(root, bg=background, width=500, height=250)
        label = Label(fram, text="Voici vos options:", bg=background, fg="red", font="Times 19 bold")
        button_descr = Button(fram, text="Accéder à la description", command=lambda: self.show_info(movie_id),
                              bg=background, fg="red", font="Times 15 bold")
        button_trailer = Button(fram, text="Accéder au vidéo", command=lambda: self.show_video(movie_id), bg=background,
                                fg="red", font="Times 15 bold")
        button_quit = Button(fram, text="Retourner à l'écran d'accueil des shows", command=ouvrir_tableau_apres_quit,
                             bg=background, fg="red", font="Times 15 bold")
        label.grid(row=0, column=0, columnspan=2, padx=30, pady=15)
        button_descr.grid(row=1, column=1, padx=12, pady=15)
        button_trailer.grid(row=2, column=1, padx=12, pady=15)
        button_quit.grid(row=3, column=1, padx=12, pady=15)
        fram.grid(row=0, column=0)
        fram.grid_propagate(0)
        root.mainloop()

class InfoDuShow(FenetreDeBase):
    def __init__(self, movie_id):

        fichier_des_shows = "ulflix.txt"
        mediatheque = Mediatheque(fichier_des_shows)
        show = mediatheque[movie_id]
        titre = show.titre

        super().__init__(titre)

        background = self.get_color_background()
        foreground = self.get_color_foreground()

        self.title(titre)

        self.width = 800
        self.height = 300

        self.cadre_show_info = Frame(self, background=background, padx=20, pady=20)

        self.titre_show_info_label = Label(self.cadre_show_info, text=str(show), font="Times 15 bold",
                                           foreground="red", background=background, padx=20, pady=20)

        self.geometry(f"{self.width}x{self.height}")

        self.ok_button = Button(self.cadre_show_info,
                           text='Ok', font="Times 14 bold", foreground="red",
                           borderwidth=0, command=self.quit)

        self.titre_show_info_label.grid(row=0, column=0, columnspan=2)
        self.ok_button.grid(row=1, column=0, columnspan = 2 ,pady=20)
        self.cadre_show_info.grid(row=0, column=0)



fenetre_accueil = ULFlixAccueilDark("Bienvenue sur ULFlix - Dark")
fenetre_accueil.mainloop()