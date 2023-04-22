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
                #return(f_kolumna,l_kolumna,h_kolumna)
            
            if rodzaj_transformacji == 'XYZ_to_flh':
                f,l,h = self.XYZ_to_flh(self.f_kolumna, self.l_kolumna, self.h_kolumna) 
                wynik = np.array([f,l,h])
                wynik = np.transpose(wynik)
                print('')
                print('Wynik transformacji XYZ do flh: ', wynik)
            
            # do tego momentu działa, reszta nie 
            
            elif rodzaj_transformacji == 'flh_to_XYZ':
                X,Y,Z = self.flh_to_XYZ(self.f_kolumna, self.l_kolumna, self.h_kolumna)
                print('Wynik transformacji flh do XYZ: ', 'X =', X,'Y =', Y, 'Z =', Z)
                
            elif rodzaj_transformacji == 'fl_GRS80_to_2000':
                X2000,Y2000 = self.fl_80_2_2000(self.f_kolumna,self.l_kolumna)
                print('Wynik transformacji fl na elipsoidzie GRS80 do układu 2000: ', 'X =', X2000,'Y =', Y2000)
            
            elif rodzaj_transformacji == 'fl_GRS80_to_1992':
                X1992,Y1992 = self.fl_80_2_1992(self.f_kolumna,self.l_kolumna)
                print('Wynik transformacji fl na elipsoidzie GRS80 do układu 1992: ', 'X =', X1992,'Y =', Y1992)
            
            elif rodzaj_transformacji == 'fl_WGS84_to_2000':
                X2000,Y2000 = self.fl_84_2_2000(self.f_kolumna,self.l_kolumna)
                print('Wynik transformacji fl na elipsoidzie WGS84 do układu 2000: ', 'X =', X2000,'Y =', Y2000)
            
            elif rodzaj_transformacji == 'fl_WGS84_to_1992':
                X1992,Y1992 = self.fl_84_2_1992(self.f_kolumna,self.l_kolumna)
                print('Wynik transformacji fl na elipsoidzie WGS80 do układu 1992: ', 'X =', X1992,'Y =', Y1992)
        return('transformacja ukończona')
                
    
    
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

#ta wersja dla pojedynczych X Y Z  
      
    # def XYZ_to_flh(self,X,Y,Z):
    #     a = 6378137
    #     e2 = 0.00669438002290 
    #     p = np.sqrt(X**2 + Y**2)
    #     f = np.arctan(Z/(p*(1-e2)))
    #     while True:
    #         N = a/np.sqrt(1-e2*np.sin(f)**2)
    #         h = (p/np.cos(f))-N
    #         fp = f
    #         f = np.arctan(Z/(p*(1-e2*(N/(N+h)))))
    #         if np.abs(fp - f) < (0.000001/206265):
    #             break
    #     l = np.arctan2(Y,X) 
    #     #self.rad_to_dms(f)
    #     #self.rad_to_dms(l)
    #     return(f,l,h)
    
# to powinno działać i dla pojedynczych i dla arrayów 
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
        #self.rad_to_dms(f)
        #self.rad_to_dms(l)
        return [f, l, h]


    
    def flh_to_XYZ(self,f,l,h):
        a = 6378137
        e2 = 0.00669438002290 
        N = a/np.sqrt(1-e2*np.sin(f)**2)
        X = (N + h)*np.cos(f)*np.cos(l)
        Y = (N + h)*np.cos(f)*np.sin(l)
        Z = (N*(1-e2)+h)*np.sin(f)
        return(X,Y,Z)
    
    def XYZ_to_neu(self,dX,X,Y,Z):
        a = 6378137
        e2 = 0.00669438002290 
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p*(1-e2)))
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
        return(R.T @ dX)


    # funkcja do zamieniania stopni min sek na przecinkowe stopnie
    def dms2degrees(self,d,m,s):
        d = d + (m/60) + (s/3600)
        return(d) 

    def dms2rad(self, d, m, s):
        kat_rad = np.radians(d + m/60 + s/3600)
        return kat_rad   
    
    # lambda poprawiona
    def lambda0_2000(self, l_deg):
        l = l_deg*np.pi/180
        if l < self.dms2rad(15, 00, 00) or l == self.dms2rad(15, 00, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(15, 00, 00) and l < self.dms2rad(16, 30, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(16, 30, 00) and l < self.dms2rad(19, 30, 00):
            l0 = self.dms2rad(18, 00, 00)
            nr_strefy = 6
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l > self.dms2rad(19, 30, 00) and l < self.dms2rad(22, 30, 00):
            l0 = self.dms2rad(21, 00, 00)
            nr_strefy = 7
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        else:
            l0 = self.dms2rad(24, 00, 00)
            nr_strefy = 8
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        return l0, nr_strefy
    
    # stara funkcja
    # def lambda0_2000(self, l_deg):
    #     l = l_deg*np.pi/180
    #     if l<self.dms2rad(15, 00, 00):
    #         l0 = self.dms2rad(15, 00, 00)
    #         nr_strefy = 5
    #         print('l0 =', l0,'nr strefy = ', nr_strefy)
    #     elif l<self.dms2rad(16, 30, 00):
    #         l0 = self.dms2rad(15, 00, 00)
    #         nr_strefy = 5
    #         print('l0 =', l0,'nr strefy = ', nr_strefy)
    #     elif l<self.dms2rad(19, 30, 00):
    #         l0 = self.dms2rad(18, 00, 00)
    #         nr_strefy = 6
    #         print('l0 =', l0,'nr strefy = ', nr_strefy)
    #     elif l<self.dms2rad(22, 30, 00):
    #         l0 = self.dms2rad(21, 00, 00)
    #         nr_strefy = 7
    #         print('l0 =', l0,'nr strefy = ', nr_strefy)
    #     else:
    #         l0 = self.dms2rad(24, 00, 00)
    #         nr_strefy = 8
    #         print('l0 =', l0,'nr strefy = ', nr_strefy)
    #     return l0, nr_strefy
 
    

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
    
    
    
   

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transformacje geodezyjne')
    subparsers = parser.add_subparsers(title='Operacja', dest='operation', required=True)

    parser_pobranie_wsp = subparsers.add_parser('pobierz_dane', help = 'Pobierz współrzędne do obliczeń z pliku txt')
    parser_pobranie_wsp.add_argument('file_path', help='scieżka do pliku w formacie cos/cos/folder/plik')
    parser_pobranie_wsp.add_argument('rodzaj_transformacji', help = 'podaj jaki rodzaj transformacji wykonać na załadowanych współrzędnych')

    parser_XYZ = subparsers.add_parser('XYZ_to_flh', help='Transformuj XYZ na flh')
    parser_XYZ.add_argument('X', type=float, help='współrzędna X')
    parser_XYZ.add_argument('Y', type=float, help='współrzędna Y')
    parser_XYZ.add_argument('Z', type=float, help='współrzędna Z')

    parser_flh = subparsers.add_parser('flh_to_XYZ', help='Transformuj flh na XYZ')
    parser_flh.add_argument('f', type=float, help='współrzędna fi')
    parser_flh.add_argument('l', type=float, help='współrzędna lambda')
    parser_flh.add_argument('h', type=float, help='współrzędna h')


    parser_XYZ_to_neu = subparsers.add_parser('XYZ_to_neu', help='Transformuj XYZ na neu')
    parser_XYZ_to_neu.add_argument('dX', type=float, help='delta X')
    parser_XYZ_to_neu.add_argument('X', type=float, help='współrzędna X')
    parser_XYZ_to_neu.add_argument('Y', type=float, help='współrzędna Y')
    parser_XYZ_to_neu.add_argument('Z', type=float, help='współrzędna Z')


    parser_fl_GRS80_to_GK2000 = subparsers.add_parser('fl_GRS80_to_2000', help='Transformuj fl GRS80 na 2000')
    parser_fl_GRS80_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    parser_fl_GRS80_to_GK1992 = subparsers.add_parser('fl_GRS80_to_1992', help='Transformuj fl GRS80 na 1992')
    parser_fl_GRS80_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')


    parser_fl_WGS84_to_GK2000 = subparsers.add_parser('fl_WGS84_to_2000', help='Transformuj fl WGS84 na 2000')
    parser_fl_WGS84_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_WGS84_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    parser_fl_WGS84_to_GK1992 = subparsers.add_parser('fl_WGS84_to_1992', help='Transformuj fl WGS84 na 1992')
    parser_fl_WGS84_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_WGS84_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    args = parser.parse_args()

    transform = Transformacje()


    if args.operation == 'pobierz_dane':
        result = transform.pobranie_wsp(args.file_path, args.rodzaj_transformacji)
    if args.operation == 'XYZ_to_flh':
        result = transform.XYZ_to_flh(args.X, args.Y, args.Z)
    elif args.operation == 'flh_to_XYZ':
        result = transform.flh_to_XYZ(args.f, args.l, args.h)
    if args.operation == 'XYZ_to_neu':
        result = transform.XYZ_to_neu(args.dX, args.X, args.Y, args.Z)        
    elif args.operation == 'fl_GRS80_to_2000':
        result = transform.fl_80_2_2000(args.f, args.l)
    elif args.operation == 'fl_GRS80_to_1992':
        result = transform.fl_80_2_1992(args.f, args.l) 
    elif args.operation == 'fl_WGS84_to_2000':
        result = transform.fl_84_2_2000(args.f, args.l)
    elif args.operation == 'fl_WGS84_to_1992':
        result = transform.fl_84_2_1992(args.f, args.l)

        
        

    print(result)



        
    
    