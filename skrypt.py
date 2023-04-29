# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:34:26 2023

@author: vikto
"""

import numpy as np
import argparse
import math

class Transformacje: 
    
    #czesc pobierajaca dane
    
    def __init__(self):
        self.wspolrzedne = []
    
    # do pobierania wsp - wsp musza byc w pliku bez spacji w kolejnosci f,l,h, oddzielone przecinkami
    # file_path to scieżka skopiowana do danego pliku 
    def pobranie_wsp(self, file_path, rodzaj_transformacji): 
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coordinates = []
                for wsp in line.strip().split(','):
                    coordinates.append((wsp))
                self.wspolrzedne.append(coordinates)
            self.f_kolumna = [row[0] for row in self.wspolrzedne]
            self.l_kolumna = [row[1] for row in self.wspolrzedne]
            self.h_kolumna = [row[2] for row in self.wspolrzedne]
            self.dx_kolumna = [row[-1] for row in self.wspolrzedne]
                #return(f_kolumna,l_kolumna,h_kolumna)
            
            if rodzaj_transformacji == 'XYZ_to_flh':
                f,l,h = self.XYZ_to_flh(self.f_kolumna, self.l_kolumna, self.h_kolumna) 
                wynik = np.array([f,l,h])
                wynik = np.transpose(wynik)
                wynik1 = np.column_stack((wynik))
                print('wynik',wynik1)
                self.zapisz(wynik1, 'wyniki_XYZ_to_flh', 'Wyniki transformacji: współrzędne f,l,h')
                print('')
                print('Wynik transformacji XYZ do flh: ', wynik)
            
           
            elif rodzaj_transformacji == 'flh_to_XYZ':
                X,Y,Z = self.flh_to_XYZ(self.f_kolumna, self.l_kolumna, self.h_kolumna)
                wynik = np.column_stack((X,Y,Z))
                #print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_flh_to_XYZ', 'Wyniki transformacji: współrzędne X, Y, Z')
                #print('Wynik transformacji flh do XYZ: ', 'X =', X,'Y =', Y, 'Z =', Z)
                
    # NEU
            elif rodzaj_transformacji == "XYZ_to_neu":
                neu = self.XYZ_to_neu_lista(self.dx_kolumna,self.f_kolumna, self.l_kolumna, self.h_kolumna)
                wynik = np.column_stack((neu))
                print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_XYZ_2_neu', 'Wyniki transformacji neu:')
                print('Wynik transformacji XYZ do neu: ', neu)
                
                
            elif rodzaj_transformacji == 'fl_GRS80_to_2000':
                X2000,Y2000 = self.fl_80_2_2000_lista(self.f_kolumna,self.l_kolumna)
                wynik = np.column_stack((X2000,Y2000))
                #print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_fl_GRS80_2_2000', 'Wyniki transformacji: współrzędne X, Y w układzie 2000')
                #print('Wynik transformacji fl na elipsoidzie GRS80 do układu 2000: ', 'X =', X2000,'Y =', Y2000)
           
            
            elif rodzaj_transformacji == 'fl_GRS80_to_1992':
                X1992,Y1992 = self.fl_80_2_1992_lista(self.f_kolumna,self.l_kolumna)
                wynik = np.column_stack((X1992,Y1992))
                #print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_fl_GRS80_2_1992', 'Wyniki transformacji: współrzędne X, Y w układzie 1992')
                #print('Wynik transformacji fl na elipsoidzie GRS80 do układu 1992: ', 'X =', X1992,'Y =', Y1992)
                
  
            
            elif rodzaj_transformacji == 'fl_WGS84_to_2000':
                X2000,Y2000 = self.fl_84_2_2000_lista(self.f_kolumna,self.l_kolumna)
                wynik = np.column_stack((X2000,Y2000))
                #print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_fl_WGS84_2_2000', 'Wyniki transformacji: współrzędne X, Y w układzie 2000')
                #print('Wynik transformacji fl na elipsoidzie WGS84 do układu 2000: ', 'X =', X2000,'Y =', Y2000)
            
            elif rodzaj_transformacji == 'fl_WGS84_to_1992':
                X1992,Y1992 = self.fl_84_2_1992_lista(self.f_kolumna,self.l_kolumna)
                wynik = np.column_stack((X1992,Y1992))
                print('wynik',wynik)
                self.zapisz(wynik, 'wyniki_fl_WGS84_2_1992', 'Wyniki transformacji: współrzędne X, Y w układzie 1992')
                #print('Wynik transformacji fl na elipsoidzie WGS80 do układu 1992: ', 'X =', X1992,'Y =', Y1992)
            else:
                print('Podaj własciwą nazwę transformacji: „XYZ_to_flh”  „flh_to_XYZ”  „XYZ_to_neu”  “fl_GRS80_to_2000”  “fl_GRS80_to_1992”  “fl_WGS84_to_2000” lub „fl_WGS84_to_1992”')
            
                
    
    
    def zapisz(self, wynik, filename, header):
        with open(filename, "w") as f:
            f.write(header + "\n" + "\n")
            np.savetxt(f, wynik, delimiter=",", fmt="%.5f", newline='\n')
            print('Wyniki zostały zapisane w pliku o nazwie:', filename)
    
    
    
    # funkcje transformacji
    
    def rad_to_dms(self,x):
        sig = ''
        if x<0:
            sig = '-'
            x = abs(x)
        x = x*180/np.pi
        d = int(x)
        m = int (60*(x-d))
        s = (x - d - m/60)*3600
        print(sig, "%3d %2d %7.5f" %(d,abs(m),abs(s)))


    
# to powinno działać i dla pojedynczych i dla arrayów 

# cos tu n działa 
    def XYZ_to_flh(self,X,Y,Z):
        a = 6378137
        e2 = 0.00669438002290 
        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z, dtype=np.float64)
        p = np.sqrt(np.square(X.astype(np.float64)) + np.square(Y.astype(np.float64)))
        f = np.arctan(np.divide(Z,(p*(1-e2))).astype(np.float64))
        while True:
            N = a/np.sqrt(1-e2*np.sin(f)**2)
            h = (p/np.cos(f))-N
            fp = f
            f = np.arctan(np.divide(Z,(p*(1-e2*(N/(N+h))))))
            if np.all(np.abs(fp - f) < (0.000001/206265)):
                break
        X = np.array(X).astype(np.float64)
        Y = np.array(Y).astype(np.float64)
        l = np.arctan2(Y,X)

        return [f, l, h]


    
    def flh_to_XYZ(self, f, l, h):
        a = 6378137
        e2 = 0.00669438002290
        
        f = np.array(f).astype(float)
        l = np.array(l).astype(float)
        h = np.array(h).astype(float)

        N = a/np.sqrt(1-e2*np.sin(f)**2)

        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - e2) + h) * np.sin(f)
        
        return (X, Y, Z)
    
    

    def XYZ_to_neu(self,dx,dy,dz,X,Y,Z):
        a = 6378137
        e2 = 0.00669438002290 
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p*(1-e2)))
        delta_wsp = np.hstack((dx,dy,dz))
        while True:
            N = a/np.sqrt(1-e2*np.sin(f)**2)
            h = (p/np.cos(f))-N
            fp = f
            f = np.arctan(Z/(p*(1-e2*(N/(N+h)))))
            if np.abs(fp - f) < (0.000001/206265):
                break
        l = np.arctan2(Y,X)
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l), np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f), 0, np.sin(f)]])       
        return(R.T @ delta_wsp)
    

    # def XYZ_to_neu_lista(self, dX, X, Y, Z):
    #     a = 6378137
    #     e2 = 0.00669438002290 
    #     p = np.sqrt(np.array(X).astype(np.float64)**2 + np.array(Y).astype(np.float64)**2)
    #     f = np.arctan(np.array(Z).astype(np.float64)/(p*(1-e2)))
    #     while True:
    #         N = a/np.sqrt(1-e2*np.sin(f)**2)
    #         h = (p/np.cos(f))-N
    #         fp = f
    #         f = np.arctan(np.array(Z).astype(np.float64)/(p*(1-e2*(N.astype(np.float64)/(N.astype(np.float64)+h.astype(np.float64))))))
    #         if np.all(np.abs(fp - f) < (0.000001/206265)):
    #             break
    #     l = np.arctan2(np.array(Y).astype(np.float64), np.array(X).astype(np.float64))
    #     n = len(dX)
    #     R = np.zeros((3, 3*n))
    #     for i in range(n):
    #         f_i, l_i = f[i], l[i]
    #         R[:, 3*i:3*i+3] = np.array([[-np.sin(f_i)*np.cos(l_i), -np.sin(l_i), np.cos(f_i)*np.cos(l_i)],
    #                                     [-np.sin(f_i)*np.sin(l_i), np.cos(l_i), np.cos(f_i)*np.sin(l_i)],
    #                                     [np.cos(f_i), 0, np.sin(f_i)]])
    #     dX = np.array(dX, dtype=float)
    #     #return (dX @ R)
    #     return(dX @ R.T)





  #  def __init__(self, a=6378137, e2=0.00669438002290):
        # self.a = a
        # self.e2 = e2
    


    def Rneu(self, f, l):
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l), np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f), 0, np.sin(f)]])
        return R





















    # funkcja do zamieniania stopni min sek na przecinkowe stopnie
    def dms2degrees(self,d,m,s):
        d = d + (m/60) + (s/3600)
        return(d) 

    def dms2rad(self, d, m, s):
        kat_rad = np.radians(d + m/60 + s/3600)
        return kat_rad   
    
    # lambda poprawiona
    def lambda0_2000(self, l_deg):
        #l = l_deg*np.pi/180
        l = np.array(l_deg, dtype=float) * np.pi/180
        
        if l < self.dms2rad(15, 00, 00) or l == self.dms2rad(15, 00, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            #print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(15, 00, 00) and l < self.dms2rad(16, 30, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            #print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(16, 30, 00) and l < self.dms2rad(19, 30, 00):
            l0 = self.dms2rad(18, 00, 00)
            nr_strefy = 6
            #print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(19, 30, 00) and l < self.dms2rad(22, 30, 00):
            l0 = self.dms2rad(21, 00, 00)
            nr_strefy = 7
            #print('l0 =', l0,'nr strefy = ', nr_strefy)
        else:
            l0 = self.dms2rad(24, 00, 00)
            nr_strefy = 8
            #print('l0 =', l0,'nr strefy = ', nr_strefy)
        return l0, nr_strefy
    
    def l0_lista(self, f_lista, l_lista):
        l0_list = []
        nr_strefy_list = []
        for l in l_lista:
            l0, nr_strefy = self.lambda0_2000(l)
            l0_list.append(l0)
            nr_strefy_list.append(nr_strefy)
        return(l0_list, nr_strefy_list)
    
    
    

   
    
    # z fi lam GRS80 do 2000
    
    def fl_80_2_2000(self, f, l): #f,l w stopniach 
        l0,nr_strefy = self.lambda0_2000(l)
        f = f/180*np.pi
        l = l/180*np.pi
         
        # elipsoida GRS80
        a = 6378137 #m
        e2 = 0.00669438002290
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l - l0
        t = np.tan(f)
        eta2 = e2prim * ((np.cos(f))**2)
        N = a / np.sqrt(1- e2 * np.sin(f)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f))
        X_gk_2000 = sigma + ((d_l**2) / 2) * N * np.sin(f) * np.cos(f) * (1 + ((d_l**2) / 12) * ((np.cos(f))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_2000 = d_l * N * np.cos(f) * (1 + (((d_l**2) / 6) * ((np.cos(f))**2) * (1 - (t**2) + eta2)) + (((d_l**4) / 120) * ((np.cos(f))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2))))
        # czesc do 2000
        m0 = 0.999923
        X2000 = X_gk_2000 * m0
        Y2000= m0 * Y_gk_2000 + nr_strefy * 1000000 + 500000
        return(X2000,Y2000)
     
# dwa rózne dla pliku i danych bo idk jak zrobic w jednym

    def fl_80_2_2000_lista(self, f_lista, l_lista):
        l0_list, nr_strefy = self.l0_lista(f_lista, l_lista)

        f_lista = [float(f)/180*np.pi for f in f_lista]
        l_lista = [float(l)/180*np.pi for l in l_lista]

        a = 6378137 
        e2 = 0.00669438002290
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        
        l_lista = l_lista
        d_l = [l_lista[i] - l0_list[i] for i in range(len(l_lista))]

        t = np.tan(f_lista)
        eta2 = e2prim * ((np.cos(f_lista))**2)
        N = a / np.sqrt(1- e2 * np.sin(f_lista)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        
        f_array = np.array(f_lista)
        sigma = a * (A0 * f_array - A2 * np.sin(2 * f_array) + A4 * np.sin(4 * f_array) - A6 * np.sin(6 * f_array))

        X_gk_2000 = sigma + ((np.array(d_l)**2) / 2) * N * np.sin(f_lista) * np.cos(f_lista) * (1 + ((np.array(d_l)**2) / 12) * ((np.cos(f_lista))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((np.array(d_l)**4) / 360) * ((np.cos(f_lista))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_2000 = np.array(d_l) * N * np.cos(f_lista) * (1 + (((np.array(d_l)**2) / 6) * ((np.cos(f_lista))**2) * (1 - (t**2) + eta2)) + (((np.array(d_l)**4) / 120) * ((np.cos(f_lista))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2))))

        m0 = 0.999923
        X2000 = X_gk_2000 * m0
        #Y2000 = m0 * Y_gk_2000 + nr_strefy * 1000000 + 500000
        Y2000 = m0 * Y_gk_2000 + np.repeat(nr_strefy, 1) * 1000000 + 500000

        #Y2000 = [m0 * Y_gk_2000[i] + nr_strefy[i] * 1000000 + 500000 for i in range(len(Y_gk_2000))]
        return (X2000, Y2000)

    
# ^^ działa


        
    # z fi lam GRS80 do 1992
        
    def fl_80_2_1992(self, f, l): #f,l w stopniach 
        l0 = self.dms2rad(19, 00, 00)
        f = f/180*np.pi
        l = l/180*np.pi
        
        # elipsoida GRS80
        a = 6378137 #m
        e2 = 0.00669438002290
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l - l0
        t = np.tan(f)
        eta2 = e2prim * ((np.cos(f))**2)
        N = a / np.sqrt(1- e2 * np.sin(f)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f))
        X_gk_92 = sigma + ((d_l**2) / 2) * N * np.sin(f) * np.cos(f) * (1 + ((d_l**2) / 12) * ((np.cos(f))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_92 = d_l * N * np.cos(f) * (1 + ((d_l**2) / 6) * ((np.cos(f))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        # do 1992
        m0 = 0.9993
        X1992 = X_gk_92 * m0 - 5300000
        Y1992 = m0 * Y_gk_92 + 500000
        return(X1992,Y1992)
    
    def fl_80_2_1992_lista(self, f_lista, l_lista): #f,l w stopniach 
        l0 = self.dms2rad(19, 00, 00)
        
        
        f_lista = [float(f)/180*np.pi for f in f_lista]
        l_lista = [float(l)/180*np.pi for l in l_lista]
        
        # elipsoida GRS80
        a = 6378137 #m
        e2 = 0.00669438002290
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l_lista - l0
        t = np.tan(f_lista)
        eta2 = e2prim * ((np.cos(f_lista))**2)
        N = a / np.sqrt(1- e2 * np.sin(f_lista)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = [a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f)) for f in f_lista]

        #sigma = a * (A0 * f_lista - A2 * np.sin(2 * f_lista) + A4 * np.sin(4 * f_lista) - A6 * np.sin(6 * f_lista))
        X_gk_92 = sigma + ((d_l**2) / 2) * N * np.sin(f_lista) * np.cos(f_lista) * (1 + ((d_l**2) / 12) * ((np.cos(f_lista))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f_lista))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_92 = d_l * N * np.cos(f_lista) * (1 + ((d_l**2) / 6) * ((np.cos(f_lista))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f_lista))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        # do 1992
        m0 = 0.9993
        X1992 = X_gk_92 * m0 - 5300000
        Y1992 = m0 * Y_gk_92 + 500000
        return X1992, Y1992


    
    
   # z fi lam WGS84 do 2000
   # wgs
   #a = 6378137 # m	
   # e2 = 0.00335281068118231893543414612613
    
    def fl_84_2_2000(self, f, l): #f,l w stopniach 
        l0,nr_strefy = self.lambda0_2000(l)
        f = f/180*np.pi
        l = l/180*np.pi
         
        # elipsoida wgs84
        a = 6378137 # m	
        e2 = 0.00335281068118231893543414612613
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l - l0
        t = np.tan(f)
        eta2 = e2prim * ((np.cos(f))**2)
        N = a / np.sqrt(1- e2 * np.sin(f)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f))
        X84_gk_2000 = sigma + ((d_l**2) / 2) * N * np.sin(f) * np.cos(f) * (1 + ((d_l**2) / 12) * ((np.cos(f))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y84_gk_2000 = d_l * N * np.cos(f) * (1 + ((d_l**2) / 6) * ((np.cos(f))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        # 2000
        m0 = 0.999923
        X2000 = X84_gk_2000 * m0
        Y2000= m0 * Y84_gk_2000 + nr_strefy * 1000000 + 500000
        return(X2000,Y2000)
    
    
    
    
    
    
    
    
    
    
    def fl_84_2_2000_lista(self, f_lista, l_lista):
        l0_list, nr_strefy = self.l0_lista(f_lista, l_lista)

        f_lista = [float(f)/180*np.pi for f in f_lista]
        l_lista = [float(l)/180*np.pi for l in l_lista]

        # elipsoida wgs84
        a = 6378137 # m	
        e2 = 0.00335281068118231893543414612613
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        
        
        d_l = [l_lista[i] - l0_list[i] for i in range(len(l_lista))]

        t = np.tan(f_lista)
        eta2 = e2prim * ((np.cos(f_lista))**2)
        N = a / np.sqrt(1- e2 * np.sin(f_lista)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        
        f_array = np.array(f_lista)
        sigma = a * (A0 * f_array - A2 * np.sin(2 * f_array) + A4 * np.sin(4 * f_array) - A6 * np.sin(6 * f_array))

        X_gk_2000 = sigma + ((np.array(d_l)**2) / 2) * N * np.sin(f_lista) * np.cos(f_lista) * (1 + ((np.array(d_l)**2) / 12) * ((np.cos(f_lista))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((np.array(d_l)**4) / 360) * ((np.cos(f_lista))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_2000 = np.array(d_l) * N * np.cos(f_lista) * (1 + (((np.array(d_l)**2) / 6) * ((np.cos(f_lista))**2) * (1 - (t**2) + eta2)) + (((np.array(d_l)**4) / 120) * ((np.cos(f_lista))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2))))

        m0 = 0.999923
        X2000 = X_gk_2000 * m0
        #Y2000 = m0 * Y_gk_2000 + nr_strefy * 1000000 + 500000
        Y2000 = m0 * Y_gk_2000 + np.repeat(nr_strefy, 1) * 1000000 + 500000

        #Y2000 = [m0 * Y_gk_2000[i] + nr_strefy[i] * 1000000 + 500000 for i in range(len(Y_gk_2000))]
        return (X2000, Y2000)

    














    # z fi lam wgs84 do 1992
    
    def fl_84_2_1992(self, f, l): #f,l w stopniach 
        l0 = self.dms2rad(19, 00, 00)
        f = f/180*np.pi
        l = l/180*np.pi
        
        # elipsoida wgs84
        a = 6378137 # m	
        e2 = 0.00335281068118231893543414612613
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l - l0
        t = np.tan(f)
        eta2 = e2prim * ((np.cos(f))**2)
        N = a / np.sqrt(1- e2 * np.sin(f)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f))
        X84_gk_92 = sigma + ((d_l**2) / 2) * N * np.sin(f) * np.cos(f) * (1 + ((d_l**2) / 12) * ((np.cos(f))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y84_gk_92 = d_l * N * np.cos(f) * (1 + ((d_l**2) / 6) * ((np.cos(f))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        # do 1992
        m0 = 0.9993
        X1992 = X84_gk_92 * m0 - 5300000
        Y1992 = m0 * Y84_gk_92 + 500000
        return(X1992,Y1992)  
    
    
    
    def fl_84_2_1992_lista(self, f_lista, l_lista): #f,l w stopniach 
        l0 = self.dms2rad(19, 00, 00)
        
        
        f_lista = [float(f)/180*np.pi for f in f_lista]
        l_lista = [float(l)/180*np.pi for l in l_lista]
        
        # elipsoida wgs84
        a = 6378137 # m	
        e2 = 0.00335281068118231893543414612613
        
        b2 = a**2 * (1 - e2)
        e2prim=((a**2) - b2) / b2
        d_l = l_lista - l0
        t = np.tan(f_lista)
        eta2 = e2prim * ((np.cos(f_lista))**2)
        N = a / np.sqrt(1- e2 * np.sin(f_lista)**2)
        A0 = 1 - (e2 / 4) - ((3 * (e2**2)) / 64) - ((5 * (e2**3)) / 256)
        A2 = (3 / 8) * (e2 + ((e2**2) / 4) + (15 * (e2**3)) / 128)
        A4 = (15 / 256) * (e2**2 + ((3 * (e2**3)) / 4))
        A6 = (35 * (e2**3)) / 3072
        sigma = [a * (A0 * f - A2 * np.sin(2 * f) + A4 * np.sin(4 * f) - A6 * np.sin(6 * f)) for f in f_lista]

        #sigma = a * (A0 * f_lista - A2 * np.sin(2 * f_lista) + A4 * np.sin(4 * f_lista) - A6 * np.sin(6 * f_lista))
        X_gk_92 = sigma + ((d_l**2) / 2) * N * np.sin(f_lista) * np.cos(f_lista) * (1 + ((d_l**2) / 12) * ((np.cos(f_lista))**2) * (5 - (t**2) + 9 * eta2 + 4 * eta2**2) + ((d_l**4) / 360) * ((np.cos(f_lista))**4) * (61 - 58 * (t**2) + (t**4) + 270 * eta2 - 330 * eta2 * (t**2)))
        Y_gk_92 = d_l * N * np.cos(f_lista) * (1 + ((d_l**2) / 6) * ((np.cos(f_lista))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f_lista))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        # do 1992
        m0 = 0.9993
        X1992 = X_gk_92 * m0 - 5300000
        Y1992 = m0 * Y_gk_92 + 500000
        return X1992, Y1992

    
    
    
    
    
    
    
    
   

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transformacje geodezyjne')
    subparsers = parser.add_subparsers(title='Operacja', dest='operation', required=True)

    parser_pobranie_wsp = subparsers.add_parser('pobierz_dane', help = 'Pobierz współrzędne do obliczeń z pliku txt')
    parser_pobranie_wsp.add_argument('file_path', help='scieżka do pliku w formacie cos/cos/folder/plik')
    parser_pobranie_wsp.add_argument('rodzaj_transformacji', help = 'podaj jaki rodzaj transformacji wykonać na załadowanych współrzędnych')

    parser_zapisz = subparsers.add_parser('zapisz_dane', help = 'zapisz dane do pliku txt w obecnym folderze')
    parser_zapisz.add_argument('wynik', help = 'wyniki transformacji')
    parser_zapisz.add_argument('filename', help = 'nazwa pliku')
    parser_zapisz.add_argument('header', help = 'pierwszy wiersz w pliku')


    parser_XYZ = subparsers.add_parser('XYZ_to_flh', help='Transformuj XYZ na flh')
    parser_XYZ.add_argument('X', type=float, help='współrzędna X')
    parser_XYZ.add_argument('Y', type=float, help='współrzędna Y')
    parser_XYZ.add_argument('Z', type=float, help='współrzędna Z')

    parser_flh = subparsers.add_parser('flh_to_XYZ', help='Transformuj flh na XYZ')
    parser_flh.add_argument('f', type=float, help='współrzędna fi')
    parser_flh.add_argument('l', type=float, help='współrzędna lambda')
    parser_flh.add_argument('h', type=float, help='współrzędna h')


    parser_XYZ_to_neu = subparsers.add_parser('XYZ_to_neu', help='Transformuj XYZ na neu')
    parser_XYZ_to_neu.add_argument('dx', type=float, help='delta X')
    parser_XYZ_to_neu.add_argument('dy', type=float, help='delta Y')
    parser_XYZ_to_neu.add_argument('dz', type=float, help='delta Z')
    parser_XYZ_to_neu.add_argument('X', type=float, help='współrzędna X')
    parser_XYZ_to_neu.add_argument('Y', type=float, help='współrzędna Y')
    parser_XYZ_to_neu.add_argument('Z', type=float, help='współrzędna Z')

    parser_XYZ_to_neu_lista = subparsers.add_parser('XYZ_to_neu_lista', help='Transformuj XYZ na neu')
    parser_XYZ_to_neu_lista.add_argument('lista dX', type=float, help='delta X')
    parser_XYZ_to_neu_lista.add_argument('lista X', type=float, help='lista współrzędnych X')
    parser_XYZ_to_neu_lista.add_argument('lista Y', type=float, help='lista współrzędnych Y')
    parser_XYZ_to_neu_lista.add_argument('lista Z', type=float, help='lista współrzędnych Z')



    parser_fl_GRS80_to_GK2000 = subparsers.add_parser('fl_GRS80_to_2000', help='Transformuj fl GRS80 na 2000')
    parser_fl_GRS80_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')
    
    # druga do listy
    parser_fl_GRS80_to_GK2000_lista = subparsers.add_parser('fl_GRS80_to_2000_lista', help='Transformuj fl GRS80 na 2000 z pliku')
    parser_fl_GRS80_to_GK2000_lista.add_argument('f_lista', type=float, help='lista współrzędnych fi w stopniach')
    parser_fl_GRS80_to_GK2000_lista.add_argument('l_lista', type=float, help='lista współrzędnych lambda w stopniach')
    

    parser_fl_GRS80_to_GK1992 = subparsers.add_parser('fl_GRS80_to_1992', help='Transformuj fl GRS80 na 1992')
    parser_fl_GRS80_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    #druga do listy
    parser_fl_GRS80_to_GK1992_lista = subparsers.add_parser('fl_GRS80_to_1992_lista', help='Transformuj fl GRS80 na 1992')
    parser_fl_GRS80_to_GK1992_lista.add_argument('f_lista', type=float, help='lista współrzędnych fi w stopniach')
    parser_fl_GRS80_to_GK1992_lista.add_argument('l_lista', type=float, help='lista współrzędnych lambda w stopniach')





    parser_fl_WGS84_to_GK2000 = subparsers.add_parser('fl_WGS84_to_2000', help='Transformuj fl WGS84 na 2000')
    parser_fl_WGS84_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_WGS84_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')
    
    parser_fl_WGS84_to_GK2000_lista = subparsers.add_parser('fl_WGS84_to_2000_lista', help='Transformuj fl WGS84 na 2000')
    parser_fl_WGS84_to_GK2000_lista.add_argument('f_lista', type=float, help='lista współrzędny fi w stopniach')
    parser_fl_WGS84_to_GK2000_lista.add_argument('l_lista', type=float, help='lista współrzędnych lambda w stopniach')
    
    


    parser_fl_WGS84_to_GK1992 = subparsers.add_parser('fl_WGS84_to_1992', help='Transformuj fl WGS84 na 1992')
    parser_fl_WGS84_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_WGS84_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')
    
    parser_fl_WGS84_to_GK1992_lista = subparsers.add_parser('fl_WGS84_to_1992_lista', help='Transformuj fl WGS84 na 1992')
    parser_fl_WGS84_to_GK1992_lista.add_argument('f_lista', type=float, help='lista współrzędny fi w stopniach')
    parser_fl_WGS84_to_GK1992_lista.add_argument('l_lista', type=float, help='lista współrzędny lamdba w stopniach')
    
    
    
    

    args = parser.parse_args()

    transform = Transformacje()


    if args.operation == 'pobierz_dane':
        result = transform.pobranie_wsp(args.file_path, args.rodzaj_transformacji)
    elif args.operation == 'XYZ_to_flh':
        f,l,h = transform.XYZ_to_flh(args.X, args.Y, args.Z)
        print('flh w radianach:', f,l,h)
        print("Szerokość geodezyjna: ", f*180/np.pi, "°")
        print("Długość geodezyjna: ", l*180/np.pi, "°")
        print("Wysokość geodezyjna: ", h)    
    elif args.operation == 'flh_to_XYZ':
        X,Y,Z = transform.flh_to_XYZ(args.f, args.l, args.h)
        print("Współrzędna X: ", X)
        print("Współrzędna Y: ", Y)
        print("Współrzędna Z: ", Z)   
        
        
    elif args.operation == 'XYZ_to_neu':
        result = transform.XYZ_to_neu(args.dx, args.dy, args.dz, args.X, args.Y, args.Z) 
        print("Współrzędne neu", result)
        
    elif args.operation == 'XYZ_to_neu_lista':
        result = transform.XYZ_to_neu(args.dX, args.X, args.Y, args.Z) 
        print("Współrzędne neu", result)        
        
        
    elif args.operation == 'fl_GRS80_to_2000':
        X2000,Y2000 = transform.fl_80_2_2000(args.f, args.l)
        print("Współrzędna X2000: ", X2000)
        print("Współrzędna Y2000: ", Y2000)
        
    # druga do listy
    elif args.operation == 'fl_GRS80_to_2000_lista':
        X2000,Y2000 = transform.fl_80_2_2000_lista(args.f_lista, args.l_lista)
        print("Lista współrzędnych X2000: ", X2000)
        print("Lista współrzędnych Y2000: ", Y2000) 
    
    
    
    
    elif args.operation == 'fl_GRS80_to_1992':
        X1992,Y1992 = transform.fl_80_2_1992(args.f, args.l) 
        print("Współrzędna X1992: ", X1992)
        print("Współrzędna Y1992: ", Y1992)
    
    #druga do listy
    elif args.operation == 'fl_GRS80_to_1992_lista':
        X1992,Y1992 = transform.fl_80_2_1992_lista(args.f_lista, args.l_lista)
        print("Lista współrzędnych X1992: ", X1992)
        print("Lista współrzędnych Y1992: ", Y1992) 
        
        
        
    elif args.operation == 'fl_WGS84_to_2000':
        X2000,Y2000 = transform.fl_84_2_2000(args.f, args.l)
        print("Współrzędna X2000: ", X2000)
        print("Współrzędna Y2000: ", Y2000)
        
    elif args.operation == 'fl_WGS84_to_2000_lista':
        X2000,Y2000 = transform.fl_84_2_2000_lista(args.f_lista, args.l_lista)
        print("Lista współrzędnych X2000: ", X2000)
        print("lista współrzędnych Y2000: ", Y2000)
        
        
        
    elif args.operation == 'fl_WGS84_to_1992':
        X1992,Y1992 = transform.fl_84_2_1992(args.f, args.l)
        print("Współrzędna X1992: ", X1992)
        print("Współrzędna Y1992: ", Y1992)
        
    elif args.operation == 'fl_WGS84_to_1992_lista':
        X1992,Y1992 = transform.fl_84_2_1992_lista(args.f_lista, args.l_lista)
        print("Lista współrzędnych X1992: ", X1992)
        print("Lista współrzędnych Y1992: ", Y1992)
       
        
        
    else:
        print("Proszę wprowadzić nazwę operacji z podanych: XYZ_to_flh, flh_to_XYZ, XYZ_to_neu, fl_GRS80_to_2000, fl_GRS80_to_1992, fl_WGS84_to_2000, fl_WGS84_to_1992 ")




        
    
    