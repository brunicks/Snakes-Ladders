# Cobras e Escadas (Snakes and Ladders)

Um jogo clássico de Cobras e Escadas desenvolvido com Python e Dash para interface gráfica interativa.

![Cobras e Escadas](https://github.com/yourusername/snakes_and_ladders/raw/main/assets/screenshot.png)

## Conteúdo

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Jogar](#como-jogar)
- [Regras do Jogo](#regras-do-jogo)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Personalização](#personalização)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python (listadas no arquivo `requirements.txt`)

## Instalação

1. Clone este repositório ou baixe os arquivos:

```bash
git clone https://github.com/yourusername/snakes_and_ladders.git
cd snakes_and_ladders
```

2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Certifique-se que você tem uma imagem do tabuleiro nomeada `board.jpg` na pasta `assets/`. Se a pasta não existir, crie-a:

```bash
mkdir assets
```

## Como Jogar

1. Inicie o aplicativo executando:

```bash
python SnakesLadders_dash.py
```

2. Abra seu navegador e acesse:
```
http://127.0.0.1:8050/
```

3. Interface do Jogo:
   - **Tabuleiro:** Visualizado no lado esquerdo da tela
   - **Status da Partida:** Painel na direita mostra informações sobre o jogo atual
   - **Botões de Controle:**
     - `🎲 Rolar Dados`: Clique para avançar no jogo
     - `🔄 Novo Jogo`: Reinicia a partida

4. Para jogar:
   - O jogador 1 (vermelho) começa
   - Clique em "Rolar Dados" para avançar
   - Os dados são rolados automaticamente e o jogador se move pelo tabuleiro
   - Se cair em uma escada, sobe automaticamente
   - Se cair em uma cobra, desce automaticamente
   - Os jogadores alternam os turnos, a menos que tirem números iguais nos dados
   - O primeiro a alcançar a casa 100 exatamente vence

## Regras do Jogo

### Básicas
- Dois jogadores começam na posição 0 (fora do tabuleiro)
- Jogador 1 (vermelho) começa, alternando com o Jogador 2 (azul)
- Avance o número exato de casas que tirar nos dados
- Se tirar números iguais nos dois dados, jogue novamente!

### Movimentos Especiais
- **Escadas:** Ao cair exatamente na base de uma escada, suba direto ao topo!
- **Cobras:** Se parar na cabeça de uma cobra, escorrega até a cauda!
- **Ricochete:** Se passar da casa 100, volta o número excedente de casas!

### Condições de Vitória
- Chegue exatamente na casa 100 para vencer
- Se passar da casa 100, volta! Exemplo: na casa 98, tirando 5, vai até 100 e volta para 97

## Estrutura do Projeto

- `SnakesLadders.py`: Classe com a lógica do jogo
- `SnakesLadders_dash.py`: Interface gráfica com Dash
- `styles.py`: Estilos CSS para a interface
- `assets/board.jpg`: Imagem do tabuleiro (necessária para o jogo)

## Personalização

### Modificando o Tabuleiro
Para usar seu próprio tabuleiro, substitua o arquivo `assets/board.jpg` por sua imagem personalizada, mantendo o mesmo nome. O tamanho recomendado é 564x564 pixels.

### Ajustando as Cobras e Escadas
As posições das cobras e escadas são definidas no arquivo `SnakesLadders.py`:

```python
# Cobras (chave: cabeça, valor: cauda)
self.snakes = {
    16: 6,
    46: 25,
    # ...
}

# Escadas (chave: base, valor: topo)
self.ladders = {
    2: 38,
    7: 14,
    # ...
}
```

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal
- **Dash**: Framework para criar a interface web interativa
- **PIL/Pillow**: Para manipulação de imagens (dados, tokens)
- **Bootstrap**: Para estilização da interface

---

Desenvolvido por [Seu Nome] - [Ano]
