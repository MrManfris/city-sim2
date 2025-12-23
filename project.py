import random
from collections import Counter
import os

income = 0

class City:
    def __init__(self):
        self.diena = 1
        self.populiacija = 10
        self.pinigai = 100
        self.tarša = 0
        self.buildings = []
        self.kataklizmas = 0
        self.happy = 100
        self.type = "normal"

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

city = City()


def build(city, building_type):

    prices = {
        "house": 50,
        "factory": 100,
        "kat_malsintojas": 200,
        "Ekologiški namai": 75,
        "Vėjo jėgainės": 50,
        "Viesbutis": 150
    }

    if building_type not in prices:
        print("Tokio pastato nėra.")
        return

    price = prices[building_type]

    if skills["pastatu_kainos_I"]["atrakinta"] == True:
        price = int(price * 0.9)
    if skills["pastatu_kainos_II"]["atrakinta"] == True:
        price = int(price * 0.65)

    if city["pinigai"] < price:
        print("Neužtenka pinigų.")
        return

    city["pinigai"] -= price

    bonus_happy = 0
    if skills["happy_I"]["atrakinta"] == True:
        bonus_happy += 5
    if skills["happy_II"]["atrakinta"] == True:
        bonus_happy += 8

    if city.type == "atlantida":
        names_map = {
            "house": "Poseidono namas",
            "factory": "Trišakių darykla",
            "Ekologiški namai": "Mėlynieji kupolai",
            "Vėjo jėgainės": "Aero kolonos",
            "Viesbutis": "Poseidono vila",
            "kat_malsintojas": "Elementų malšintojas"
        }
    elif city.type == "yharnam":
        names_map = {
            "house": "Išgyventojų namas",
            "factory": "Saw cleaverių darykla",
            "Ekologiški namai": "Katedra",
            "Vėjo jėgainės": "Medžiotojo Vėjo stulpai",
            "Viesbutis": "Raudonojo Mėnulio Užeiga",
            "kat_malsintojas": "Medžioklinės nakties vengykla"
        }
    else:
        
        names_map = {
            "house": "Namas",
            "factory": "Fabrikas",
            "Ekologiški namai": "Ekologiškas namas",
            "Vėjo jėgainės": "Vėjo jėgainė",
            "Viesbutis": "Viešbutis",
            "kat_malsintojas": "Kataklizmų malšintojas"
        }

 
    if building_type == "house":
        city["populiacija"] += 5
        city["happy"] = min(100, city["happy"] + 5 + bonus_happy)

    elif building_type == "factory":
        city["tarša"] += 20
        city["happy"] -= 10
        city["kataklizmas"] += 25
        if skills["anti_kat_fabrikai_I"]["atrakinta"] == True:
            city["kataklizmas"] -= 10
        if skills["anti_kat_fabrikai_II"]["atrakinta"] == True:
            city["kataklizmas"] -= 15
        city["kataklizmas"] = max(0, city["kataklizmas"])

    elif building_type == "kat_malsintojas":
        city["tarša"] += 9
        city["kataklizmas"] = max(0, city["kataklizmas"] - 25)

    elif building_type == "Ekologiški namai":
        city["populiacija"] += 15
        city["tarša"] -= 10
        city["happy"] = min(100, city["happy"] + 10 + bonus_happy)

    elif building_type == "Vėjo jėgainės":
        city["tarša"] -= 5
        city["happy"] = min(100, city["happy"] + 8 + bonus_happy)

    elif building_type == "Viesbutis":
        city["tarša"] += 5
        city["happy"] -= 3

   
    city["buildings"].append(names_map[building_type])
    print(f"Pastatytas {names_map[building_type]} už {price}")
    input("Paspausk ENTER, kad tęsti...")
def kita_diena(city):
    global income
    income = 0
    fabrikai = ["fabrikas", "trišakių darykla", "saw cleaverių darykla"]


    for b in city["buildings"]:
        if b.lower() in fabrikai:
            if city["happy"] > 40:
                income += 10
            else:
                print(f"Fabrikas {b} streikuoja! Pajamų iš jo nebėra!")

   
    income += city["populiacija"]

  
    bonus_happy = 0
    if skills["happy_I"]["atrakinta"]:
        bonus_happy += 5
    if skills["happy_II"]["atrakinta"]:
        bonus_happy += 8

   
    effective_happy = min(100, city["happy"] + bonus_happy)

    if effective_happy < 25:
        loss = min(50, income)
        income -= loss
        print("Gyventojai beproto nelaimingi! Pajamos sumažėjo {}".format(loss))
    elif effective_happy < 50:
        loss = min(10, income)
        income -= loss
        print("Gyventojai labai nelaimingi! Pajamos sumažėjo {}".format(loss))
    elif effective_happy < 75:
        loss = min(5, income)
        income -= loss
        print("Gyventojai nelaimingi! Pajamos sumažėjo {}".format(loss))


   
    income = max(0, income)

   
    city["pinigai"] += income
    city["diena"] += 1

    print(f"Pajamos : {income}")

    emigracija = 0
    if city["diena"] % 5 == 0:
        if city["happy"] < 25:
            emigracija = min(20, city["populiacija"])
        elif city["happy"] < 40:
            emigracija = min(6, city["populiacija"])
        elif city["happy"] < 65:
            emigracija = min(2, city["populiacija"])
        if emigracija > 0:
            city["populiacija"] -= emigracija
            print(f"Dėl mažo džiaugsmo iš miesto emigravo {emigracija} gyventojų. Liko gyventojų: {city['populiacija']}")

   
    reduction = 0
    if "Vėjo jėgainės" in city["buildings"]:
        reduction += 10 
    if skills["ekologija_I"]["atrakinta"] == True:
        reduction += 10
    if skills["ekologija_II"]["atrakinta"] == True:
        reduction += 19
    city["tarša"] -= reduction
    if city["tarša"] < 0:
        city["tarša"] = 0

    
    if "Ekologiški namai" in city["buildings"]:
        city["tarša"] -= 10
    if skills["ekologija_I"]["atrakinta"] == True:
        reduction += 10
    if skills["ekologija_II"]["atrakinta"] == True:
        reduction += 19
    city["tarša"] -= reduction
    if city["tarša"] < 0:
        city["tarša"] = 0
        
def check_kataklizmas(city):
    if city["kataklizmas"] <= 0:
        return

    roll = random.randint(1, 100)
    if roll <= city["kataklizmas"] and city["buildings"]:
        lost = random.choice(city["buildings"])
        city["buildings"].remove(lost)
        city["populiacija"] = max(0, city["populiacija"] - 10)
        city["kataklizmas"] = 0
        print(f"KATAKLIZMAS! Sugriautas {lost}")

def show_city(city):
    global counts
    os.system("cls" if os.name == "nt" else "clear")
    print(f"--- DIENA {city['diena']} ---")
    print("Gyventojai:", city["populiacija"])
    print("Džiaugsmo lygis:", city["happy"])
    print("Pinigai:", city["pinigai"])
    print("Tarša:", city["tarša"])
    counts = Counter(city["buildings"])
    pastatai = ", ".join(f"{b} x{c}" for b, c in counts.items()) if counts else "Nėra"
    print("Pastatai:", pastatai)
    print(kita_diena(city))
    print(f"Kataklizmo šansas: {city["kataklizmas"]}")


skills = {
    "pastatu_kainos_I": {"kaina": 200, "atrakinta": False, "reikia": None},
    "pastatu_kainos_II": {"kaina": 600, "atrakinta": False, "reikia": "Pastatu_kainos_I"},
    "ekologija_I": {"kaina": 100, "atrakinta": False, "reikia": None},
    "ekologija_II": {"kaina": 350, "atrakinta": False, "reikia": "ekologija_I"},
    "anti_kat_fabrikai_I": {"kaina": 200, "atrakinta": False, "reikia": None},
    "anti_kat_fabrikai_II": {"kaina": 500, "atrakinta": False, "reikia": "anti_kat_fabrikai_I"},
    "happy_I": {"kaina" : 300, "atrakinta": False, "reikia": None},
    "happy_II": {"kaina" : 850, "atrakinta": False, "reikia": "happy_I"}
}

def skilu_pirkimas(city, skills):
    skill = input("Įvesk skill pavadinimą: ")
    if skill not in skills:
        print("Tokio skill nėra")
        return
    s = skills[skill]
    if s["atrakinta"]:
        print("Jau toki skill turite")
        return
    if s["reikia"] and not skills[s["reikia"]]["atrakinta"]:
        print(f"Reikia šito {s['reikia']}, kad atrakinti šį skill.")
        return
    if city["pinigai"] < s["kaina"]:
        print("Neužtenka pinigų")
        return
    city["pinigai"] -= s["kaina"]
    s["atrakinta"] = True
    print(f"Nusipirkote šį, {skill}")
    input("Paspausk ENTER, kad tęsti...")
def secret_ending(city):
    os.system("cls")  
    print("\n*** Paslaptingas miestas (Atlantida)! ***")
    print("\nTau pasirinkus 993 aplink tavo namą atsirado vandens ratąs ir tave su tavo namu Poseidono ranka įtraukė į rato gilumas.\nTu trenkeis galva į lubas, kai tave traukė į gilumas.\nAtsikėlęs pamatei, kad tu Poseidono rūbuose ir priešais tave matosi įspūdingo grožio paslaptingas miestas!\n Ir tu supratai...Tai Atlantida!\n Miestas apie kurį pasakojimos legendos ir dabar jis tavo rankuose.")
    city["populiacija"] = 50
    city["pinigai"] = 500
    city["tarša"] = 0
    city["happy"] = 100
    city["buildings"] = []
    city["kataklizmas"] = 0
    city["diena"] = 1
    print("Tavo nuotykis tęsiasi...\n")
    city.type = "atlantida"

def secret_ending_2(city):
    os.system("cls")  
    print("\n*** Yharnam (secret ending 2)! ***")
    print("\nKai pasirinki 994 tau, net nespėjus suprasti, kas vyksta tave paguldo ant stalo ir su švirkštu į veną įpila Old Blood ir tu prarandi sąmonę.\n Atsikėlei jau Yharname mieste kur vyksta medžioklinė naktis, bet dabar medžioklinė naktis neprasidės ir tu supranti, kad Yharnamas tavo rankuose ir iki medžioklinės nakties tu juo vaduovauji, o, kai prasidės...")
    city["populiacija"] = 30
    city["populiacija"] = 30
    city["pinigai"] = 800
    city["tarša"] = 45
    city["happy"] = 80
    city["buildings"] = []
    city["kataklizmas"] = 0
    city["diena"] = 1
    city.type = "yharnam"
    print("Tavo nuotykis tęsiasi, kol kas...\n")
while True:

    show_city(city)
    if city.type == "atlantida":
        print("\nVeiksmai:")
        print("1 - Statyti Poseidono namą (50)")
        print("2 - Statyti Trišakių daryklą (100)")
        print("4 - Statyti Kristalinius bokštus (75)")
        print("5 - Statyti Aero kolonas (50)")
        print("6 - Statyti Poseidono vilą (150)")
        print("7 - Statyti elementų malšintoją(200)")
        print("\nSkill tree")
        print("8 - Pastatu kainos I (200) Mažina pastatų kainas ant 10%")
        print("9 - Pastatu kainos II (600) Reikia turėti Pastatu kainos I. Mažina pastatų kainas ant 35% ")
        print("10 - ekologija I (100) Mažina fabriku išleidžiama taršą ant 10")
        print("11 - ekologija II (350) Reikia turėti ekologija I.  Mažina fabriku išleidžiama taršą ant 19")
        print("12 - anti kataklizminiai fabrikai I (200) Mažina kataklizmo šansa ant 10 (veikia tik su fabrikais)9")
        print("13 - anti kataklizminiai fabrikai II (500) Reikia turėti anti kataklizminiai fabrikai I.  Mažina kataklizmo šansa ant 15 (veikia tik su fabrikais)9")
        print("14 - happy I (300)  Didina gaunama gyventojų džiaugsmą ant 5 (veikia tik su namu, eko namy ir vėjo jėgainėmis)")
        print("15 - happy II (850) Reikia turėti happy I.  Didina gaunama gyventojų džiaugsmą ant 8 (veikia tik su namu, eko namu ir vėjo jėgainėmis)3")   
        print("0 - Išeiti")
        print("Paspauskite ENTER, kad patekti į kitą dieną.")
        print("Kai perkate skill ir jums rašo įrašykite skill pavadinimą  rašykite taip: Pastatu_kainos_II\n")
    elif city.type == "yharnam":
        print("\nVeiksmai:")
        print("1 - Statyti Išgyventojų namą (50)")
        print("2 - Statyti Saw cleaverių daryklą (100)")
        print("4 - Statyti Katedras (75)")
        print("5 - Statyti Medžiotojo Vėjo Stulpai (50)")
        print("6 - Statyti Raudonojo Mėnulio Užeiga (150)")
        print("7 - Statyti medžioklinės nakties vengyklą(200)")
        print("\nSkill tree")
        print("8 - Pastatu kainos I (200) Mažina pastatų kainas ant 10%")
        print("9 - Pastatu kainos II (600) Reikia turėti Pastatu kainos I. Mažina pastatų kainas ant 35% ")
        print("10 - ekologija I (100) Mažina fabriku išleidžiama taršą ant 10")
        print("11 - ekologija II (350) Reikia turėti ekologija I.  Mažina fabriku išleidžiama taršą ant 19")
        print("12 - anti kataklizminiai fabrikai I (200) Mažina kataklizmo šansa ant 10 (veikia tik su fabrikais)9")
        print("13 - anti kataklizminiai fabrikai II (500) Reikia turėti anti kataklizminiai fabrikai I.  Mažina kataklizmo šansa ant 15 (veikia tik su fabrikais)9")
        print("14 - happy I (300)  Didina gaunama gyventojų džiaugsmą ant 5 (veikia tik su namu, eko namy ir vėjo jėgainėmis)")
        print("15 - happy II (850) Reikia turėti happy I.  Didina gaunama gyventojų džiaugsmą ant 8 (veikia tik su namu, eko namu ir vėjo jėgainėmis)3")   
        print("0 - Išeiti")
        print("Paspauskite ENTER, kad patekti į kitą dieną.")
        print("Kai perkate skill ir jums rašo įrašykite skill pavadinimą  rašykite taip: Pastatu_kainos_II\n")
    else:
        print("\nVeiksmai:")
        print("1 - Statyti namą (50)")
        print("2 - Statyti fabriką (100)")
        print("4 - Statyti ekologišką namą(75)")
        print("5 - Statyti vėjo jėgaines(50)")
        print("6 - Statyti viesbutį(150)")
        print("7 - Statyti kataklizmų malšintoją(200)")
        print("\nSkill tree")
        print("8 - pastatu kainos I (200) Mažina pastatų kainas ant 10%")
        print("9 - pastatu kainos II (600) Reikia turėti Pastatu kainos I. Mažina pastatų kainas ant 35% ")
        print("10 - ekologija I (100) Mažina fabriku išleidžiama taršą ant 10")
        print("11 - ekologija II (350) Reikia turėti ekologija I.  Mažina fabriku išleidžiama taršą ant 19")
        print("12 - anti kataklizminiai fabrikai I (200) Mažina kataklizmo šansa ant 10 (veikia tik su fabrikais)9")
        print("13 - anti kataklizminiai fabrikai II (500) Reikia turėti anti kataklizminiai fabrikai I.  Mažina kataklizmo šansa ant 15 (veikia tik su fabrikais)9")
        print("14 - happy I (300)  Didina gaunama gyventojų džiaugsmą ant 5 (veikia tik su namu, eko namy ir vėjo jėgainėmis)")
        print("15 - happy II (850) Reikia turėti happy I.  Didina gaunama gyventojų džiaugsmą ant 8 (veikia tik su namu, eko namu ir vėjo jėgainėmis)3")   
        print("0 - Išeiti")
        print("Paspauskite ENTER, kad patekti į kitą dieną.")
        print("Kai perkate skill ir jums rašo įrašykite skill pavadinimą  rašykite taip: Pastatu_kainos_II\n")

    choice = input("Pasirink: ")

    if choice == "1":
        build(city, "house")

    elif choice == "2":
        build(city, "factory")

    elif choice == "993":
        secret_ending(city)
        city.type = "atlantida"
        input("Paspausk ENTER, kad tęsti žaidimą Atlantidoje")
    
    elif choice == "4":
        build(city, "Ekologiški namai")
    elif choice == "5":
        build(city, "Vėjo jėgainės")
    elif choice == "6":
        build(city, "Viesbutis")
    elif choice == "7":
        build(city,"kat_malsintojas")
    elif choice in ["8", "9", "10","11","12","13", "14", "15"]:
        skilu_pirkimas(city,skills)
    elif choice == "994":
        secret_ending_2(city)
        city.type = "yharnam"
        input("Paspausk ENTER, kad tęsti žaidimą Yharname")
    elif choice == "0":
        print("Ačiū, kad žaidėte!")
        break

    if city["tarša"] >= 100:
        print(f"\n Jūsų miesto taršos lygis pakilo taip stipriai, kad miesto išlaikyti nebeįmanoma.\n Išlaikėtė miestą {city["diena"]} dienų.\n Turėjote {city["pinigai"]} pinigų.\n Gyventojų džiaugsmo lygis buvo {city["happy"]}.\n Jūsų miesto gyventojų pajamos: {income}.\n Štai kokius pastatus turėjote: {counts}.\n Ačiū, kad žaidėte!")
        break
    if city["populiacija"] <= 0:
        print(f"\nJūs neišlaikėtė savo miesto.\n Išlaikėtė miestą {city["diena"]} dienų.\n Turėjote {city["pinigai"]} pinigų.Gyventojų džiaugsmo lygis buvo {city["happy"]}\n Jūsų miesto gyventojų pajamos: {income}.\n Štai kokius pastatus turėjote: {counts}.\n Ačiū, kad žaidėte!")
        break
    if city["happy"] <= 0:
        print(f"\nGyventojai nekenčia šio miesto ir emigravo į kitus miestus .\n Išlaikėtė miestą {city["diena"]} dienų.\n Turėjote {city["pinigai"]} pinigų.\n Jūsų miesto gyventojų pajamos: {income}.\n Štai kokius pastatus turėjote: {counts}.\n Ačiū, kad žaidėte!")
        break
    if city["pinigai"] >= 100000:
        print(f"Jūsų miestas augo ir vis dar auga ir atneša didelius pinigus! Jums pavyko išlaikyti miestą ir padaryti jį vienu iš geriausiu miestu pasaulyje! Iki miesto išlaikėte miestą {city["diena"]} dienų.\n Turėjote {city["pinigai"]} pinigų.Gyventojų džiaugsmo lygis buvo {city["happy"]}\n Jūsų miesto gyventojų pajamos: {income}.\n Štai kokius pastatus turėjote: {counts}.\n Ačiū, kad žaidėte!")
        break