# INST326\_The\_Groupe\_Final\_Project

Final Project Repository

# Purpose:

* Characters.json\- a file with every character and all their attributes that the game file uses to set players’ names, health, defense, and attacking moves  
* .gitattributes \- The file on which the program is stored and is run through a command line argument  
* README.md \- This file \- has documentation of the program \- the purpose, how to use it and run it, and attribution

# Instructions:

* Run the file from the command line, the only two arguments needed are .gitattributes and Characters.json  
* The program is a fighting game, and the player inputs are pretty simple. Once the file is run, you pick a character by typing in a number, then once the computer picks a player and the game begins, you select your move based on multiple options when it says in the terminal that it’s your move. You’ll continue doing this until either you or the computer player is out of health, which ends the game.   
* The program will continuously keep you updated, showing you possible move options each turn and both the health of you and the computer player. 

# Rules

* Type in the correct inputs \- if you don’t, you’ll get “"Invalid choice. Please select a valid number." or "Invalid input. Please enter a number."  
* There’s a cooldown on different moves \- if you input the same move back to back, you’ll get the message "{move\_name} is on cooldown\!"

# Attribution:

| Method/Function | Primary Author | Techniques Demonstrated |
| :---- | :---- | :---- |
| \_\_init\_\_() | Correy Little | json.load() |
| \_\_lt\_\_() | Correy Little | magic methods other than \_\_init\_\_() |
| take\_turn | Jeffrey Beamer, Jr. | Conditional Expressions |
| parse\_arguments | Jeffrey Beamer, Jr. | The Argument Parser Class |
| apply\_move | Michael Stamatos | F-strings containing expressions |
| choose\_character | Michael Stamatos | Optional parameters and/or keyword arguments  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

