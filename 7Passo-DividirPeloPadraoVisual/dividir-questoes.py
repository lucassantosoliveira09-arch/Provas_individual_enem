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

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_azul(imagem, cor_alvo, tolerancia=20, altura_faixa=4):
    largura, altura = imagem.size
    pixels = imagem.load()
    posicoes_corte = []
    
    # =================================================================
    # ATENÇÃO AQUI: CALIBRAÇÃO DO X
    # =================================================================
    # No GIMP, meça a distância da borda preta da esquerda até o início 
    # da linha divisória da QUESTÃO (logo após a palavra "QUESTÃO 03").
    # Se a sua imagem branca começa mais para a direita, aumente esse número.
    x_inicio = 180  
    largura_verificacao = 50  # Precisa encontrar 50 pixels seguidos da cor da linha
    
    y = 0
    while y < altura - altura_faixa:
        faixa_encontrada = True
        
        for dy in range(altura_faixa):
            for dx in range(largura_verificacao):
                x_atual = x_inicio + dx
                
                if x_atual >= largura:
                    faixa_encontrada = False
                    break
                    
                pixel = pixels[x_atual, y + dy]
                r, g, b = pixel[:3]
                
                # Se encontrar fundo branco (255, 255, 255) ou o preto de fora, cancela
                if (abs(r - cor_alvo[0]) > tolerancia or 
                    abs(g - cor_alvo[1]) > tolerancia or 
                    abs(b - cor_alvo[2]) > tolerancia):
                    faixa_encontrada = False
                    break
            if not faixa_encontrada:
                break
        
        if faixa_encontrada:
            # OBS3: Corta 15 pixels ACIMA da linha para não raspar no texto
            posicao_corte = y - 15  
            if posicao_corte < 0:  
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Linha divisória REAL detectada em y={y}, ponto de corte y={posicao_corte}")
            y += altura_faixa + 80  # Pula um espaço para não ler a mesma linha bi-dimensional
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    if not os.path.exists(caminho_imagem):
        print(f"Erro: O arquivo '{caminho_imagem}' não foi encontrado!")
        return

    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    print(f"Imagem carregada com sucesso: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_azul(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhuma divisória encontrada! O valor de 'x_inicio' ou o RGB estão incorretos.")
        return
    
    print(f"Sucesso: {len(posicoes_corte)} linhas de corte mapeadas.")
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo}")
        
        posicao_anterior = posicao_corte
    
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        nome_arquivo = f"questao_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salva última parte: {caminho_completo}")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_divididas" 

    # Cor RGB aproximada do traço escuro da prova (convertida de porcentagem do GIMP)
    cor_do_padrao = converter_cor_gimp_para_rgb(13.7, 12.1, 12.5) 
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída!")