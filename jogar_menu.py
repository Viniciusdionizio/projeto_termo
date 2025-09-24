import curses,time
from biblioteca import biblioteca_br,biblioteca_eng


def curses_input(stdscr, prompt="",pos=(10,10)): #input no curses
	stdscr.addstr(0,0,prompt)
	stdscr.refresh()
	curses.echo()
	s = stdscr.getstr(pos[0], pos[1]+len(prompt))
	curses.noecho()
	return s.decode("utf-8")    

def jogar_menu(stdscr):
	curses.curs_set(0)
	stdscr.nodelay(False)
	altura,largura = stdscr.getmaxyx()
	x = largura//2
	y = altura//2

	curses.init_pair(1, curses.COLOR_WHITE,curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_WHITE,curses.COLOR_YELLOW)
	curses.init_pair(3, curses.COLOR_WHITE,curses.COLOR_GREEN)
    
	def letras(palavra):
		dicc = {}
		for i in palavra:
			dicc[i] = 0
		for i in palavra:
			dicc[i] += 1
		return dicc

	def printar_palavra(stdscr):
		palavra = 'furar'
		contador = 0

		while True:
			dicc=letras(palavra)
			if contador > 5:
				stdscr.addstr(y,x-4,'DERROTA!')
				stdscr.refresh()
				stdscr.getch()
				break
			contador +=1
			while True:  # repete até o jogador digitar 5 letras
				a = curses_input(stdscr, "", ((y-10)+contador*3, x-5//2))
				if len(a) == 5:
					break
				else:
					stdscr.addstr(3, x-(27//2),"DIGITE EXATAMENTE 5 LETRAS!", curses.color_pair(1))
					stdscr.refresh()
					time.sleep(1.5)
					stdscr.move(3, x-(27//2))   # limpa aviso
					stdscr.clrtoeol()
					stdscr.move((y-10)+contador*3, x-5)
					stdscr.clrtoeol()
					stdscr.refresh()
				
			for i in range(5):
				letra=a[i]
				if letra == palavra[i]:
					dicc[letra]-=1
					stdscr.addstr((y-10)+contador*3,x-len(a)//2+i,f'{letra}',curses.color_pair(3))
				stdscr.refresh()
			for j in range(5):
				letra=a[j]
				if letra != palavra[j]:
					if letra not in dicc.keys() or dicc[letra]==0:
						stdscr.addstr((y-10)+contador*3,x-len(a)//2+j,f'{letra}',curses.color_pair(1))
					else: 
						stdscr.addstr((y-10)+contador*3,x-len(a)//2+j,f'{letra}',curses.color_pair(2))
						dicc[letra]-=1
			stdscr.refresh()
				
			if a == palavra:
				stdscr.addstr(3,x-7,'VITÓRIA!!',curses.color_pair(3))
				stdscr.refresh()
				time.sleep(3)
				break

	printar_palavra(stdscr)
curses.wrapper(jogar_menu)
