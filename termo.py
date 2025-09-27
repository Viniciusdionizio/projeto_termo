import curses, time
from biblioteca import biblioteca_br, dicionario_letras


def curses_input(stdscr, prompt="", pos=(10,10)):  # input no curses
    stdscr.refresh()
    curses.echo()
    s = stdscr.getstr(pos[0],pos[1]+len(prompt))
    curses.noecho()
    return s.decode("utf-8") 

def printar_teclado(stdscr, alfabeto, y, x):
    layout = ["ABCDEFGHI","JKLMNOPQR","STUVWXYZ"]
    for linha_idx,linha in enumerate(layout):
        for cor_idx,letra in enumerate(linha):
            if alfabeto[letra] > 0:
                cor = curses.color_pair(alfabeto[letra])
            else: cor = curses.color_pair(0)
            stdscr.addstr(y + linha_idx*2,x + cor_idx*3, letra, cor)

def jogar_menu(stdscr):
    stdscr.refresh()
    curses.curs_set(0)
    stdscr.nodelay(False)
    altura,largura = stdscr.getmaxyx()
    x = largura//2
    y = altura//2

    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_RED)
    curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_YELLOW)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_GREEN)

    def letras(palavra):
        dicc = {}
        for i in palavra:
            dicc[i] = 0
        for i in palavra:
            dicc[i] += 1
        return dicc

    def printar_palavra(stdscr):
        palavra = biblioteca_br()
        contador = 0
        alfabeto = {chr(c): 0 for c in range(ord('A'), ord('Z')+1)}

        while True:
            stdscr.addstr(3, x-22, "DIGITE UMA PALAVRA: ")
            stdscr.refresh()
            dicc = letras(palavra)

            if contador > 5:
                stdscr.move(3, x-22)
                stdscr.clrtoeol()
                stdscr.addstr(3, x-5, "DERROTA!!!", curses.color_pair(1))
                stdscr.refresh()
                time.sleep(3)
                stdscr.clear()
                break
            contador += 1

            while True:
                entrada = curses_input(stdscr, "", (3, x-5//2))
                a = entrada.lower()
                a_display = entrada.upper()
                if len(a) == 5:
                    stdscr.move(3, x-5//2)
                    stdscr.clrtoeol()
                    break
                else: #se for diferented e 5 letras
                    stdscr.move(3, x-22)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-(27//2), "DIGITE EXATAMENTE 5 LETRAS!", curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(1)
                    stdscr.move(3, x-22)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-22, "DIGITE UMA PALAVRA: ")
                    stdscr.refresh()

            cores = [1] * 5 #processa as cores 
            usados = dict(dicc)

            for i in range(5):
                if a[i] == palavra[i]:
                    cores[i] = 3
                    usados[a[i]] -= 1
            for i in range(5):
                if cores[i] == 1 and a[i] in usados and usados[a[i]] > 0:
                    cores[i] = 2
                    usados[a[i]] -= 1

            for i in range(5): # atualiza alfabeto
                letra = a_display[i]
                if cores[i] == 3:   
                    alfabeto[letra] = 3
                elif cores[i] == 2 and alfabeto[letra] < 2:
                    alfabeto[letra] = 2
                elif cores[i] == 1 and alfabeto[letra] == 0:
                    alfabeto[letra] = 1

            for i in range(5): #mostrar a palavra
                display = dicionario_letras(a_display[i])
                for linha_idx, linha in enumerate(display):
                    stdscr.addstr((y-17)+contador*4+linha_idx, x-20//2+4*i, linha, curses.color_pair(cores[i]))
                stdscr.refresh()
                time.sleep(0.15)

            printar_teclado(stdscr, alfabeto, y+14, x-13)
            stdscr.refresh()

            if a == palavra:
                stdscr.move(3, x-22)
                stdscr.clrtoeol()
                stdscr.addstr(3, x-5, "VITÓRIA!!!", curses.color_pair(3))
                stdscr.refresh()
                time.sleep(3)
                stdscr.clear()
                break

    printar_palavra(stdscr)

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    altura,largura = stdscr.getmaxyx()
    text=['Jogar','Ranking','Sair']
    head=["████████╗███████╗██████╗ ███╗   ███╗ ██████╗ ",
          "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔═══██╗",
          "   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║",
          "   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║",
          "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝",
          "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ "]
    
    select=0
    x = largura//2 - len(text[0])//2
    y = altura//2
    
    while True:
        stdscr.refresh()
        for j in range(len(head)): #imprime "TERMO" na tela
            w = largura//2-len(head[0])//2
            stdscr.addstr(y//2+j,w,head[j])
        
        for i in range(len(text)): #mostra a opção que você está
            if i == select:
                stdscr.addstr(y+i,x,text[i],curses.A_REVERSE)
            else:   
                stdscr.addstr(y+i,x,text[i])
        
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and select != 0: #para cima
            select-=1
            stdscr.clear()
        elif key == curses.KEY_DOWN and select < len(text)-1: #para baixo
            select+=1
        elif key == curses.KEY_ENTER or key in [10,13]: #enter
            stdscr.clear()
            if select == len(text)-1: #sair
                break
            if select == 0: #jogar
                jogar_menu(stdscr)
        elif key == 27: #se apertar esc vai quebrar
            break

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main_menu)
