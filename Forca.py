import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
import random
import xml.etree.ElementTree as ET

# função que fornece ula última dica faltando apenas um erro
def obter_dica():
    posicao=listapalavras.index(palavra_escolhida)
    messagebox.showinfo('Última dica', dicas[posicao])

# Função para habilitar os botões ao iniciar o jogo
def habilita_botoes():
    palpite_button["state"] = 'active'
    reiniciar_button["state"] = 'active'
    inicia_button['state'] = 'disable'

# Função para desabilitar os botões apos finalizar partida    
def desabilita_botoes():
    palpite_button["state"] = 'disable'
    reiniciar_button["state"] = 'disable'
    inicia_button['state'] = 'active'

# Função para iniciar a parti
def iniciar_partida():
    global temaSelecionado
    if cb_lista.get() == '':
        messagebox.showinfo('Tema não selecionado', 'Para iniciar o jogo é necessário selecionar um tema')
    else:
        habilita_botoes()
        obterPalavras()
        temaSelecionado = cb_lista.get()        
               
def escolher_palavra_aleatoria():
    global palavra_escolhida, palavras
    if len(palavras) > 0:      
        palavra_escolhida = palavra_aleatoria()
        palavras.remove(palavra_escolhida)
        palavra_escolhida = palavra_escolhida.upper()
        palavra_var.set("_ " * len(palavra_escolhida))
    else:
        messagebox.showinfo('Sem palavras', 'As palavras esgotaram para este tema, selecione um novo tema')
  
def palavra_aleatoria():
   global palavras
   return random.choice(palavras)

# Função para verificar o palpite do usuário
def verificar_palpite(palpite):
    palpite = palpite.upper() 
    if palpite in palpites_errados: # Verifica se a letra já foi digitada
        messagebox.showinfo( 'Letra repetida', f'A letra {palpite} já foi digitada')
    elif palpite in '0123456789': # Verifica foi digitada um número
        messagebox.showinfo('Número digitado', f'O número {palpite} digitada não é letra')
    else:
        palpites.append(palpite)
        if palpite in palavra_escolhida:
            atualizar_palavra_oculta()
        else:   
            palpites_errados.append(palpite)
            letras_erradas_var.set(" ".join(palpites_errados))
            desenhar_boneco(len(palpites_errados))  # Desenha uma parte do boneco para cada erro
    verificar_vitoria_derrota()
    entrada_palpite.delete(0, tk.END)  # Limpa a caixa de entrada

# Função para desenhar o boneco
def desenhar_boneco(erros):
    # A cada erro, desenha uma parte do boneco: cabeça, tronco, braços e pernas
    partes_boneco = [cabeça, tronco, braço_esquerdo, braço_direito, perna_esquerda, perna_direita]
    if erros <= len(partes_boneco):
        canvas.create_oval(partes_boneco[erros-1], width=2, outline="black")

# Função para atualizar a palavra oculta
def atualizar_palavra_oculta():
    global palavra_escolhida
    palavra_oculta = ""
    for letra in palavra_escolhida:
        if letra in palpites:
            palavra_oculta += letra + " "
        else:
            palavra_oculta += "_ "
    palavra_var.set(palavra_oculta)

# Função para verificar se o jogador ganhou ou perdeu
def verificar_vitoria_derrota():
    global palavra_escolhida, mostraDica
    if all(letra in palpites for letra in palavra_escolhida):
        palavra_var.set(f"A palavra era {palavra_escolhida}. Você ganhou!")
    elif len(palpites_errados) >= 6:
        palavra_var.set("Você perdeu!")
        desabilita_botoes()
    elif len(palpites_errados) == 5 and mostraDica == 0:
        obter_dica()
        mostraDica = 1
        
    

# Função para obter os temas que estão estruturados no arquivo xml 
def obterTemas():
    global temas
    for filha in root:
        temas.append(filha.tag)
        
# Função para obter as palavras e dicas do arquivo xml
def obterPalavras():
    global palavras, dicas, listapalavras
    a = cb_lista.get()
    palavras.clear()
    dicas.clear()
    listapalavras.clear()
    for cidade in root.find(a):
        palavras.append(cidade.find('nome').text)
        dicas.append(cidade.find('dica').text)
        listapalavras.append(cidade.find('nome').text.upper())
    escolher_palavra_aleatoria() # --> escolhendo a palavra aleatoria

# Criar instância do aqruivo xml e referenciar objeto em memória
tree = ET.parse('palavras.xml')
root = tree.getroot()

# Cria a janela principal
janela = tk.Tk()
janela.title('Jogo da Forca')

# Variáveis para controle
palpites = []
palpites_errados = []
palavra_var = tk.StringVar()
letras_erradas_var = tk.StringVar()
letras_erradas_var.set("")
temas = []
palavras =[]
dicas = []
listapalavras=[]
temaSelecionado=''
mostraDica=0

# Widgets
canvas = tk.Canvas(janela, width=200, height=200)  # Canvas para desenhar a forca e o boneco
canvas.pack(pady=20)

# Coordenadas para desenhar o boneco
cabeça = (140, 40, 160, 60)  # Ajustando a posição da cabeça
tronco = (150, 60, 150, 100)  # Ajustando a posição do tronco
braço_esquerdo = (140, 70, 150, 70)  # Ajustando a posição do braço esquerdo
braço_direito = (160, 70, 150, 70)  # Ajustando a posição do braço direito
perna_esquerda = (145, 120, 150, 100)  # Ajustando a posição da perna esquerda
perna_direita = (155, 120, 150, 100)  # Ajustando a posição da perna direita


# Cria a forca
canvas.create_line((100, 20, 100, 140), width=2)
canvas.create_line((100, 20, 150, 20), width=2)
canvas.create_line((150, 20, 150, 40), width=2)

palavra_label = tk.Label(janela, textvariable=palavra_var, font=("Helvetica", 16))
palavra_label.pack(pady=20)

entrada_palpite = tk.Entry(janela)
entrada_palpite.pack(pady=20)
entrada_palpite.bind("<Return>", lambda event: verificar_palpite(entrada_palpite.get()))  # Liga a tecla Enter ao palpite

palpite_button = tk.Button(janela, text="Palpite", state="disabled", command=lambda: verificar_palpite(entrada_palpite.get()))
palpite_button.pack(pady=20)

letras_erradas_label = tk.Label(janela, textvariable=letras_erradas_var, font=("Helvetica", 16), fg="red")
letras_erradas_label.pack(pady=20)

# Função para reiniciar o jogo
def reiniciar_jogo():
    global palavra_escolhida, palpites, palpites_errados, temaSelecionado, mostraDica
    canvas.delete("boneco")  # Remove o boneco do canvas
    if temaSelecionado != cb_lista.get():
        palavras.clear()
        obterPalavras()
        temaSelecionado = cb_lista.get()
    # escolher_palavra_aleatoria()
    escolher_palavra_aleatoria()
    palpites.clear()  # Limpa os palpites
    palpites_errados.clear()  # Limpa os palpites errados
    mostraDica = 0
    palavra_var.set("_ " * len(palavra_escolhida))  # Reseta a palavra oculta
    letras_erradas_var.set("")  # Limpa as letras erradas
    entrada_palpite.config(state=tk.NORMAL)  # Reabilita a entrada de texto
    palpite_button.config(state=tk.NORMAL)  # Reabilita o botão de palpite

# Combobox e label para escolha de temas
lab_tema= Label(janela, text="Selecione um dos temas abaixo")
lab_tema.pack(pady=20)
obterTemas()
cb_lista = Combobox(janela, value=temas)
cb_lista.pack(pady=20)
inicia_button = tk.Button(janela, text="Iniciar partida", command=iniciar_partida)
inicia_button.pack(pady=20)

#cb_lista.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

# Botão de Reiniciar
reiniciar_button = tk.Button(janela, state="disabled", text="Reiniciar", command=reiniciar_jogo)
reiniciar_button.pack(pady=20)


def desenhar_boneco(erros):
    # A cada erro, desenha uma parte do boneco: cabeça, tronco, braços e pernas
    partes_boneco = [cabeça, tronco, braço_esquerdo, braço_direito, perna_esquerda, perna_direita]
    if erros <= len(partes_boneco):
        canvas.create_oval(partes_boneco[erros-1], width=2, outline="black", tags="boneco")


# Inicia o loop principal (A janela)
janela.mainloop()