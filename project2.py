#!/usr/bin/python3
''' RGP Game modified and enhanced by Quentin '''

# Import shutil for centering text
import shutil

# Import pygame for audio capabilities
import pygame

# Import time to use sleep
import time

def main():
    # Define function for sound effects
    def playAudio(selection):
        pygame.mixer.init()
        pygame.mixer.music.load(selection)
        pygame.mixer.music.set_volume(.35)
        pygame.mixer.music.play(-1)

    # Display game instructions
    def showInstructions():
        playAudio('.\\audio\\main_background.mp3')

        #print a main menu and the commands
        """Show the game instructions when called"""
        
        # Centers text in terminal
        cols, rows = shutil.get_terminal_size()
        print(("RPG Game").center(cols))
        print(("========================================").center(cols))
        print('''
        Instructions:
        Find the hidden treasure to win!
        Commands include go direction, get item, and attack commands:
            go [north, south, east, west]
            go [down, up] - (if in stairwell)
            get [item]
            teleport - Issue the teleport command and then select a room from the list
            attack [monster]
        ''')

    # Display player statistics
    def showStatus():
        """determine the current status of the player"""
        # print the player's current location
        print('---------------------------')
        print('You are in the ' + currentRoom)
        # print what the player is carrying
        print('Inventory:', inventory)
        # check if there's an item in the room, if so print it
        if "item" in rooms[currentRoom]:
            print('You see a ' + rooms[currentRoom]['item'])
            print("---------------------------")

    # Empty list that will append items to as found throughout the game
    inventory = []

    # Rooms dictionary that contains a room name for the key, and another dictionary for the value
    rooms = {
            'Hall': {
                'south': 'Kitchen',
                'east': 'Dining Room',
                },
            'Kitchen': {
                'north': 'Hall',
                'south': 'Stairwell #1',
                'item': 'potion'
                },
            'Stairwell #1': {
                'up': 'Kitchen',
                'down': 'Servants Hall'
                },
            'Servants Hall': {
                'north': 'Stairwell #1',
                'west': 'Sitting Room',
                'east': 'Boot Room',
                },
            'Sitting Room': {
                'east': 'Servants Hall',
                'item': 'key'
                },
            'Boot Room': {
                'west': 'Servants Hall',
                'south': 'Stairwell #2'
                },
            'Stairwell #2': {
                'up': 'Boot Room',
                'down': 'Dungeon'
                },
            'Dungeon': {
                'north': 'Stairwell #2',
                'east': 'Treasure Room',
                'item': 'monster'
                },
            'Treasure Room': {
                'west': 'Dungeon',
                'item': 'treasure'
                },
            'Dining Room': {
                'west': 'Hall',
                'south': 'Drawing Room',
                },
            'Drawing Room': {
                'north': 'Dining Room',
                'east': 'Garden'
                },
            'Garden': {
                'west': 'Drawing Room',
                'item': 'sword'
                }
            }

    # Call showInstructions function
    showInstructions()

    # Setting the starting room to the Hall
    currentRoom = "Hall"

    # Create playGame function that asks the user if they ar ready and plays audio
    def playGame():
        showInstructions()
        play_game = input("Are you ready to play? (y/n): ").lower()

        if play_game == 'y':
            playAudio('.\\audio\\main_theme_master.mp3')
        else:
            exit()
    playGame()

    # While loop that shows the status after each move and prints out text depending on the player's move and location
    while True:
        showStatus()

        move = ''
        while move == '':
            move = input('>')

        move = move.lower().split(" ", 1)

        if move[0] == 'go':
            if move[1] in rooms[currentRoom]:
                currentRoom = rooms[currentRoom][move[1]]
            else:
                print("You can't go that way!")

        # If using the get command on a potion, key, sword, or treasure, then a sound will play
        if move[0] == 'get':
            if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and rooms[currentRoom]['item'] == 'potion':
                playAudio('.\\audio\\select_potion.mp3')
                time.sleep(1)
                playAudio('.\\audio\\main_theme_master.mp3')
                inventory.append(move[1])
                print(move[1] + ' got!')
                del rooms[currentRoom]['item']
            elif "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and rooms[currentRoom]['item'] == 'key' or rooms[currentRoom]['item'] == 'sword' or rooms[currentRoom]['item'] == 'treasure':
                playAudio('.\\audio\\select_other.mp3')
                time.sleep(1)
                playAudio('.\\audio\\main_theme_master.mp3')
                inventory.append(move[1])
                print(move[1] + ' got!')
                del rooms[currentRoom]['item']
            else:
                print("Can't get " + move[1] + "!")

        # If the attack command is issued and sword is in inventory, then you can attack the monster
        if move[0] == 'attack':
            if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item'] and 'sword' in inventory:
                print('You attack the monster with the sword, and the monster fainted!')
                del rooms[currentRoom]['item']
            else:
                print("There's nothing to attack here...")

        # If teleport command is issued a list of rooms will display showing which rooms you can teleport to
        if move[0] == 'teleport':
            for room in rooms.keys():
                print(room)
            tele_location = input("Enter a room to teleport: ")
            if tele_location not in rooms.keys():
                print("That is not a valid room...")
            else:
                playAudio('.\\audio\\teleport.mp3')
                time.sleep(1)
                currentRoom = tele_location

        if currentRoom == 'Dungeon':
            playAudio('.\\audio\\main_combat_master.mp3')
        else:
            playAudio('.\\audio\\main_theme_master.mp3')

        # If in room with sword and you do not have the potion, then you are teleported out of the room
        if 'item' in rooms[currentRoom] and 'sword' in rooms[currentRoom]['item'] and 'potion' not in inventory:
            print('---------------------------')
            print("You are in the Garden")
            print("There's a sword stuck in a stone here, but you need a special potion in order to pull it out!")
            print("Teleporting you to the Hall")
            playAudio('.\\audio\\teleport.mp3')
            time.sleep(1)
            currentRoom = 'Hall'
            playAudio('.\\audio\\main_theme_master.mp3')    

        # If in room with monster and you do not have the sword, you will be teleported out of the room
        if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item'] and 'sword' not in inventory:
            print('---------------------------')
            print("The monster is too strong and you fainted...find a weapon to defeat it!")
            print("Teleporting you to the Drawing Room")
            playAudio('.\\audio\\teleport.mp3')
            time.sleep(1)
            currentRoom = 'Drawing Room'
            playAudio('.\\audio\\main_theme_master.mp3')
        elif 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item'] and 'sword' in inventory:
            playAudio('.\\audio\\main_combat_master.mp3')

        # If in room with treasure and key is not in the inventory, then you cannot get the treasure yet and will be telported out of room
        if 'item' in rooms[currentRoom] and 'treasure' in rooms[currentRoom]['item'] and 'key' not in inventory:
            print('---------------------------')
            print("To open the Treasure Room, you need a key!")
            print("Find the key to claim your treasure!")
            print("Teleporting you to the Servants Hall")
            playAudio('.\\audio\\teleport.mp3')
            time.sleep(1)
            currentRoom = 'Servants Hall'
            playAudio('.\\audio\\main_theme_master.mp3')
        
        # Once in the Treasure Room, key and treasurea nd in inventory, then you win the game
        if currentRoom == 'Treasure Room' and 'key' in inventory and 'treasure' in inventory:
            print('You found the treasure chest full of gold...YOU WIN!')
            break

if __name__ == "__main__":
    main()