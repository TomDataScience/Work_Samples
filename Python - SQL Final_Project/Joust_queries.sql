SELECT * FROM joust_game.joust_instances;

UPDATE joust_instances SET p1_atk_stance = 'BRACED' ORDER BY joustID DESC LIMIT 1;
UPDATE joust_instances SET p1_score = 1 ORDER BY joustID DESC LIMIT 1;

DELETE FROM joust_instances WHERE p1_score < 3 and p2_score < 3