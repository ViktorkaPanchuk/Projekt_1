# Projekt_1

# Transformacje - dokumentacja
**Moduł Transformacje zawiera metody: XYZ_to_flh, flh_to_XYZ XYZ_to_neu, fl_80_2_gk2000, fl_80_2_gk1992, fl_84_2_gk2000, fl_84_2_gk1992**. 

Funkcje wykorzystują się dla transformacji pojedynczych punktów albo przekształcania danych z pliku wejściowego.
Do obsługi programu najlepiej używać wiersza poleceń (Command Prompt lub Windows POwerShell)

## Spis treści:
- [Do zainstalowania](#do-zainstalowania)
- [rad_to_dms](#rad_to_dms)
- [XYZ_to_flh80](#xyz_to_flh80)
- [XYZ_to_flh84](#xyz_to_flh84)
- [flh_to_XYZ80](#flh_to_xyz80)
- [flh_to_XYZ84](#flh_to_xyz84)
- [XYZ_to_neu80](#xyz_to_neu80)
- [XYZ_to_neu84](#xyz_to_neu84)
- [dms2degrees](#dms2degrees)
- [dms2rad](#dms2rad)
- [lambda0_2000](#lambda0_2000)
- [fl_80_2_gk2000](#fl_80_2_gk2000)
- [fl_80_2_gk1992](#fl_80_2_gk1992)
- [fl_84_2_gk2000](#fl_84_2_gk2000)
- [fl_84_2_gk1992](#fl_84_2_gk1992)
- [Funkcje dla list współrzędnych](#funkcje-dla-list-współrzędnych)
- [XYZ_to_neu_lista80](#xyz_to_neu_lista80)
- [XYZ_to_neu_lista84](#xyz_to_neu_lista84)
- [fl_80_2_gk2000_lista](#fl_80_2_gk2000_lista)
- [fl_80_2_gk1992_lista](#fl_80_2_gk1992_lista)
- [fl_84_2_gk2000_lista](#fl_84_2_gk2000_lista)
- [fl_84_2_gk1992_lista](#fl_84_2_gk1992_lista)
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

## XYZ_to_flh80
Funkcja ta konwertuje współrzędne kartezjańskie X, Y i Z na szerokość geograficzną f, długość geograficzną l oraz wysokość h nad poziomem elipsoidy, dla elipsoidy GRS80.

- Argumenty:

X (typ: float) - wartość współrzędnej X w metrach w układzie kartezjańskim.

Y (typ: float) - wartość współrzędnej Y w metrach w układzie kartezjańskim.

Z (typ: float) - wartość współrzędnej Z w metrach w układzie kartezjańskim.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (f, l, h), gdzie f to szerokość geograficzna w radianach, l to długość geograficzna w radianach, a h to wysokość nad poziomem elipsoidy w metrach.

## XYZ_to_flh84
Funkcja ta konwertuje współrzędne kartezjańskie X, Y i Z na szerokość geograficzną f, długość geograficzną l oraz wysokość h nad poziomem elipsoidy, dla elipsoidy WGS84. 

- Argumenty:

X (typ: float) - wartość współrzędnej X w metrach w układzie kartezjańskim.

Y (typ: float) - wartość współrzędnej Y w metrach w układzie kartezjańskim.

Z (typ: float) - wartość współrzędnej Z w metrach w układzie kartezjańskim.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (f, l, h), gdzie f to szerokość geograficzna w radianach, l to długość geograficzna w radianach, a h to wysokość nad poziomem elipsoidy w metrach.

## flh_to_XYZ80
Funkcja ta konwertuje współrzędne geograficzne f, l i h na współrzędne kartezjańskie X, Y i Z. Argumentami metody są wartości f, l i h, dla elipsoidy GRS80.

- Argumenty:

f (typ: float) - wartość szerokości geograficznej w radianach.

l (typ: float) - wartość długości geograficznej w radianach.

h (typ: float) - wartość wysokości nad poziomem elipsoidy w metrach.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (X, Y, Z), gdzie X, Y, Z to wartości współrzędnych w układzie kartezjańskim.

## flh_to_XYZ84
Funkcja ta konwertuje współrzędne geograficzne f, l i h na współrzędne kartezjańskie X, Y i Z. Argumentami metody są wartości f, l i h, dla elipsoidy WGS84.

- Argumenty:

f (typ: float) - wartość szerokości geograficznej w radianach.

l (typ: float) - wartość długości geograficznej w radianach.

h (typ: float) - wartość wysokości nad poziomem elipsoidy w metrach.

- Zwraca:

Funkcja zwraca trzy wartości typu float w postaci krotki (X, Y, Z), gdzie X, Y, Z to wartości współrzędnych w układzie kartezjańskim.

## XYZ_to_neu80
Funkcja przelicza zmiany we współrzędnych XYZ na zmiany wzdłuż północnego, wschodniego i pionowego kierunku. Wartości X, Y i Z odpowiadają współrzędnym geocentrycznym, a dX to wektor zmian we współrzędnych XYZ. Funkcja liczy dla elipsoidy GRS80.

- Argumenty:

X (typ:float) - wartość współrzędnej X w metrach w układzie kartezjańskim.

Y (typ:float) - wartość współrzędnej Y w metrach w układzie kartezjańskim.

Z (typ:float) - wartość współrzędnej Z w metrach w układzie kartezjańskim.

dx (typ:float) - delta X

dy (typ:float) - delta Y

dz (typ:float) - delta Z

- Zwraca:

Funkcja zwraca wektor 3-elementowy w postaci listy, zawierający zmiany wzdłuż północnego, wschodniego i pionowego kierunku.

## XYZ_to_neu84
Funkcja przelicza zmiany we współrzędnych XYZ na zmiany wzdłuż północnego, wschodniego i pionowego kierunku. Wartości X, Y i Z odpowiadają współrzędnym geocentrycznym, a dX to wektor zmian we współrzędnych XYZ. Funkcja liczy dla elipsoidy WGS84.

- Argumenty:

X (typ:float) - wartość współrzędnej X w metrach w układzie kartezjańskim.

Y (typ:float) - wartość współrzędnej Y w metrach w układzie kartezjańskim.

Z (typ:float) - wartość współrzędnej Z w metrach w układzie kartezjańskim.

dx (typ:float) - delta X w metrach

dy (typ:float) - delta Y w metrach

dz (typ:float) - delta Z w metrach

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
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-2000 dla elipsoidy GRS80.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - płaską współrzędną X w układzie PL-2000 w metrach

Y2000 (typ:float) - płaską współrzędną Y w układzie PL-2000 w metrach

## fl_80_2_gk1992
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-1992 dla elipsoidy GRS80.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - płaską współrzędną X w układzie PL-1992 w metrach

Y1992 (typ:float) - płaską współrzędną Y w układzie PL-1992 w metrach

## fl_84_2_gk2000
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-2000 dla elipsoidy WGS84.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - płaską współrzędną X w układzie PL-2000 w metrach

Y2000 (typ:float) - płaską współrzędną Y w układzie PL-2000 w metrach

## fl_84_2_gk1992
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-1992 dla elipsoidy WGS84.

- Argumenty:

f (typ:float)- szerokość geograficzna w stopniach dziesiętnych

l (typ:float) - długość geograficzna w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - płaską współrzędną X w układzie PL-1992 w metrach

Y1992 (typ:float) - płaską współrzędną Y w układzie PL-1992 w metrach





## Funkcje dla list współrzędnych

## XYZ_to_neu_lista80
Funkcja bierze za argumenty listy wartości, a następnie stosuje funkcję XYZ_to_neu, tak aby można było przeliczyć współrzędne do układu neu dla serii punktów. Funkcja liczy współrzędne dla elipsoidy GRS80.

- Argumenty:
x_kolumna (typ:float) - lista wartości współrzędnych X w metrach w układzie kartezjańskim.

y_kolumna (typ:float) - lista wartość współrzędnych Y w metrach w układzie kartezjańskim.

z_kolumna (typ:float) - lista wartość współrzędnych Z w metrach w układzie kartezjańskim.

dx_kolumna (typ:float) - lista delta X w metrach

dy_kolumna (typ:float) - lista delta Y w metrach

dz_kolumna (typ:float) - lista delta Z w metrach

- Zwraca:

Funkcja zwraca listę wektorów zawierającą zmiany wzdłuż północnego, wschodniego i pionowego kierunku.

## XYZ_to_neu_lista84
Funkcja bierze za argumenty listy wartości, a następnie stosuje funkcję XYZ_to_neu, tak aby można było przeliczyć współrzędne do układu neu dla serii punktów.Funkcja liczy współrzędne dla elipsoidy WGS84.

- Argumenty:
x_kolumna (typ:float) - lista wartości współrzędnych X w metrach w układzie kartezjańskim.

y_kolumna (typ:float) - lista wartość współrzędnych Y w metrach w układzie kartezjańskim.

z_kolumna (typ:float) - lista wartość współrzędnych Z w metrach w układzie kartezjańskim.

dx_kolumna (typ:float) - lista delta X w metrach

dy_kolumna (typ:float) - lista delta Y w metrach

dz_kolumna (typ:float) - lista delta Z w metrach

- Zwraca:

Funkcja zwraca listę wektorów zawierającą zmiany wzdłuż północnego, wschodniego i pionowego kierunku.



## fl_80_2_gk2000_lista
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-2000 dla elipsoidy GRS80. Jednak w odróżnieniu do poprzedniej funkcji, bierze ona za argumenty listy współrzędnych początkowych.

- Argumenty:

f_lista (typ:float) - lista szerokości geograficzne w stopniach dziesiętnych

l_lista (typ:float) - lista długości geograficznych w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - lista współrzędnych X w układzie PL-2000 w metrach

Y2000 (typ:float) - lista współrzędnych Y w układzie PL-2000 w metrach



## fl_80_2_gk1992_lista
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-1992 dla elipsoidy GRS80. Jednak w odróżnieniu do poprzedniej funkcji, bierze ona za argumenty listy współrzędnych 

- Argumenty:

f_lista (typ:float) - lista szerokości geograficzne w stopniach dziesiętnych

l_lista (typ:float) - lista długości geograficznych w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - lista współrzędnych X w układzie PL-1992 w metrach

Y1992 (typ:float) - lista współrzędnych Y w układzie PL-1992 w metrach



## fl_84_2_gk2000_lista
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL2000 dla elipsoidy WGS84. Jednak w odróżnieniu do poprzedniej funkcji, bierze ona za argumenty listy współrzędnych 

- Argumenty:

f_lista (typ:float) - lista szerokości geograficzne w stopniach dziesiętnych

l_lista (typ:float) - lista długości geograficznych w stopniach dziesiętnych

- Zwraca:

X2000 (typ:float) - lista współrzędnych X w układzie PL-2000 w metrach

Y2000 (typ:float) - lista współrzędnych Y w układzie PL-2000 w metrach



## fl_84_2_gk1992_lista
Funkcja przelicza współrzędne geograficzne na płaskie współrzędne PL-1992 dla elipsoidy WGS84.

- Argumenty:

f_lista (typ:float) - lista szerokości geograficzne w stopniach dziesiętnych

l_lista (typ:float) - lista długości geograficznych w stopniach dziesiętnych

- Zwraca:

X1992 (typ:float) - lista współrzędnych X w układzie PL-1992 w metrach

Y1992 (typ:float) - lista współrzędnych Y w układzie PL-1992 w metrach



### Funkcje pobierające i zapisujące dane

## Funkcja pobieranie_wsp
Funkcja pobiera dane z zewnętrznego pliku tekstowego i zależnie od podanej komendy stosuje wybraną funkcję (z funkcji powyższych). 

- Argumenty:

file_patch - skopiowana ścieżka do folderu z odpowiednio sformatowanymi danymi początowymi

rodziaj_tranfsormacji - wybrany z podanych: XYZ_to_flh, flh_to_XYZ, XYZ_to_neu, fl_GRS80_to_2000, fl_GRS80_to_1992, fl_WGS84_to_2000, fl_WGS84_to_1992

- Zwraca:
  wynik - jest to np.array złożony z tylu kolumn ile wartości zwraca wybrana transformacja, który funkcja zapisz zapisuje w zewnętrznym pliku.

## Funkcja zapisz
Funkcja ta jest zaimplementowana wewnątrz funkcji pobieranie_wsp. Jej argumenty są z góry podane dla każdej z możliwych transformacji. Funkcja ta zapisuje wyniki danej transformacji w pliku tekstowym, w folderze w którym znajduje się program.

- Argumenty:

wynik - jest to wynik transformacji do której stosujemy metodę zapisz

filename - jest to nazwa pod jaką plik zostanie zapisany, jest ona podana dla każdej z możliwych transformacji

header - krótki opis wyniku, który jest zapisywany w pierwszej linijce pliku txt























## Instrukcja używania funkcji
Aby zainstalować skrypt Pythona zawierający klasy i definicje z transformacjami geodezyjnymi, należy wykonać następujące kroki:

1. Pobierz kod źródłowy skryptu z repozytorium Github. Program znajduje się na gałęzi master.

2. Zainstaluj Pythona na swoim komputerze, jeśli jeszcze go nie masz (werscja Pythona 3.9).

3. Otwórz wiersz poleceń (cmd) i przejdź do katalogu, w którym znajduje się skrypt.

4. Użyj polecenia "pip install nazwa_biblioteki" (gdzie "nazwa_biblioteki" to nazwa biblioteki, którą chcesz zainstalowa), aby zainstalować wszystkie wymagane biblioteki.

  Przykład:
  
    pip install numpy

Po wykonaniu tych kroków, skrypt będzie gotowy do użycia.

Aby użyć skryptu, można wprowadzać pojedyncze dane przez wiersz poleceń lub użyć pliku z danymi. W przypadku pojedynczych danych, należy uruchomić skrypt i wprowadzić dane ręcznie w konsoli. W przypadku użycia pliku z danymi, należy umieścić dane w pliku tekstowym, oddzielając je przecinkami bez spacji w kolejności **f,l,h (X,Y,Z)**, a następnie wpisać nazwę pliku z rozszerzeniem (jeśli plik z danymi znajduje się jednym folderze ze skryptem) albo podać ścieżkę do pliku, po czym wpisać nazwę metody transformacji.



    
    
    
Przykład użycia skryptu z pojedynczymi danymi:

- **W programie Spyder (Python 3.9.13):**
        
        from skrypt.py import fl_80_2_gk2000

        f = 53.1 # szerokość geograficzna
        l = 18.6 # długość geograficzna

        X, Y = fl_80_2_gk2000(f, l)

        print("X: ", X)
        print("Y: ", Y)

- **Przez wiersz poleceń:**

- Przykłady użycia programu:

![Example screenshot](/screens/flh_2_XYZ.png)

- [ ] **Gdzie:**

  - "C:\Users\vikto\OneDrive\Dokumenty\Geodezja\Informatyka_II\Projekty\Projekt_1" - ścieżka do skryptu
   
  - "python" - program, przy pomocy którego uruchamiamy skrypt
   
  - "skrypt.py" - nazwa skryptu, który będzie uruchomiony _albo_ ścieżka do skryptu
   
  - "flh_to_XYZ" - nazwa transformacji, którą chcemy wykonać
   
  - "51 21 100" - dane (w tym przypadku flh), które będą transformowane

Przykład użycia skryptu z danymi z pliku:

Zamiast pojedynczych danych trzeba podać plik z danymi.
  
![Example screenshot](/screens/XYZ_to_neu.png)

- [ ] **Gdzie:**

  - "C:\Users\vikto\OneDrive\Dokumenty\Geodezja\Informatyka_II\Projekty\Projekt_1" - ścieżka do skryptu
   
  - "python" - program, przy pomocy którego uruchamiamy skrypt
   
  - "skrypt.py" - nazwa skryptu, który będzie uruchomiony **albo** ścieżka do skryptu
   
  - "pobierz_dane" - polecenie, którego używamy do pobierania danych z pliku .txt
   
  - "neu.txt" - nazwa pliku, z którego pobieramy dane _albo_ ścieżka do pliku
  
  - "XYZ_to_neu" - nazwa transformacji, którą chcemy wykonać
  
![Example screenshot](/screens/in.png)

&uarr; Plik wejściowy:


&darr; Plik wyjściowy:

![Example screenshot](/screens/out.png)



## Użycie funkcji flh_to_XYZ

    \ścieżka do pliku w którym znajduje się program>python skrypt.py flh_to_XYZ 52 21 100
    
Wynik:

           Współrzędna X:  570754.7914051721
           Współrzędna Y:  -3454934.216159615
           Współrzędna Z:  5313127.8261839645

## Użycie funkcji XYZ_to_flh

    \ścieżka do pliku w którym znajduje się program>python skrypt.py XYZ_to_flh 52 21 100
     
Wynik:

    flh w radianach: -0.0023451302834425155 1.1869787035063277 -6378081.0369568365
    Szerokość geodezyjna:  -0.13436606764957462 °
    Długość geodezyjna:  68.00887008282287 °
    Wysokość geodezyjna:  -6378081.0369568365
    
    
# Użycie funkcji XYZ_to_neu

    \ścieżka do pliku w którym znajduje się program>python skrypt.py XYZ_to_neu 10 20 30 40 50 60
    
Wynik:

    Współrzędne neu (70.04399884419017, 6.583592135001265, 92.56770894637975)
    
# Użycie funkcji fl_GRS80_to_2000 

    \ścieżka do pliku w którym znajduje się program>python skrypt.py fl_GRS80_to_2000 21 52

Wynik:

    Współrzędna X2000:  2601137.0663114763
    Współrzędna Y2000:  11500168.930870896

# Użycie funkcji fl_GRS80_to_2000 

    \ścieżka do pliku w którym znajduje się program>python skrypt.py fl_GRS80_to_1992 21 52
    
Wynik:

    Współrzędna X1992:  -2578465.7034921288
    Współrzędna Y1992:  4076199.4923393293

# Użycie funkcji fl_WGS80_to_2000 

    \ścieżka do pliku w którym znajduje się program>python skrypt.py fl_WGS84_to_2000 21 52

Wynik:    
   
    Współrzędna X2000:  2608244.775180605
    Współrzędna Y2000:  11499210.939543033
    
# Użycie funkcji fl_WGS84_to_1992 

    \ścieżka do pliku w którym znajduje się program>python skrypt.py fl_WGS84_to_1992 21 52
    
Wynik:

    Współrzędna X1992:  -2571531.2926037298
    Współrzędna Y1992:  4074907.456206129
    
    
    
## Użycie funkcji pobieranie_danych do obliczenia transformacji dla serii punktów

    \ścieżka do pliku w którym znajduje się program>python skrypt.py pobierz_dane "ścieżka do pliku z danymi" "nazwa transformacji"
    
pod nazwą transformacji należy wkleić nazwę z niżej wymienionych:


XYZ_to_flh80

XYZ_to_flh84

flh_to_XYZ80

flh_to_XYZ84

XYZ_to_neu80

XYZ_to_neu84
 
fl_GRS80_to_2000

fl_GRS80_to_1992

fl_WGS84_to_2000

fl_WGS84_to_1992




## Przygotowanie pliku z danymi

Dane w pliku dla transformacji XYZ_to_flh oraz flh_to_XYZ muszą być w formacie:

    współrzędna1,współrzędna2,współrzędna3,
    współrzędna4,współrzędna5,współrzędna6,
    itd

to jest: współrzędne muszą być ustawione w kolumnach, przedzielone przecinkami oraz bez spacji pomiędzy nimi.

Dane w pliku dla transformacji XYZ_to_neu muszą być w formacie:

    współrzędnaX,współrzędnaY,współrzędnaZ,dX,dY,dZ,
    współrzędnaX,współrzędnaY,współrzędnaZ,dX,dY,dZ,
    itd
    
    
Dane w pliku dla transformacji do i z układów PL-2000 i PL-1992 muszą być w formacie:

    współrzędnaF,współrzędnaL,
    współrzędnaF,współrzędnaL,
    itd  




## Przykłady wyników dla funkcji pobierz_dane
Gdy obliczamy transformacje dla pliku txt, program nie wyświetla wyników w wierszu poleceń, lecz zapisuje je do pliku txt.
Używając funkcji pobierz_dane otrzymamy zatem odpowiedzi jak na przykładach:




![Example screenshot](/screens/80_to_1992.png)


![Example screenshot](/screens/80_to_2000.png)


![Example screenshot](/screens/84_to_1992.png)


![Example screenshot](/screens/84_to_2000.png)


![Example screenshot](/screens/flh_xyz.png)


![Example screenshot](/screens/xyz_neu.png)


![Example screenshot](/screens/xyz_to_flh.png)










