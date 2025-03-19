from PIL import Image

# Abre a imagem
image_path = "board.jpg"
try:
    with Image.open(image_path) as img:
        width, height = img.size
        print(f"Dimensões da imagem:")
        print(f"Largura: {width}px")
        print(f"Altura: {height}px")
except FileNotFoundError:
    print(f"Erro: Arquivo '{image_path}' não encontrado")
except Exception as e:
    print(f"Erro ao abrir a imagem: {e}")