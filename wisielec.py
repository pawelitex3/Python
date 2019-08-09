import pygame, sys
pygame.init()

class Przycisk(object):
    def __init__(self, szerokosc, wysokosc, x, y, kolor, tekst=''):
        self.kolor = kolor
        self.tekst = tekst
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.x = x
        self.y = y

    def rysuj(self, obraz, outline=None):
        pygame.draw.rect(obraz, self.kolor, (self.x, self.y, self.szerokosc, self.wysokosc), 0)

        if self.tekst != '':
            font = pygame.font.SysFont('verdana', 20)
            tekst = font.render(self.tekst, 1, (255, 255, 255))
            obraz.blit(tekst, (self.x + (self.szerokosc/2 - tekst.get_width()/2), self.y + (self.wysokosc/2 - tekst.get_height()/2)))

    def isOver(self, pozycja):
        if pozycja[0] > self.x and pozycja[0] < self.x+self.szerokosc:
            if pozycja[1] > self.y and pozycja[1] < self.y+self.wysokosc:
                return True

def StworzPrzyciski():
    LITERKI = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUWVXYZŹŻ.'
    k=0
    tablica = []
    for i in range(6):
        for j in range(6):
            if j!=5 or i!=5:
                kwadrat = Przycisk(80, 80, j * 100 + 30, i * 100 + 60, (230, 100, 150), LITERKI[k])
                tablica.append(kwadrat)
                k+=1
    return tablica

def RysujPrzyciski(Przyciski, obraz):
    for p in Przyciski:
        p.rysuj(obraz)

    pygame.display.flip()

def SprawdzCzyWHasle(haslo, litera):
    for znak in haslo:
        if znak == litera:
            return True
    return False

def RysujKoniecGry(obraz, tekst):
    koniec = Przycisk(400, 100, 750, 470, (0, 0, 40), tekst)
    koniec.rysuj(obraz)

def WyswietlPoczatkoweLitery(haslo, obraz):
    odgadywane = ''
    pozostalo = 0
    for litera in haslo:
        if litera != ' ':
            odgadywane+='_ '
            pozostalo+=1
        else:
            odgadywane+='  '
    WyswietloneHaslo = Przycisk(600, 100, 650, 100, (0, 0, 40), odgadywane)
    WyswietloneHaslo.rysuj(obraz)
    return WyswietloneHaslo, pozostalo

def ZmienLitery(WyswietloneHaslo, haslo, litera, obraz, pozostalo):
    i=0
    noweHaslo = ''
    for l in haslo:
        if l == litera:
            noweHaslo += litera + ' '
            pozostalo-=1
        else:
            noweHaslo += WyswietloneHaslo.tekst[2*i] + ' '
        i+=1
    WyswietloneHaslo.tekst = noweHaslo
    WyswietloneHaslo.rysuj(obraz)
    return WyswietloneHaslo, pozostalo

rozmiar = szerokosc, wysokosc = 1280, 720
screen = pygame.display.set_mode(rozmiar)

haslo = input()
haslo = haslo.upper()
obrazki = []
Wcisniete = []
Przyciski = StworzPrzyciski()
RysujPrzyciski(Przyciski, screen)
szansa = 0

WyswietloneHaslo, pozostalo = WyswietlPoczatkoweLitery(haslo, screen)

obrazki.append("wisielec1.png")
obrazki.append("wisielec2.png")
obrazki.append("wisielec3.png")
obrazki.append("wisielec4.png")
obrazki.append("wisielec5.png")
obrazki.append("wisielec6.png")
obrazki.append("wisielec7.png")
obrazki.append("wisielec8.png")
obrazki.append("wisielec9.png")
obrazki.append("wisielec10.png")

for i in range(36):
    Wcisniete.append(0)

while True:

    for event in pygame.event.get():
        pozycja = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            i=0
            for p in Przyciski:
                if p.isOver(pozycja) and Wcisniete[i] != 1 and szansa < 10:
                    p.kolor = (230, 0, 150)
                    Wcisniete[i] = 1
                    if SprawdzCzyWHasle(haslo, p.tekst):
                       p.kolor = (100, 255, 0)
                       WyswietloneHaslo, pozostalo = ZmienLitery(WyswietloneHaslo, haslo, p.tekst, screen, pozostalo)
                       print(pozostalo)
                       if pozostalo == 0:
                           RysujKoniecGry(screen, "BRAWO! HASŁO ZOSTAŁO ODGADNIĘTE!")
                           szansa = 10
                    else:
                        wisielec = pygame.image.load(obrazki[szansa])
                        pozycja_wisielca = wisielec.get_rect()
                        pozycja_wisielca = pozycja_wisielca.move([780, 200])
                        screen.fill((0, 0, 0))
                        screen.blit(wisielec, pozycja_wisielca)
                        pygame.display.flip()
                        szansa += 1
                        if szansa<10:
                            pass
                        else:
                            RysujKoniecGry(screen, "KONIEC GRY")

                    print(p.tekst)
                i+=1
            WyswietloneHaslo.rysuj(screen)
            RysujPrzyciski(Przyciski, screen)

        elif event.type == pygame.MOUSEMOTION:
            i=0
            for p in Przyciski:
                if p.isOver(pozycja) and Wcisniete[i]!=1 and szansa < 10:
                    p.kolor = (230, 0, 0)
                elif Wcisniete[i]!=1:
                    p.kolor = (230, 100, 150)
                i+=1
            WyswietloneHaslo.rysuj(screen)
            RysujPrzyciski(Przyciski, screen)
