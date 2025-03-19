class SnakesLadders:
    """
    A class that implements the Snakes and Ladders game logic.
    
    This class handles player positions, turn management, game rules for 
    snakes and ladders, and win conditions.
    """
    
    def __init__(self):
        """Initialize the game state."""
        # Initialize players on square 0 (off the board)
        self.player_positions = [0, 0]
        # Player 1 starts (index 0)
        self.current_player = 0
        # Game is not over initially
        self.game_over = False
        # Move history for replay/undo functionality
        self.move_history = []
        # Define snakes (key: head, value: tail)
        self.snakes = {
            16: 6,
            46: 25,
            49: 11,
            62: 19,
            64: 60,
            74: 53,
            89: 68,
            92: 88,
            95: 75,
            99: 80
        }
        # Define ladders (key: bottom, value: top)
        self.ladders = {
            2: 38,
            7: 14,
            8: 31,
            15: 26,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            78: 98,
            87: 94
        }
    
    def play(self, die1, die2):
        """
        Process a player's turn with the given dice rolls.
        
        Args:
            die1 (int): First die roll (1-6)
            die2 (int): Second die roll (1-6)
            
        Returns:
            str: Message indicating the result of the move
        """
        # Check if game is already over
        if self.game_over:
            return "Game over!"
        
        # Get current player number (1 or 2)
        player_num = self.current_player + 1
        
        # Calculate total move
        move = die1 + die2
        
        # Save the previous position for move history and message generation
        old_position = self.player_positions[self.current_player]
        
        # Update player position
        new_position = old_position + move
        
        # Create move record
        move_record = {
            "player": self.current_player,
            "dice": (die1, die2),
            "from": old_position,
            "to": new_position,
            "special": None
        }
        
        # Handle bouncing off the end
        if new_position > 100:
            new_position = 100 - (new_position - 100)
            move_record["special"] = "bounce"
        
        # Check for snakes
        snake_message = ""
        if new_position in self.snakes:
            old_snake_position = new_position
            new_position = self.snakes[new_position]
            snake_message = f" Oops! Snake from {old_snake_position} to {new_position}."
            move_record["special"] = "snake"
            move_record["snake_from"] = old_snake_position
        
        # Check for ladders
        ladder_message = ""
        if new_position in self.ladders:
            old_ladder_position = new_position
            new_position = self.ladders[new_position]
            ladder_message = f" Nice! Ladder from {old_ladder_position} to {new_position}."
            move_record["special"] = "ladder"
            move_record["ladder_from"] = old_ladder_position
        
        # Update player position
        self.player_positions[self.current_player] = new_position
        move_record["final"] = new_position
        self.move_history.append(move_record)
        
        # Check for win condition
        if new_position == 100:
            self.game_over = True
            return f"Player {player_num} Wins with a roll of {die1}+{die2}!"
        
        # Create detailed move message
        move_message = f"Player {player_num} rolled {die1}+{die2}={move} and moved from {old_position} to {new_position}."
        if snake_message:
            move_message += snake_message
        if ladder_message:
            move_message += ladder_message
        
        # Determine next player - if dice are the same, player gets another turn
        if die1 != die2:
            self.current_player = 1 - self.current_player
            move_message += f" Player {self.current_player + 1}'s turn now."
        else:
            move_message += f" Double roll! Player {player_num} gets another turn."
        
        return move_message
    
    def get_player_positions(self):
        """Return the current positions of both players."""
        return self.player_positions
    
    def get_current_player(self):
        """Return the current player (0 for Player 1, 1 for Player 2)."""
        return self.current_player
    
    def is_game_over(self):
        """Return whether the game is over."""
        return self.game_over
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.__init__()
        
    def get_move_history(self):
        """Return the history of moves in the game."""
        return self.move_history
    
    def get_game_stats(self):
        """Return statistics about the current game."""
        if not self.move_history:
            return {"turns": 0, "moves": {0: 0, 1: 0}, "snakes": {0: 0, 1: 0}, "ladders": {0: 0, 1: 0}}
        
        stats = {
            "turns": len(self.move_history),
            "moves": {0: 0, 1: 0},  # Count of moves by player
            "snakes": {0: 0, 1: 0},  # Count of snakes hit by player
            "ladders": {0: 0, 1: 0},  # Count of ladders climbed by player
            "doubles": {0: 0, 1: 0},  # Count of doubles rolled by player
        }
        
        for move in self.move_history:
            player = move["player"]
            stats["moves"][player] += 1
            
            # Count snakes, ladders, and doubles
            if move["special"] == "snake":
                stats["snakes"][player] += 1
            elif move["special"] == "ladder":
                stats["ladders"][player] += 1
                
            if move["dice"][0] == move["dice"][1]:
                stats["doubles"][player] += 1
                
        return stats