"""
from datetime import datetime  # datum

produkter = {
    100: {"namn": "Pepsi max", "pris": 22.90,"Pristyp":"st"},
    101: {"namn": "Mjölk", "pris": 10,"Pristyp":"st"},
    102: {"namn": "Bröd", "pris": 20,"Pristyp":"st"},
    103: {"namn": "Ägg", "pris": 30,"Pristyp":"st"},
    104: {"namn": "Smör", "pris": 25,"Pristyp":"kg"},
    105: {"namn": "Ris", "pris": 55.90,"Pristyp":"kg"},
    106: {"namn": "Pasta", "pris": 55.90,"Pristyp":"kg"},
    107: {"namn": "Havregrynsgröt", "pris": 55.90,"Pristyp":"kg"},
    108: {"namn": "Yoghurt", "pris": 22.50,"Pristyp":"st"},
    109: {"namn": "Mjöl", "pris": 12.90,"Pristyp":"st"},
    110: {"namn": "Strösocker", "pris": 27.90,"Pristyp":"kg"},
    111: {"namn": "Salt", "pris": 12.50,"Pristyp":"kg"},
    112: {"namn": "Bananer", "pris": 4.50,"Pristyp":"st"},
    113: {"namn": "Apelsin", "pris": 6.90,"Pristyp":"st"},
    114: {"namn": "Äpplen", "pris": 5.40,"Pristyp":"st"},
    115: {"namn": "Potatis", "pris": 17.90,"Pristyp":"kg"},
    116: {"namn": "Gurka", "pris": 14.90,"Pristyp":"st"},
    117: {"namn": "Isbergsallat", "pris": 17.90,"Pristyp":"st"},
    118: {"namn": "Kyckling", "pris": 112.90,"Pristyp":"kg"},
    119: {"namn": "Köttbullar", "pris": 70.90,"Pristyp":"kg"},
    120: {"namn": "Kladdkaka", "pris": 25.90,"Pristyp":"st"}
}

# Definiera en klass för att hantera produkter
class Product:
    def __init__(self, product_id, name, price, price_type):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.price_type = price_type

# Globala variabler
kvittonummer = 0000  # För att hålla reda på kvitto-nummer

# Filnamn för att spara kvitton
Kvitto_fil = f"Kvitto_{datetime.now().strftime('%Y-%m-%d')}.txt"  # Filnamn för dagens kvitto


def file_kvitto(kvitto):
   
    with open(Kvitto_fil, "a", encoding="utf-8") as file:  # encoding="utf-8" för svenska tecken
        file.write(kvitto + "\n\n")  # Spara kvitto med en ny rad

def NyKund():
    global kvittonummer  # Gör den globala variabeln tillgänglig i funktionen
    kvitto_lista = []  # Lista för att hålla produkter som kunden köper
    print("Skriv in produktens id och antal i formatet: <produktid> <antal>")
    print("Skriv 'PAY' för att gå vidare till betalning.")
    while True:  
        Produkt_Antal = input("ProduktId och Antal: ")
            
        if Produkt_Antal.upper() != "PAY": #om användaren inte har skrivit in PAY, fortsätt med att sätta in produkter
            # Dela upp inmatningen där det finns mellanslag
            data = Produkt_Antal.split()
            
            #kollar att användaren verkligen har lagt in två värden som har ett mellan slag
            if len(data) != 2:
                print("Fel: Du måste mata in både produkt-ID och antal. Försök igen.")
                continue  
            else:
             produktid = int(data[0])
             antal = float(data[1])
            
            # Kontrollera om produktid finns i listan över produkter
             if produktid in produkter:
                produktNamn = produkter[produktid]["namn"]
                pris = produkter[produktid]["pris"]
                
                # Beräkna totalpris för produkten
                totalPris = pris * antal
                
                # Lägg till produktinformation i kvitto-listan
                kvitto_lista.append({
                    "namn": produktNamn,
                    "antal": antal,
                    "pris": pris,
                    "totalpris": totalPris
                })
                
                # Skriv ut produktens information
                #print(f"Produkt: {produktNamn}, Antal: {antal}, Pris per styck: {pris} kr, Totalpris: {totalPris:.2f} kr")
             else:
                print("Fel: Produkt-ID finns inte i systemet.")
        
       
        elif Produkt_Antal.upper() == "PAY":
             # Skapa kvitto med datum och spara det
            if kvitto_lista == []:
                 print("Fel: Du måste lägga till minst en produkt innan du kan betala.")
                 continue
            
            else:
              datum = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
              total_summa = sum(item["totalpris"] for item in kvitto_lista)  # Beräkna total summa
            
              kvittonummer += 1  # Öka kvitto nummer med 1
            
              # Bygg kvitto-strängen
              kvitto = f"Kvitto nummer: {kvittonummer:04d}\n"
              kvitto += f"Datum: {datum}\n"
              for item in kvitto_lista:
                 kvitto += (f"{item['namn']} {item['antal']} * {item['pris']:.2f} = {item['totalpris']:.2f} kr\n")
                          
              kvitto += f"Total: {total_summa:.2f} kr"
            
              print(kvitto)  # Skriv ut kvittot i terminalen
            
              # Spara kvitto i fil
              file_kvitto(kvitto)
              break  # Avsluta kundsession
        
            
       

def main():
    while True:
        print("1: Ny kund")
        print("2: Administera produkter")
        print("0: Avsluta")
        menu = input("Välj meny: ")
        menu = int(menu)

        if menu == 1:
            NyKund()
        elif menu == 0:
            print("Program avslutas") 
            break
        else:
            print("Menyval är ej godkänt, försök igen.")

# Starta programmet
main()

""" 
