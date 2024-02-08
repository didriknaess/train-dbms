# **README**
## ER-diagram
Vedlagt ligger ER-modellen vi har benyttet til å modellere informasjonen gitt av oppgaveteksten. Denne rent teknisk en Enhanced ER-model (EER), men vi kommer til å gjennomgående referere til den som en ER-modell. Vi har benyttet sentrale konsepter fra pensum som total, disjunkt spesialisering, svake entitetsklasser, avledede attributter, binære og trinære relasjonsklasser samt ordinære entitetsklasser. En viktig merknad er de fargede relasjonsklassene, markert for å tydeliggjøre krysningen med andre relasjonsklasser. Videre ønsker vi å understreke at vi etter beste evne har forsøkt å være konsise med modelleringen. Avledede attributter har vi i kontrast til vanlige attributter modellert med stiplede ellipser for å understreke forskjellen. Klasser merkes i teksten med fet skrift og PascalCase. 

ER-modellen utarbeidet fra oppgaveteksten: (https://www.figma.com/file/BcUaKSy33XOy3WCo6Q6cCt/Databaser-EER-diagram?node-id=0%3A1&t=snn3xOBEKCvbYp5Y-1)

## **Antakelser og forutsetninger**
I denne delen skal vi gjøre rede for antagelser og forutsetninger som er gjort i sammenheng med ER-diagrammet. Dette er altså vår tolkning og anvendelse av informasjonen gitt i oppgaveteksten. For å gjøre det så oversiktlig som mulig, har vi delt ER-diagrammet inn i ulike deler: vogn-, strekning-, billett-, og togrute-delene. Grunnet sammenhenger i form av relasjoner mellom delene, vil det naturligvis foreligge overlapp. 

## Vogn-delen av diagrammet
Vogn-entiteten representerer fysiske, eksisterende vogner. Vi har ingen støtte for teoretiske vogntyper, da vi antar at dette ikke er ønskelig i modellen. Vi antar at en operatør kan eie enkeltvogner, og har derfor muliggjort dette ved relasjonen VognEiesAv. En Operatør må videre eie minst én Vogn. Dette mener vi er en forutsetning for at en Operatør skal lagres i databasen. Følgelig kan en Vogn kun eies av én Operatør. Navnet til en Operatør antar vi er unikt, slik vanlig praksis er for foretak. 
I entiteten Vognoppsett sin relasjon til Vogn er det gjort antagelsen at et spesifikt Vognoppsett er satt sammen av en mengde fysiske, eksisterende Vogn-er. Det finnes altså i vår modell ikke noen støtte for teoretiske vognoppsett. Oppgaveteksten spesifiserer at et Vognoppsett skal være “satt sammen av togvogner av tilgjengelige vogntyper”. Dette tolket vi som om at en Operatør altså kan danne Vognoppsett bestående av egeneide, tilgjengelige, fysiske Vogn-er. Et Vognoppsett antar vi må bestå av minst én Vogn, og at de ulike Vogn-ene kan være med i null (f. eks når de er på lager) og til flere Vognoppsett (dersom de benyttes flere ganger på en dag). Vi antar videre at en Operatør kun lagrer Vognoppsett som har blitt benyttet eller benyttes med en tilknyttet Togrute. Dette er modellert i RuteOppsett-relasjonen. 
Oppgaveteksten spesifiserer at “Setene er nummerert fra forenden av vogna og fra venstre mot høyre”, og lignende med Soveplass-er og SoveKupé-er. I modellen vår er det derfor gjort antagelsen at nummereringene starter fra 1 i hver enkelt Vogn. Disse objektene er derfor modellert som svake entitetsklasser. 
I oppgaveteksten kommer det frem at “En sovevogn med fire sovekupéer vil ha soveplasser fra nummer en til nummer åtte”. Derfor antar vi at en SoveKupé må ha to Soveplasser.

## Billett-delen av diagrammet
Fra oppgaveteksten har vi både at “En billett gjelder enten et sete i en sittevogn eller en seng i en sovevogn” og “For å reise med en togrute kjøper en kunde billett til en eller flere plasser i en togruteforekomst”. Basert på denne tvetydigheten, landet vi på antagelsen om at en Billett ikke kan tilhøre mer enn én Soveplass eller ett Sete. 
Vi antar at det i databasen lagres både brukte og aktive Billett-er. Derfor har Sete, Soveplass og SoveKupé kardinalitet (0, n). De trenger altså ikke ha tilhørende Billett-er dersom de står på lager, og de kan ha mange tilhørende dersom den spesifikke entiteten har deltatt i flere billettsalg.
Siden man som Kunde må være registrert i Operatør-enes felles kunderegister, antar vi at det ikke er nødvendig med en relasjon mellom Operatør- og Kunde-entitetsklassene.
Vi antar i relasjonen TilknyttetRute at en Ruteforekomst kan ha null Billett-er kjøpt. Videre antar vi at en Billett kan eksistere uten å ha blitt kjøpt, og at en Billett kun kan tilhøre én RuteForekomst, og følgelig én Banestrekning. 

## Strekning-delen av diagrammet
Vi antar at Banestrekning-er ikke kan overlappe, og følgelig at Delstrekning-er derfor kun kan tilhøre én Banestrekning. Denne antagelsen baseres på oversikten over Norges jernbanenett, publisert av Bane NOR (Bane NOR, 2022), som vi har valgt å følge i vår miniverden. En Banestrekning må videre ha minst én Delstrekning, men kan også ha flere. Fra oppgaveteksten har vi at “En delstrekning går mellom to jernbanestasjoner”. Her antar vi at de gjeldende to [jernbane]Stasjon-ene er de eneste på strekningen, og følgelig at Delstrekning-er ikke kan overlappe. 
Vi antar at kun [jernbane]Stasjon-er som er aktive lagres i databasen. Derfor må det være tilknyttet minst én Delstrekning. Dette vil være for Stasjoner som befinner seg i enden av en Banestrekning som ikke bygger videre med andre Banestrekninger. Videre vil det for en Stasjon være mulig å befinne seg i skjæringspunktet mellom flere Banestrekning-er (f. eks i Oslo). Dermed vil det for en Stasjon være mulig å ha en relasjon til flere Delstrekning-er. 

## Rute-delen av diagrammet
Oppgaveteksten spesifiserer at “En togrute har en togruteforekomst for hver dag som togruten kjøres”. Med dette antar vi at de mener datoer. Grunnet dette finnes det i vår modell både Togrute og RuteForekomst som entitetsklasser. Togrute må være tilknyttet minst én RuteForekomst, og kan være tilknyttet mange. Vi antar her at Togrute spesifiserer er en spesiell rute med rutetider hentet fra Togrutetabell. RuteForekomst er spesifikk for hver av de ulike datoene denne Togrute-n kjøres, og er av den grunn markert som en svak entitetsklasse med identifiserende nøkkel ‘dato’.
Vi antar at en Togrute ikke går over flere Banestrekning-er, hvilket forklarer kardinalitet (1,1). I TogruteTabell antar vi at et tog sitt opphold på en Stasjon er såpass kort at tid for avgang og ankomst kan abstraheres til ett enkelt tidspunkt-attributt. 
Restriksjoner som ikke dekkes av ER-modellen
Slik modellen er nå vil antall Sete-r ikke kunne sjekkes for gyldighet når instansene av Vogn-er opprettes. Med dette mener vi at dersom en Vogn har en gitt radstørrelse, så vil det ikke være mulig å sørge for at Vogn-ene har et antall som tilsvarer radstørrelse * n, der n er antall rader. Dette må sjekkes med logikk i programmet. 
Det er ikke mulig å spesifisere at det må være dobbelt så mange SoveKupé-er som Soveplass-er i en Sovevogn bare ved hjelp av kardinalitetene. Dette er en restriksjon som avhenger av sammenhengen mellom SoveKupé og Sengeplass. Videre kan modellen vår ikke garantere at Soveplass-ene og SoveKupé-ene som tilhører hverandre, befinner seg på samme Vogn. Dette håndteres med mappingen i SQL.
Slik modellen er nå, kan man ikke spesifisere at flere Billett-er på en KundeOrdre gjelder Billett-er på ett og samme tog. Dette dekkes delvis av relasjonen tilknyttet RuteForekomst, men ikke nok til å garantere riktig håndtering. Dette må dekkes i et applikasjonsprogram. 
En Billett har to Stasjon-er tilknyttet seg: endeStasjon og startStasjon (herunder brukes mappingverdiene til deres primærnøkler). ER-modellen alene kan ikke sørge for at disse Stasjon-ene er på samme Togrute, og følgelig samme Banestrekning. Dette må sjekkes av et applikasjonsprogram. 

# **Mapping**
Dersom et attributt er en del av en supernøkkel (altså et nøkkelattributt) er det implisitt gitt at denne verdien ikke kan være NULL, og dette vil derfor ikke begrunnes under. 
Dersom en relasjon er representert som en egen tabell er utgangspunktet at de tilknyttede entitetene som fremmednøklene refererer til ikke nødvendigvis må inkluderes i relasjonen, unntak (restriksjoner) vil nevnes som fotnoter. 
Merk at ER-modellen inneholder spesialtegn som f.eks. ‘ø’ og ‘é’, men disse er fjernet (i dette tilfellet erstattet med ‘o’ og ‘e’) i mappingen for å forhindre kompileringsfeil i SQL. Vi var usikre hvordan SQL håndterte UNICODE-tegn og valgte derfor heller å være på den sikre siden.
Null-restriksjon: Nøkkelattributter som er del av primærnøkkel kan aldri være null. Videre kan ikke fremmednøkler være null med mindre nedre kardinalitetsgrense er 0. I vår modell er det kun kundeNr-attributtet i Billett som dette holder for. 
Rekkefølgen på entitetsklassene er i intitaliseringsrekkefølge. Ved f.eks. alfabetisk rekkefølge ville vi fått intitaliseringsfeil, da flere tabeller ville referert med fremmednøkkel til andre tabeller som enda ikke er opprettet. Relasjonsklasser er derimot sortert alfabetisk, da rekkefølge her er vilkårlig ettersom alle entiteter er på plass.

# **Entiteter** 

Operator ( navn ), F = {} - 4NF

Vognoppsett ( vognoppsettID ), F = {} - 4NF

Sittevogn ( vognID, navn, radStorrelse, operatorNavn ), F = {vognID → navn, radStorrelse, operatorNavn} - 4NF
* operatorNavn er fremmednøkkel mot Operator (kan ikke være NULL).

Sovevogn ( vognID, navn, operatorNavn ), F = {vognID → navn, operatorNavn} - 4NF
* operatorNavn er fremmednøkkel mot Operator (kan ikke være NULL). 

Sete ( vognID, seteNr, radNr ), F = {vognID, seteNr → radNr} - 4NF
* vognID er fremmednøkkel mot identifiserende klasse SitteVogn (kan ikke være NULL).

Soveplass ( vognID, sengNr ), F = {} - 4NF
* vognID er fremmednøkkel mot identifiserende klasse SoveVogn.

Sovekupe ( vognID, kupeNr, seng1Nr, seng2Nr ), F = {} - 4NF
* vognID er fremmednøkkel mot identifiserende klasse SoveVogn (kan ikke være NULL), seng1Nr og seng2Nr er fremmednøkler mot de 2 respektive Seng-entitetene som er del av Sovekupe-en (ingen av disse kan være NULL). 

Banestrekning ( banestrekningID, navn, fremdriftsenergi ), F = {banestrekningID → navn, fremdriftsenergi} - 4NF

Togrute ( togruteID, retning, banestrekningID ), F = {togruteID → retning, banestrekningID} - 4NF
* banestrekningID er fremmednøkkel mot Banestrekning (kan ikke være NULL).

RuteForekomst ( togruteID, dato ), F = {} - 4NF
* togruteID er fremmednøkkel mot Togrute (kan ikke være NULL).

Stasjon ( navn, hoydemeter ), F = {navn → hoydemeter} - 4NF

Kunde ( kundeNr, navn, epost, tlfNr ), F = {kundeNr → navn, epost, tlfNr} - 4NF

KundeOrdre ( ordreNr, tidspunktKjopt, kundeNr ), F = {ordreNr → tidspunktKjopt, kundeNr} - 4NF
* kundeNr er fremmednøkkel mot Kunde (kan ikke være NULL).

Billett ( billettID, startStasjon, endeStasjon, ordreNr, togruteID, dato )m, F = {billettID → startStasjon, endeStasjon, togruteID, dato } - 4NF
* startStasjon og endeStasjon er begge nøkler mot 2 ulike Stasjon-er (ingen av disse kan være NULL), ordreNr er fremmednøkkel mot KundeOrdre (kan være NULL), (togruteID, dato) er fremmednøkkel mot RuteForekomst (kan ikke være NULL).

SeteBillett ( billettID, vognID, seteNr ), F = {} - 4NF
* billettID er fremmednøkkel mot superklassen Billett, (vognID, seteNr) er fremmednøkkel mot Sete. 

SengeBillett ( billettID, togruteID, dato ), F = {} - 4NF
* billettID er fremmednøkkel mot superklassen Billett, (togruteID, dato) er fremmednøkkel mot RuteForekomst (ingen av disse verdiene kan være NULL).

TogruteTabell ( tabellID, togruteID ), F = {tabellID → togruteID} - 4NF
* togruteID er fremmednøkkel mot Togrute (kan ikke være NULL), togruteID er alternativ nøkkel.

Delstrekning (endepunkt1Navn, endepunkt2Navn, lengde, sportype, banestrekningID, plassering, retning ), F = { (endepunkt1Navn, endepunkt2Navn) → lengde, sportype, banestrekningID, plasserg, retning } - 4NF
* banestrekningID er fremmednøkkel mot Banestrekning, Stasjon1Navn og Stasjon2Navn er to separate fremmednøkler mot Stasjon (ingen av disse verdiene kan være NULL). 
* her brukes fremmednøklene endepunkt1Navn & endepunkt2Navn som erstatning for delstrekningID (i ER-modell) ettersom det ikke er vanlig praksis å føre fremmednøkler i ER. 

# **Relasjoner** 
KupeReserveres ( togruteID, dato, vognID, kupeNr ), F = {} - 4NF
* (togruteID, dato) er fremmednøkkel mot RuteForekomst, (vognID, kupeNr) er fremmednøkkel mot SoveKupe

RuteOppsett ( togruteID, operatorNavn, vognoppsettID ), F ={togruteID → operatorNavn, vognoppsettID} - 4NF
* togruteID er fremmednøkkel mot Togrute, operatorNavn er fremmednøkkel mot Operator, vognoppsettID er fremmednøkkel mot Vognoppsett. 

SattSammenAv ( vognoppsettID, vognID, plassering ), F = {vognoppsettID, vognID → plassering} - 4NF
* vognoppsettID er fremmednøkkel mot Vognoppsett, vognID er fremmednøkkel mot Vogn, som er superklassen til Sovevogn og Sittevogn i ER-modellen. Bruker superklassen her for å slippe å forklare to ulike tabeller med identisk funksjon. 

TilknyttetSeng ( billettID, vognID, kupeNr, sengNr ), F ={billettID → vognID, kupeNr, sengNr} - 4NF
* billettID er fremmednøkkel mot Billett, (vognID, kupeNr) er fremmednøkkel mot SoveKupe, (vognID, sengNr) er fremmednøkkel mot Soveplass.

TogruteGarInnom ( stasjonNavn, tabellID, tidspunkt ), F = {navn, tabellID → tidspunkt} - 4NF
* stasjonNavn er fremmednøkkel mot Stasjon, tabellID er fremmednøkkel mot TogruteTabell.

# **Forklaring av normalformer**
Høy normalform i datamodellering fører til mindre redundans, færre dataanomalier og mer konsistent datalagring. Denne databasemodellen vil inneholde hyppig endring av tilstand, spesielt med tanke på våre antagelser rundt Vogn og hyppigheten rundt daglig Billett-salg, vil sterk normalisering være en styrke. Videre vil man lagre store mengder data tilknyttet f. eks. Stasjon-er og Banestrekning-er, og man ønsker da å minimere belastningen av databasen. Ulempen av dette er potensielt mer komplekse spørringer (Elmasri & Navathe, 2016). 
Mappingen over har kun tabeller på fjerde normalform. Dette betyr at alle restriksjoner fra og med 1NF til og med 4NF (inkl. BCNF) holder for alle disse entitetsklassene. Disse restriksjonene er som følger (definisjon i kursiv, deretter begrunnelse): 

**Første normalform** - Attributtenes domener inneholder kun atomiske (udelelige) attributter. Dette holder da ingen entiteter i ER-diagrammet er tilknyttet flerverdiattributter, og vi er garantert å unngå duplikater da alle tupler har en entydig primærnøkkel (Midtstraum, 2021a). 

**Andre normalform** - Det finnes ingen ikke-nøkkelattributter som er delvis avhengig av en kandidatnøkkel. Som nevnt i 1NF har alle tupler i tabellen en entydig primærnøkkel, enten ved at alle andre attributter er funksjonelt avhengig av denne, eller ved fravær av funksjonelle avhengigheter slik at mengden av alle attributter er eneste nøkkel (Midtstraum, 2021a). 

**Boyce-Codd normalform** - Alle venstresideattributt i funksjonelle avhengigheter skal bestå av en (hel) supernøkkel og derfor er entydig identifikator for tabellen. Dersom dette holder vil også restriksjonene for 3NF trivielt holde, da disse i praksis kun er en mindre spesifikk variant av BCNF (Midtstraum, 2021a).  

**Fjerde normalform** - For alle ikke-trivielle MVD-er på formen X ->> Y, må det være slik at X er en supernøkkel i tabellen. Dette holder åpenbart, da vi ingen tabeller i vår mapping har noen MVD-er som restriksjoner (Midtstraum, 2021b). 

# **SQL-script**
I utgangspunktet har SQL-programmet de samme manglene som ER-diagrammet, men unntak av noen ekstra restriksjoner. Disse antagelsene og forklaringene listes under. Vi har valgt å benytte oss av ‘PRIMARY KEY’-nøkkelordene fremfor å tagge nøkkelattributter med ‘UNIQUE’-restriksjoner. 

## ‘NOT NULL’-restriksjoner
I utgangspunktet er alle attributter i SQL-scriptet merket med ‘NOT NULL’-restriksjonen. Unntak er som følger:
navn i Sittevogn & Sovevogn - Brukes for å formidle et spesifikt ‘format’ å sette opp en vogn på. Kan bli problematisk å tvinge dette for skreddersydde vogner, i tillegg til at navnet streng tatt ikke er nødvendig for at entitetene skal fungere som i ER-modellen. 
navn i Banestrekning - Ikke nødvendig for å innfri entitetens funksjonalitet. I oversikten fra Bane NOR er det eksempler på Banestrekning-er uten navn (Bane NOR, 2022). 
tidspunktKjøpt i KundeOrdre - Kan f.eks. være ukjent. Uansett irrelevant for entitetens funksjonalitet og ikke hensiktsmessig å kreve. 
ordreNr i Billett - Grunnet kardinalitet i relasjonen mellom Billett og KundeOrdre (0,1) trenger ikke nødvendigvis en Billett å ha fremmednøkkel mot KundeOrdre. 

## ‘CASCADE’-ing av fremmednøkler
Uten unntak er alle fremmednøkler markert med ON UPDATE CASCADE. Dette betyr at dersom ID i entiteten denne klassen refererer til oppdateres, vil også denne fremmednøkkelen oppdateres for å referere til samme element. Dette forhindrer at fremmednøkler refererer til ugyldige verdier. 
Videre er de fleste klasser merket med ON DELETE CASCADE, dette er for alle entiteter som er eksistensavhengige via en relasjon til en annen entiteter, ergo entiteter som har relasjoner med kardinaliteter (x, y) der x == 1. Rent praktisk fører dette til at denne entiteten også slettes dersom entiteten fremmednøkkelen referer til slettes. 
Den eneste fremmednøkkelen som benytter seg av ON UPDATE CASCADE og ikke ON DELETE CASCADE er ordreNr i Billett, da usolgte Billett-er ikke vil ha en relasjon til KundeOrdre (representert med kardinalitet (0, 1) i ER-diagrammet).

## ‘CHECK’-er av attributter
radStørrelse i SitteVogn må være større enn 0. Gir ikke mening å ha negativ eller ikke-eksisterende rader i en sittevogn. 
lengde i Delstrekning må være større enn 0. Gir ikke mening med negative avstander, og om avstand er null vil det være samme stasjon. 
plassering i Delstrekning må være et heltall lik 0 eller større. Dette skal fungere som en index for strekningens plassering i Banestrekning-en den er tilknyttet, og vi tillater ikke negativ indeksering. 

# **Kode**
Se vedlagt fil project_init.sql for script som initialiserer entitetsklasser og relasjonsklasser. Merk at filen også inneholder eksempeldataen fra brukerhistorie 1 - 3 utover kun prosjektinitaliseringen. Linje 199 - 344 er derfor i utgangspunktet ikke relevant for innlevering 1. 

# **Referanser**
Bane NOR. (2022, 11. desember). Togstrekninger og linjekart. Bane NOR. Hentet 12. mars, 2023, fra https://www.banenor.no/reisende/Banestrekninger/
Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th edition). Pearson.
Midtstraum, R. (2021a, 16. februar). Normalformer fra 1NF til BCNF [PowerPoint-lysbilder]. Blackboard NTNU.
Midtstraum, R. (2021b, 16. februar). Normaliseringsteori: MVD-er, 4NF [PowerPoint-lysbilder]. Blackboard NTNU.


