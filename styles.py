# Custom CSS styles for animations and visual effects
CUSTOM_STYLES = '''
/* Animações dos Dados */
.dice {
    transition: transform 0.3s ease;
}

.dice.rolling {
    animation: roll-dice 0.5s linear;
}

@keyframes roll-dice {
    0% { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(180deg) scale(0.8); }
    100% { transform: rotate(360deg) scale(1); }
}

/* Status do Jogo */
.turn-indicator {
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    border: 2px solid;
    transition: all 0.3s ease;
}

.turn-indicator.player1 {
    border-color: #ff0000;
    background: rgba(255,0,0,0.1);
}

.turn-indicator.player2 {
    border-color: #0000ff;
    background: rgba(0,0,255,0.1);
}

/* Progresso dos Jogadores */
.progress-bar {
    height: 20px;
    border-radius: 10px;
    transition: width 0.5s ease-in-out;
    margin: 5px 0;
    text-align: center;
    color: white;
    font-weight: bold;
}

.progress-bar.player1 { background: linear-gradient(45deg, #ff0000, #ff6666); }
.progress-bar.player2 { background: linear-gradient(45deg, #0000ff, #6666ff); }
'''