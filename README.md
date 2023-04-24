# Projekt_1

# Transformacje - dokumentacja
Moduł Transformacje zawiera metody: XYZ_to_flh, flh_to_XYZ XYZ_to_neu, fl_80_2_gk2000, fl_80_2_gk1992, fl_84_2_gk2000, fl_84_2_gk1992

## Spis treści:
- [Do zainstalowania](#do-zainstalowania)
- [rad_to_dms](#rad_to_dms)
- [XYZ_to_flh](#xyz_to_flh)
- [flh_to_XYZ](#flh_to_xyz)
- [XYZ_to_neu](#xyz_to_neu)
- [dms2degrees](#dms2degrees)
- [dms2rad](#dms2rad)
- [lambda0_2000](#lambda0_2000)
- [fl_80_2_gk2000](#fl_80_2_gk2000)
- [fl_80_2_gk1992](#fl_80_2_gk1992)
- [fl_84_2_gk2000](#fl_84_2_gk2000)
- [fl_84_2_gk1992](#fl_84_2_gk1992)
- [Instrukcja używania funkcji](#instrukcja-używania-funkcji)


## Do zainstalowania
- Programy:

  - Python 3.9.13
  
  lub
  - Python 3.10.11
  
- Biblioteki:

  - NumPy
  - Argparse
  - Math

## rad_to_dms
Funkcja ta konwertuje wartość kątową w radianach na stopnie, minuty i sekundy. Argumentem metody jest liczba typu float oznaczająca wartość kąta w radianach.

- Argumenty:
 
x (typ: float) - wartość kąta w radianach.

- Zwraca:

Funkcja nie zwraca wartości, ponieważ jest pomocniczą do wykonania Transformacji.

## XYZ_to_flh
Funkcja ta konwertuje współrzędne kartezjańskie X, Y i Z na szerokość geograficzną f, długość geograficzną l oraz wysokość h nad poziomem elipsoidy. 

- Argumenty:

X (typ: float) - wartość współrzędnej X w układzie kartezjańskim.

Y (typ: float) - wartość współrzędnej Y w układzie kartezjańskim.

Z (typ: float) - wartość współrzędnej Z w układzie kartezjańskim.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (f, l, h), gdzie f to szerokość geograficzna w radianach, l to długość geograficzna w radianach, a h to wysokość nad poziomem elipsoidy w metrach.

## flh_to_XYZ
Funkcja ta konwertuje współrzędne geograficzne f, l i h na współrzędne kartezjańskie X, Y i Z. Argumentami metody są wartości f, l i h.

- Argumenty:

f (typ: float) - wartość szerokości geograficznej w radianach.

l (typ: float) - wartość długości geograficznej w radianach.

h (typ: float) - wartość wysokości nad poziomem elipsoidy w metrach.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (X, Y, Z), gdzie X, Y, Z to wartości współrzędnych w układzie kartezjańskim.

## XYZ_to_neu
Funkcja przelicza zmiany we współrzędnych XYZ na zmiany wzdłuż północnego, wschodniego i pionowego kierunku. Wartości X, Y i Z odpowiadają współrzędnym geocentrycznym, a dX to wektor zmian we współrzędnych XYZ.

- Argumenty:

dX (typ:list) - wektor zmian we współrzędnych X, Y i Z

X (typ:float) - wartość współrzędnej X w układzie kartezjańskim.

Y (typ:float) - wartość współrzędnej X w układzie kartezjańskim.

Z (typ:float) - wartość współrzędnej X w układzie kartezjańskim.

- Zwraca:

Funkcja zwraca wektor 3-elementowy w postaci listy, zawierający zmiany wzdłuż północnego, wschodniego i pionowego kierunku.

## dms2degrees
Funkcja przelicza stopnie, minuty, sekundy na stopnie w postaci dziesiętnej.

- Argumenty:

d (typ:int) - stopnie

m (typ:int) - minuty

s (typ:float) - sekundy

- Zwraca:

Funkcja zwraca jedną wartość typu float kąta w stopniach dziesiętnych.

## dms2rad
Funkcja przelicza stopnie, sekundy, minuty w radiany.

- Argumenty:

d (typ:int) - stopnie

m (typ:int) - minuty

s (typ:float) - sekundy

- Zwraca:

Funkcja zwraca jedną wartość typu float kąta w radianach.


## lambda0_2000
Funkcja lambda0_2000 służy do wyznaczenia długości geograficznej punktu centralnego strefy UTM dla danego punktu o zadanej długości geograficznej. Funkcja ta przyjmuje jeden argument l_deg, który jest długością geograficzną punktu, podaną w stopniach.

- Argumenty:

l_deg (typ:float) - wartość długości geograficznej punktu, podana w stopniach dziesiętnych.


- Zwraca: 

Funkcja zwraca dwie wartości:

l0: długość geograficzna punktu centralnego strefy UTM, wyznaczona w radianach.

nr_strefy: numer strefy UTM, do której należy punkt o zadanej długości geograficznej.

## fl_80_2_gk2000
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne Gaussa-Krüger w układzie 2000 dla elipsoidy GRS80.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - płaską współrzędną X w układzie Gaussa-Krüger 2000

Y2000 (typ:float) - płaską współrzędną Y w układzie Gaussa-Krüger 2000

## fl_80_2_gk1992
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne Gaussa-Krüger w układzie 1992 dla elipsoidy GRS80.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - płaską współrzędną X w układzie Gaussa-Krüger 2000

Y1992 (typ:float) - płaską współrzędną Y w układzie Gaussa-Krüger 2000

## fl_84_2_gk2000
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne Gaussa-Krüger w układzie 2000 dla elipsoidy WGS84.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - płaską współrzędną X w układzie Gaussa-Krüger 2000

Y2000 (typ:float) - płaską współrzędną Y w układzie Gaussa-Krüger 2000

## fl_84_2_gk1992
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne Gaussa-Krüger w układzie 1992 dla elipsoidy WGS84.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - płaską współrzędną X w układzie Gaussa-Krüger 1992

Y1992 (typ:float) - płaską współrzędną Y w układzie Gaussa-Krüger 1992

## Instrukcja używania funkcji
Aby zainstalować skrypt Pythona zawierający klasy i definicje z transformacjami geodezyjnymi, należy wykonać następujące kroki:

1. Pobierz kod źródłowy skryptu z repozytorium Github.

2. Zainstaluj Pythona na swoim komputerze, jeśli jeszcze go nie masz (werscja Pythona 3.9).

3. Otwórz wiersz poleceń (cmd) i przejdź do katalogu, w którym znajduje się skrypt.

4. Użyj polecenia "pip install nazwa_biblioteki" (gdzie "nazwa_biblioteki" to nazwa biblioteki, którą chcesz zainstalowa), aby zainstalować wszystkie wymagane biblioteki.

  Przykład:
  
    pip install numpy

Po wykonaniu tych kroków, skrypt będzie gotowy do użycia.

Aby użyć skryptu, można wprowadzać pojedyncze dane przez wiersz poleceń lub użyć pliku z danymi. W przypadku pojedynczych danych, należy uruchomić skrypt i wprowadzić dane ręcznie w konsoli. W przypadku użycia pliku z danymi, należy umieścić dane w pliku tekstowym, oddzielając je spacjami, a następnie przekazać nazwę pliku jako argument do skryptu.

Przykład użycia skryptu z pojedynczymi danymi:

- W programie Spyder (Python 3.9.13):
        
        from skrypt.py import fl_80_2_gk2000

        f = 53.1 # szerokość geograficzna
        l = 18.6 # długość geograficzna

        X, Y = fl_80_2_gk2000(f, l)

        print("X: ", X)
        print("Y: ", Y)

- Przez wiersz poleceń:

![Example screenshot](/Użycie_def.png)

Przykład użycia skryptu z danymi z pliku:

Zamiast pojedynczych danych trzeba podać plik z danymi.
  
    python skrypt.py dane.txt












