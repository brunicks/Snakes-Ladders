class SnakesLadders:
    """
    Classe com a lógica do jogo.
    
    Essa classe cuida da posição dos jogadores, gerencia os turnos, define as regras e condições de vitória.
    """
    
    def __init__(self):
        """Inicializa o jogo."""
        # Inicializa as posições dos jogadores
        self.player_positions = [0, 0]
        # Jogador 1 começa (índice 0)
        self.current_player = 0
        # Jogo não está finalizado inicialmente
        self.game_over = False
        # Histórico de movimentos para replay/desfazer
        self.move_history = []
        # Define as cobras (chave: cabeça, valor: cauda)
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
        # Define as escadas (chave: base, valor: topo)
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
        Processa o turno do jogador com os dados rolados.
        
        Args:
            die1 (int): Primeiro dado (1-6)
            die2 (int): Segundo dado (1-6)
            
        Returns:
            str: Mensagem indicando o resultado do movimento
        """
        # Verifica se o jogo já acabou
        if self.game_over:
            return "Jogo finalizado!"
        
        # Obtém o número do jogador atual (1 ou 2)
        player_num = self.current_player + 1
        
        # Calcula o movimento total
        move = die1 + die2
        
        # Salva a posição anterior para histórico e mensagem
        old_position = self.player_positions[self.current_player]
        
        # Atualiza posição do jogador
        new_position = old_position + move
        
        # Cria registro do movimento
        move_record = {
            "player": self.current_player,
            "dice": (die1, die2),
            "from": old_position,
            "to": new_position,
            "special": None
        }
        
        # Trata ricochete no final do tabuleiro
        if new_position > 100:
            new_position = 100 - (new_position - 100)
            move_record["special"] = "bounce"
        
        # Verifica cobras
        snake_message = ""
        if new_position in self.snakes:
            old_snake_position = new_position
            new_position = self.snakes[new_position]
            snake_message = f" Opaa mermão! Cobra lazarenta em {old_snake_position} para {new_position}."
            move_record["special"] = "snake"
            move_record["snake_from"] = old_snake_position
        
        # Verifica escadas
        ladder_message = ""
        if new_position in self.ladders:
            old_ladder_position = new_position
            new_position = self.ladders[new_position]
            ladder_message = f" Boa malandrão! Escadinha top de {old_ladder_position} ate {new_position}."
            move_record["special"] = "ladder"
            move_record["ladder_from"] = old_ladder_position
        
        # Atualiza posição do jogador
        self.player_positions[self.current_player] = new_position
        move_record["final"] = new_position
        self.move_history.append(move_record)
        
        # Verifica condição de vitória
        if new_position == 100:
            self.game_over = True
            return f"Jogador {player_num} venceu rolando: {die1}+{die2}!"
        
        # Cria mensagem detalhada do movimento
        move_message = f"Jogador {player_num} rolou {die1}+{die2}={move} e andou de {old_position} para {new_position}."
        if snake_message:
            move_message += snake_message
        if ladder_message:
            move_message += ladder_message
        
        # Determina próximo jogador - se os dados forem iguais, jogador ganha outra rodada
        if die1 != die2:
            self.current_player = 1 - self.current_player
            move_message += f" Turno do jogador {self.current_player + 1}."
        else:
            move_message += f" Rolou dupla! Jogador {player_num} ganha mais uma rodada."
        
        return move_message
    
    def get_player_positions(self):
        """Retorna as posições atuais dos dois jogadores."""
        return self.player_positions
    
    def get_current_player(self):
        """Retorna o jogador atual (0 para Jogador 1, 1 para Jogador 2)."""
        return self.current_player
    
    def is_game_over(self):
        """Retorna se o jogo está finalizado."""
        return self.game_over
    
    def reset_game(self):
        """Reinicia o jogo para seu estado inicial."""
        self.__init__()
        
    def get_move_history(self):
        """Retorna o histórico de movimentos do jogo."""
        return self.move_history
    
    def get_game_stats(self):
        """Retorna estatísticas do jogo atual."""
        if not self.move_history:
            return {"turnos": 0, "movimentos": {0: 0, 1: 0}, "cobras": {0: 0, 1: 0}, "escadas": {0: 0, 1: 0}}
        
        stats = {
            "turnos": len(self.move_history),
            "movimentos": {0: 0, 1: 0},  # Contagem de movimentos por jogador
            "cobras": {0: 0, 1: 0},  # Contagem de cobras atingidas por jogador
            "escadas": {0: 0, 1: 0},  # Contagem de escadas subidas por jogador
            "duplas": {0: 0, 1: 0},  # Contagem de duplas roladas por jogador
        }
        
        for move in self.move_history:
            player = move["player"]
            stats["movimentos"][player] += 1
            
            # Conta cobras, escadas e duplas
            if move["special"] == "snake":
                stats["cobras"][player] += 1
            elif move["special"] == "ladder":
                stats["escadas"][player] += 1
                
            if move["dice"][0] == move["dice"][1]:
                stats["duplas"][player] += 1
                
        return stats