from tkinter import *
from tkinter import ttk, messagebox
import tkintermapview

from model import (
    uzytkownicy_systemu,
    centra,
    klienci,
    pracownicy,
    rezerwacje,
    wspolrzedne_adresow,
    wspolrzedne_miast
)


JASNY_NIEBIESKI = "#dff3ff"
JASNY_NIEBIESKI_2 = "#eef9ff"
NIEBIESKI_PRZYCISK = "#b8e0ff"
NIEBIESKI_AKTYWNY = "#9ed3ff"
NIEBIESKI_ZAKLADKA = "#cfeeff"


def ustaw_styl_ttk() -> None:
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "TNotebook",
        background=JASNY_NIEBIESKI,
        borderwidth=0
    )

    style.configure(
        "TNotebook.Tab",
        background=NIEBIESKI_ZAKLADKA,
        padding=[12, 6]
    )

    style.map(
        "TNotebook.Tab",
        background=[("selected", NIEBIESKI_AKTYWNY)]
    )


def ustaw_kolory(widget) -> None:
    try:
        if isinstance(widget, (Frame, LabelFrame, Label)):
            widget.configure(bg=JASNY_NIEBIESKI)

        elif isinstance(widget, Button):
            widget.configure(
                bg=NIEBIESKI_PRZYCISK,
                activebackground=NIEBIESKI_AKTYWNY,
                relief=RAISED,
                bd=1
            )

        elif isinstance(widget, (Entry, Listbox, Text)):
            widget.configure(bg=JASNY_NIEBIESKI_2)

    except TclError:
        pass

    for dziecko in widget.winfo_children():
        ustaw_kolory(dziecko)


def normalizuj_tekst(tekst: str) -> str:
    return tekst.strip().lower()


def nastepne_id(lista_data: list) -> int:
    if len(lista_data) == 0:
        return 1
    return max(element["id"] for element in lista_data) + 1


def znajdz_po_id(lista_data: list, id_obiektu: int):
    for element in lista_data:
        if element["id"] == id_obiektu:
            return element
    return None


def wyczysc_pola(pola: list) -> None:
    for pole in pola:
        pole.delete(0, END)


def wpisz_do_pola(pole: Entry, wartosc) -> None:
    pole.delete(0, END)
    pole.insert(0, str(wartosc))


def pobierz_wspolrzedne_centrum_z_adresu(entry_miasto: Entry, entry_adres: Entry):
    miasto = normalizuj_tekst(entry_miasto.get())
    adres = normalizuj_tekst(entry_adres.get())

    klucz = (miasto, adres)

    if klucz in wspolrzedne_adresow:
        return wspolrzedne_adresow[klucz]

    messagebox.showerror(
        "Błąd",
        "Nie ma takiego adresu w bazie adresów.\n\n"
        "Sprawdź, czy miasto i adres są wpisane poprawnie."
    )
    return None


def pobierz_wspolrzedne_klienta_z_miasta(entry_miasto: Entry):
    miasto = normalizuj_tekst(entry_miasto.get())

    if miasto in wspolrzedne_miast:
        return wspolrzedne_miast[miasto]

    messagebox.showerror(
        "Błąd",
        "Nie ma takiego miasta w bazie miast.\n\n"
        "Dostępne miasta to: Warszawa, Krakow, Gdansk, Lublin, Wroclaw, Poznan, Lodz, Katowice, Torun, Bialystok."
    )
    return None


def pasuje_do_filtra(element: dict, fraza: str, pole: str, pola_do_filtrowania: dict) -> bool:
    fraza = fraza.lower().strip()

    if fraza == "":
        return True

    if pole == "Wszystko":
        tekst = " ".join(str(wartosc).lower() for wartosc in element.values())
        return fraza in tekst

    nazwa_pola = pola_do_filtrowania[pole]
    tekst = str(element[nazwa_pola]).lower()

    return fraza in tekst


def sprawdz_logowanie() -> None:
    login = entry_login.get()
    haslo = entry_haslo.get()

    for uzytkownik in uzytkownicy_systemu:
        if uzytkownik["login"] == login and uzytkownik["haslo"] == haslo:
            otworz_aplikacje()
            return

    messagebox.showerror("Błąd logowania", "Błędny login lub hasło.")


def otworz_aplikacje() -> None:
    for widget in root.winfo_children():
        widget.destroy()

    root.title("System zarządzania centrami konferencyjnymi")
    root.geometry("1250x760")
    root.configure(bg=JASNY_NIEBIESKI)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=BOTH, expand=True)

    zakladka_centra = Frame(notebook)
    zakladka_klienci = Frame(notebook)
    zakladka_pracownicy = Frame(notebook)
    zakladka_rezerwacje = Frame(notebook)

    notebook.add(zakladka_centra, text="Centra konferencyjne")
    notebook.add(zakladka_klienci, text="Klienci")
    notebook.add(zakladka_pracownicy, text="Pracownicy")
    notebook.add(zakladka_rezerwacje, text="Rezerwacje i raporty")

    utworz_zakladke_centra(zakladka_centra)
    utworz_zakladke_klienci(zakladka_klienci)
    utworz_zakladke_pracownicy(zakladka_pracownicy)
    utworz_zakladke_rezerwacje(zakladka_rezerwacje)

    ustaw_kolory(root)


# CENTRA KONFERENCYJNE

def odswiez_liste_centrow(dane=None) -> None:
    global wyswietlane_centra

    if dane is None:
        dane = centra

    wyswietlane_centra = dane
    listbox_centra.delete(0, END)

    for centrum in wyswietlane_centra:
        listbox_centra.insert(
            END,
            f"{centrum['id']} - {centrum['nazwa']} ({centrum['miasto']})"
        )


def filtruj_centra(event=None) -> None:
    fraza = entry_filtr_centra.get()
    wybrane_pole = combo_filtr_centra.get()

    pola_centra = {
        "Miasto": "miasto",
        "Nazwa centrum": "nazwa",
        "Adres": "adres"
    }

    wyniki = []

    for centrum in centra:
        if pasuje_do_filtra(centrum, fraza, wybrane_pole, pola_centra):
            wyniki.append(centrum)

    odswiez_liste_centrow(wyniki)
    odswiez_mape_centrow(wyniki)


def pokaz_centrum(event=None) -> None:
    wybor = listbox_centra.curselection()

    if len(wybor) == 0:
        return

    i = wybor[0]
    centrum = wyswietlane_centra[i]

    wpisz_do_pola(entry_centrum_nazwa, centrum["nazwa"])
    wpisz_do_pola(entry_centrum_miasto, centrum["miasto"])
    wpisz_do_pola(entry_centrum_adres, centrum["adres"])
    wpisz_do_pola(entry_centrum_latitude, centrum["latitude"])
    wpisz_do_pola(entry_centrum_longitude, centrum["longitude"])

    mapa_centra.set_position(centrum["latitude"], centrum["longitude"])
    mapa_centra.set_zoom(12)


def dodaj_centrum() -> None:
    wspolrzedne = pobierz_wspolrzedne_centrum_z_adresu(
        entry_centrum_miasto,
        entry_centrum_adres
    )

    if wspolrzedne is None:
        return

    latitude, longitude = wspolrzedne

    nowe_centrum = {
        "id": nastepne_id(centra),
        "nazwa": entry_centrum_nazwa.get(),
        "miasto": entry_centrum_miasto.get(),
        "adres": entry_centrum_adres.get(),
        "latitude": latitude,
        "longitude": longitude
    }

    centra.append(nowe_centrum)
    filtruj_centra()
    wyczysc_pola(pola_centrum)

    messagebox.showinfo("Sukces", "Dodano nowe centrum konferencyjne.")


def aktualizuj_centrum() -> None:
    wybor = listbox_centra.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz centrum z listy.")
        return

    wspolrzedne = pobierz_wspolrzedne_centrum_z_adresu(
        entry_centrum_miasto,
        entry_centrum_adres
    )

    if wspolrzedne is None:
        return

    latitude, longitude = wspolrzedne

    i = wybor[0]
    centrum = wyswietlane_centra[i]

    centrum["nazwa"] = entry_centrum_nazwa.get()
    centrum["miasto"] = entry_centrum_miasto.get()
    centrum["adres"] = entry_centrum_adres.get()
    centrum["latitude"] = latitude
    centrum["longitude"] = longitude

    wpisz_do_pola(entry_centrum_latitude, latitude)
    wpisz_do_pola(entry_centrum_longitude, longitude)

    filtruj_centra()
    messagebox.showinfo("Sukces", "Zaktualizowano centrum konferencyjne.")


def usun_centrum() -> None:
    wybor = listbox_centra.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz centrum z listy.")
        return

    i = wybor[0]
    centrum = wyswietlane_centra[i]

    centra.remove(centrum)

    filtruj_centra()
    wyczysc_pola(pola_centrum)
    messagebox.showinfo("Sukces", "Usunięto centrum konferencyjne.")


def odswiez_mape_centrow(dane=None) -> None:
    if dane is None:
        dane = centra

    for marker in markery_centra:
        marker.delete()

    markery_centra.clear()

    for centrum in dane:
        marker = mapa_centra.set_marker(
            centrum["latitude"],
            centrum["longitude"],
            text=centrum["nazwa"]
        )
        markery_centra.append(marker)


def utworz_zakladke_centra(zakladka: Frame) -> None:
    global listbox_centra
    global entry_filtr_centra, combo_filtr_centra
    global entry_centrum_nazwa, entry_centrum_miasto, entry_centrum_adres
    global entry_centrum_latitude, entry_centrum_longitude
    global pola_centrum
    global mapa_centra, markery_centra, wyswietlane_centra

    markery_centra = []
    wyswietlane_centra = centra.copy()

    ramka_lista = Frame(zakladka)
    ramka_formularz = LabelFrame(zakladka, text="Dane centrum")
    ramka_mapa = LabelFrame(zakladka, text="Mapa centrów konferencyjnych")

    ramka_lista.grid(row=0, column=0, padx=10, pady=10, sticky=N)
    ramka_formularz.grid(row=0, column=1, padx=10, pady=10, sticky=N)
    ramka_mapa.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    Label(ramka_lista, text="Lista centrów:").grid(row=0, column=0, columnspan=3)

    Label(ramka_lista, text="Filtruj po:").grid(row=1, column=0, sticky=W)
    combo_filtr_centra = ttk.Combobox(
        ramka_lista,
        values=["Wszystko", "Miasto", "Nazwa centrum", "Adres"],
        state="readonly",
        width=18
    )
    combo_filtr_centra.set("Wszystko")
    combo_filtr_centra.grid(row=1, column=1, pady=5)
    combo_filtr_centra.bind("<<ComboboxSelected>>", filtruj_centra)

    Label(ramka_lista, text="Szukaj:").grid(row=2, column=0, sticky=W)
    entry_filtr_centra = Entry(ramka_lista, width=30)
    entry_filtr_centra.grid(row=2, column=1, columnspan=2, pady=5)
    entry_filtr_centra.bind("<KeyRelease>", filtruj_centra)

    listbox_centra = Listbox(ramka_lista, width=45, height=14)
    listbox_centra.grid(row=3, column=0, columnspan=3)
    listbox_centra.bind("<<ListboxSelect>>", pokaz_centrum)

    Button(ramka_lista, text="Usuń", command=usun_centrum).grid(row=4, column=0, pady=5)
    Button(ramka_lista, text="Odśwież mapę", command=filtruj_centra).grid(row=4, column=1, pady=5)

    Label(ramka_formularz, text="Nazwa:").grid(row=0, column=0, sticky=W)
    Label(ramka_formularz, text="Miasto:").grid(row=1, column=0, sticky=W)
    Label(ramka_formularz, text="Adres:").grid(row=2, column=0, sticky=W)
    Label(ramka_formularz, text="Szerokość:").grid(row=3, column=0, sticky=W)
    Label(ramka_formularz, text="Długość:").grid(row=4, column=0, sticky=W)

    entry_centrum_nazwa = Entry(ramka_formularz, width=35)
    entry_centrum_miasto = Entry(ramka_formularz, width=35)
    entry_centrum_adres = Entry(ramka_formularz, width=35)
    entry_centrum_latitude = Entry(ramka_formularz, width=35)
    entry_centrum_longitude = Entry(ramka_formularz, width=35)

    entry_centrum_nazwa.grid(row=0, column=1)
    entry_centrum_miasto.grid(row=1, column=1)
    entry_centrum_adres.grid(row=2, column=1)
    entry_centrum_latitude.grid(row=3, column=1)
    entry_centrum_longitude.grid(row=4, column=1)

    pola_centrum = [
        entry_centrum_nazwa,
        entry_centrum_miasto,
        entry_centrum_adres,
        entry_centrum_latitude,
        entry_centrum_longitude
    ]

    Button(ramka_formularz, text="Dodaj", command=dodaj_centrum).grid(row=5, column=0, pady=10)
    Button(ramka_formularz, text="Zapisz zmiany", command=aktualizuj_centrum).grid(row=5, column=1, pady=10)
    Button(ramka_formularz, text="Wyczyść", command=lambda: wyczysc_pola(pola_centrum)).grid(row=6, column=0, columnspan=2)

    mapa_centra = tkintermapview.TkinterMapView(ramka_mapa, width=1150, height=400, corner_radius=4)
    mapa_centra.set_position(52.0, 19.0)
    mapa_centra.set_zoom(6)
    mapa_centra.grid(row=0, column=0)

    odswiez_liste_centrow()
    odswiez_mape_centrow()


# KLIENCI

def odswiez_liste_klientow(dane=None) -> None:
    global wyswietlane_klienci

    if dane is None:
        dane = klienci

    wyswietlane_klienci = dane
    listbox_klienci.delete(0, END)

    for klient in wyswietlane_klienci:
        listbox_klienci.insert(
            END,
            f"{klient['id']} - {klient['imie']} {klient['nazwisko']} ({klient['firma']}, {klient['miasto']})"
        )


def filtruj_klientow(event=None) -> None:
    fraza = entry_filtr_klienci.get()
    wybrane_pole = combo_filtr_klienci.get()

    pola_klienci = {
        "Miasto": "miasto",
        "Nazwisko": "nazwisko",
        "Firma": "firma"
    }

    wyniki = []

    for klient in klienci:
        if pasuje_do_filtra(klient, fraza, wybrane_pole, pola_klienci):
            wyniki.append(klient)

    odswiez_liste_klientow(wyniki)
    odswiez_mape_klientow(wyniki)


def pokaz_klienta(event=None) -> None:
    wybor = listbox_klienci.curselection()

    if len(wybor) == 0:
        return

    i = wybor[0]
    klient = wyswietlane_klienci[i]

    wpisz_do_pola(entry_klient_imie, klient["imie"])
    wpisz_do_pola(entry_klient_nazwisko, klient["nazwisko"])
    wpisz_do_pola(entry_klient_firma, klient["firma"])
    wpisz_do_pola(entry_klient_miasto, klient["miasto"])
    wpisz_do_pola(entry_klient_latitude, klient["latitude"])
    wpisz_do_pola(entry_klient_longitude, klient["longitude"])

    mapa_klienci.set_position(klient["latitude"], klient["longitude"])
    mapa_klienci.set_zoom(12)


def dodaj_klienta() -> None:
    wspolrzedne = pobierz_wspolrzedne_klienta_z_miasta(entry_klient_miasto)

    if wspolrzedne is None:
        return

    latitude, longitude = wspolrzedne

    nowy_klient = {
        "id": nastepne_id(klienci),
        "imie": entry_klient_imie.get(),
        "nazwisko": entry_klient_nazwisko.get(),
        "firma": entry_klient_firma.get(),
        "miasto": entry_klient_miasto.get(),
        "latitude": latitude,
        "longitude": longitude
    }

    klienci.append(nowy_klient)
    filtruj_klientow()
    wyczysc_pola(pola_klient)

    messagebox.showinfo("Sukces", "Dodano klienta.")


def aktualizuj_klienta() -> None:
    wybor = listbox_klienci.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz klienta z listy.")
        return

    wspolrzedne = pobierz_wspolrzedne_klienta_z_miasta(entry_klient_miasto)

    if wspolrzedne is None:
        return

    latitude, longitude = wspolrzedne

    i = wybor[0]
    klient = wyswietlane_klienci[i]

    klient["imie"] = entry_klient_imie.get()
    klient["nazwisko"] = entry_klient_nazwisko.get()
    klient["firma"] = entry_klient_firma.get()
    klient["miasto"] = entry_klient_miasto.get()
    klient["latitude"] = latitude
    klient["longitude"] = longitude

    wpisz_do_pola(entry_klient_latitude, latitude)
    wpisz_do_pola(entry_klient_longitude, longitude)

    filtruj_klientow()
    messagebox.showinfo("Sukces", "Zaktualizowano klienta.")


def usun_klienta() -> None:
    wybor = listbox_klienci.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz klienta z listy.")
        return

    i = wybor[0]
    klient = wyswietlane_klienci[i]

    klienci.remove(klient)

    filtruj_klientow()
    wyczysc_pola(pola_klient)
    messagebox.showinfo("Sukces", "Usunięto klienta.")


def odswiez_mape_klientow(dane=None) -> None:
    if dane is None:
        dane = klienci

    for marker in markery_klienci:
        marker.delete()

    markery_klienci.clear()

    for klient in dane:
        marker = mapa_klienci.set_marker(
            klient["latitude"],
            klient["longitude"],
            text=f"{klient['imie']} {klient['nazwisko']}"
        )
        markery_klienci.append(marker)


def utworz_zakladke_klienci(zakladka: Frame) -> None:
    global listbox_klienci
    global entry_filtr_klienci, combo_filtr_klienci
    global entry_klient_imie, entry_klient_nazwisko, entry_klient_firma
    global entry_klient_miasto, entry_klient_latitude, entry_klient_longitude
    global pola_klient
    global mapa_klienci, markery_klienci, wyswietlane_klienci

    markery_klienci = []
    wyswietlane_klienci = klienci.copy()

    ramka_lista = Frame(zakladka)
    ramka_formularz = LabelFrame(zakladka, text="Dane klienta")
    ramka_mapa = LabelFrame(zakladka, text="Mapa klientów")

    ramka_lista.grid(row=0, column=0, padx=10, pady=10, sticky=N)
    ramka_formularz.grid(row=0, column=1, padx=10, pady=10, sticky=N)
    ramka_mapa.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    Label(ramka_lista, text="Lista klientów:").grid(row=0, column=0, columnspan=3)

    Label(ramka_lista, text="Filtruj po:").grid(row=1, column=0, sticky=W)
    combo_filtr_klienci = ttk.Combobox(
        ramka_lista,
        values=["Wszystko", "Miasto", "Nazwisko", "Firma"],
        state="readonly",
        width=18
    )
    combo_filtr_klienci.set("Wszystko")
    combo_filtr_klienci.grid(row=1, column=1, pady=5)
    combo_filtr_klienci.bind("<<ComboboxSelected>>", filtruj_klientow)

    Label(ramka_lista, text="Szukaj:").grid(row=2, column=0, sticky=W)
    entry_filtr_klienci = Entry(ramka_lista, width=30)
    entry_filtr_klienci.grid(row=2, column=1, columnspan=2, pady=5)
    entry_filtr_klienci.bind("<KeyRelease>", filtruj_klientow)

    listbox_klienci = Listbox(ramka_lista, width=55, height=14)
    listbox_klienci.grid(row=3, column=0, columnspan=3)
    listbox_klienci.bind("<<ListboxSelect>>", pokaz_klienta)

    Button(ramka_lista, text="Usuń", command=usun_klienta).grid(row=4, column=0, pady=5)
    Button(ramka_lista, text="Odśwież mapę", command=filtruj_klientow).grid(row=4, column=1, pady=5)

    Label(ramka_formularz, text="Imię:").grid(row=0, column=0, sticky=W)
    Label(ramka_formularz, text="Nazwisko:").grid(row=1, column=0, sticky=W)
    Label(ramka_formularz, text="Firma:").grid(row=2, column=0, sticky=W)
    Label(ramka_formularz, text="Miasto:").grid(row=3, column=0, sticky=W)
    Label(ramka_formularz, text="Szerokość:").grid(row=4, column=0, sticky=W)
    Label(ramka_formularz, text="Długość:").grid(row=5, column=0, sticky=W)

    entry_klient_imie = Entry(ramka_formularz, width=35)
    entry_klient_nazwisko = Entry(ramka_formularz, width=35)
    entry_klient_firma = Entry(ramka_formularz, width=35)
    entry_klient_miasto = Entry(ramka_formularz, width=35)
    entry_klient_latitude = Entry(ramka_formularz, width=35)
    entry_klient_longitude = Entry(ramka_formularz, width=35)

    entry_klient_imie.grid(row=0, column=1)
    entry_klient_nazwisko.grid(row=1, column=1)
    entry_klient_firma.grid(row=2, column=1)
    entry_klient_miasto.grid(row=3, column=1)
    entry_klient_latitude.grid(row=4, column=1)
    entry_klient_longitude.grid(row=5, column=1)

    pola_klient = [
        entry_klient_imie,
        entry_klient_nazwisko,
        entry_klient_firma,
        entry_klient_miasto,
        entry_klient_latitude,
        entry_klient_longitude
    ]

    Button(ramka_formularz, text="Dodaj", command=dodaj_klienta).grid(row=6, column=0, pady=10)
    Button(ramka_formularz, text="Zapisz zmiany", command=aktualizuj_klienta).grid(row=6, column=1, pady=10)
    Button(ramka_formularz, text="Wyczyść", command=lambda: wyczysc_pola(pola_klient)).grid(row=7, column=0, columnspan=2)

    mapa_klienci = tkintermapview.TkinterMapView(ramka_mapa, width=1150, height=400, corner_radius=4)
    mapa_klienci.set_position(52.0, 19.0)
    mapa_klienci.set_zoom(6)
    mapa_klienci.grid(row=0, column=0)

    odswiez_liste_klientow()
    odswiez_mape_klientow()


# PRACOWNICY

def odswiez_liste_pracownikow(dane=None) -> None:
    global wyswietlane_pracownicy

    if dane is None:
        dane = pracownicy

    wyswietlane_pracownicy = dane
    listbox_pracownicy.delete(0, END)

    for pracownik in wyswietlane_pracownicy:
        listbox_pracownicy.insert(
            END,
            f"{pracownik['id']} - {pracownik['imie']} {pracownik['nazwisko']} ({pracownik['stanowisko']}, {pracownik['miasto']})"
        )


def filtruj_pracownikow(event=None) -> None:
    fraza = entry_filtr_pracownicy.get()
    wybrane_pole = combo_filtr_pracownicy.get()

    pola_pracownicy = {
        "Miasto": "miasto",
        "Nazwisko": "nazwisko",
        "Stanowisko": "stanowisko"
    }

    wyniki = []

    for pracownik in pracownicy:
        if pasuje_do_filtra(pracownik, fraza, wybrane_pole, pola_pracownicy):
            wyniki.append(pracownik)

    odswiez_liste_pracownikow(wyniki)
    odswiez_mape_pracownikow(wyniki)


def pokaz_pracownika(event=None) -> None:
    wybor = listbox_pracownicy.curselection()

    if len(wybor) == 0:
        return

    i = wybor[0]
    pracownik = wyswietlane_pracownicy[i]

    wpisz_do_pola(entry_pracownik_imie, pracownik["imie"])
    wpisz_do_pola(entry_pracownik_nazwisko, pracownik["nazwisko"])
    wpisz_do_pola(entry_pracownik_stanowisko, pracownik["stanowisko"])
    wpisz_do_pola(entry_pracownik_id_centrum, pracownik["id_centrum"])
    wpisz_do_pola(entry_pracownik_miasto, pracownik["miasto"])
    wpisz_do_pola(entry_pracownik_latitude, pracownik["latitude"])
    wpisz_do_pola(entry_pracownik_longitude, pracownik["longitude"])

    mapa_pracownicy.set_position(pracownik["latitude"], pracownik["longitude"])
    mapa_pracownicy.set_zoom(12)


def dodaj_pracownika() -> None:
    try:
        id_centrum = int(entry_pracownik_id_centrum.get())
    except ValueError:
        messagebox.showerror("Błąd", "ID centrum musi być liczbą.")
        return

    centrum = znajdz_po_id(centra, id_centrum)

    if centrum is None:
        messagebox.showerror("Błąd", "Nie ma centrum o takim ID.")
        return

    nowy_pracownik = {
        "id": nastepne_id(pracownicy),
        "imie": entry_pracownik_imie.get(),
        "nazwisko": entry_pracownik_nazwisko.get(),
        "stanowisko": entry_pracownik_stanowisko.get(),
        "id_centrum": id_centrum,
        "miasto": centrum["miasto"],
        "latitude": centrum["latitude"],
        "longitude": centrum["longitude"]
    }

    pracownicy.append(nowy_pracownik)
    filtruj_pracownikow()
    wyczysc_pola(pola_pracownik)

    messagebox.showinfo("Sukces", "Dodano pracownika.")


def aktualizuj_pracownika() -> None:
    wybor = listbox_pracownicy.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz pracownika z listy.")
        return

    try:
        id_centrum = int(entry_pracownik_id_centrum.get())
    except ValueError:
        messagebox.showerror("Błąd", "ID centrum musi być liczbą.")
        return

    centrum = znajdz_po_id(centra, id_centrum)

    if centrum is None:
        messagebox.showerror("Błąd", "Nie ma centrum o takim ID.")
        return

    i = wybor[0]
    pracownik = wyswietlane_pracownicy[i]

    pracownik["imie"] = entry_pracownik_imie.get()
    pracownik["nazwisko"] = entry_pracownik_nazwisko.get()
    pracownik["stanowisko"] = entry_pracownik_stanowisko.get()
    pracownik["id_centrum"] = id_centrum
    pracownik["miasto"] = centrum["miasto"]
    pracownik["latitude"] = centrum["latitude"]
    pracownik["longitude"] = centrum["longitude"]

    wpisz_do_pola(entry_pracownik_miasto, centrum["miasto"])
    wpisz_do_pola(entry_pracownik_latitude, centrum["latitude"])
    wpisz_do_pola(entry_pracownik_longitude, centrum["longitude"])

    filtruj_pracownikow()
    messagebox.showinfo("Sukces", "Zaktualizowano pracownika.")


def usun_pracownika() -> None:
    wybor = listbox_pracownicy.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz pracownika z listy.")
        return

    i = wybor[0]
    pracownik = wyswietlane_pracownicy[i]

    pracownicy.remove(pracownik)

    filtruj_pracownikow()
    wyczysc_pola(pola_pracownik)
    messagebox.showinfo("Sukces", "Usunięto pracownika.")


def odswiez_mape_pracownikow(dane=None) -> None:
    if dane is None:
        dane = pracownicy

    for marker in markery_pracownicy:
        marker.delete()

    markery_pracownicy.clear()

    for pracownik in dane:
        marker = mapa_pracownicy.set_marker(
            pracownik["latitude"],
            pracownik["longitude"],
            text=f"{pracownik['imie']} {pracownik['nazwisko']}"
        )
        markery_pracownicy.append(marker)


def utworz_zakladke_pracownicy(zakladka: Frame) -> None:
    global listbox_pracownicy
    global entry_filtr_pracownicy, combo_filtr_pracownicy
    global entry_pracownik_imie, entry_pracownik_nazwisko, entry_pracownik_stanowisko
    global entry_pracownik_id_centrum, entry_pracownik_miasto
    global entry_pracownik_latitude, entry_pracownik_longitude
    global pola_pracownik
    global mapa_pracownicy, markery_pracownicy, wyswietlane_pracownicy

    markery_pracownicy = []
    wyswietlane_pracownicy = pracownicy.copy()

    ramka_lista = Frame(zakladka)
    ramka_formularz = LabelFrame(zakladka, text="Dane pracownika")
    ramka_mapa = LabelFrame(zakladka, text="Mapa pracowników")

    ramka_lista.grid(row=0, column=0, padx=10, pady=10, sticky=N)
    ramka_formularz.grid(row=0, column=1, padx=10, pady=10, sticky=N)
    ramka_mapa.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    Label(ramka_lista, text="Lista pracowników:").grid(row=0, column=0, columnspan=3)

    Label(ramka_lista, text="Filtruj po:").grid(row=1, column=0, sticky=W)
    combo_filtr_pracownicy = ttk.Combobox(
        ramka_lista,
        values=["Wszystko", "Miasto", "Nazwisko", "Stanowisko"],
        state="readonly",
        width=18
    )
    combo_filtr_pracownicy.set("Wszystko")
    combo_filtr_pracownicy.grid(row=1, column=1, pady=5)
    combo_filtr_pracownicy.bind("<<ComboboxSelected>>", filtruj_pracownikow)

    Label(ramka_lista, text="Szukaj:").grid(row=2, column=0, sticky=W)
    entry_filtr_pracownicy = Entry(ramka_lista, width=30)
    entry_filtr_pracownicy.grid(row=2, column=1, columnspan=2, pady=5)
    entry_filtr_pracownicy.bind("<KeyRelease>", filtruj_pracownikow)

    listbox_pracownicy = Listbox(ramka_lista, width=55, height=14)
    listbox_pracownicy.grid(row=3, column=0, columnspan=3)
    listbox_pracownicy.bind("<<ListboxSelect>>", pokaz_pracownika)

    Button(ramka_lista, text="Usuń", command=usun_pracownika).grid(row=4, column=0, pady=5)
    Button(ramka_lista, text="Odśwież mapę", command=filtruj_pracownikow).grid(row=4, column=1, pady=5)

    Label(ramka_formularz, text="Imię:").grid(row=0, column=0, sticky=W)
    Label(ramka_formularz, text="Nazwisko:").grid(row=1, column=0, sticky=W)
    Label(ramka_formularz, text="Stanowisko:").grid(row=2, column=0, sticky=W)
    Label(ramka_formularz, text="ID centrum:").grid(row=3, column=0, sticky=W)
    Label(ramka_formularz, text="Miasto:").grid(row=4, column=0, sticky=W)
    Label(ramka_formularz, text="Szerokość:").grid(row=5, column=0, sticky=W)
    Label(ramka_formularz, text="Długość:").grid(row=6, column=0, sticky=W)

    entry_pracownik_imie = Entry(ramka_formularz, width=35)
    entry_pracownik_nazwisko = Entry(ramka_formularz, width=35)
    entry_pracownik_stanowisko = Entry(ramka_formularz, width=35)
    entry_pracownik_id_centrum = Entry(ramka_formularz, width=35)
    entry_pracownik_miasto = Entry(ramka_formularz, width=35)
    entry_pracownik_latitude = Entry(ramka_formularz, width=35)
    entry_pracownik_longitude = Entry(ramka_formularz, width=35)

    entry_pracownik_imie.grid(row=0, column=1)
    entry_pracownik_nazwisko.grid(row=1, column=1)
    entry_pracownik_stanowisko.grid(row=2, column=1)
    entry_pracownik_id_centrum.grid(row=3, column=1)
    entry_pracownik_miasto.grid(row=4, column=1)
    entry_pracownik_latitude.grid(row=5, column=1)
    entry_pracownik_longitude.grid(row=6, column=1)

    pola_pracownik = [
        entry_pracownik_imie,
        entry_pracownik_nazwisko,
        entry_pracownik_stanowisko,
        entry_pracownik_id_centrum,
        entry_pracownik_miasto,
        entry_pracownik_latitude,
        entry_pracownik_longitude
    ]

    Button(ramka_formularz, text="Dodaj", command=dodaj_pracownika).grid(row=7, column=0, pady=10)
    Button(ramka_formularz, text="Zapisz zmiany", command=aktualizuj_pracownika).grid(row=7, column=1, pady=10)
    Button(ramka_formularz, text="Wyczyść", command=lambda: wyczysc_pola(pola_pracownik)).grid(row=8, column=0, columnspan=2)

    mapa_pracownicy = tkintermapview.TkinterMapView(ramka_mapa, width=1150, height=400, corner_radius=4)
    mapa_pracownicy.set_position(52.0, 19.0)
    mapa_pracownicy.set_zoom(6)
    mapa_pracownicy.grid(row=0, column=0)

    odswiez_liste_pracownikow()
    odswiez_mape_pracownikow()


# REZERWACJE I RAPORTY

def opis_rezerwacji(rezerwacja: dict) -> str:
    klient = znajdz_po_id(klienci, rezerwacja["id_klienta"])
    centrum = znajdz_po_id(centra, rezerwacja["id_centrum"])

    if klient is not None:
        klient_txt = f"{klient['imie']} {klient['nazwisko']}"
    else:
        klient_txt = "brak klienta"

    if centrum is not None:
        centrum_txt = centrum["nazwa"]
    else:
        centrum_txt = "brak centrum"

    return f"{rezerwacja['id']} - {klient_txt} | {centrum_txt} | {rezerwacja['data']}"


def odswiez_liste_rezerwacji() -> None:
    listbox_rezerwacje.delete(0, END)

    for rezerwacja in rezerwacje:
        listbox_rezerwacje.insert(END, opis_rezerwacji(rezerwacja))


def pokaz_rezerwacje(event=None) -> None:
    wybor = listbox_rezerwacje.curselection()

    if len(wybor) == 0:
        return

    i = wybor[0]
    rezerwacja = rezerwacje[i]

    wpisz_do_pola(entry_rez_id_klienta, rezerwacja["id_klienta"])
    wpisz_do_pola(entry_rez_id_centrum, rezerwacja["id_centrum"])
    wpisz_do_pola(entry_rez_data, rezerwacja["data"])
    wpisz_do_pola(entry_rez_sala, rezerwacja["sala"])
    wpisz_do_pola(entry_rez_liczba_osob, rezerwacja["liczba_osob"])


def dodaj_rezerwacje() -> None:
    try:
        id_klienta = int(entry_rez_id_klienta.get())
        id_centrum = int(entry_rez_id_centrum.get())

        if znajdz_po_id(klienci, id_klienta) is None:
            messagebox.showerror("Błąd", "Nie ma klienta o takim ID.")
            return

        if znajdz_po_id(centra, id_centrum) is None:
            messagebox.showerror("Błąd", "Nie ma centrum o takim ID.")
            return

        nowa_rezerwacja = {
            "id": nastepne_id(rezerwacje),
            "id_klienta": id_klienta,
            "id_centrum": id_centrum,
            "data": entry_rez_data.get(),
            "sala": entry_rez_sala.get(),
            "liczba_osob": int(entry_rez_liczba_osob.get())
        }

        rezerwacje.append(nowa_rezerwacja)
        odswiez_liste_rezerwacji()
        wyczysc_pola(pola_rezerwacja)
        messagebox.showinfo("Sukces", "Dodano rezerwację.")

    except ValueError:
        messagebox.showerror("Błąd", "ID klienta, ID centrum i liczba osób muszą być liczbami.")


def aktualizuj_rezerwacje() -> None:
    wybor = listbox_rezerwacje.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz rezerwację z listy.")
        return

    try:
        id_klienta = int(entry_rez_id_klienta.get())
        id_centrum = int(entry_rez_id_centrum.get())

        if znajdz_po_id(klienci, id_klienta) is None:
            messagebox.showerror("Błąd", "Nie ma klienta o takim ID.")
            return

        if znajdz_po_id(centra, id_centrum) is None:
            messagebox.showerror("Błąd", "Nie ma centrum o takim ID.")
            return

        i = wybor[0]
        rezerwacje[i]["id_klienta"] = id_klienta
        rezerwacje[i]["id_centrum"] = id_centrum
        rezerwacje[i]["data"] = entry_rez_data.get()
        rezerwacje[i]["sala"] = entry_rez_sala.get()
        rezerwacje[i]["liczba_osob"] = int(entry_rez_liczba_osob.get())

        odswiez_liste_rezerwacji()
        messagebox.showinfo("Sukces", "Zaktualizowano rezerwację.")

    except ValueError:
        messagebox.showerror("Błąd", "ID klienta, ID centrum i liczba osób muszą być liczbami.")


def usun_rezerwacje() -> None:
    wybor = listbox_rezerwacje.curselection()

    if len(wybor) == 0:
        messagebox.showwarning("Uwaga", "Najpierw wybierz rezerwację z listy.")
        return

    i = wybor[0]
    rezerwacje.pop(i)

    odswiez_liste_rezerwacji()
    wyczysc_pola(pola_rezerwacja)
    messagebox.showinfo("Sukces", "Usunięto rezerwację.")


def raport_klienci_centrum() -> None:
    tekst_raport.delete("1.0", END)

    try:
        id_centrum = int(entry_raport_id_centrum.get())
    except ValueError:
        messagebox.showerror("Błąd", "ID centrum musi być liczbą.")
        return

    centrum = znajdz_po_id(centra, id_centrum)

    if centrum is None:
        tekst_raport.insert(END, "Nie ma centrum o takim ID.")
        return

    tekst_raport.insert(END, f"Klienci centrum: {centrum['nazwa']}\n\n")

    znalezione_id = []

    for rezerwacja in rezerwacje:
        if rezerwacja["id_centrum"] == id_centrum:
            if rezerwacja["id_klienta"] not in znalezione_id:
                znalezione_id.append(rezerwacja["id_klienta"])

    if len(znalezione_id) == 0:
        tekst_raport.insert(END, "Brak klientów dla wybranego centrum.")
        return

    for id_klienta in znalezione_id:
        klient = znajdz_po_id(klienci, id_klienta)

        if klient is not None:
            tekst_raport.insert(
                END,
                f"ID: {klient['id']} | {klient['imie']} {klient['nazwisko']} | {klient['firma']}\n"
            )


def raport_rezerwacje_klienta() -> None:
    tekst_raport.delete("1.0", END)

    try:
        id_klienta = int(entry_raport_id_klienta.get())
    except ValueError:
        messagebox.showerror("Błąd", "ID klienta musi być liczbą.")
        return

    klient = znajdz_po_id(klienci, id_klienta)

    if klient is None:
        tekst_raport.insert(END, "Nie ma klienta o takim ID.")
        return

    tekst_raport.insert(END, f"Rezerwacje klienta: {klient['imie']} {klient['nazwisko']}\n\n")

    znaleziono = False

    for rezerwacja in rezerwacje:
        if rezerwacja["id_klienta"] == id_klienta:
            centrum = znajdz_po_id(centra, rezerwacja["id_centrum"])

            if centrum is not None:
                nazwa_centrum = centrum["nazwa"]
            else:
                nazwa_centrum = "brak danych"

            tekst_raport.insert(
                END,
                f"ID rezerwacji: {rezerwacja['id']}\n"
                f"Centrum: {nazwa_centrum}\n"
                f"Data: {rezerwacja['data']}\n"
                f"Sala: {rezerwacja['sala']}\n"
                f"Liczba osób: {rezerwacja['liczba_osob']}\n"
                f"-----------------------------\n"
            )

            znaleziono = True

    if not znaleziono:
        tekst_raport.insert(END, "Ten klient nie ma rezerwacji.")


def utworz_zakladke_rezerwacje(zakladka: Frame) -> None:
    global listbox_rezerwacje
    global entry_rez_id_klienta, entry_rez_id_centrum, entry_rez_data
    global entry_rez_sala, entry_rez_liczba_osob
    global pola_rezerwacja
    global entry_raport_id_centrum, entry_raport_id_klienta, tekst_raport

    ramka_lista = Frame(zakladka)
    ramka_formularz = LabelFrame(zakladka, text="Dane rezerwacji")
    ramka_raport = LabelFrame(zakladka, text="Raporty")

    ramka_lista.grid(row=0, column=0, padx=10, pady=10, sticky=N)
    ramka_formularz.grid(row=0, column=1, padx=10, pady=10, sticky=N)
    ramka_raport.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W)

    Label(ramka_lista, text="Lista rezerwacji:").grid(row=0, column=0)
    listbox_rezerwacje = Listbox(ramka_lista, width=70, height=14)
    listbox_rezerwacje.grid(row=1, column=0, columnspan=3)
    listbox_rezerwacje.bind("<<ListboxSelect>>", pokaz_rezerwacje)

    Button(ramka_lista, text="Usuń", command=usun_rezerwacje).grid(row=2, column=0, pady=5)

    Label(ramka_formularz, text="ID klienta:").grid(row=0, column=0, sticky=W)
    Label(ramka_formularz, text="ID centrum:").grid(row=1, column=0, sticky=W)
    Label(ramka_formularz, text="Data:").grid(row=2, column=0, sticky=W)
    Label(ramka_formularz, text="Sala:").grid(row=3, column=0, sticky=W)
    Label(ramka_formularz, text="Liczba osób:").grid(row=4, column=0, sticky=W)

    entry_rez_id_klienta = Entry(ramka_formularz, width=35)
    entry_rez_id_centrum = Entry(ramka_formularz, width=35)
    entry_rez_data = Entry(ramka_formularz, width=35)
    entry_rez_sala = Entry(ramka_formularz, width=35)
    entry_rez_liczba_osob = Entry(ramka_formularz, width=35)

    entry_rez_id_klienta.grid(row=0, column=1)
    entry_rez_id_centrum.grid(row=1, column=1)
    entry_rez_data.grid(row=2, column=1)
    entry_rez_sala.grid(row=3, column=1)
    entry_rez_liczba_osob.grid(row=4, column=1)

    pola_rezerwacja = [
        entry_rez_id_klienta,
        entry_rez_id_centrum,
        entry_rez_data,
        entry_rez_sala,
        entry_rez_liczba_osob
    ]

    Button(ramka_formularz, text="Dodaj", command=dodaj_rezerwacje).grid(row=5, column=0, pady=10)
    Button(ramka_formularz, text="Zapisz zmiany", command=aktualizuj_rezerwacje).grid(row=5, column=1, pady=10)
    Button(ramka_formularz, text="Wyczyść", command=lambda: wyczysc_pola(pola_rezerwacja)).grid(row=6, column=0, columnspan=2)

    Label(ramka_raport, text="ID centrum:").grid(row=0, column=0, sticky=W)
    entry_raport_id_centrum = Entry(ramka_raport, width=20)
    entry_raport_id_centrum.grid(row=0, column=1, padx=5)

    Button(
        ramka_raport,
        text="Pokaż klientów wybranego centrum",
        command=raport_klienci_centrum
    ).grid(row=0, column=2, padx=5)

    Label(ramka_raport, text="ID klienta:").grid(row=1, column=0, sticky=W)
    entry_raport_id_klienta = Entry(ramka_raport, width=20)
    entry_raport_id_klienta.grid(row=1, column=1, padx=5)

    Button(
        ramka_raport,
        text="Pokaż rezerwacje klienta",
        command=raport_rezerwacje_klienta
    ).grid(row=1, column=2, padx=5)

    tekst_raport = Text(ramka_raport, width=130, height=12)
    tekst_raport.grid(row=2, column=0, columnspan=3, pady=10)

    odswiez_liste_rezerwacji()


# OKNO LOGOWANIA

root = Tk()
root.title("Logowanie do systemu")
root.geometry("400x230")
root.configure(bg=JASNY_NIEBIESKI)

ustaw_styl_ttk()

ramka_logowanie = Frame(root)
ramka_logowanie.pack(pady=30)

Label(ramka_logowanie, text="Logowanie do systemu", font=("Arial", 14, "bold")).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=10
)

Label(ramka_logowanie, text="Login:").grid(row=1, column=0, sticky=W, pady=5)
entry_login = Entry(ramka_logowanie, width=30)
entry_login.grid(row=1, column=1, pady=5)

Label(ramka_logowanie, text="Hasło:").grid(row=2, column=0, sticky=W, pady=5)
entry_haslo = Entry(ramka_logowanie, width=30, show="*")
entry_haslo.grid(row=2, column=1, pady=5)

Button(ramka_logowanie, text="Zaloguj", command=sprawdz_logowanie).grid(
    row=3,
    column=0,
    columnspan=2,
    pady=15
)

Label(ramka_logowanie, text="Dane testowe: admin / admin").grid(row=4, column=0, columnspan=2)

ustaw_kolory(root)

root.mainloop()
