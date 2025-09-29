import curses, time
from biblioteca import biblioteca_br, dicionario_letras


def curses_input(stdscr, prompt="", pos=(10,10)):
    stdscr.refresh()
    curses.echo()
    s = stdscr.getstr(pos[0],pos[1]+len(prompt))
    curses.noecho()
    return s.decode("utf-8") 

def printar_teclado(stdscr, alfabeto, y, x):
    layout = ["ABCDEFGHI","JKLMNOPQR","STUVWXYZ"]
    for linha_idx,linha in enumerate(layout):
        for colunn_idx,letra in enumerate(linha):
            if alfabeto[letra] > 0:
                cor = curses.color_pair(alfabeto[letra])
            else: 
                cor = curses.color_pair(0)
            stdscr.addstr(y + linha_idx,x + colunn_idx*3, letra, cor)

def jogar_menu(stdscr):
    curses.resizeterm(40,152)
    stdscr.clear()
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

    def printar_palavra(stdscr, modo):
        palavra1 = biblioteca_br()
        palavra2 = biblioteca_br()
        p1=p2=0
        contador=0
        while palavra2 == palavra1:
            palavra2 = biblioteca_br()

        alfabeto = {chr(c): 0 for c in range(ord('A'), ord('Z')+1)}

        if modo == 1:
            limite = 7
        else:
            limite = 6

        while True:
            stdscr.addstr(3, x-34, "DIGITE UMA PALAVRA DE 5 LETRAS: ")
            stdscr.refresh()
            if contador >= limite:
                stdscr.move(3, x-34)
                stdscr.clrtoeol()
                stdscr.addstr(3, x-5, "DERROTA!!!", curses.color_pair(1))
                if modo==0:
                    stdscr.addstr(4, x-10, f"A PALAVRA ERA {palavra1.upper()}", curses.color_pair(1))
                else: 
                    stdscr.addstr(4, x-14, f"AS PALAVRAS ERAM {palavra1.upper()} E {palavra2.upper()}", curses.color_pair(1))
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
                break
            contador += 1

            while True: #recebe a palavara
                entrada = curses_input(stdscr, "", (3, x-5//2))
                lower = entrada.lower()
                upper = entrada.upper()
                if len(entrada) == 5 and entrada.isalpha():
                    stdscr.move(3, x-5//2)
                    stdscr.clrtoeol()
                    break
                else:
                    stdscr.move(3, x-34)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-(27//2), "DIGITE EXATAMENTE 5 LETRAS!", curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(1)
                    stdscr.move(3, x-34)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-34, "DIGITE UMA PALAVRA DE 5 LETRAS: ")
                    stdscr.refresh()

#parte solo
            if modo == 0:
                cores = [1] * 5
                usados = letras(palavra1)
                for i in range(5):
                    if lower[i] == palavra1[i]:
                        cores[i] = 3
                        usados[lower[i]] -= 1
                for i in range(5):
                    if cores[i] == 1 and lower[i] in usados and usados[lower[i]] > 0:
                        cores[i] = 2
                        usados[lower[i]] -= 1

                for i in range(5): #teclado solo
                    letra = upper[i]
                    if cores[i] == 3:
                        alfabeto[letra] = 3
                    elif cores[i] == 2 and alfabeto[letra] < 2:
                        alfabeto[letra] = 2
                    elif cores[i] == 1 and alfabeto[letra] == 0:
                        alfabeto[letra] = 1

                for i in range(5): #mostra no display
                    display = dicionario_letras(upper[i])
                    for linha_idx, linha in enumerate(display):
                        stdscr.addstr((y-17)+contador*4+linha_idx, x-20//2+4*i, linha, curses.color_pair(cores[i]))
                    stdscr.refresh()
                    time.sleep(0.15)

                if lower == palavra1: #se acertar
                    stdscr.move(3, x-34)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-5, "VITÓRIA!!!", curses.color_pair(3))
                    stdscr.refresh()
                    stdscr.getch()
                    stdscr.clear()
                    break

#parte dueto
            else:
                cores1 = [1] * 5
                cores2 = [1] * 5
                usados1 = letras(palavra1)
                usados2 = letras(palavra2)

                for i in range(5): #cores palavra 1
                    if lower[i] == palavra1[i]:
                        cores1[i] = 3
                        usados1[lower[i]] -= 1
                for i in range(5):
                    if cores1[i] == 1 and lower[i] in usados1 and usados1[lower[i]] > 0:
                        cores1[i] = 2
                        usados1[lower[i]] -= 1

                for i in range(5): #cores palavra2
                    if lower[i] == palavra2[i]:
                        cores2[i] = 3
                        usados2[lower[i]] -= 1
                for i in range(5):
                    if cores2[i] == 1 and lower[i] in usados2 and usados2[lower[i]] > 0:
                        cores2[i] = 2
                        usados2[lower[i]] -= 1

                for i in range(5): #teclado dueto compartilhado
                    letra = upper[i]
                    melhor = max(cores1[i], cores2[i])
                    if melhor > alfabeto[letra]:
                        alfabeto[letra] = melhor

                for i in range(5): #mostra o display na tela das 2 colunas de palavras lá
                    display = dicionario_letras(upper[i])
                    for linha_idx, linha in enumerate(display):
                        if p1==0: #se acertar para de mostrar
                            stdscr.addstr((y-17)+contador*4+linha_idx, x-30+4*i, linha, curses.color_pair(cores1[i]))
                        if p2==0: #mesma coisa
                            stdscr.addstr((y-17)+contador*4+linha_idx, x+10+4*i, linha, curses.color_pair(cores2[i]))
                    stdscr.refresh()
                    time.sleep(0.15)

                if lower == palavra1:
                    msg = "VOCÊ ACERTOU A PALAVRA 1!"
                    p1=1
                elif lower == palavra2:
                    msg = "VOCÊ ACERTOU A PALAVRA 2!"
                    p2=1      
                elif p1 == 1 and p2 == 1:
                    msg = "VITÓRIA!!!"
                else:
                    msg = None

                if msg:
                    stdscr.move(3, x-34)
                    stdscr.clrtoeol()
                    stdscr.addstr(3, x-len(msg)//2, msg, curses.color_pair(3))
                    stdscr.refresh()
                    time.sleep(1)                   
                    if p1==1 and p2==1:
                        stdscr.getch()
                        stdscr.clear()
                        break
                    else:
                        stdscr.move(3, x-34)
                        stdscr.clrtoeol()


            printar_teclado(stdscr, alfabeto, y+16, x-13)
            stdscr.refresh()
    
    def escolher_modo(stdscr):
        options=['SOLO','DUETO']
        altura,largura = stdscr.getmaxyx()
        select=0

        while True:
            stdscr.refresh()
            for i in range(len(options)): #mostra a opção que você está
                if i == select:
                    stdscr.addstr(altura//2+i,largura//2-2,options[i],curses.A_REVERSE)
                else:   
                    stdscr.addstr(altura//2+i,largura//2-2,options[i])
                
            key = stdscr.getch()

            if key == curses.KEY_UP and select != 0: #para cima
                select-=1
                stdscr.clear()
            elif key == curses.KEY_DOWN and select < len(options)-1: #para baixo
                select+=1
            elif key == curses.KEY_ENTER or key in [10,13]: #enter
                stdscr.clear()
                printar_palavra(stdscr,select)
                break

    escolher_modo(stdscr)

def aviso(stdscr):
    altura,largura = stdscr.getmaxyx()
    stdscr.addstr(altura//2, largura//2-23,'ESSE PROGRAMA DEVE SER RODADO EM TELA CHEIA!!!')
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()

def main_menu(stdscr): #parte do menu principal
    curses.resizeterm(40,152)
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(False)
    altura,largura = stdscr.getmaxyx()
    text=['JOGAR','SAIR']
    head=["████████╗███████╗██████╗ ███╗   ███╗ ██████╗ ",
          "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔═══██╗",
          "   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║",
          "   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║",
          "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝",
          "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ "]
    
    select=0
    x = largura//2 - len(text[0])//2
    y = altura//2

    aviso(stdscr)

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
