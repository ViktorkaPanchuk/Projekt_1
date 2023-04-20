# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:34:26 2023

@author: vikto
"""

# Program/skrypt musi:
# - być napisany jako klasa zawierająca metody implementujące poszczególne transformacje
# - posiadać strukturę, w której definicje są oddzielone od wywołań klauzulą 'if __name__ == "__main__"'
# - implementować następujące trnsformacje (bez analizy dokładnościowej):
#     - XYZ (geocentryczne) -> BLH (elipsoidalne fi, lambda, h) - pomoce naukowe: http://www.asgeupos.pl/index.php?wpg_type=tech_transf&sub=xyz_blh, https://ewmapa.pl/dane/wytyczne_g-1.10.pdf, http://www.geonet.net.pl/images/2002_12_uklady_wspolrz.pdf
#     - BLH -> XYZ - pomoce naukowe: http://www.asgeupos.pl/index.php?wpg_type=tech_transf&sub=xyz_blh, https://ewmapa.pl/dane/wytyczne_g-1.10.pdf, http://www.geonet.net.pl/images/2002_12_uklady_wspolrz.pdf
#     - XYZ -> NEUp (topocentryczne northing, easting, up) - pomoce naukowe: https://notatek.pl/transformacja-wspolrzednych-geocentrycznych-odbiornika-do-wspolrzednych-topocentrycznych
#     - BL(GRS80, WGS84, ew. Krasowski) -> 2000 - pomoce naukowe: http://www.geonet.net.pl/images/2002_12_uklady_wspolrz.pdf, https://ewmapa.pl/dane/wytyczne_g-1.10.pdf, http://www.asgeupos.pl/index.php?wpg_type=tech_transf&sub=xyz_blh
#     - BL(GRS80, WGS84, ew. Krasowski) -> 1992 - pomoce naukowe: http://www.geonet.net.pl/images/2002_12_uklady_wspolrz.pdf, https://ewmapa.pl/dane/wytyczne_g-1.10.pdf, http://www.asgeupos.pl/index.php?wpg_type=tech_transf&sub=xyz_blh



import numpy as np
import argparse

class Transformacje: 
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
        
    def XYZ_to_flh(self,X,Y,Z):
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
        self.rad_to_dms(f)
        self.rad_to_dms(l)
        return(f,l,h)
    
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

#karo
    # z fi lam GRS80 do 2000
    
    def dms2rad(self, d, m, s):
        kat_rad = np.radians(d + m/60 + s/3600)
        return kat_rad   
    
    def lambda0_2000(self, l_deg):
        l = l_deg*np.pi/180
        if l<self.dms2rad(15, 00, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l<self.dms2rad(16, 30, 00):
            l0 = self.dms2rad(15, 00, 00)
            nr_strefy = 5
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l<self.dms2rad(19, 30, 00):
            l0 = self.dms2rad(18, 00, 00)
            nr_strefy = 6
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        elif l<self.dms2rad(22, 30, 00):
            l0 = self.dms2rad(21, 00, 00)
            nr_strefy = 7
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        else:
            l0 = self.dms2rad(24, 00, 00)
            nr_strefy = 8
            print('l0 =', l0,'nr strefy = ', nr_strefy)
        return l0, nr_strefy
    
    def fl_80_2_gk2000(self, f, l): #f,l w stopniach 
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
        Y_gk_2000 = d_l * N * np.cos(f) * (1 + ((d_l**2) / 6) * ((np.cos(f))**2) * (1 - (t**2) + eta2) + ((d_l**4) / 120) * ((np.cos(f))**4) * (5 - 18 * (t**2) + (t**4) + 14 * eta2 - 58 * eta2 * (t**2)))
        return(X_gk_2000, Y_gk_2000, nr_strefy)   
        
    # z fi lam GRS80 do 1992
        
    def fl_80_2_gk1992(self, f, l): #f,l w stopniach 
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
        return(X_gk_92, Y_gk_92)   
    
    
   # z fi lam WGS84 do 2000
   # wgs
   #a = 6378137 # m	
   # e2 = 0.00335281068118231893543414612613
   # cos?? ≈ 6.356.752,314 245 2 m
    
    def fl_84_2_gk2000(self, f, l): #f,l w stopniach 
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
        return(X84_gk_2000, Y84_gk_2000, nr_strefy)   
    
    # z fi lam wgs84 do 1992
    
    def fl_84_2_gk1992(self, f, l): #f,l w stopniach 
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
        return(X84_gk_92, Y84_gk_92)   
    




    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transformacje geodezyjne')
    subparsers = parser.add_subparsers(title='Operacja', dest='operation', required=True)

    parser_XYZ = subparsers.add_parser('XYZ_to_flh', help='Transformuj XYZ na flh')
    parser_XYZ.add_argument('X', type=float, help='współrzędna X')
    parser_XYZ.add_argument('Y', type=float, help='współrzędna Y')
    parser_XYZ.add_argument('Z', type=float, help='współrzędna Z')

    parser_flh = subparsers.add_parser('flh_to_XYZ', help='Transformuj flh na XYZ')
    parser_flh.add_argument('f', type=float, help='współrzędna fi')
    parser_flh.add_argument('l', type=float, help='współrzędna lambda')
    parser_flh.add_argument('h', type=float, help='współrzędna h')

    parser_fl_GRS80_to_GK2000 = subparsers.add_parser('fl_GRS80_to_GK2000', help='Transformuj fl GRS80 na GK2000')
    parser_fl_GRS80_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    parser_fl_GRS80_to_GK1992 = subparsers.add_parser('fl_GRS80_to_GK1992', help='Transformuj fl GRS80 na GK1992')
    parser_fl_GRS80_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS80_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    parser_fl_GRS84_to_GK2000 = subparsers.add_parser('fl_GRS84_to_GK2000', help='Transformuj fl GRS84 na GK2000')
    parser_fl_GRS84_to_GK2000.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS84_to_GK2000.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    parser_fl_GRS84_to_GK1992 = subparsers.add_parser('fl_GRS84_to_GK1992', help='Transformuj fl GRS84 na GK1992')
    parser_fl_GRS84_to_GK1992.add_argument('f', type=float, help='współrzędna fi w stopniach')
    parser_fl_GRS84_to_GK1992.add_argument('l', type=float, help='współrzędna lambda w stopniach')

    args = parser.parse_args()

    transform = Transformacje()

    if args.operation == 'XYZ_to_flh':
        result = transform.XYZ_to_flh(args.X, args.Y, args.Z)
    elif args.operation == 'flh_to_XYZ':
        result = transform.flh_to_XYZ(args.f, args.l, args.h)
    elif args.operation == 'fl_GRS80_to_GK2000':
        result = transform.fl_80_2_gk2000(args.f, args.l)
    elif args.operation == 'fl_GRS80_to_GK1992':
        result = transform.fl_80_2_gk1992(args.f, args.l) 
    elif args.operation == 'fl_GRS84_to_GK2000':
        result = transform.fl_84_2_gk2000(args.f, args.l)
    elif args.operation == 'fl_GRS84_to_GK1992':
        result = transform.fl_84_2_gk1992(args.f, args.l)
        

    print(result)


    
    
    
    