/* Legger info om togrutene på Nordlandsbanen */
-- 'Togrute'-r
INSERT INTO Togrute VALUES (1, 1, 1); -- Trondheim-Bodø Dag
INSERT INTO Togrute VALUES (2, 1, 1); -- Trondheim-Bodø Natt
INSERT INTO Togrute VALUES (3, 0, 1); -- Mo i Rana-Trondheim Morgen

-- 'TogruteTabell'-er
INSERT INTO TogruteTabell VALUES (1, 1);
INSERT INTO TogruteTabell VALUES (2, 2);
INSERT INTO TogruteTabell VALUES (3, 3);

-- 'TogruteGårGjennom'-relasjoner
/* TogruteTabell 1 */
INSERT INTO TogruteGårGjennom VALUES ("Trondheim", 1, "07:49");
INSERT INTO TogruteGårGjennom VALUES ("Steinkjer", 1, "09:51");
INSERT INTO TogruteGårGjennom VALUES ("Mosjøen", 1, "13:20");
INSERT INTO TogruteGårGjennom VALUES ("Mo i Rana", 1, "14:31");
INSERT INTO TogruteGårGjennom VALUES ("Fauske", 1, "16:49");
INSERT INTO TogruteGårGjennom VALUES ("Bodø", 1, "17:34");
/* TogruteTabell 2 */
INSERT INTO TogruteGårGjennom VALUES ("Trondheim", 2, "23:05");
INSERT INTO TogruteGårGjennom VALUES ("Steinkjer", 2, "00:57");
INSERT INTO TogruteGårGjennom VALUES ("Mosjøen", 2, "04:41");
INSERT INTO TogruteGårGjennom VALUES ("Mo i Rana", 2, "05:55");
INSERT INTO TogruteGårGjennom VALUES ("Fauske", 2, "08:19");
INSERT INTO TogruteGårGjennom VALUES ("Bodø", 2, "09:05");
/* TogruteTabell 3 */
INSERT INTO TogruteGårGjennom VALUES ("Mo i Rana", 3, "08:11");
INSERT INTO TogruteGårGjennom VALUES ("Mosjøen", 3, "09:14");
INSERT INTO TogruteGårGjennom VALUES ("Steinkjer", 3, "12:31");
INSERT INTO TogruteGårGjennom VALUES ("Trondheim", 3, "14:13");

-- 'Operator'
INSERT INTO Operator VALUES ("SJ");

-- 'SitteVogn'-er
/* SJ-sittevogn-1 #1 (vogn #1) */
INSERT INTO Sittevogn VALUES (1, "SJ-sittevogn-1", 4, "SJ");
INSERT INTO Sete VALUES (1, 1, 1);
INSERT INTO Sete VALUES (1, 2, 1);
INSERT INTO Sete VALUES (1, 3, 1);
INSERT INTO Sete VALUES (1, 4, 1);
INSERT INTO Sete VALUES (1, 5, 2);
INSERT INTO Sete VALUES (1, 6, 2);
INSERT INTO Sete VALUES (1, 7, 2);
INSERT INTO Sete VALUES (1, 8, 2);
INSERT INTO Sete VALUES (1, 9, 3);
INSERT INTO Sete VALUES (1, 10, 3);
INSERT INTO Sete VALUES (1, 11, 3);
INSERT INTO Sete VALUES (1, 12, 3);
/* SJ-sittevogn-1 #2 (vogn #2) */
INSERT INTO Sittevogn VALUES (2, "SJ-sittevogn-1", 4, "SJ");
INSERT INTO Sete VALUES (2, 1, 1);
INSERT INTO Sete VALUES (2, 2, 1);
INSERT INTO Sete VALUES (2, 3, 1);
INSERT INTO Sete VALUES (2, 4, 1);
INSERT INTO Sete VALUES (2, 5, 2);
INSERT INTO Sete VALUES (2, 6, 2);
INSERT INTO Sete VALUES (2, 7, 2);
INSERT INTO Sete VALUES (2, 8, 2);
INSERT INTO Sete VALUES (2, 9, 3);
INSERT INTO Sete VALUES (2, 10, 3);
INSERT INTO Sete VALUES (2, 11, 3);
INSERT INTO Sete VALUES (2, 12, 3);
/* SJ-sittevogn-1 #3 (vogn #3) */
INSERT INTO Sittevogn VALUES (3, "SJ-sittevogn-1", 4, "SJ");
INSERT INTO Sete VALUES (3, 1, 1);
INSERT INTO Sete VALUES (3, 2, 1);
INSERT INTO Sete VALUES (3, 3, 1);
INSERT INTO Sete VALUES (3, 4, 1);
INSERT INTO Sete VALUES (3, 5, 2);
INSERT INTO Sete VALUES (3, 6, 2);
INSERT INTO Sete VALUES (3, 7, 2);
INSERT INTO Sete VALUES (3, 8, 2);
INSERT INTO Sete VALUES (3, 9, 3);
INSERT INTO Sete VALUES (3, 10, 3);
INSERT INTO Sete VALUES (3, 11, 3);
INSERT INTO Sete VALUES (3, 12, 3);
/* SJ-sittevogn-1 #4 (vogn #4) */
INSERT INTO Sittevogn VALUES (4, "SJ-sittevogn-1", 4, "SJ");
INSERT INTO Sete VALUES (4, 1, 1);
INSERT INTO Sete VALUES (4, 2, 1);
INSERT INTO Sete VALUES (4, 3, 1);
INSERT INTO Sete VALUES (4, 4, 1);
INSERT INTO Sete VALUES (4, 5, 2);
INSERT INTO Sete VALUES (4, 6, 2);
INSERT INTO Sete VALUES (4, 7, 2);
INSERT INTO Sete VALUES (4, 8, 2);
INSERT INTO Sete VALUES (4, 9, 3);
INSERT INTO Sete VALUES (4, 10, 3);
INSERT INTO Sete VALUES (4, 11, 3);
INSERT INTO Sete VALUES (4, 12, 3);

-- 'SoveVogn'-er
/* SJ-sovevogn-1 #1 (vogn #5) */
INSERT INTO Sovevogn VALUES (5, "SJ-sovevogn-1", "SJ");
INSERT INTO Soveplass VALUES (5, 1);
INSERT INTO Soveplass VALUES (5, 2);
INSERT INTO Sovekupe VALUES (5, 1, 1, 2);
INSERT INTO Soveplass VALUES (5, 3);
INSERT INTO Soveplass VALUES (5, 4);
INSERT INTO Sovekupe VALUES (5, 2, 3, 4);
INSERT INTO Soveplass VALUES (5, 5);
INSERT INTO Soveplass VALUES (5, 6);
INSERT INTO Sovekupe VALUES (5, 3, 5, 6);
INSERT INTO Soveplass VALUES (5, 7);
INSERT INTO Soveplass VALUES (5, 8);
INSERT INTO Sovekupe VALUES (5, 4, 7, 8);


-- 'Vognoppsett'-er
INSERT INTO Vognoppsett VALUES (1); -- For Togrute 1
INSERT INTO Vognoppsett VALUES (2); -- For Togrute 2
INSERT INTO Vognoppsett VALUES (3); -- For Togrute 3

-- 'SattSammenAv'-relasjoner
/* Format: SattSammenAv(vognoppsettID, vognID, plassering) */
INSERT INTO SattSammenAvSittevogn VALUES (1, 1, 1);
INSERT INTO SattSammenAvSittevogn VALUES (1, 2, 2);
INSERT INTO SattSammenAvSittevogn VALUES (2, 3, 1);
INSERT INTO SattSammenAvSovevogn VALUES (2, 5, 1);
INSERT INTO SattSammenAvSittevogn VALUES (3, 4, 1);

-- 'RuteOppsett'-relasjoner
/* Format: RuteOppsett(togruteID, operatorNavn, vognoppsettID) */
INSERT INTO RuteOppsett VALUES (1, "SJ", 1);
INSERT INTO RuteOppsett VALUES (2, "SJ", 2);
INSERT INTO RuteOppsett VALUES (3, "SJ", 3);