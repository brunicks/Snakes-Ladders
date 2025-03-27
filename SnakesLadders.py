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
        """Processa o turno do jogador com os dados rolados."""
        if self.game_over:
            return "Jogo finalizado!"
        
        player_num = self.current_player + 1
        move = die1 + die2
        old_position = self.player_positions[self.current_player]
        new_position = old_position + move
        
        # Cria mensagem detalhada do movimento
        message_parts = [
            f"Jogador {player_num} rolou {die1}+{die2}={move}",
            f"e andou de {old_position} para {new_position}"
        ]
        
        # Trata ricochete
        if new_position > 100:
            bounce_back = new_position - 100
            new_position = 100 - bounce_back
            message_parts.append(
                f"RICOCHETE! Passou do 100 por {bounce_back} casas e voltou de 100 para {new_position}!"
            )
        
        # Verifica cobras
        if new_position in self.snakes:
            old_snake_pos = new_position
            new_position = self.snakes[new_position]
            message_parts.append(
                f"Opaa mermão! Cobra lazarenta te pegou na casa {old_snake_pos}! Desceu até a casa {new_position}! 🐍"
            )
        
        # Verifica escadas
        if new_position in self.ladders:
            old_ladder_pos = new_position
            new_position = self.ladders[new_position]
            message_parts.append(
                f"Boa malandrão! Achou uma escadinha top na casa {old_ladder_pos}! Subiu direto pra casa {new_position}! 🪜"
            )
        
        # Atualiza posição
        self.player_positions[self.current_player] = new_position
        
        # Verifica vitória
        if new_position == 100:
            self.game_over = True
            message_parts.append(f"🏆 VENCEDOR! Jogador {player_num} chegou na casa 100!")
            return " | ".join(message_parts)
        
        # Próximo turno
        if die1 != die2:
            next_player = 2 if self.current_player == 0 else 1
            message_parts.append(f"Agora é a vez do Jogador {next_player}! 🎲")
            self.current_player = 1 - self.current_player
        else:
            message_parts.append(f"🎯 DADOS IGUAIS! Jogador {player_num} joga novamente!")
        
        return " | ".join(message_parts)
    
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