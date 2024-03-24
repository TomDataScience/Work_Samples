import mysql.connector           #Connect to the database
from statistics import mode      #To help determine most used data from joust database
import random                    #To help simulate dice rolls
import player_positions
import Rules
class data_Base():
    connect = 'N'
    active = 'N'
    def __init__(self,connect,active):
        self.connect = connect
        self.active = active
    def connect_to_db(self):
            if __name__ == '__main__':
                self.connect = mysql.connector.connect(
                user='root',
                password='root',
                host='127.0.0.1',
                database='joust_game')
    def close_db(self):
        self.connect.close()
    def rules_race_stats(self):
        print()
        print()
        print("Players choose their playable race and class.")
        print("These choices give you bonuses or reductions that will affect your dice rolls.")
        print()
        print("---PLAYABLE RACES---")
        print()
        self.active = self.connect.cursor() 
        self.race_all_sql =("""SELECT character_type, defense_stat, attack_stat, animal_h_stat FROM character_data WHERE char_stat_type = 'RACE';""")      #SQL Query to pull all playable race data for players to view
        self.active.execute(self.race_all_sql)    #Execute requested query    
        for row in self.active.fetchall():
            print("Race Type: ",row[0],"| Base Defense: ",row[1],"| Base Attack: ",row[2]," | Base Animal Handling Stat: ",row[3])
    def rules_class_stats(self):
       print()
       print()
       print("---PLAYABLE CLASSES---")
       print()
       self.active = self.connect.cursor() 
       self.class_all_sql =("""SELECT character_type, defense_stat, attack_stat, animal_h_stat FROM character_data WHERE char_stat_type = 'CLASS';""")      #SQL Query to pull all playable class data for players to view
       self.active.execute(self.class_all_sql)    #Execute requested query    
       for row in self.active.fetchall():
            print("Class Type: ",row[0],"| Defense Bonus: ",row[1],"| Attack Bonus: ",row[2]," | Animal Handling Bonus: ",row[3])
    def rules_attack_stance(self):
        print("The Various Attack Stances and their statistics are:")
        print()
        print("---ATTACK STANCES---")
        print()
        self.active = self.connect.cursor() 
        self.attack_stance_sql =("""SELECT character_type, defense_stat, attack_stat, animal_h_stat FROM character_data WHERE char_stat_type = 'ATTACK S';""") #Pulls all attack stances to view
        self.active.execute(self.attack_stance_sql)    #Execute requested query    
        for row in self.active.fetchall():
            print("Attack Stance: ",row[0],"| Defense Bonus: ",row[1],"| Attack Bonus: ",row[2]," | Animal Handling Bonus: ",row[3]) 
        print()
        print("Note * HIS = High in Saddle- An Aggressive form of riding which grants the player a high attack boost at the risk of being unseated easily. ")
        print("       Braced-  A Defensive form of riding which grants the player a high animal handling boost for their braced check at the risk of having low attack and not scoring a point.")
        print()                                                                                                                                                                                                                                                                                                                                 
##Character Object to build the Characters/Pull data from the DB and Run the Game##
class Character():
    player_name = 'N'
    race_type = 'N'
    class_type = 'N'
    base_defense = 0
    base_attack = 0
    base_animal_handling = 0
    defense_bonus = 0
    attack_bonus = 0
    animal_handling_bonus = 0
    attack_stance = 'N'
    banner_color = 'N'
    c_total_defense =  0
    c_total_attack = 0
    c_total_a_h = 0
    player_damage = 0
    player_attack = 0
    player_brace = 0
    player_score = 0
    connect = 'None'
    active = 'None'
    s_defense_bonus = 0
    s_attack_bonus = 0
    s_animal_handling_bonus = 0
    atk_update = 'N'
    update_value = 0
    def __init__(self,player_name, race_type,class_type,base_defense, base_attack,base_animal_handling,defense_bonus,attack_bonus,animal_handling_bonus,attack_stance,banner_color,c_total_defense,c_total_attack,c_total_a_h,player_damage,
                 player_attack,player_brace,player_score,connect,active,s_defense_bonus,s_attack_bonus,s_animal_handling_bonus,atk_update, update_value):
        self.player_name = player_name
        self.race_type = race_type
        self.class_type = class_type
        self.base_defense = base_defense
        self.base_attack = base_attack
        self.base_animal_handling = base_animal_handling
        self.defense_bonus = defense_bonus
        self.attack_bonus = attack_bonus
        self.animal_handling_bonus = animal_handling_bonus
        self.attack_stance = attack_stance
        self.banner_color = banner_color
        self.c_total_defense = c_total_defense
        self.c_total_attack = c_total_attack
        self.c_total_a_h = c_total_a_h
        self.player_score = player_score
        self.player_damage = player_damage
        self.player_attack = player_attack
        self.player_brace = player_brace
        self.connect = connect
        self.active = active
        self.s_defense_bonus = s_defense_bonus
        self.s_attack_bonus = s_attack_bonus
        self.s_animal_handling_bonus = s_animal_handling_bonus
        self.atk_update = atk_update
        self.update_value = update_value
#Builds Player Characters based on user input                
    def user_input(self):
        if __name__ == '__main__':
            #Connects to Database
            self.connect = mysql.connector.connect(
                user='root',
                password='root',
                host='127.0.0.1',
                database='joust_game') 
        self.player_name = input("What is your name? ")
        self.run_race = 'TRUE'
        self.active = self.connect.cursor()                  #### Prepares to grab data from the database
        while self.run_race == "TRUE":
            self.race_list = ['HUMAN','DWARF', 'ELF','ORC' ] # Only Valid Options users can choose. 
            self.race_type_input= input("What character do you want to be? Choices: Human, Dwarf, Elf, Orc: ")
            self.race_upper = self.race_type_input.upper()
            self.race_type = [self.race_upper]                   #Formatted to be read by the database.
            if self.race_type_input.upper() in self.race_list:
                self.run_race = 'FALSE'
                break
            else:
                print()
                print("That is not an available race. Please select one of the playable races")
                del self.race_type                               #Resets race_type in the event the player entered wrong data
                print()
        self.race_sql =("""SELECT * FROM character_data WHERE char_stat_type = 'RACE' AND character_type like %s;""")      #SQL Query to pull playable race data for the character object based on user input
        self.active.execute(self.race_sql,(self.race_type))    #Execute requested query    
        for row in self.active.fetchall():            #data from the select statement is used to populate attributes for the character object. 
            self.base_defense = row[3]                
            self.base_attack = row[4]
            self.base_animal_handling = row[5]
        self.race_type = str.title(self.race_upper)              #formated race_type so it can be viewed properly in the print statements below.
        self.run_class = 'TRUE'
        self.active_c = self.connect.cursor()  
        while self.run_class == "TRUE":
            self.class_list = ['KNIGHT','WARRIOR', 'RANGER','BARBARIAN' ]   # Only Valid Options users can choose. 
            self.class_type_input= input("What class do you want to be? Choices: Knight, Warrior, Ranger, Barbarian: ") 
            self.class_upper = self.class_type_input.upper()
            self.class_type = [self.class_upper]                         #Formatted to be read by the database.
            if self.class_type_input.upper() in self.class_list:
                self.run_class = 'FALSE'
                break
            else:
                print()
                print("That is not an available class. Please select one of the playable classes")
                del self.class_type                                  #Resets class_type in the event the player entered wrong data
                print()
        self.class_sql =("""SELECT * FROM character_data WHERE char_stat_type = 'CLASS' AND character_type like %s;""")   #SQL Query to pull playable class data for the character object based on user input
        self.active_c.execute(self.class_sql,(self.class_type))    #Execute requested query    
        for row in self.active.fetchall():             #data from the select statement is used to populate attributes for the character object. 
            self.defense_bonus = row[3]
            self.attack_bonus = row[4]
            self.animal_handling_bonus = row[5]
        self.class_type = str.title(self.class_upper)
        self.banner_color = input("What color do you want your banner to be? ")
        self.c_total_defense = self.base_defense + self.defense_bonus              #Character is data is updated based on results from SQL tables.
        self.c_total_attack = self.base_attack + self.attack_bonus                 #Character is data is updated based on results from SQL tables.
        self.c_total_a_h = self.base_animal_handling + self.animal_handling_bonus  #Character is data is updated based on results from SQL tables.
        self.connect.close()
#User Option during the game. Adjusts their stats based on choice of one of the following actions.   
##Change this to pull data from the table. 
##Use Update Statment to modify the instance table.   
    def choose_attack_stance(self):
        if __name__ == '__main__':
            #Connects to Database
            self.connect = mysql.connector.connect(
                user='root',
                password='root',
                host='127.0.0.1',
                database='joust_game')                                             
        self.pick_attack_stance = 'TRUE'
        self.active_a = self.connect.cursor() 
        while self.pick_attack_stance == "TRUE":
            self.attack_list = ['NORMAL','AGGRESSIVE','DEFENSIVE', 'BRACED','HIS' ]       # Only Valid Options users can choose. 
            print ("Attack Stance Choices: Normal, Aggressive, Defensive, Braced, High in Saddles (HIS)")
            print()
            self.attack_stance_input= input(f"{self.player_name} choose your Attack Stance: ") 
            self.attack_stance_upper = self.attack_stance_input.upper()
            self.attack_stance = [self.attack_stance_upper] 
            if self.attack_stance_input.upper() in self.attack_list:
                self.pick_attack_stance = 'FALSE'
                break
            else:
                print()
                print("That is not an attack stance. Please select one of the available attack stances")
                del self.attack_stance
                print()
        self.attack_sql =("""SELECT * FROM character_data WHERE char_stat_type = 'ATTACK S' AND character_type = %s;""")   #SQL Query to pull playable class data for the character object based on user input
        self.active_a.execute(self.attack_sql,(self.attack_stance))    #Execute requested query    
        for row in self.active_a.fetchall():             #data from the select statement is used to populate attributes for the character object. 
            self.s_defense_bonus = row[3]
            self.s_attack_bonus = row[4]
            self.s_animal_handling_bonus = row[5]
        self.class_type = str.title(self.class_upper)
        self.c_total_defense = int(self.base_defense + self.defense_bonus + self.s_defense_bonus)            #Character is data is updated based on results from SQL tables.
        self.c_total_attack = int(self.base_attack + self.attack_bonus  + self.s_attack_bonus)                #Character is data is updated based on results from SQL tables.
        self.c_total_a_h = int(self.base_animal_handling + self.animal_handling_bonus + self.s_animal_handling_bonus) #Character is data is updated based on results from SQL tables.
        self.connect.close()
#Logic that allows the users' to attack during the game.        
    def attack(self):
        self.choose_to_attack = 'NO'
        while self.choose_to_attack == "NO":
            self.choose_to_attack= input(f"{self.player_name} are you ready to attack?: ") 
            if self.choose_to_attack.upper() == 'YES':
                print()
                print(f"{self.player_name} has rolled to Attack!")
                self.c_player_attack = int(random.randint(1,20)) + int(self.c_total_attack)
                print()
                break
            else:
                self.choose_to_attack = 'NO'
                print()
                print("We shall await your attack command")
                print()
#Logic that allows the users' to roll for damage during the game.
    def roll_damage(self):
        self.player_damage= 'NO'
        while self.player_damage == "NO":
            self.player_damage= input(f"{self.player_name} are you ready to roll for damage?: ") 
            if self.player_damage.upper() == 'YES':
                print()
                print(f"{self.player_name} has rolled for damage!")
                self.c_player_damage = int(random.randint(1,12)) + 3                                  ### Builds a simulated damage roll based on random module. 
                print()
                break
            else:
                self.player_damage = 'NO'
                print()
                print("Do not hesitate! un-seat for foe! ")
                print()
#Logic that allows the users' to roll for a brace check during the game.
    def brace(self):
        self.brace_check = 'NO'
        while self.brace_check == "NO":
            self.brace_check= input(f"{self.player_name} are you ready roll your brace check? ") 
            if self.brace_check.upper() == 'YES':
                print()
                print(f"{self.player_name} has braced for incoming damage!")
                self.c_player_brace = int(random.randint(1,20)) + int(self.c_total_a_h)          ### Builds a simulated braced check based on random module. 
                print()
                break
            else:
                self.brace_check = 'NO'
                print()
                print("You must defend yourself! Hurry!! ")
                print()
#Resets player scores for a new game.
    def reset_player_scores(self):
        self.player_score = 0
#The two calculations to determine how many points are scored,
    def player_score_hit(self):
        self.player_score = int(self.player_score + 1)
    def player_score_unseat(self):
        self.player_score = int(self.player_score + 3) 
#Displays the stats of the user's character after their input. 
    def display_character(self):
        print(f"Welcome to the joust {self.player_name} the {self.race_type} {self.class_type} flying the {self.banner_color} banner! ")
        print("------------")
        print("Below are your character stats for the joust!")
        print("------------")
        print(f"Defense: {self.c_total_defense}")
        print(f"Attack Bonus: {self.c_total_attack}")
        print(f"Animal Handling: {self.c_total_a_h}")
        print("------------")
####PLAYER 1 and PLAYER 2 OBJECTS #####################################  
database = data_Base('N','N')          
player1 = Character('N','N','N',0,0,0,0,0,0,'N','N',0,0,0,0,0,0,0,'None','None',0,0,0,'N',0)
player2 = Character('N','N','N',0,0,0,0,0,0,'N','N',0,0,0,0,0,0,0,'None','None',0,0,0,'N',0)

#Function to gather introduce the players, gather their input and build their characters for the game
def most_common(List):
    return(mode(List))
def helpful_tips():
    race_list = []
    class_list =[]
    atk_s_list =[]
    database.connect_to_db()
    active = database.connect.cursor()
    race_sql =("""SELECT player1_race FROM joust_instances UNION ALL SELECT player2_race FROM joust_instances;""")      #SQL Query to pull playable race data for the character object based on user input
    active.execute(race_sql)    #Execute requested query    
    for row in active.fetchall():            #data from the select statement is used to populate attributes for the character object. 
        race_list.append(row[0])
    c_active = database.connect.cursor()            
    class_sql =("""SELECT player1_class FROM joust_instances UNION ALL SELECT player2_class FROM joust_instances;""")      #SQL Query to pull playable race data for the character object based on user input
    c_active.execute(class_sql)    #Execute requested query    
    for row in active.fetchall():            #data from the select statement is used to populate attributes for the character object. 
        class_list.append(row[0])
    atk_active = database.connect.cursor()            
    atk_s_sql =("""SELECT p1_atk_stance FROM joust_instances UNION ALL SELECT p1_atk_stance FROM joust_instances;""")      #SQL Query to pull playable race data for the character object based on user input
    atk_active.execute(atk_s_sql)    #Execute requested query    
    for row in active.fetchall():            #data from the select statement is used to populate attributes for the character object. 
        atk_s_list.append(row[0])
    most_common_race = most_common(race_list)
    most_common_class = most_common(class_list)
    most_common_atk = most_common(atk_s_list)
    print()
    print(f"-----HELPFUL TIPS-----")
    print(f"Most Used Race: {most_common_race}.\nMost Used Class: {most_common_class}.\nMost used attack stance is {most_common_atk}. ")
def high_score():
    database.connect_to_db()
    hs_active = database.connect.cursor()            
    high_score_sql =("""SELECT player1_name, player1_race, player1_class, p1_score FROM joust_instances UNION ALL SELECT player2_name, player2_race, player2_class, p2_score  FROM joust_instances ORDER BY p1_score DESC LIMIT 1;""")
    hs_active.execute(high_score_sql)    #Execute requested query    
    for row in hs_active.fetchall():          
        player_name = row[0]
        player_race = row[1]
        player_class =row[2]
        player_score = row[3] 
    try:
        print(f"{player_name} the {player_race} {player_class} currently holds the high score for the joust game with a score of {player_score}")
    except UnboundLocalError:
        pass
def rules_function():
    database.connect_to_db()
    Rules.rules_intro()
    database.rules_race_stats()
    database.rules_class_stats()
    Rules.rules_how_to_play()
    database.rules_attack_stance()
    Rules.game_mechanics()
    helpful_tips()
    database.close_db()    
def player_intros():
    print("Player 1 create your character!")
    player1.user_input()
    player1.display_character()
    print("Player 2 create your character!")
    player2.user_input()
    player2.display_character()
##This function Runs the logics for the game and handles the game mechanics.     
def joust():
    joust_run = 'YES'
    while joust_run.upper() == 'YES':
        print("Starting Positions")
        print("---------------------------------")
        ##Players are allowed to choose their attacks and confirm they are attacking.
        player_positions.starting_position()
        player1.choose_attack_stance()
        player2.choose_attack_stance()
        update_atk_stances()
        ###Attack rolls are simulated.
        player1.attack()
        player2.attack()
        print(f"{player1.player_name} attacks with a score of {player1.c_player_attack} against {player2.player_name}'s defense score of {int(player2.c_total_defense)} ")
        print(f"{player2.player_name} attacks with a score of {player2.c_player_attack} against {player1.player_name}'s defense score of {int(player1.c_total_defense)} ")
        ## If statements to compared the players' rolls/stats to determine if they score hits/damage/misses
        if int(player1.c_player_attack) >= int(player2.c_total_defense) and int(player1.c_total_defense) >= int(player2.c_player_attack): 
            player1.player_score_hit()
            print()
            print(f"{player1.player_name} strikes a blow!!!")
            print()
            print(f"{player1.player_name} Roll for Damage, {player2.player_name} make a brace check!")
            player1.roll_damage()
            player2.brace()
            print(f"{player1.player_name} hits {player2.player_name} for {player1.c_player_damage} damage against {player2.player_name}'s brace check of score {player2.c_player_brace}")
            if player1.c_player_damage >= player2.player_brace:
                player1.player_score_unseat()
                print(f"{player2.player_name} has been struck down!")
                player_positions.P1_Unseats_P2_Misses()
            else:
                print(f"{player2.player_name} has not been un-seated! The joust continues")
                player_positions.P1_Hits_P2_Misses()
        elif int(player1.c_player_attack) >= int(player2.c_total_defense) and int(player1.c_total_defense) <= int(player2.c_player_attack):
            player1.player_score_hit()
            player2.player_score_hit()
            print()
            print(f"{player1.player_name} strikes a blow!!!")
            print(f"{player2.player_name} strikes a blow!!!")
            print()
            print(f"{player1.player_name} Roll for Damage, {player2.player_name} make a brace check!")
            print(f"{player2.player_name} Roll for Damage, {player1.player_name} make a brace check!")
            player1.roll_damage()
            player2.roll_damage()
            player1.brace()
            player2.brace()
            print(f"{player1.player_name} hits {player2.player_name} for {player1.c_player_damage} damage against {player2.player_name}'s brace check of score {player2.c_player_brace}")
            print(f"{player2.player_name} hits {player1.player_name} for {player2.c_player_damage} damage against {player1.player_name}'s brace check of score {player1.c_player_brace}")
            if player1.c_player_damage >= player2.c_player_brace and player2.c_player_damage >= player1.c_player_brace:
                player1.player_score_unseat()
                player2.player_score_unseat()
                print("Both Riders have been struck down!")
                player_positions.both_players_unseated()
            elif player1.c_player_damage >= player2.c_player_brace and int(player2.c_player_damage) <= player1.c_player_brace:
                player1.player_score_unseat()
                print(f"{player2.player_name} has been struck down!")
                player_positions.P1_unseats_P2_Hits()
            elif int(player1.c_player_damage) <= player2.c_player_brace and int(player2.c_player_damage) >= player1.c_player_brace:
                player2.player_score_unseat()
                print(f"{player1.player_name} has been struck down!")
                player_positions.P2_unseats_P1_Hits()
            elif int(player1.c_player_damage) <= player2.c_player_brace and int(player2.c_player_damage) <= player1.c_player_brace:
                print("Neither Rider have been struck down! The joust continues!")
                player_positions.both_players_hit()
        elif int(player1.c_player_attack) <= int(player2.c_total_defense) and int(player1.c_total_defense) <= int(player2.c_player_attack):
            player2.player_score_hit()
            print()
            print(f"{player2.player_name} strikes a blow!!!")
            print()
            print(f"{player2.player_name} Roll for Damage, {player1.player_name} make a brace check!")
            player2.roll_damage()
            player1.brace()
            print(f"{player2.player_name} hits {player1.player_name} for {player2.c_player_damage} damage against {player1.player_name}'s brace check of score {player1.c_player_brace}")
            if int(player2.c_player_damage) >= player1.c_player_brace:
                player2.player_score_unseat()
                print(f"{player1.player_name} has been struck down!")
                player_positions.P2_Unseats_P1_Misses()
            else:
                print(f"{player1.player_name} has not been un-seated! The joust continues")
                player_positions.P2_Hits_P1_Misses()
        elif int(player1.c_player_attack) <= int(player2.c_total_defense) and int(player1.c_total_defense) >= int(player2.c_player_attack):
            print("Both Players Missed! The Joust Continues!!")
            player_positions.both_players__miss()
        else:
            print('ERROR')
        ##Shows Player Score at the end of each round###
        print(f"{player1.player_name}'s score: {player1.player_score} | {player2.player_name}'s score: {player2.player_score} ")
        print()
        print()
        ### Checks the players' scores and determines a winner if conditions are met. 
        if player1.player_score >= 3 or player2.player_score >= 3:
            update_player_scores()
            if player1.player_score > player2.player_score:
                joust_run = 'No'
                print (f"{player1.player_name} the mighty {player1.race_type} {player1.class_type} raises their {player1.banner_color} banner in victory!")
                print()
            elif player2.player_score > player1.player_score:
                joust_run = 'No'
                print()
                print (f"{player2.player_name} the triumphant {player2.race_type} {player2.class_type} raises their {player2.banner_color} banner in victory!")
            else:
                print()
                print(f"{player1.player_name} the {player1.race_type} {player1.class_type} and {player2.player_name} the {player2.race_type} {player2.class_type} are now tied\nThe joust will continue until a winner is declared!")
                print(f"Ready yourselves for battle!")
        else:
            pass
##Inserts the joust results and player data to the database. 
def insert_data():
    database.connect_to_db()
    sql = "INSERT INTO joust_instances (joustID,player1_name,player2_name,player1_race,player2_race,player1_class,player2_class,p1_defense_bonus,p1_attack_bonus,p1_animal_h_bonus,p2_defense_bonus,p2_attack_bonus,p2_animal_h_bonus,p1_banner,p2_banner,p1_score,p2_score)\
                                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (0,player1.player_name,player2.player_name,player1.race_type,player2.race_type,player1.class_type,player2.class_type,int(player1.c_total_defense),player1.c_total_attack,
                  int(player1.c_total_a_h),int(player2.c_total_defense),player2.c_total_attack,int(player2.c_total_a_h),player1.banner_color,player2.banner_color,player1.player_score,player2.player_score)
    active = database.connect.cursor()                     #Requested the required scripts
    active.execute(sql,values)    #Execute requested query    
    database.connect.commit();                                                             ###Needs to execute UPDATE,DELETE, INSERT
    print(active.rowcount,"We are ready to Joust!")   
    database.connect.close()                         ###Needs to execute UPDATE,DELETE, INSERT
def update_atk_stances():
    database.connect_to_db()
    p1_atk_stance_sql = ("""UPDATE joust_instances SET p1_atk_stance = %s ORDER BY joustID DESC LIMIT 1;""")
    p2_atk_stance_sql = ("""UPDATE joust_instances SET p2_atk_stance = %s ORDER BY joustID DESC LIMIT 1;""")
    p1_atk_active = database.connect.cursor() 
    p2_atk_active = database.connect.cursor() 
    p1_atk_active.execute(p1_atk_stance_sql,player1.attack_stance)
    database.connect.commit()
    p2_atk_active.execute(p2_atk_stance_sql,player2.attack_stance)
    database.connect.commit();
    database.connect.close()  
    pass  
def update_player_scores():
    database.connect_to_db()
    p1_score_update_sql = ("""UPDATE joust_instances SET p1_score = %s ORDER BY joustID DESC LIMIT 1;""")
    p2_score_update_sql = ("""UPDATE joust_instances SET p2_score = %s ORDER BY joustID DESC LIMIT 1;""")
    p1_active_s = database.connect.cursor()
    p1_score_update = [player1.player_score] 
    p2_score_update = [player2.player_score] 
    p2_active_s = database.connect.cursor() 
    p1_active_s.execute(p1_score_update_sql,p1_score_update)
    database.connect.commit();
    p2_active_s.execute(p2_score_update_sql,p2_score_update)
    database.connect.commit();
    database.connect.close()  
#run_gam function builds the logic to allow the players to cylce through the different options of building characters, seeing the rules, playing the game and ending the game. 
def run_game():
    run_program = 'YES'
    reset_players = 'YES'
    print("Welcome to the Joust Game! The mini-game based on the popular table top game...Dungeons and Dragons!")
    while run_program.upper() == 'YES':
        database.connect_to_db()
        rules_Y_N = 'FALSE'
        while rules_Y_N == "FALSE":
            Y_N_list = ['YES','NO']    #Created list of only Yes or No Answer
            rules_input = input("Do you want to see the rules? (YES/NO): ")
            if rules_input.upper() in Y_N_list:
                rules_Y_N = 'TRUE'
            else:
                print()
                print("Please Choose YES or NO")
                print()
        if rules_input.upper() == 'YES':
            rules_function()
        else:
            pass
        player1.reset_player_scores()
        player2.reset_player_scores()
        if reset_players.upper() == 'YES':
            print()
            print()
            high_score()
            print()
            print()
            player_intros()
            insert_data()
            joust()
        else:
            high_score()
            player1.reset_player_scores()
            player2.reset_player_scores()
            insert_data()
            joust()
        run_program_Y_N = 'FALSE'
        while run_program_Y_N == "FALSE":
            run_program = input("Do you want to play again? (YES/NO): ")
            if run_program.upper() in Y_N_list:
                run_program_Y_N = 'TRUE'
            else:
                print()
                print("Please Choose YES or NO")
                print()
        if run_program.upper() == 'YES':
            reset_Y_N = 'FALSE'
            while reset_Y_N == 'FALSE':
                reset_players = input("Do you want to create new characters? (YES/NO): ")
                if reset_players.upper() in Y_N_list: 
                    reset_Y_N = 'TRUE'
                else:
                    print()
                    print("Please Choose YES or NO")
                    print()
        else:
            print("Thank you for playing!")
            print("Program Ended") 
            database.close_db()
    
##Launches Game###   
run_game()        