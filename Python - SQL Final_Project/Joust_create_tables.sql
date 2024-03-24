CREATE TABLE playable_races (
	raceID int NOT NULL AUTO_INCREMENT,
    race_type varchar(20) NOT NULL,
    base_defense int(2) NOT NULL,
    base_attack int(2) NOT NULL,
    base_animal_h int(2) NOT NULL,
    PRIMARY KEY(raceID));
CREATE TABLE playable_classes (
	classID int NOT NULL AUTO_INCREMENT,
    class_type varchar(20) NOT NULL,
    defense_bonus int(2) NOT NULL,
    attack_bonus int(2) NOT NULL,
    animal_h_bonus int(2) NOT NULL,
    PRIMARY KEY(classID));
CREATE TABLE attack_stances (
	stanceID int NOT NULL AUTO_INCREMENT,
    attack_stance varchar(20) NOT NULL,
    s_defense_bonus int(2) NOT NULL,
    s_attack_bonus int(2) NOT NULL,
    s_animal_h_bonus int(2) NOT NULL,
    PRIMARY KEY(classID));
    
CREATE TABLE joust_instances (
	joustID int NOT NULL AUTO_INCREMENT,
    player1_name varchar(20) NOT NULL,
    player2_name varchar(20) NOT NULL,
    player1_race varchar(20) NOT NULL,
    player2_race varchar(20) NOT NULL,
	player1_class varchar(20) NOT NULL,
    player2_class varchar(20) NOT NULL,
    p1_defense_bonus int(2) NOT NULL,
    p1_attack_bonus int(2) NOT NULL,
    p1_animal_h_bonus int(2) NOT NULL,
	p2_defense_bonus int(2) NOT NULL,
    p2_attack_bonus int(2) NOT NULL,
    p2_animal_h_bonus int(2) NOT NULL,
    p1_banner varchar(20) NOT NULL,
    p2_banner varchar(20) NOT NULL,
    joust_instancesp1_score int(2) NOT NULL,
    p2_score int(2) NOT NULL,
    PRIMARY KEY(joustID)); 