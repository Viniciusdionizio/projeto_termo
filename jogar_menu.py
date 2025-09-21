import curses
from biblioteca import biblioteca_br,biblioteca_eng


def curses_input(stdscr, prompt="",pos=[10,10]): #input no curses
	stdscr.clear()
	stdscr.addstr(pos[0],pos[1],prompt)
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
    
	def erro(palavra):
		dicc = {}
		for i in palavra:
			dicc[i] = 0
		for i in palavra:
			dicc[i] += 1
		return dicc

	def letra_letra(palavra,p):
		lista_final=[]
		c = erro(p)
		lista = [*range(len(p))]
		for letra in palavra:
			for i in lista:
				if palavra[i] == p[i] and palavra[i] == letra:
					lista_final.append(palavra[i])
					c[palavra[i]] -= 1
					lista.remove(i)
					break
		for i in lista:
			if palavra[i] in p and c[palavra[i]] > 0:
				lista_final.append(palavra[i])
				c[palavra[i]] -= 1
			else:
				lista_final.append(palavra[i])
		return lista_final

	def printar_palavra(stdscr):
		palavra = biblioteca_br()
		contador = 0

		while True:
			if contador > 5:
				stdscr.addstr('Derrota')
				break
			contador +=1
			a=curses_input(stdscr,"",[10,10])
			l = letra_letra(a, palavra)
			for i in range(len(l)):
				if l[i] == palavra[i]:
					stdscr.addstr(y,x+i,f'{l[i]}',curses.color_pair(3))
				elif l[i] != palavra[i]:
					stdscr.addstr(y,x+1,f'{l[i]}',curses.color_pair(1))
			if a == palavra:
				stdscr.clear()
				break
	printar_palavra(stdscr)
curses.wrapper(jogar_menu)