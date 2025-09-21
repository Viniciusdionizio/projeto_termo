import curses,time
from biblioteca import biblioteca_br,biblioteca_eng


def curses_input(stdscr, prompt="",pos=[0,0]): #input no curses
	stdscr.clear()
	stdscr.addstr(pos[0],pos[1],prompt)
	stdscr.refresh()
	curses.echo()
	s = stdscr.getstr(0, len(prompt))
	curses.noecho()
	return s.decode("utf-8")    

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    altura,largura = stdscr.getmaxyx()
    text=['Jogar','Ranking','Opções','Sair']
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

        if key == curses.KEY_UP and select!=0: #para cima
            select-=1
            stdscr.clear()
        elif key == curses.KEY_DOWN and select<len(text)-1: #para baixo
            select+=1
        elif key == curses.KEY_ENTER or key in [10,13]: #enter
            stdscr.clear()
            stdscr.getch()
            if select == len(text)-1: #sair
                break
            if select == 0: #jogar
                stdscr.clear()
        elif key == 27: #se apertar esc vai quebrar
            break

        stdscr.refresh()

curses.wrapper(main_menu)
