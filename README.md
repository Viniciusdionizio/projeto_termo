Termo (Wordle) — Versão Terminal em Python

Recriação simples do jogo Termo (Wordle) para terminal, desenvolvida em Python com as bibliotecas: curses, time e random.

Como jogar:  
- O jogo escolhe uma palavra secreta de 5 letras.  
- Você tem 6 tentativas para adivinhar no modo solo, e 7 para adivinhar no mo dueto.  
- Digite uma palavra e pressione Enter.  
- O jogo indica o resultado de cada letra com cores:

🟩 Verde → letra correta e na posição certa  
🟨 Amarelo → letra existe, mas em outra posição  
🟥 Vermelho → letra não está na palavra  

Executar:  
bash
python3 termo.py
