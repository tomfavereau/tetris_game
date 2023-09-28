#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 20:24:31 2023

@author: tom
"""

from tkinter import *
from random import randrange
from random import choice
#import pygame


def rgb(rgb):
    return "#%02x%02x%02x" % rgb  


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    


class Tetris:
    def __init__(self):
        ###fenetre
        self.window = Tk()
        self.window.title("Tetris")
        
        ###couleur blocs 
        self.dico_couleur = [(rgb((255, 255, 102)), rgb((255, 255, 0))), 
           (rgb((102, 255, 255)), rgb((0, 255, 255))), 
           (rgb((102, 102, 255)), rgb((0, 0, 255))),
           (rgb((255, 102, 255)), rgb((255, 0, 255))),
           (rgb((102, 255, 102)), rgb((0, 255, 0))), 
           (rgb((255, 102, 102)), rgb((255, 0, 0)))]
        
        self.image = PhotoImage(file = "fond2.png")
        
        self.jeu = Canvas(self.window, width = 600, height = 600, bg="black")
        self.jeu.grid(column = 0, row = 0)
        
        self.jeu.create_image(0, 0, image= self.image, anchor='nw')
        # 400 pour le jeux et 200 pour les autre information 
        
        #info complémentaire 
        self.jeu.create_polygon([400, 0], [410, 0], [410, 600], [400, 600], fill = "grey")
        
        #piece suivante 
        self.jeu.create_polygon([450, 100], [460, 100], [460, 200], [450, 200], fill = 'grey')
        self.jeu.create_polygon([560, 100], [570, 100], [570, 200], [560, 200], fill = 'grey')
        self.jeu.create_polygon([450, 100], [450, 110], [570, 110], [570, 100], fill = 'grey')
        self.jeu.create_polygon([450, 190], [450, 200], [570, 200], [570, 190], fill = 'grey')
        
        
        #score 
        self.score = 0
        self.afficher_score = self.jeu.create_text(500, 300, text="socre : "+ str(self.score), fill='white', font=('arial', 15))
        
        ###matrice du jeu
        self.matrice = [[0 for _ in range(15)] for _ in range(10)]
        self.dico_polygon = {} #gère les polygone pour les effacer
        
        ###pieces
        
        #liste pièces
        #sont définit par rapport au plus au centre
        # ex : la ligne [][][][] s'écrit [-1, 0, 1, 2]
        self.liste_piece = [[(-1, 0), (0, 0), (1, 0), (2, 0)], 
                            [(-1, 1), (0, 1), (1, 1), (1, 0)],
                            [(0, 0), (1, 0), (1, 1), (0, 1)], 
                             [(-1, 0), (0, 0), (0, 1), (1, 1)],
                             [(-1, 1), (0, 1), (0, 0), (1, 0)],
                             [(-1, 0), (-1, 1), (0, 1), (1, 1)], 
                             [(-1, 0), (0, 0), (1, 0), (0, 1)]]
        
        self.pos_piece = [(3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1)] #pos de depart des pièce 
        
        #piece actu
        #self.piece_actu = [[randrange(2, 4)+1/2, 1], choice(self.liste_piece), randrange(6)] #une coordoné et une pièce
        #on vas définir les pièce comme des liste de bloc 
        piece = randrange(7)
        x, y = randrange(2, 7), 1
        self.piece_actu = [[x, y], self.liste_piece[piece], randrange(6)]
        x2, y2 = randrange(2, 7), 1
        piece2 = randrange(7)
        couleur2 = randrange(6)
        self.piece_suiv = [[x2, y2], self.liste_piece[piece2], couleur2]
        self.suprimer_piece_suiv = []
        
        for i in self.piece_suiv[1]:
            x2, y2 = 500+20*i[0], 130+20*i[1]
           
            #bordure dégradé
            b1 = self.jeu.create_polygon([x2, y2], [x2+20, y2], [x2+20, y2+20], [x2, y2+20], fill=self.dico_couleur[couleur2][1])
        
            #interieur
            b2 = self.jeu.create_polygon([x2+5, y2+5], [x2+15, y2+5], [x2+15, y2+15], [x2+5, y2+15], fill = self.dico_couleur[couleur2][0])
        
            self.suprimer_piece_suiv.append((b1, b2))
        
        
        self.window.bind('<d>', self.droite)
        self.window.bind('<q>', self.gauche)
        self.window.bind('<e>', self.tourner_droite)
        self.window.bind('<a>', self.tourner_gauche)
        self.window.bind('<k>', self.debug)
        
        
        
        self.dessiner()
        
        self.tomber()
        
        
        
        self.window.mainloop()
        
    def create_bloc(self, couleur, coord):
        x, y = coord
        #bordure dégradé
        b1 = self.jeu.create_polygon([x, y], [x+40, y], [x+40, y+40], [x, y+40], fill=self.dico_couleur[couleur][1])
        
        #interieur
        b2 = self.jeu.create_polygon([x+5, y+5], [x+35, y+5], [x+35, y+35], [x+5, y+35], fill = self.dico_couleur[couleur][0])
        
        return (b1, b2, couleur)
        
    def dessiner(self):
        x, y = self.piece_actu[0]
        couleur = self.piece_actu[2]
        for i in self.piece_actu[1]:
            self.dico_polygon[(x+i[0], y+i[1])] = self.create_bloc(couleur, [40*x+40*i[0], 40*y+40*i[1]])
            
            
    def new_piece(self):
        piece = randrange(7)
        x, y = randrange(2, 7), 1
        couleur = randrange(6)
        
        for i in self.suprimer_piece_suiv:
            self.jeu.delete(i[0])
            self.jeu.delete(i[1])
        self.suprimer_piece_suiv = []
        
        self.piece_actu = self.piece_suiv
        self.piece_suiv = [[x, y], self.liste_piece[piece], couleur]
        
        #on dessine la piece suivante
        for i in self.piece_suiv[1]:
            x2, y2 = 500+20*i[0], 130+20*i[1]
            #bordure dégradé
            b1 = self.jeu.create_polygon([x2, y2], [x2+20, y2], [x2+20, y2+20], [x2, y2+20], fill=self.dico_couleur[couleur][1])
        
            #interieur
            b2 = self.jeu.create_polygon([x2+5, y2+5], [x2+15, y2+5], [x2+15, y2+15], [x2+5, y2+15], fill = self.dico_couleur[couleur][0])
        
            self.suprimer_piece_suiv.append((b1, b2))
            
        
        self.dessiner()
    
    def tomber(self):
        x, y = self.piece_actu[0]
        peut_tomber = True
        for i in self.piece_actu[1]: # on verifie les colisions
            if y+i[1]+1 == 15 or self.matrice[int(x+i[0])][int(y+i[1]+1)] == 1:
                peut_tomber = False
        if peut_tomber:
            for i in self.piece_actu[1]:

                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][0])
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][1])
                del self.dico_polygon[(x+i[0], y+i[1])]
            self.piece_actu[0][1] += 1
            
            
            self.dessiner()
        else:
            for i in self.piece_actu[1]:
                self.matrice[int(x+i[0])][int(y+i[1])] = 1
            
            self.vider_ligne()
            self.new_piece()
        
        self.jeu.after(500, self.tomber)
        
    def droite(self, d):
        x, y = self.piece_actu[0]
        peut_droite = True
        for i in self.piece_actu[1]:
            if x+1+i[0] == 10 or self.matrice[int(x+i[0]+1)][int(y+i[1])] == 1:
                peut_droite = False
        
        if peut_droite: 
            for i in self.piece_actu[1]:
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][0])
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][1])
                del self.dico_polygon[(x+i[0], y+i[1])]
            
            
                    
            self.piece_actu[0][0] += 1
            
            
            self.dessiner()
        
    def gauche(self, g):
        x, y = self.piece_actu[0]
        peut_gauche = True
        for i in self.piece_actu[1]:
            if x+i[0]-1 == -1 or self.matrice[int(x+i[0]-1)][int(y+i[1])] == 1:
                peut_gauche = False
        
        if peut_gauche: 
        
            for i in self.piece_actu[1]:
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][0])
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][1])
                del self.dico_polygon[(x+i[0], y+i[1])]
            self.piece_actu[0][0] -= 1
            
            
            self.dessiner()
    
    def tourner_droite(self, e):
        x, y = self.piece_actu[0]
        peut_tourner = True 
        for i in self.piece_actu[1]:
            if x+i[1]>=10 or x+i[1]<0 or y-i[0]>=15 or y-i[0]<0 or self.matrice[int(x+i[1])][int(y-i[0])] == 1:
                peut_tourner = False 
        if peut_tourner:
            for i in self.piece_actu[1]:
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][0])
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][1])
                del self.dico_polygon[(x+i[0], y+i[1])]
            
            for i in range(len(self.piece_actu[1])):
                a, b = self.piece_actu[1][i]
                self.piece_actu[1][i] = [b, -a]
            
            self.dessiner()
            
    
    def tourner_gauche(self, a):
        x, y = self.piece_actu[0]
        peut_tourner = True 
        for i in self.piece_actu[1]:
            if x-i[1]>=10 or x-i[1]<0 or y+i[0]>=15 or y+i[0]<0 or self.matrice[int(x-i[1])][int(y+i[0])] == 1:
                peut_tourner = False 
        if peut_tourner:
            for i in self.piece_actu[1]:
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][0])
                self.jeu.delete(self.dico_polygon[(x+i[0], y+i[1])][1])
                del self.dico_polygon[(x+i[0], y+i[1])]
            
            for i in range(len(self.piece_actu[1])):
                a, b = self.piece_actu[1][i]
                self.piece_actu[1][i] = [-b, a]
            
            self.dessiner()
            
    def vider_ligne(self):
        
        for i in range(0, 15, 1):
            s = 0
            for j in range(10):
                s += self.matrice[j][i]
            if s == 10:
                #print(self.dico_polygon)
                #on actualise la score
                self.score += 500
                self.jeu.delete(self.afficher_score)
                self.afficher_score = self.jeu.create_text(500, 300, text="socre : "+ str(self.score), fill='white', font=('arial', 15))
                
                #on fait déscendre les pièce
                for j in range(10):
                    self.matrice[j][i] = 0
                    self.jeu.delete(self.dico_polygon[(j, i)][0])
                    self.jeu.delete(self.dico_polygon[(j, i)][1])
                    del self.dico_polygon[(j, i)]
                
                for k in range(i-1, -1, -1):
                    for j in range(10):
                        if self.matrice[j][k] == 1:
                            self.matrice[j][k] = 0
                            self.matrice[j][k+1] = 1
                            self.dico_polygon[(j, k+1)] = self.create_bloc(self.dico_polygon[(j, k)][2], (40*j, 40*(k+1)))
                            self.jeu.delete(self.dico_polygon[(j, k)][0])
                            self.jeu.delete(self.dico_polygon[(j, k)][1])
                            del self.dico_polygon[(j, k)]
                
       
    def debug(self, k):
        print(self.dico_polygon)
        


t = Tetris()
