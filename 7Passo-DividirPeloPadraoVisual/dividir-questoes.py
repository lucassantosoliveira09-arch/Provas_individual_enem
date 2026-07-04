"""
Propósito: Dividir as questões por padrão. Observa-se que ao início de cada questão tem uma faixa de alguma cor, que é o padrão de início de cada questão
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a imagem "colunas_concatenadas_verticalmente.png" do passo 6 para essa pasta do passo 7

OBS2: puxe a pasta "inteiras" do passo 5 para essa pasta do passo 7

OBS3: este código foi originalmente preparado para percorrer cada pixel de cima para baixo, analizando o penúltimo pixel da direita (linha 55), procurando por um padrão visual vertical de 10 pixels RGB 0-255 (64, 193, 243), seguido de 7 pixels RGB 0-255 (179, 230, 250), 4 px RGB 0-255 (64, 193, 243) e 8 px RGB 0-255 (179, 230, 250). Quando encontrava esse padrão, cortava-se 13 pixels acima de começar o padrão (linha 71).

OBS4: tendo isso em mente, use o GIMP para identificar qual é o padrão visual da sua prova (que indica o início de cada questão), quantos pixels acima do padrão visual você precisa cortar, e também qual pixel é melhor percorrer para procurar por essa faixa. SEJA CRÍTICO(A)!

OBS5: em algumas situações, o pixel procurado é a mesma cor de uma imagem ou letra. Nesses casos, você pode pedir para percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel. Isso vai depender do padrão visual da sua prova.

OBS6: além disso, em algumas situações, o padrão visual varia um pixel ou outro. Por isso, é interessante considerar uma margem de erro de 3 pixels para mais e 3 pixels para menos em cada uma das faixas do seu padrão visual.

OBS6: use IA para mudar minimamente o código a fim de cortar sua imagem seguindo o padrão visual vertical da sua prova, qual pixel percorrer, qual cor RGB 0-255 procurar, quantos pixels acima do padrão visual cortar, e se necessário, percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel.

OBS7: rode esse código para cada imagem que você precisa cortar. Atualize as linhas 138 e 139 para identificar a imagem e atualize o nome da pasta de saída também

OBS8: execute o código, e abra as imagens para conferir se as questões foram divididas corretamente. Se não, ajuste os valores de corte e execute novamente.
"""

from PIL import Image
import os

def encontrar_faixa_divisoria(imagem, cor_alvo, tolerancia=15, altura_faixa=6):
    """
    Procura a linha divisória varrendo a coluna X informada no GIMP.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # OBS4: Baseado no seu print do GIMP, a linha passa perfeitamente no X = 68
    x_pesquisa = 68
    
    y = 0
    while y < altura - altura_faixa:
        faixa_encontrada = True
        
        # Verifica se há uma sequência vertical de pixels da cor alvo
        for dy in range(altura_faixa):
            # Garante que não vai tentar ler fora da largura da imagem por segurança
            if x_pesquisa >= largura:
                x_pesquisa = largura - 2
                
            pixel = pixels[x_pesquisa, y + dy]
            r, g, b = pixel[:3]
            
            # OBS6: Tolerância para pequenas variações de tons
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # OBS3/OBS4: Quantos pixels cortar ACIMA do padrão para não raspar no texto
            pixels_acima = 15  
            posicao_corte = y - pixels_acima
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão visual encontrado em y={y}. Cortando em y={posicao_corte}")
            
            # Pula a faixa encontrada + uma margem para evitar detecção duplicada
            y += altura_faixa + 30  
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente usando os pontos encontrados
    """
    if not os.path.exists(caminho_imagem):
        print(f"Erro: O arquivo '{caminho_imagem}' não foi encontrado!")
        return

    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_divisoria(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhuma faixa divisória encontrada com os valores RGB fornecidos.")
        return
    
    print(f"Encontradas {len(posicoes_corte)} linhas divisórias para corte")
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Recorta a questão correspondente
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Salva o bloco da última questão até o final do arquivo
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        nome_arquivo = f"questao_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo última parte: {caminho_completo}")

if __name__ == "__main__":
    # OBS7: Definição dos arquivos de entrada e saída
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_divididas"                        
    
    # Valores RGB obtidos diretamente do seu print do GIMP (image_bb45ab.png)
    cor_do_padrao = (35, 31, 32) 
    
    print(f"Iniciando busca pelo padrão de cor: RGB {cor_do_padrao}")
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão de questões concluída com sucesso!")