from datetime import datetime  # datum
import os


#klass för att hantera produkter
class Product:
    def __init__(self, produktid, namn, pris, pristyp):
        self.produktid= produktid
        self.namn = namn
        self.pris = pris
        self.pristyp = pristyp




# Filnamn för att spara kvitton och kvittonummer

kvittonummer_fil='kvittoNummer.txt' #sparar alla kvittonummer

#spara info om kvittot
def filekvitto(kvitto):
    """sparar kvittot i fil"""
    Kvitto_fil = f"RECEIPT__{datetime.now().strftime('%Y-%m-%d')}.txt"  # Filnamn för dagens kvitto
    with open(Kvitto_fil, "a", encoding="utf-8") as file:  # encoding="utf-8" för svenska tecken
        file.write(kvitto + "\n----------------------------------------------------\n")  # Spara kvitto med en ny rad
    print("Kvitto skapad")
        
            
#Läsa in filen med produkter
def loadItems(file_name):
    """Hämtar produkter från filen"""
    produkter={} #lägg alla varorna i produkt filen i en dicctonary
    file = open(file_name, 'r', encoding='utf-8')
    
    #går genom hela strängen i loop, tar bort mellan slag och annat oönskat, sedan delar in strängen i enskilda ord.
    for line in file:
        rader = line.strip().split(",") 
        
    #varje rad måste ha produktid, namn, pris, pristyp
        if len(rader) == 4:
         produktid=int(rader[0])
         namn=rader[1]
         pris=float(rader[2])
         pristyp=rader[3]
        
         produkter[produktid]=Product(produktid,namn,pris,pristyp) #lägger in produkter som har läst från filen i dictonary produkter.
        else:
         print(f"Fel: icke godkänt format i raden: {rader}")
         
        
    file.close() #stänger filen
  
    return produkter #retunerar produkt dictonary

def fileKvittoNummer(kvittonummer):
    """Sparar det senaste kvittonumret till en fil."""
    #skriver över det gamla kvitto nummer med det senaste
    file=open(kvittonummer_fil, 'w', encoding='utf-8') 
    file.write(str(f"{kvittonummer:04d}"))
        
def loadKvittonummer():
    """Läser det senaste kvittonumret från en fil."""
    if os.path.exists(kvittonummer_fil):  # Kontrollera om filen finns
        kvittonummer_file=open(kvittonummer_fil, "r", encoding='utf-8')
        kvitto_nummer= kvittonummer_file.read().strip() #tar bort oönskad karatäer och mellan slag
        kvittonummer_file.close() #stänger filen efter man har läst klart
        
        # Kontrollera om kvitto_nummer är ett heltal
        if kvitto_nummer.isdigit():  
                return int(kvitto_nummer)  # Konverterar till int och returnerar
        else:
            print("Fel format i kvittonummer")
            return 0
    else: 
        print("Filen finns inte")
        return 0 #retunerar 0 som kvittonummer för att de sedan ska sparas i kvitto filen
       
    

def Nyttköp(produkter,kvittonummer):
    """Lägger till produkter i kvitto """
    
    kvitto_lista = []  # Lista för att hålla produkter som kunden köper
    print("Skriv in produktens id och antal i formatet: <produktid> <antal>")
    print("Skriv 'PAY' för att gå vidare till betalning.")
    
    while True:  
        Produkt_Antal = input("ProduktId och Antal: ")
            
        if Produkt_Antal.upper() != "PAY": #om användaren inte har skrivit in PAY, fortsätt med att sätta in produkter
            # Dela upp inmatningen där det finns mellanslag
            data = Produkt_Antal.split()
            
            #kollar att användaren verkligen har lagt in två värden som har ett mellan slag
            if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
             
                produktid = int(data[0])
                antal = float(data[1])
            
            # Kontrollera om produktid finns i listan över produkter
                if produktid in produkter:
                   produktNamn = produkter[produktid].namn
                   pris = produkter[produktid].pris
                   pristyp = produkter[produktid].pristyp  
                  
                  # Beräkna totalpris för produkten, en produkt i taget
                   totalPris = pris * antal
                
                  # Lägg till produktinformation i kvitto-listan
                   kvitto_lista.append({
                    "namn": produktNamn,
                    "antal": antal,
                    "pris": pris,
                    "pristyp":pristyp,
                    "totalpris": totalPris
                   })
                
               #produkt finns ej i produkt filen
                else:
                   print("Produkten finns ej i listan, testa igen")
            else:
                print("Fel:Du måste mata in både produkt-ID och antal. Testa igen.")
                continue 
       
        elif Produkt_Antal.upper() == "PAY":
               # Skapa kvitto med datum och spara det
             
             if kvitto_lista == []: #kan ej spara ett tomt kvitto, kollar detta genom att kolla om kvitto listan är tom
                 print("Fel: Du måste lägga till minst en produkt innan du kan betala.")
                 continue
            
             else:
                  #lägger dagens datum och tid på toppen av kvittot
                  datum = datetime.now().strftime("%d-%m-%Y %H:%M:%S") 
                  # Beräkna total summa
                  total_summa = sum(item["totalpris"] for item in kvitto_lista)  
            
                  kvittonummer += 1  # Öka kvitto nummer med 1
             
            
                  # Bygg kvitto-strängen
                  kvitto = f"Kvitto nummer: {kvittonummer:04d}\n"
                  kvitto += f"Datum: {datum}\n"
                  for item in kvitto_lista:
                    kvitto += (f"{item['namn']} ({item['pristyp']}) {item['antal']} * {item['pris']:.2f} = {item['totalpris']:.2f} kr\n")
                          
                  kvitto += f"Total: {total_summa:.2f} kr"
            
                  print(kvitto)  # Skriv ut kvittot i terminalen
              
                  
                  filekvitto(kvitto) # Spara kvitto i fil
                  fileKvittoNummer(kvittonummer) #spara kvittonummer
                  break  # Avsluta
       
        
            
       

def main():    
    produkter= loadItems('produkter.txt')  # Ladda produkter från fil
    
    while True:
        kvittonummer=loadKvittonummer() #hämtar kvittonummer
        print("1: Ny kund")
        print("0: Avsluta")
        meny = input("Välj meny: ")
        
        if meny.isdigit() and int(meny) in [0, 1]: #meny ska vara tal. 1 eller 0
            meny = int(meny)
     
            if meny == 1:
               Nyttköp(produkter,kvittonummer)
            elif meny == 0:
              print("Program avslutas") 
              break
        else:
            print("Menyval är ej godkänt, försök igen.")
       

# Starta programmet
main()
