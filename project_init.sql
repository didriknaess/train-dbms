/* Entity Classes */
CREATE TABLE Operator (
	navn TEXT NOT NULL,
	PRIMARY KEY(navn)
);

CREATE TABLE Vognoppsett (
	vognoppsettID INTEGER NOT NULL,
	PRIMARY KEY(vognoppsettID)
);

CREATE TABLE Sittevogn (
	vognID INTEGER NOT NULL,
	navn TEXT,
	radStørrelse INTEGER NOT NULL CHECK(radStørrelse > 0),
    operatorNavn TEXT NOT NULL,
	PRIMARY KEY(vognID),
    FOREIGN KEY(operatorNavn) REFERENCES Operator(navn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Sovevogn (
	vognID INTEGER NOT NULL,
	navn TEXT,
    operatorNavn TEXT NOT NULL,
	PRIMARY KEY(vognID),
    FOREIGN KEY(operatorNavn) REFERENCES Operator(navn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Sete (
	vognID INTEGER NOT NULL,
	seteNr INTEGER NOT NULL,
	radNr INTEGER NOT NULL,
	PRIMARY KEY(vognID,seteNr),
    FOREIGN KEY(vognID) REFERENCES SitteVogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Soveplass (
	vognID INTEGER NOT NULL,
	sengNr INTEGER NOT NULL,
	PRIMARY KEY(vognID,sengNr),
    FOREIGN KEY(vognID) REFERENCES Sovevogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Sovekupe (
	vognID INTEGER NOT NULL,
	kupeNr INTEGER NOT NULL,
    seng1Nr INTEGER NOT NULL,
    seng2Nr INTEGER NOT NULL,
	PRIMARY KEY(vognID,kupeNr),
    FOREIGN KEY(vognID) REFERENCES Sovevogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognID, seng1Nr) REFERENCES Soveplass(vognID, sengNr) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognID, seng2Nr) REFERENCES Soveplass(vognID, sengNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Banestrekning (
	banestrekningID INTEGER NOT NULL,
	navn TEXT,
	elektrisk BINARY NOT NULL, /* enten elektrisk eller diesel */
	PRIMARY KEY(banestrekningID)
);

CREATE TABLE Togrute (
	togruteID	INTEGER NOT NULL,
    retning BINARY NOT NULL, /* enten med Banestrekning-ens hovedretning eller imot */ 
    banestrekningID INTEGER NOT NULL,
	PRIMARY KEY(togruteID),
    FOREIGN KEY(banestrekningID) REFERENCES Banestrekning(banestrekningID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE RuteForekomst (
    togruteID INTEGER NOT NULL,
    dato DATE NOT NULL,
    PRIMARY KEY(togruteID, dato),
    FOREIGN KEY(togruteID) REFERENCES Togrute(togruteID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Stasjon (
    navn TEXT NOT NULL,
    hoydemeter NUMBER NOT NULL,
    PRIMARY KEY(navn)
);

CREATE TABLE Kunde (
	kundeNr INTEGER NOT NULL,
	navn TEXT NOT NULL,
	epost TEXT NOT NULL,
	tlfNr INTEGER NOT NULL,
	PRIMARY KEY(kundeNr)
);

CREATE TABLE KundeOrdre (
	ordreNr INTEGER NOT NULL,
	tidspunktKjøpt DATE,
	kundeNr INTEGER NOT NULL,
	PRIMARY KEY(ordreNr),
	FOREIGN KEY(kundeNr) REFERENCES Kunde(kundeNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Billett (
	billettID	INTEGER NOT NULL,
    startStasjon TEXT NOT NULL, --FK?
    endeStasjon TEXT NOT NULL, --FK?
    ordreNr INTEGER,
    togruteID INTEGER NOT NULL,
    dato DATE NOT NULL,
	PRIMARY KEY(billettID),
    FOREIGN KEY(startStasjon) REFERENCES Stasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(endeStasjon) REFERENCES Stasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(ordreNr) REFERENCES KundeOrdre(ordreNr) ON UPDATE CASCADE,
    FOREIGN KEY(togruteID, dato) REFERENCES RuteForekomst(togruteID, dato) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SeteBillett (
	billettID INTEGER NOT NULL,
	vognID INTEGER NOT NULL,
	seteNr INTEGER NOT NULL,
	PRIMARY KEY(billettID),
    FOREIGN KEY(billettID) REFERENCES Billett(billettID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognID, seteNr) REFERENCES Sete(vognID, seteNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SengeBillett (
	billettID INTEGER NOT NULL,
	vognID INTEGER NOT NULL,
    sengNr DATE NOT NULL,
	PRIMARY KEY(billettID),
	FOREIGN KEY(billettID) REFERENCES Billett(billettID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(vognID, sengNr) REFERENCES Soveplass(vognID, sengNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Delstrekning (
    endepunkt1Navn TEXT NOT NULL, 
    endepunkt2Navn TEXT NOT NULL, 
    lengde NUMBER NOT NULL CHECK(lengde > 0),
    dobbeltspor BINARY NOT NULL, /* enten dobbelt- eller enkeltspor */
    banestrekningID INTEGER NOT NULL,
    plassering INTEGER NOT NULL CHECK (plassering >= 0),
    retning BINARY NOT NULL, /* enten fra Stasjon1 til Stasjon2 eller motsatt */
    PRIMARY KEY(endepunkt1Navn, endepunkt2Navn),
    FOREIGN KEY(banestrekningID) REFERENCES Banestrekning(banestrekningID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(endepunkt1Navn) REFERENCES Stasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(endepunkt2Navn) REFERENCES Stasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TogruteTabell (
    tabellID INTEGER NOT NULL,
    togruteID INTEGER NOT NULL,
    PRIMARY KEY(tabellID),
    FOREIGN KEY(togruteID) REFERENCES Togrute(togruteID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE RuteOppsett (
    togruteID INTEGER NOT NULL,
    operatorNavn TEXT NOT NULL,
    vognoppsettID INTEGER NOT NULL,
    PRIMARY KEY(togruteID),
    FOREIGN KEY(togruteID) REFERENCES Togrute(togruteID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(operatorNavn) REFERENCES Operator(navn) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognoppsettID) REFERENCES Vognoppsett(vognoppsettID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Splittet SattSammenAv i to relasjonstabeller, da det ikke finnes noen Vogn-superklasse i Databasen (abstrahert bort i mapping): 
CREATE TABLE SattSammenAvSittevogn (
    vognoppsettID INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    plassering INTEGER NOT NULL,
    PRIMARY KEY(vognoppsettID, vognID),
    FOREIGN KEY(vognoppsettID) REFERENCES Vognoppsett(vognoppsettID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognID) REFERENCES Sittevogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE SattSammenAvSovevogn (
    vognoppsettID INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    plassering INTEGER NOT NULL,
    PRIMARY KEY(vognoppsettID, vognID),
    FOREIGN KEY(vognoppsettID) REFERENCES Vognoppsett(vognoppsettID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(vognID) REFERENCES Sovevogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TogruteGårGjennom (
    stasjonNavn TEXT NOT NULL,
    tabellID INTEGER NOT NULL,
    tidspunkt TIME NOT NULL,
    PRIMARY KEY(stasjonNavn, tabellID),
    FOREIGN KEY(stasjonNavn) REFERENCES Stasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(tabellID) REFERENCES TogruteTabell(tabellID) ON UPDATE CASCADE ON DELETE CASCADE
);