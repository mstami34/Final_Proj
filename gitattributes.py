import random
import json
import argparse

class Game:
    """
    Represents a fighting game between a player and a CPU opponent.

    Attributes:
        characters (list): List of character data loaded from a JSON file.
        player (dict): The player's chosen character.
        cpu (dict): The CPU's randomly chosen character.
        cooldowns (dict): Tracks the cooldowns of each character's moves.
        active_defenses (dict): Tracks whether a character has an active block or dodge effect.
    """

    def __init__(self, character_file):
        """
        Initializes the Game class by loading character data from a JSON file.

        Args:
            character_file (str): Path to the JSON file containing character data.

        Side-effects:
            - Opens and reads the character file.
            - Initializes attributes like `characters`, `player`, `cpu`, `cooldowns`, and `active_defenses`.
        """
        with open(character_file, 'r') as file:
            self.characters = json.load(file)["characters"]
        self.player = None
        self.cpu = None
        self.cooldowns = {}
        self.active_defenses = {}

    def __lt__(self, other):
        """
        Compares the player's health with the CPU's health to determine the outcome.

        Args:
            other (Game): The game instance for comparison (in this case, itself).

        Returns:
            bool: True if the player's health is less than the CPU's health, False otherwise.
        """
        return self.player["health"] < self.cpu["health"]

    def choose_character(self):
        """
        Allows the player to choose a character and randomly assigns a CPU character.

        Side-effects:
            - Updates `self.player` and `self.cpu` with the selected and assigned characters.
            - Prints available characters and player/CPU choices to the console.
        """
        print("Available characters:")
        for idx, char in enumerate(self.characters):
            print(f"{idx + 1}. {char['name']} (Health: {char['health']}) (Defense: {char['defense']})")
        while True:
            try:
                choice = int(input("Choose your character (1/2/3): ")) - 1
                if 0 <= choice < len(self.characters):
                    break
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.player = self.characters[choice]
        self.cpu = random.choice([char for idx, char in enumerate(self.characters) if idx != choice])
        print(f"You chose {self.player['name']}. CPU chose {self.cpu['name']}.")

    def reset_cooldowns(self):
        """
        Resets move cooldowns and defense statuses for both the player and the CPU.

        Side-effects:
            - Initializes or resets `self.cooldowns` for all moves to 0.
            - Sets `self.active_defenses` for both characters to False.
        """
        for char in [self.player, self.cpu]:
            self.cooldowns[char["name"]] = {list(move.keys())[0]: 0 for move in char["player_moves"]}
            self.active_defenses[char["name"]] = False

    def show_moves(self, char):
        """
        Displays the available moves and their cooldowns for a given character.

        Args:
            char (dict): The character whose moves will be displayed.

        Side-effects:
            - Prints the character's moves and cooldown information to the console.
        """
        print(f"\n{char['name']}'s moves:")
        for idx, move in enumerate(char["player_moves"]):
            move_name = list(move.keys())[0]
            cooldown = self.cooldowns[char["name"]][move_name]
            print(f"{idx + 1}. Move: {move_name} (Cooldown: {cooldown})")

    def apply_move(self, attacker, defender, move_key):
        """
        Executes a move from the attacker on the defender, applying damage or effects.

        Args:
            attacker (dict): The character performing the move.
            defender (dict): The character receiving the move's effects.
            move_key (int): The index of the move in the attacker's move list.

        Returns:
            bool: True if the move was successfully executed, False otherwise.

        Side-effects:
            - Updates defender's health if the move is an attack and no defense is active.
            - Activates defense effects if the move is a block or dodge.
            - Adjusts move cooldowns in `self.cooldowns`.
            - Resets active defense for the defender if an attack is nullified.
            - Prints move details, damage dealt, and applied effects to the console.
        """
        move = attacker["player_moves"][move_key]
        move_name = list(move.keys())[0]

        if self.cooldowns[attacker["name"]][move_name] > 0:
            print(f"{move_name} is on cooldown!")
            return False

        if self.active_defenses[defender["name"]]:
            print(f"{defender['name']} blocked or dodged the attack!")
            self.active_defenses[defender["name"]] = False
            self.cooldowns[attacker["name"]][move_name] = move.get("cooldown", 0)
            return True

        if move.get("effect") in ["blocks next attack", "dodge next attack"]:
            print(f"{attacker['name']} used {move_name}! {move['effect'].capitalize()}.")
            self.active_defenses[attacker["name"]] = True
            self.cooldowns[attacker["name"]][move_name] = move.get("cooldown", 0)
            return True

        damage = move["damage"] - defender["defense"]
        damage = max(damage, 0)
        defender["health"] -= damage
        print(f"{attacker['name']} used {move_name}! It dealt {damage} damage.")
        self.cooldowns[attacker["name"]][move_name] = move.get("cooldown", 0)

        if "effect" in move:
            print(f"Effect applied: {move['effect']}")

        return True

    def take_turn(self, attacker, defender):
        """
        Allows the attacker to select and execute a move against the defender.

        Args:
            attacker (dict): The character taking their turn.
            defender (dict): The character defending against the attack.

        Side-effects:
            - For the player, prompts move selection and validates input.
            - For the CPU, randomly selects a move.
            - Calls `apply_move` to execute the move.
        """
        if attacker == self.player:
            self.show_moves(attacker)
            while True:
                try:
                    move_idx = int(input(f"Choose a move for {attacker['name']} (1-{len(attacker['player_moves'])}): ")) - 1
                    if 0 <= move_idx < len(attacker["player_moves"]):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            move_idx = random.choice(range(len(attacker["player_moves"])))

        self.apply_move(attacker, defender, move_idx)

    def reduce_cooldowns(self):
        """
        Decreases the cooldown of all moves by 1 for both the player and the CPU.

        Side-effects:
            - Updates `self.cooldowns` for all moves.
        """
        for char in [self.player, self.cpu]:
            for move in self.cooldowns[char["name"]]:
                if self.cooldowns[char["name"]][move] > 0:
                    self.cooldowns[char["name"]][move] -= 1

    def play(self):
        """
        Runs the main game loop, alternating turns between the player and the CPU.

        Side-effects:
            - Prints turn information, character health, and outcomes to the console.
        """
        self.choose_character()
        self.reset_cooldowns()

        turn = 0
        while self.player["health"] > 0 and self.cpu["health"] > 0:
            print(f"\n{self.player['name']} Health: {self.player['health']}")
            print(f"{self.cpu['name']} Health: {self.cpu['health']}\n")
            if turn == 0:
                print("Your turn!")
                self.take_turn(self.player, self.cpu)
            else:
                print("CPU's turn!")
                self.take_turn(self.cpu, self.player)

            self.reduce_cooldowns()
            turn = 1 - turn

        if self < self.cpu:
            print("You lost! CPU wins.")
        else:
            print("You won! CPU is defeated.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="A text-based fighting game.")
    parser.add_argument(
        "-f", "--file", type=str, default="Characters.json", help="Path to the character JSON file."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    game = Game(args.file)
    game.play()
    
