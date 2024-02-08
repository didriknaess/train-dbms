/* Legger inn data for Nordlandsbanen */
-- 'Stasjon'-er
INSERT INTO Stasjon VALUES ("Trondheim", 5.1);
INSERT INTO Stasjon VALUES ("Steinkjer", 3.6);
INSERT INTO Stasjon VALUES ("Mosjøen", 6.8);
INSERT INTO Stasjon VALUES ("Mo i Rana", 3.5);
INSERT INTO Stasjon VALUES ("Fauske", 34.0);
INSERT INTO Stasjon VALUES ("Bodø", 4.1);

-- 'Banestrekning'
INSERT INTO Banestrekning VALUES (1, "Nordlandsbanen", 0);

-- 'Delstrekning'-er
/* Format: Delstrekning(endepunkt1Navn, endepunkt2Navn, lengde, dobbeltspor, banestrekningID, plassering, retning) */
INSERT INTO Delstrekning VALUES ("Trondheim", "Steinkjer", 120, 1, 1, 1, 1);
INSERT INTO Delstrekning VALUES ("Steinkjer", "Mosjøen", 280, 0, 1, 2, 1);
INSERT INTO Delstrekning VALUES ("Mosjøen", "Mo i Rana", 90, 0, 1, 3, 1);
INSERT INTO Delstrekning VALUES ("Mo i Rana", "Fauske", 170, 0, 1, 4, 1);
INSERT INTO Delstrekning VALUES ("Fauske", "Bodø", 60, 0, 1, 5, 1);