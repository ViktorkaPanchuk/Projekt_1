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

def XYZ_to_flh(X,Y,Z):
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
    return(f,l,h)