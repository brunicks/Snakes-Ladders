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
from SnakesLadders import SnakesLadders

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server

# Adiciona CSS personalizado
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
                      /* Estilos da seção de regras */
            .card-header h4 {
                color: #2c3e50;
            }
            
            .card-body h5 {
                color: #34495e;
                border-bottom: 2px solid #eee;
                padding-bottom: 8px;
            }
            
            .card-body ul {
                list-style-type: none;
                padding-left: 0;
            }
            
            .card-body li {
                margin-bottom: 12px;
                padding-left: 25px;
                position: relative;
            }
            
            .card-body li:before {
                position: absolute;
                left: 0;
                top: 2px;
            }
            
            .card-body small {
                color: #666;
                font-style: italic;
                display: block;
                margin-top: 5px;
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

# Cria uma instância do jogo
game = SnakesLadders()

# Função para gerar imagens de dados
def create_dice_image(value):
    """Cria uma imagem de um dado com o valor fornecido."""
    img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Desenha o contorno do dado
    draw.rectangle([(5, 5), (95, 95)], outline=(0, 0, 0), width=2)
    
    # Desenha os pontos baseados no valor
    if value in [1, 3, 5]:
        # Ponto central
        draw.ellipse([(45, 45), (55, 55)], fill=(0, 0, 0))
    
    if value in [2, 3, 4, 5, 6]:
        # Ponto superior-esquerdo
        draw.ellipse([(20, 20), (30, 30)], fill=(0, 0, 0))
        # Ponto inferior-direito
        draw.ellipse([(70, 70), (80, 80)], fill=(0, 0, 0))
    
    if value in [4, 5, 6]:
        # Ponto superior-direito
        draw.ellipse([(70, 20), (80, 30)], fill=(0, 0, 0))
        # Ponto inferior-esquerdo
        draw.ellipse([(20, 70), (30, 80)], fill=(0, 0, 0))
    
    if value == 6:
        # Ponto meio-esquerdo
        draw.ellipse([(20, 45), (30, 55)], fill=(0, 0, 0))
        # Ponto meio-direito
        draw.ellipse([(70, 45), (80, 55)], fill=(0, 0, 0))
    
    # Converte para base64 para exibição no Dash
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return f"data:image/png;base64,{b64encode(buffer.getvalue()).decode()}"

# Tokens dos jogadores
def create_player_token(player_num):
    """Cria uma imagem de token do jogador."""
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

# Layout para a aplicação Dash
app.layout = dbc.Container([
    # Cabeçalho
    dbc.Row([
        dbc.Col([
            html.H1("Cobras e Escadas", className="text-center mb-4"),
            html.Div(id="game-message", className="alert alert-info text-center"),
        ], width=12)
    ], className="mb-4"),
    
    # Tabuleiro do Jogo e Controles
    dbc.Row([
        # Coluna Esquerda - Tabuleiro
        dbc.Col([
            html.Div([
                html.Img(id="board-image", className="img-fluid"),
                html.Div(id="player-tokens"),
            ], style={"position": "relative"})
        ], width=8),
        
        # Coluna Direita - Controles
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Status da Partida"),
                dbc.CardBody([
                    html.Div([
                        html.Div(id="player1-info", className="player-info player1 mb-2"),
                        html.Div(id="player2-info", className="player-info player2 mb-4"),
                    ], className="game-status mb-4"),
                    
                    html.H4("Turno Atual", className="text-center mb-3"),
                    html.Div(id="player-turn", className="current-turn mb-3"),
                    html.Div([
                        html.Div(id="player1-position", className="player-position"),
                        html.Div(id="player2-position", className="player-position"),
                    ], className="positions-display mb-4"),
                    
                    html.Div([
                        html.Img(id="die1-image", src=create_dice_image(1), 
                               style={"width": "80px", "height": "80px", "margin": "0 10px"}),
                        html.Img(id="die2-image", src=create_dice_image(1), 
                               style={"width": "80px", "height": "80px", "margin": "0 10px"}),
                    ], className="d-flex justify-content-center mb-4"),
                    
                    dbc.Button("Rolar Dados", id="roll-button", color="primary", 
                             className="mb-3 w-100", size="lg"),
                    dbc.Button("Novo Jogo", id="reset-button", color="secondary", 
                             className="w-100"),
                    
                    html.Div(id="game-state", style={"display": "none"}),
                    dcc.Store(id="dice-values", data={"die1": 1, "die2": 1}),
                    dcc.Store(id="board-dimensions", data={"width": 564, "height": 564}),
                ])
            ])
        ], width=4)
    ], className="mb-4"),
    
    # Seção de Regras
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H4("🎲 Regras do Jogo", className="text-center mb-0")
                ),
                dbc.CardBody([
                    dbc.Row([
                        # Coluna de Regras Básicas
                        dbc.Col([
                            html.H5("📜 Regras Básicas", className="mb-3"),
                            html.Ul([
                                html.Li("Dois jogadores começam na posição 0"),
                                html.Li("Jogador Vermelho (1) começa, alternando com o Azul (2)"),
                                html.Li("Avance pelos números em ordem até chegar ao 100"),
                                html.Li("Se tirar números iguais nos dados, jogue novamente!")
                            ], className="mb-4"),
                        ], width=4),
                        
                        # Coluna de Movimentos Especiais
                        dbc.Col([
                            html.H5("🎯 Movimentos Especiais", className="mb-3"),
                            html.Ul([
                                html.Li([
                                    html.Strong("🪜 Escadas: "), 
                                    "Ao cair exatamente na base, suba direto ao topo!"
                                ]),
                                html.Li([
                                    html.Strong("🐍 Cobras: "), 
                                    "Se parar na cabeça, escorrega até a cauda!"
                                ])
                            ], className="mb-4"),
                        ], width=4),
                        
                        # Coluna de Condições de Vitória
                        dbc.Col([
                            html.H5("🏆 Como Vencer", className="mb-3"),
                            html.Ul([
                                html.Li([
                                    "Chegue exatamente na casa 100",
                                    ]),
                                    html.Li([
                                    "Se passar, volta! Exemplo: na casa 98, ",
                                    "tirando 5, vai até 100 e volta para 97"
                                ]),                              
                            ]),
                        ], width=4),
                    ])
                ])
            ], className="shadow")
        ], width=12)
    ])
], fluid=True)

# Callback para rolar os dados e atualizar o estado do jogo
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
    
    # Inicializa ou reinicia o jogo
    if triggered_id == "reset-button" or game_state is None:
        game.__init__()
        return (
            {"die1": 1, "die2": 1},
            create_dice_image(1),
            create_dice_image(1),
            "Jogo começou! Turno do jogador 1.",
            "active",
            html.Div("Turno do jogador 1", style={"color": "red", "font-weight": "bold"}),
            f"Player 1: Posição {positions[0]}",
            f"Player 2: Posição {positions[1]}",
            html.Div(f"P1: Posição {positions[0]}", style={"background": "rgba(255,0,0,0.2)"}),
            html.Div(f"P2: Posição {positions[1]}", style={"background": "rgba(0,0,255,0.2)"}),
        )
    
    # Rola os dados
    if triggered_id == "roll-button" and roll_clicks:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        result = game.play(die1, die2)
        current_player = game.get_current_player() + 1
        positions = game.get_player_positions()
        
        # Mensagem mais informativa
        if "ladder" in result.lower():
            message = html.Div([
                html.Strong("ESCADA! 🪜 "), result
            ], style={"color": "green", "font-size": "1.2em"})
        elif "snake" in result.lower():
            message = html.Div([
                html.Strong("COBRAA! 🐍 "), result
            ], style={"color": "red", "font-size": "1.2em"})
        elif "wins" in result.lower():
            message = html.Div([
                html.Strong("🏆 VENCEDOR!!! "), result
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
            html.Div(f"Turno do jogador {current_player}", style=player_turn_style) 
                if "wins" not in result.lower() else "",
            f"Player 1: Posição {positions[0]}",
            f"Player 2: Posição {positions[1]}",
            html.Div(f"P1: Posição {positions[0]}", 
                    style={"background": "rgba(255,0,0,0.2)", "padding": "5px", "border-radius": "5px"}),
            html.Div(f"P2: Posição {positions[1]}", 
                    style={"background": "rgba(0,0,255,0.2)", "padding": "5px", "border-radius": "5px"}),
        )
    
    # Retorno padrão (estado atual do jogo)
    current_player = game.get_current_player() + 1
    return (
        dice_data,
        create_dice_image(dice_data["die1"]),
        create_dice_image(dice_data["die2"]),
        "Jogue os dados ou começe um novo jogo.",
        game_state or "active",
        html.Div(f"Turno do jogador {current_player}", 
                style={"color": "red" if current_player == 1 else "blue", "font-weight": "bold"}),
        f"Player 1: Posição {positions[0]}",
        f"Player 2: Posição {positions[1]}",
        html.Div(f"P1: Posição {positions[0]}", 
                style={"background": "rgba(255,0,0,0.2)", "padding": "5px", "border-radius": "5px"}),
        html.Div(f"P2: Posição {positions[1]}", 
                style={"background": "rgba(0,0,255,0.2)", "padding": "5px", "border-radius": "5px"}),
    )

# Callback para atualizar os tokens dos jogadores no tabuleiro
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
    """Atualiza as dimensões do tabuleiro com valores conhecidos."""
    return {"width": 564, "height": 564}  # Dimensões fixas de board.jpg

# Adicione um callback para carregar a imagem do tabuleiro
@app.callback(
    Output("board-image", "src"),
    Input("board-image", "id")
)
def update_board_image(_):
    """Carrega a imagem do tabuleiro da pasta assets."""
    return app.get_asset_url("board.jpg")

# Executa a aplicação
if __name__ == "__main__":
    app.run_server(debug=True)
