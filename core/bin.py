"""
def check_name(n, l):
    return n.strip() in l


replace_elements = ["|", ";", ":", "/", "(", ")", "-", "–"]


def rep_com(element):
    for el in replace_elements:
        element = element.replace(el, ",")
    return element


names_skip = [
    "Tania",
    "Jorge",
    "Armando",
    "Pedro",
    "Carlosempregado",
    "JosePintoirmão",
    "Noémia",
    "Joaquim",
    "Joel",
    "Ricardo",
    "nan",
    "paulocsa@sapo.pt",
    "Luísa",
    "João",
    "marido",
]
for contact in df:
    telephones = rep_com(str(contact)).split(",")
    print(telephones)
    for t in telephones:
        t = t.replace(" ", "")
        print(t)
        if any(check_name(n, t) for n in names_skip) or not t:
            continue
        print(int(t))
"""
