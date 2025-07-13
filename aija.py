import random

subjects = ["äijät", "leidit", "frendit", "äijä", "vaimo", "kundi", "jätkät", "homiet", "homot",
            "pellet", "dudet", "jäbä", "spede", "dude"]
actions = ["siistii", "hyvä", "helmee", "äijää", "siistii", "asiallist", "kuulii"]
places = ["thaikuis", "briteis", "jenkeis", "indois", "baaris", "balil", "japanis", "malil", "mäkis",
            "pohjoisnaval", "turkis", "olympialaisis", "ausseis", "brasseis", "meksikos", "kanadas", "gobin aavikol",
            "kapkaupungis", "lontoos", "intias", "asuntomessuil", "pakistanis", "etelä-naval", "tiibetis", "kiinas",
            "siperias", "x-gamesis", "ymca:s", "tongal", "tulivuores", "lontoos", "muukalaislegioonas", "vietnamis",
            "etelä-koreas", "luolas", "vankilassa", "fudiksen mm-finaalis", "pohjois-koreas", "viidakos", "hervannas",
            "superbowlissa", "hesburgeris", "lastentarhassa"]
activities = ["surffaa", "skeittaa", "reilaa", "roadtripil", "daivaa", "suunnistaa", "kiipeilee", "ryyppää",
                "parkouraa", "seilaa", "wakeboardaa", "työharjottelus", "kokkaa", "metsästää", "ampumas", "juoksee",
                "bodaamas", "deejiinä", "ratsastaa", "pyöräilee", "töis", "travellaa", "reissaa", "räppää",
                "tappelemas", "kouluttaa", "suihkussa", "punnertaa", "snowboardaa", "maratoonis", "piirtää", "maalaan",
                "paskal", "kusel", "nyrkkeilee", "meditoimas"]
intros = ["tänää meikä kokkaa", "tänää meikäijä kokkaa", "tänää mä väsään", "tänään meikä tekee",
            "tänään meitsi väsää dinneriks", "tänään mä duunaan", "pistän koht tost snadit väännöt"]
dishes = ["äijäwokkii", "viikon marinoitunutta kengurufilettä", "täytettyjä crepejä", "äijäpihvii", "paahdettuu lammast",
            "pakurikääpää", "kanttarellej", "virtahepoo", "koiraa", "aasinpotkaa", "kaviaarii", "miekkakalaa", "torvisienii",
            "jättiläismustekalaa", "hanhenmaksaa", "kobe-pihvii", "kateenkorvaa", "porsaankylkee", "äijäsalaattii",
            "hampurilaisii", "kebabbii", "kissaa", "banaaneita", "falafelii", "kanansiipii", "valaanlihaa", "kenguruu",
            "sammalta", "pizzaa", "perunoit", "gorillaa", "vyötiäistä", "hamstereit", "nokkosii", "apinanaivoja",
            "pässin kiveksii", "merihevost", "etanoit", "merimakkaraa", "muurahaiskarhuu", "haggista", "karitsaa",
            "käärmettä"]
garnishes = ["wasabiemulsiol", "ranskalaisil", "pastal", "korianteril", "hummeril", "mädätettynä", "kanansiivil",
                "riisillä", "ruisleiväl", "keitettynä", "sushil", "käristettynä", "couscousil", "sokerikuorrutuksel",
                "juustol", "virtahevon suolessa", "kermaviilil", "yrttiöljyl", "maustekurkumal", "katkaravuil",
                "friteerattuna", "keittona", "kaviaaril", "höyrytettynä", "muurahaisilla", "paistettuna", "liekitettynä",
                "fazerin sinisellä", "makkaral", "silvottuna", "jugurtil", "vetisenä"]
extras = ["tashimoto-heinää jonka poimin shiribetsu-joen rannalt kun olin reilaa japanis",
            "abessiinialaist kurttuviikunaa jota saan paikalliselt tarhurilt etiopiast",
            "mökin takapihalt poimittuu pitkälehtikihokkii", "sichuanin maakunnast poimittuu sareptaninsinappii",
            "tämmösii tyrnimustikka-risteytysmarjoi joita sain turun yliopiston genetiikan laitoksen äijilt",
            "perus suomalaist japaninpersiljaa jota ny löytyy kaikkien pihast", "neidonhiuspuu-uutet",
            "mustanmeren merilevää", "jauhettuu ruusunjuurta", "dodon höyhenii", "omakasvattamaa ananast",
            "jauhettuu kääpiöponinkavioo", "mustanmerenruusua jotka poimin georgian haikil",
            "kuopas paahdettui maakastanjoit", "frendin luomutilal kasvattamaa mukulakirvelii",
            "makeen kirpeit ananaskirsikoit", "saframii", "tasmanian tuholaisen karvoi", "basilikaa", "sitruunamehuu",
            "jättiläispunapuun ydintä", "jakinmaitorahkaa", "valaanrasvaa", "vaimon kasvattamaa minttuu",
            "jauhettuu ykssarvisen sarvee", "viimesen dinosauruksen suomuja", "murkkujen kusta", "koivun kaarnaa",
            "mes-juustoo pari siivuu"]
verbs = ["tuomaan", "antaan", "lisään"]
descriptions = ["semmost syvyyt siihe", "vähä semmost itämaist twistii siihe", "terävyyttä tähä", "pehmeyttä reunoihi",
                "vähä siihe semmost twistii", "vähä semmost äijämäisyyt sekaa", "makuhermoil vähä lomafiilist",
                "vähä semmost bläästii siihe", "tulista twistii siihe"]
dressings = ["vatikaanist saatuu balsamicoo, terveisii vaa konklaavin äijille :D", "maapähkinä-vinegrettee",
                "timjamis liuotettuu inkiväärii", "tämmöst viskisiirappii", "oliiviöljyä", "sivetindroppingei",
                "orpolapsien kyynelii", "savulohismetanaa", "tummaa rommii", "kolaa", "vladimirin pirtuu", "kossuu",
                "hp-kastiket", "ketsuppii", "poron verta", "meduusan limaa", "sinivalaan verta"]
endings = ["pyöräytä valkokastikkees", "glaseerataan nopee", "pyöräytetää pannul limen kaa", "flambeerataa punkul",
            "paistetaan neljä tuntii", "keitetään etikassa", "suurustetaan", "kuivatetaan"]
final_steps = ["loppuun viel pikku suola", "lopuks viel silaus curacaoo", "lopuks viel pikku pippurit",
                "lopuks heitetään koko paska roskiin", "lopuks viel pienet öljyt", "lopuks viel annetaan paahtua pari tuntii",
                "lopuks viel pikku limet", "lopuks viel pikku chilit", "lopuks viel pienet pyöräytykset",
                "lopuks annetaan jäähtyy pari päivää", "mut alkuun pienet äijätumut", "mut alkuun otetaa pienet paukut",
                "lopuks annetaan hautuu pari minsaa"]

def random_choice(lst):
    return random.choice(lst)

def random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def aija_story():
    t = random_choice(subjects)
    s = random_choice(actions)
    e = random_choice(places)
    n = random_choice(activities)
    u = random_choice(intros)
    k = random_choice(dishes)
    l = random_choice(garnishes)
    o = random_choice(extras)
    r = random_choice(verbs)
    m = random_choice(descriptions)
    
    def append_dressing_or_ending():
        return f'dressingiks {random_choice(dressings)}.' if random_int(1, 100) > 50 else f'ja sit viel {random_choice(endings)} :D'

    def append_final_step():
        return f' {random_choice(final_steps)}.' if random_int(1, 100) > 50 else ''

    is_plural = t.endswith("t")
    
    story = f"moro {t} :D mitä {t}. {s} nähä {'teit' if is_plural else 'sua'} :D {u} {'teil' if is_plural else 'sulle'} {k} {l}. tän reseptin opin kun olin {e} {n} :D pistetää sekaa vähän {o} {r} {m} :D {append_dressing_or_ending()}"
    
    return story

def mega_aija(count):
    t = random_choice(subjects)
    s = random_choice(actions)
    u = random_choice(intros)
    k = random_choice(dishes)
    l = random_choice(garnishes)
    e = random_choice(places)
    n = random_choice(activities)

    def append_dressing_or_ending():
        return f'dressingiks {random_choice(dressings)}.' if random_int(1, 100) > 50 else f'ja sit viel {random_choice(endings)} :D'

    def append_final_step():
        return f' {random_choice(final_steps)}.' if random_int(1, 100) > 50 else ''
    
    is_plural = t.endswith("t")
    story = f"moro {t} :D mitä {t}. {s} nähä {'teit' if is_plural else 'sua'} :D {u} {'teil' if is_plural else 'sulle'} {k} {l}. tän reseptin opin kun olin {e} {n} :D"

    for i in range(int(count)):
        t = random_choice(subjects)
        s = random_choice(actions)
        e = random_choice(places)
        n = random_choice(activities)
        u = random_choice(intros)
        k = random_choice(dishes)
        l = random_choice(garnishes)
        o = random_choice(extras)
        r = random_choice(verbs)
        m = random_choice(descriptions)

        substory = f" pistetää sekaa vähän {o} {r} {m} :D {append_dressing_or_ending()} ja"
        story += substory
    
    story +=  f" {append_final_step()} nonii toivottavasti maistuu. mä rakastan {'teit' if is_plural else 'sua'} {t} :D"
    return story

def aija_spurdo():
    return aija_story().replace('t', 'd').replace('c', 'g').replace('k', 'g').replace('p', 'b').replace('x', 'gs').replace('z', 'ds')

# Example usage:
if __name__ == "__main__":
    print(aija_story())
    print(aija_spurdo())