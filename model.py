# Dane użytkowników systemu

uzytkownicy_systemu = [
    {
        "login": "admin",
        "haslo": "admin"
    }
]


# Dane centrów konferencyjnych

centra = [
    {
        "id": 1,
        "nazwa": "Szawa Conference - Centrum Konferencyjne",
        "miasto": "Warszawa",
        "adres": "ul. Jutrzenki 137",
        "latitude": 52.1985742,
        "longitude": 20.9332268
    },
    {
        "id": 2,
        "nazwa": "CKF13 Centrum Konferencyjne",
        "miasto": "Krakow",
        "adres": "ul. Fabryczna 13",
        "latitude": 50.0622463,
        "longitude": 19.9740164
    },
    {
        "id": 3,
        "nazwa": "Qubus Centrum Konferencyjne Gdansk",
        "miasto": "Gdansk",
        "adres": "ul. Chmielna 47/52",
        "latitude": 54.3451566,
        "longitude": 18.6554487
    },
    {
        "id": 4,
        "nazwa": "Lubelskie Centrum Konferencyjne",
        "miasto": "Lublin",
        "adres": "ul. Artura Grottgera 2",
        "latitude": 51.2474448,
        "longitude": 22.5495652
    },
    {
        "id": 5,
        "nazwa": "Wroclaw Congress Center",
        "miasto": "Wroclaw",
        "adres": "Plac Konstytucji 3 Maja 3",
        "latitude": 51.0992749,
        "longitude": 17.0401391
    }
]


# Dane klientów

klienci = [
    {
        "id": 1,
        "imie": "Anna",
        "nazwisko": "Kos",
        "firma": "GeoProjekt",
        "miasto": "Warszawa",
        "latitude": 52.2297,
        "longitude": 21.0122
    },
    {
        "id": 2,
        "imie": "Jan",
        "nazwisko": "Zugaj",
        "firma": "BudPlan",
        "miasto": "Krakow",
        "latitude": 50.0647,
        "longitude": 19.9450
    },
    {
        "id": 3,
        "imie": "Katarzyna",
        "nazwisko": "Mocarska",
        "firma": "MapGeo",
        "miasto": "Gdansk",
        "latitude": 54.3520,
        "longitude": 18.6466
    },
    {
        "id": 4,
        "imie": "Marta",
        "nazwisko": "Wojciechowska",
        "firma": "GeoSystem",
        "miasto": "Lublin",
        "latitude": 51.2465,
        "longitude": 22.5684
    },
    {
        "id": 5,
        "imie": "Tomasz",
        "nazwisko": "Szymanowski",
        "firma": "Inzynieria24",
        "miasto": "Wroclaw",
        "latitude": 51.1079,
        "longitude": 17.0385
    }
]


# Dane pracowników

pracownicy = [
    {
        "id": 1,
        "imie": "Eryk",
        "nazwisko": "Zielinski",
        "stanowisko": "Manager",
        "id_centrum": 1,
        "miasto": "Warszawa",
        "latitude": 52.1985742,
        "longitude": 20.9332268
    },
    {
        "id": 2,
        "imie": "Eliza",
        "nazwisko": "Lewandowska",
        "stanowisko": "Recepcjonistka",
        "id_centrum": 2,
        "miasto": "Krakow",
        "latitude": 50.0622463,
        "longitude": 19.9740164
    },
    {
        "id": 3,
        "imie": "Piotr",
        "nazwisko": "Kaminski",
        "stanowisko": "Koordynator",
        "id_centrum": 3,
        "miasto": "Gdansk",
        "latitude": 54.3451566,
        "longitude": 18.6554487
    },
    {
        "id": 4,
        "imie": "Agnieszka",
        "nazwisko": "Mazur",
        "stanowisko": "Specjalista ds. rezerwacji",
        "id_centrum": 4,
        "miasto": "Lublin",
        "latitude": 51.2474448,
        "longitude": 22.5495652
    },
    {
        "id": 5,
        "imie": "Pawel",
        "nazwisko": "Grabowski",
        "stanowisko": "Technik",
        "id_centrum": 5,
        "miasto": "Wroclaw",
        "latitude": 51.0992749,
        "longitude": 17.0401391
    }
]


# Dane rezerwacji

rezerwacje = [
    {
        "id": 1,
        "id_klienta": 1,
        "id_centrum": 1,
        "data": "2026-06-15",
        "sala": "Sala A",
        "liczba_osob": 80
    },
    {
        "id": 2,
        "id_klienta": 2,
        "id_centrum": 2,
        "data": "2026-06-18",
        "sala": "Sala B",
        "liczba_osob": 60
    },
    {
        "id": 3,
        "id_klienta": 3,
        "id_centrum": 3,
        "data": "2026-06-20",
        "sala": "Sala C",
        "liczba_osob": 100
    },
    {
        "id": 4,
        "id_klienta": 4,
        "id_centrum": 4,
        "data": "2026-06-22",
        "sala": "Sala D",
        "liczba_osob": 50
    },
    {
        "id": 5,
        "id_klienta": 5,
        "id_centrum": 5,
        "data": "2026-06-25",
        "sala": "Sala E",
        "liczba_osob": 120
    }
]


# Baza adresów dla centrów konferencyjnych
# Program pobiera z niej współrzędne na podstawie miasta i adresu.

wspolrzedne_adresow = {
    ("warszawa", "ul. jutrzenki 137"): (52.1985742, 20.9332268),
    ("krakow", "ul. fabryczna 13"): (50.0622463, 19.9740164),
    ("gdansk", "ul. chmielna 47/52"): (54.3451566, 18.6554487),
    ("lublin", "ul. artura grottgera 2"): (51.2474448, 22.5495652),
    ("wroclaw", "plac konstytucji 3 maja 3"): (51.0992749, 17.0401391),
    ("poznan", "stary rynek 2"): (52.4082663, 16.9344477),
    ("lodz", "ul. piotrkowska 104"): (51.7687323, 19.4569911),
    ("katowice", "al. wojciecha korfantego 35"): (50.2648919, 19.0237815),
    ("torun", "rynek staromiejski 1"): (53.0102721, 18.6048094),
    ("bialystok", "ul. lipowa 1"): (53.1324886, 23.1599117)
}


# Baza miast dla klientów
# Program pobiera z niej współrzędne klienta na podstawie miasta.

wspolrzedne_miast = {
    "warszawa": (52.2297, 21.0122),
    "krakow": (50.0647, 19.9450),
    "gdansk": (54.3520, 18.6466),
    "lublin": (51.2465, 22.5684),
    "wroclaw": (51.1079, 17.0385),
    "poznan": (52.4064, 16.9252),
    "lodz": (51.7592, 19.4560),
    "katowice": (50.2649, 19.0238),
    "torun": (53.0138, 18.5984),
    "bialystok": (53.1325, 23.1688)
}