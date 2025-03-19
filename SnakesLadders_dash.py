import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import numpy as np
from base64 import b64encode
import os
import random
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Import the SnakesLadders game class
from SnakesLadders import SnakesLadders

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Snakes and Ladders</title>
        {%favicon%}
        {%css%}
        <style>
            .player-info-overlay {
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 1000;
                background: rgba(255,255,255,0.8);
                padding: 10px;
                border-radius: 5px;
            }
            .player-info {
                margin: 5px;
                padding: 5px;
                border-radius: 3px;
            }
            .player1 { background: rgba(255,0,0,0.2); }
            .player2 { background: rgba(0,0,255,0.2); }
            .current-turn {
                font-size: 1.5em;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border-radius: 5px;
            }
            .player-position {
                text-align: center;
                padding: 5px;
                margin: 5px;
                border-radius: 3px;
            }
            .positions-display {
                display: flex;
                justify-content: space-around;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Create a game instance
game = SnakesLadders()

# Function to generate dice images
def create_dice_image(value):
    """Create an image of a die with the given value."""
    img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw the die outline
    draw.rectangle([(5, 5), (95, 95)], outline=(0, 0, 0), width=2)
    
    # Draw the pips based on the value
    if value in [1, 3, 5]:
        # Center pip
        draw.ellipse([(45, 45), (55, 55)], fill=(0, 0, 0))
    
    if value in [2, 3, 4, 5, 6]:
        # Top-left pip
        draw.ellipse([(20, 20), (30, 30)], fill=(0, 0, 0))
        # Bottom-right pip
        draw.ellipse([(70, 70), (80, 80)], fill=(0, 0, 0))
    
    if value in [4, 5, 6]:
        # Top-right pip
        draw.ellipse([(70, 20), (80, 30)], fill=(0, 0, 0))
        # Bottom-left pip
        draw.ellipse([(20, 70), (30, 80)], fill=(0, 0, 0))
    
    if value == 6:
        # Middle-left pip
        draw.ellipse([(20, 45), (30, 55)], fill=(0, 0, 0))
        # Middle-right pip
        draw.ellipse([(70, 45), (80, 55)], fill=(0, 0, 0))
    
    # Convert to base64 for display in Dash
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return f"data:image/png;base64,{b64encode(buffer.getvalue()).decode()}"

# Player tokens
def create_player_token(player_num):
    """Create a player token image."""
    size = 50  # Tamanho aumentado para melhor visibilidade
    colors = [(255, 0, 0, 230), (0, 0, 255, 230)]  # Vermelho e Azul com alta opacidade
    
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Desenha círculo com borda branca
    draw.ellipse([(0, 0), (size, size)], fill=colors[player_num], 
                outline=(255, 255, 255), width=2)
    
    # Adiciona número do jogador
    try:
        font = ImageFont.truetype("arial.ttf", 25)
    except IOError:
        font = ImageFont.load_default()
    
    # Centraliza o texto
    text = str(player_num + 1)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Adiciona sombra para melhor legibilidade
    draw.text((x+1, y+1), text, fill=(0, 0, 0, 128), font=font)
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return f"data:image/png;base64,{b64encode(buffer.getvalue()).decode()}"

# Layout for the Dash application
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Snakes and Ladders", className="text-center mb-4"),
            html.Div(id="game-message", className="alert alert-info text-center"),
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            # Board image and player info overlay
            html.Div([
                html.Img(id="board-image", className="img-fluid"),
                html.Div(id="player-tokens"),
                # Informação dos jogadores sobreposta ao tabuleiro
                html.Div([
                    html.Div(id="player1-info", className="player-info player1"),
                    html.Div(id="player2-info", className="player-info player2"),
                ], className="player-info-overlay")
            ], style={"position": "relative"})
        ], width=8),
        
        dbc.Col([
            # Game controls
            dbc.Card([
                dbc.CardHeader("Game Controls"),
                dbc.CardBody([
                    html.Div([
                        # Placar
                        html.Div([
                            html.H4("Current Turn", className="text-center mb-3"),
                            html.Div(id="player-turn", className="current-turn mb-3"),
                            html.Div([
                                html.Div(id="player1-position", className="player-position"),
                                html.Div(id="player2-position", className="player-position"),
                            ], className="positions-display mb-3"),
                        ], className="game-status"),
                        
                        html.Div([
                            html.Img(id="die1-image", src=create_dice_image(1), 
                                   style={"width": "80px", "height": "80px", "margin": "0 10px"}),
                            html.Img(id="die2-image", src=create_dice_image(1), 
                                   style={"width": "80px", "height": "80px", "margin": "0 10px"}),
                        ], className="d-flex justify-content-center mb-4"),
                        
                        dbc.Button("Roll Dice", id="roll-button", color="primary", 
                                 className="mb-3 w-100", size="lg"),
                        dbc.Button("New Game", id="reset-button", color="secondary", 
                                 className="w-100"),
                        
                        html.Div(id="game-state", style={"display": "none"}),
                        dcc.Store(id="dice-values", data={"die1": 1, "die2": 1}),
                        dcc.Store(id="board-dimensions", data={"width": 564, "height": 564}),  
                    ])
                ])
            ])
        ], width=4)
    ])
], fluid=True)

# Callback to roll dice and update game state
@app.callback(
    [Output("dice-values", "data"),
     Output("die1-image", "src"),
     Output("die2-image", "src"),
     Output("game-message", "children"),
     Output("game-state", "children"),
     Output("player-turn", "children"),
     Output("player1-info", "children"),
     Output("player2-info", "children"),
     Output("player1-position", "children"),
     Output("player2-position", "children")],
    [Input("roll-button", "n_clicks"),
     Input("reset-button", "n_clicks")],
    [State("dice-values", "data"),
     State("game-state", "children")]
)
def update_game(roll_clicks, reset_clicks, dice_data, game_state):
    triggered_id = ctx.triggered_id
    positions = game.get_player_positions()
    
    # Initialize or reset game
    if triggered_id == "reset-button" or game_state is None:
        game.__init__()
        return (
            {"die1": 1, "die2": 1},
            create_dice_image(1),
            create_dice_image(1),
            "Game started! Player 1's turn.",
            "active",
            html.Div("Player 1's turn", style={"color": "red", "font-weight": "bold"}),
            f"Player 1: Square {positions[0]}",
            f"Player 2: Square {positions[1]}",
            html.Div(f"P1: Square {positions[0]}", style={"background": "rgba(255,0,0,0.2)"}),
            html.Div(f"P2: Square {positions[1]}", style={"background": "rgba(0,0,255,0.2)"}),
        )
    
    # Roll dice
    if triggered_id == "roll-button" and roll_clicks:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        result = game.play(die1, die2)
        current_player = game.get_current_player() + 1
        positions = game.get_player_positions()
        
        # Mensagem mais informativa
        if "ladder" in result.lower():
            message = html.Div([
                html.Strong("LADDER! 🪜 "), result
            ], style={"color": "green", "font-size": "1.2em"})
        elif "snake" in result.lower():
            message = html.Div([
                html.Strong("SNAKE! 🐍 "), result
            ], style={"color": "red", "font-size": "1.2em"})
        elif "wins" in result.lower():
            message = html.Div([
                html.Strong("🏆 WINNER! "), result
            ], style={"color": "gold", "font-size": "1.5em", "font-weight": "bold"})
        else:
            message = result
        
        player_turn_style = {
            "color": "red" if current_player == 1 else "blue",
            "font-weight": "bold"
        }
        
        return (
            {"die1": die1, "die2": die2},
            create_dice_image(die1),
            create_dice_image(die2),
            message,  # Usando a mensagem formatada
            "over" if "wins" in result.lower() else "active",
            html.Div(f"Player {current_player}'s turn", style=player_turn_style) 
                if "wins" not in result.lower() else "",
            f"Player 1: Square {positions[0]}",
            f"Player 2: Square {positions[1]}",
            html.Div(f"P1: Square {positions[0]}", 
                    style={"background": "rgba(255,0,0,0.2)", "padding": "5px", "border-radius": "5px"}),
            html.Div(f"P2: Square {positions[1]}", 
                    style={"background": "rgba(0,0,255,0.2)", "padding": "5px", "border-radius": "5px"}),
        )
    
    # Default return (estado atual do jogo)
    current_player = game.get_current_player() + 1
    return (
        dice_data,
        create_dice_image(dice_data["die1"]),
        create_dice_image(dice_data["die2"]),
        "Roll the dice or start a new game.",
        game_state or "active",
        html.Div(f"Player {current_player}'s turn", 
                style={"color": "red" if current_player == 1 else "blue", "font-weight": "bold"}),
        f"Player 1: Square {positions[0]}",
        f"Player 2: Square {positions[1]}",
        html.Div(f"P1: Square {positions[0]}", 
                style={"background": "rgba(255,0,0,0.2)", "padding": "5px", "border-radius": "5px"}),
        html.Div(f"P2: Square {positions[1]}", 
                style={"background": "rgba(0,0,255,0.2)", "padding": "5px", "border-radius": "5px"}),
    )

# Callback to update player tokens on the board
@app.callback(
    Output("player-tokens", "children"),
    [Input("game-state", "children"),
     Input("board-image", "src")],
    [State("board-dimensions", "data")]
)
def update_player_tokens(game_state, board_src, board_dims):
    if game_state is None or board_src is None:
        return []
    
    # Dimensões exatas do tabuleiro e configurações
    BOARD_WIDTH = 564  # largura da imagem do tabuleiro
    BOARD_HEIGHT = 564  # altura da imagem do tabuleiro
    GRID_SIZE = 10  # tabuleiro 10x10
    TOKEN_SIZE = 40  # tamanho reduzido para caber melhor nas células
    
    # Calcula o tamanho de cada célula
    cell_width = BOARD_WIDTH / GRID_SIZE
    cell_height = BOARD_HEIGHT / GRID_SIZE
    
    player_positions = game.get_player_positions()
    player_tokens = []
    
    for player_num, position in enumerate(player_positions):
        if position > 0:  # se o jogador está no tabuleiro
            # Converte a posição para coordenadas de grid
            pos = position - 1
            
            # Calcula linha e coluna
            row = 9 - (pos // 10)  # inverte as linhas pois 100 está no topo
            col = pos % 10
            
            # Ajusta a coluna para linhas que vão da direita para esquerda
            if (9 - row) % 2 == 1:  # Linhas pares (contando de cima) vão da direita para esquerda
                col = 9 - col
            
            # Calcula as coordenadas em pixels
            left = col * cell_width + (cell_width - TOKEN_SIZE) / 2
            top = row * cell_height + (cell_height - TOKEN_SIZE) / 2
            
            # Ajusta posição quando dois jogadores estão na mesma casa
            if player_num == 1 and position == player_positions[0]:
                left += TOKEN_SIZE / 3
                top += TOKEN_SIZE / 3
            
            player_tokens.append(
                html.Img(
                    src=create_player_token(player_num),
                    style={
                        "position": "absolute",
                        "left": f"{left}px",
                        "top": f"{top}px",
                        "width": f"{TOKEN_SIZE}px",
                        "height": f"{TOKEN_SIZE}px",
                        "z-index": str(1000 + player_num),  # Player 2 fica sobre Player 1
                        "transition": "all 0.5s ease-in-out",  # Animação suave
                        "border-radius": "50%",  # Torna a imagem circular
                        "box-shadow": "2px 2px 5px rgba(0,0,0,0.3)"  # Adiciona sombra
                    }
                )
            )
    
    return player_tokens

@app.callback(
    Output("board-dimensions", "data"),
    Input("board-image", "src")
)
def update_board_dimensions(_):
    """Update board dimensions with known values."""
    return {"width": 564, "height": 564}  # Fixed dimensions of board.jpg

# Adicione um callback para carregar a imagem do tabuleiro
@app.callback(
    Output("board-image", "src"),
    Input("board-image", "id")
)
def update_board_image(_):
    """Load the board image from assets folder."""
    return app.get_asset_url("board.jpg")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)