from tkinter import filedialog ##Usado para abrir uma janela de diálogo que permite ao usuário selecionar um arquivo ou diretório
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pygame.mixer as mixer ##Usada para reprodução de áudio
import pygame
import imagens_rc ##Arquivo com as definições das imagens utilizadas
import sys
import os ## fornece uma maneira de usar funcionalidades dependentes do sistema operacional

mixer.init() ##Inicia o módulo mixer
pygame.init() ##Inicia o módulo pygame

class MP3Player(QMainWindow): ##Classe principal, subclasse da classe QMainWindow
    def __init__(self): ## Define o método __init__, que é o construtor da classe
        super(MP3Player, self).__init__() ##Chama o construtor da classe pai, QMainWindow, para garantir que as inicializações e configurações básicas da janela principal sejam feitas corretamente

        ##Configs da janela principal

        self.resize(350, 500) ##Defindo o tamanho da janela
        self.setMinimumSize(QSize(350, 100)) ##tamanho min
        self.setMaximumSize(QSize(350, 500)) ##tamanho max
        self.setBaseSize(QSize(350, 500)) ##Tamanho base
        icon = QIcon() ##Definindo icone da janela
        icon.addFile(u":/music.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle(u"Music Player") ##Definindo o nome da janela

        ##Configs do Widget principal
        self.mp3player = QWidget(self)
        self.mp3player.setMinimumSize(QSize(350, 100)) ##tamanho min
        self.mp3player.setMaximumSize(QSize(350, 500)) ##tamanho max
        self.mp3player.setBaseSize(QSize(350, 500)) ##Tamanho base

        ##Configs layout vertical do Widget principal
        self.verticalLayout = QVBoxLayout(self.mp3player) 
        self.verticalLayout.setSpacing(0) ##Zerando o espaço entre as caixas
        self.verticalLayout.setContentsMargins(0, 0, 0, 0) ##Retirando as bordas
        
        ##Configs Frame 'Container' central
        self.central = QFrame(self.mp3player)
        self.central.setMaximumSize(QSize(350, 400)) ##tamanho max
        self.central.setBaseSize(QSize(350, 400)) ##Tamanho base
        self.central.setStyleSheet(u"background-image: url(:/background.png);") ##Setando imagem para style
        
        ##Configs botão upload
        self.upload = QPushButton(self.central)
        self.upload.setGeometry(QRect(161, 360, 25, 25)) ##Setando tamanho e posição
        self.upload.setStyleSheet(u"border-image: url(:/upload.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.upload.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.upload.clicked.connect(self.adicionarmusica) ##Adicionando a função de adicionar musica ao botão

        ##Personalizando a fonte da lista
        fonte = QFont()
        fonte.setFamily(u"Arial")
        fonte.setPointSize(10)

        ##Configs da lista de música
        self.lista = QListWidget(self.central)
        self.lista.setGeometry(QRect(26, 40, 297, 318)) ##Setando tamanho e posição
        self.lista.setFont(fonte) ##Chamando as configs de fonte para as músicas adicionadas
        self.lista.setStyleSheet(u"background-image: url(:/transparent.png);" "border-image: url(:/listbackground.png);" "color: rgb(255, 255, 255);") ##Setando imagem para style
        self.lista.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) ##Bloqueando o Scroll Horizontal na lista
        self.lista.itemClicked.connect(self.reproduzirmusicaselecionada) ##Adicionando a função de reproduzir musica ao selecionar na lista

        ##Configs layout vertical do Widget central
        self.verticalLayout.addWidget(self.central)

        ##Configs do Frame 'Container' Player
        self.player = QFrame(self.mp3player)
        self.player.setMinimumSize(QSize(100, 100)) ##tamanho min
        self.player.setMaximumSize(QSize(350, 100)) ##tamanho max
        self.player.setBaseSize(QSize(400, 100)) ##Tamanho base
        self.player.setStyleSheet(u"background-image: url(:/footer.png);") ##Setando imagem para style

        ##Configs botão stop
        self.stop = QPushButton(self.player)
        self.stop.setGeometry(QRect(24, 30, 40, 40)) ##Setando tamanho e posição
        self.stop.setStyleSheet(u"border-image: url(:/stop.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.stop.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.stop.clicked.connect(self.pararmusica) ##Adicionando a função de parar musica ao botão

        ##Configs botão pause
        self.pause = QPushButton(self.player)
        self.pause.setGeometry(QRect(286, 30, 40, 40)) ##Setando tamanho e posição
        self.pause.setStyleSheet(u"border-image: url(:/pause.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.pause.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.pause.clicked.connect(self.pausarmusica) ##Adicionando a função de pausar musica ao botão

        ##Configs botão back
        self.back = QPushButton(self.player)
        self.back.setGeometry(QRect(78, 25, 50, 50)) ##Setando tamanho e posição
        self.back.setStyleSheet(u"border-image: url(:/back.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.back.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.back.clicked.connect(self.voltarmusica) ##Adicionando a função de voltar a musica ao botão

        ##Configs botão next
        self.next = QPushButton(self.player)
        self.next.setGeometry(QRect(221, 25, 50, 50)) ##Setando tamanho e posição
        self.next.setStyleSheet(u"border-image: url(:/next.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.next.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.next.clicked.connect(self.proximamusica) ##Adicionando a função de pular musica ao botão

        ##Configs botão play
        self.play = QPushButton(self.player)
        self.play.setGeometry(QRect(142, 17, 65, 65)) ##Setando tamanho e posição
        self.play.setStyleSheet(u"border-image: url(:/play.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style
        self.play.setCursor(QCursor(Qt.PointingHandCursor)) ##Mudança de seta para handcursor
        self.play.clicked.connect(self.retomarmusica) ##Adicionando a função de remotar musica pausada ao botão

        ##Configs linha decorativa
        self.line = QPushButton(self.player)
        self.line.setGeometry(QRect(0, 0, 350, 9)) ##Setando tamanho e posição
        self.line.setStyleSheet(u"border-image: url(:/linha.png);" "background-image: url(:/transparent.png);") ##Setando imagem para style

        ##Configs layout vertical do Widget Player
        self.verticalLayout.addWidget(self.player)
        self.setCentralWidget(self.mp3player)

        self.playlist = [] ##Setando o tipo da playlist (lista de reprodução)
        self.item = 0 ##variável que controla o índice da música atual na lista de reprodução

    ##Funções dos botões do Player

    def adicionarmusica(self): ##Função para adicionar música nova
        mixer.init() ##Inicializa o mixer do Pygame
        selecionar = filedialog.askdirectory() ##Abre uma janela para selecionar um diretório de arquivos, que será armazenado na variável selecionar
        for root, dirs, files in os.walk(selecionar): ##Percorre recursivamente a variável selecionar e retorna três valores em cada iteração:
            for file in files:                        ##root (caminho da raiz do diretório), dirs (uma lista de subdiretórios) e files (uma lista de arquivos)
                if file.endswith(".mp3"): ##Verifica se o arquivo possui a extensão ".mp3"
                    filepath = os.path.join(root, file) ##Combina o caminho do diretório atual com o nome do arquivo para obter o caminho completo do arquivo
                    self.playlist.append(filepath) ##Adiciona o caminho completo do arquivo à lista de reprodução
                    filename = os.path.basename(filepath) ##Extrai o nome do arquivo do caminho completo
                    self.lista.addItem(filename) ##Adiciona o nome do arquivo a playlist visual
        if not self.playlist: ##Se a lista de reprodução estiver vazia, a função retorna sem fazer mais nada
            return
        
        self.item = 0 ##Define o índice da música atual como 0 (primeira música da lista)
        self.reproduzirmusica() ##Inicia a reprodução da música atual

    def reproduzirmusica(self):
        if self.item >= len(self.playlist): ##Verifica se o índice atual é <= ao tamanho da playlist
            return                          ##Se for verdadeiro,todas as músicas da lista foram reproduzidas e a função retorna, encerrando a reprodução

        item = self.playlist[self.item] ##Obtém o caminho completo do arquivo de música atual da lista de reprodução, com base no índice atual
        mixer.music.load(item) ##Carrega a música especificado pelo caminho item para reprodução
        mixer.music.play() ##Inicia a reprodução da música atual

    def pararmusica(self): ##Função parar parar e limpar a playlist
        mixer.music.stop() ##Para o mixer do Pygame
        self.playlist.clear() ##limpa a playlist de músicas
        self.lista.clear() ##Limpa a lista visual de músicas
        self.item = 0 ##Define o índice da música atual como 0 novamente

    def pausarmusica(self): ##Função para pausar a música atual
        mixer.music.pause() ##Pausa o mixer do Pygame

    def retomarmusica(self): ##Função para retormar a música pausada
        mixer.music.unpause() ##"Despausa" o mixer do Pygame

    def proximamusica(self): ##Função para pular a música atual
        self.item += 1 ##Incrementa o valor da variável item em 1
        if self.item >= len(self.playlist): ##Verifica se o valor de item é maior ou igual ao tamanho da lista de reprodução... 
            self.item = 0                   ##...Se for verdadeiro, significa que todas as músicas da lista foram reproduzidas e, nesse caso...
        self.reproduzirmusica()             ##...O índice é resetado para 0, ou seja, a reprodução volta à primeira música da lista

    def voltarmusica(self): ##Função para voltar para música anterior
        self.item -= 1 ##Diminui o valor da variável item em 1
        if self.item < 0:                      ##Verifica se o valor de item é menor que 0. Se for verdadeiro, significa que a reprodução está na primeira...
            self.item = len(self.playlist) - 1 ##...Música da lista e, nesse caso, o índice é definido para o último elemento da lista de reprodução
        self.reproduzirmusica() ##inicia a reprodução da música atual

    def reproduzirmusicaselecionada(self, item): ##Função para reproduzir a música seleciona a partir da lista visual
        index = self.lista.row(item) ##Obtém o índice da linha selecionada na lista visual de músicas, representada pela variável item
        self.item = index       ##Atribui o valor do índice obtido à variável item  Isso atualiza o índice da música atual na...
        self.reproduzirmusica() ##...Lista de reprodução para corresponder à música selecionada pelo usuário na lista visual


if __name__ == "__main__": ##Verifica se o arquivo Python está sendo executado diretamente, e não importado como um módulo por outro arquivo
    app = QApplication(sys.argv) ##Instancia a classe QApplication
    app.setStyle("Fusion") ##Define o estilo visual da aplicação como "Fusion"
    mainWin = MP3Player() ##Instancia a classe principal
    mainWin.show() ## Exibe a janela principal da aplicação
    sys.exit(app.exec()) ##Inicia o loop de eventos da aplicação
