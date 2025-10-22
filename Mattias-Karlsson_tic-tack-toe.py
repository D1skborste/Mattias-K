from  random import randint


"""Tic-Tac-Toe. Spelaren möter datorn, som alltid börjar med 'X' i mitten. Spelaren för första moven,
därefter väljer datorn en ruta baserat på randint.
Att göra/buggar/notes längst ner"""

#Sätter initiala värden som att lägga spelplanen och pågående spel/runda
board = [[1,"O",3],[4,"O",6],[7,8,9]]
play = True
match = True
wincount = 0

#En print som gör spelplanen mer läsbar. går att förbättra
def display_board(board=board):
    print("==============")
    for i in board:
        print(i, sep="\n")

def new_board(board=board):
    #del board [:]
    board = [[1,2,3],[4,"O",6],[7,8,9]]
    return board

"""Spelarens move. playermove_is_legal kollar om spelaren har valt en ledig ruta. Då jag har döpt rutorna till
 nummer från 1-9 är det enkelt att räkna om till spelplanens index"""
def enter_move(board=board):
    playermove_is_legal = False
    
    # För att undvika att spelet crashar, försöker jag omvandla input till int med "try/except". Är det ej int krävs ny input
    while not playermove_is_legal:
        playermove_is_int = False    
        playermove = input("Provide your move with number 1-9: ")
        while not playermove_is_int:
            try:
                playermove = int(playermove)
                playermove_is_int = True
            except:
                playermove = input("Somethin went wrong. Are you sure it's a number? ")

# använder modulos operator för att placera pjäsen på rätt plats. 
        y = playermove % 3-1
        for x in board:
            if playermove in x: 
                x[y]="O"
                playermove_is_legal = True
                display_board()
                print("^ Player's move ^")
                return board
        print("That move is illegal, try again")
        

# Datorn är nästan copy-pastad från spelaren, skillnaden är att jag inte ger felmeddelande om datorn väljer en redan tagen ruta.
# Istället körs randint tills en ledig ruta hittas. Första feedbacken i konsolen är först när pjäs är lagd.
def draw_move(board=board):
    playermove_is_legal = False
    
    while not playermove_is_legal:
        playermove = randint(1, 9)
        
        y = playermove % 3-1
        for x in board:
            if playermove in x:
                x[y]="X"
                playermove_is_legal = True
                display_board()
                print("^ Computer's move ^")
                return board
    
# Med hjälp av len(set) kontrolleras om spelet är vunnet, då set inte kan innehålla dubletter kommer len ge 1, om alla är lika.
# Med hjälp av range(len), fås siffrorna för att navigera index för att kontrollera diagonala rutorna.
def checkDiagonals(board=board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

def returnwin(board=board):
#    board = checkDiagonals()
    flip_table = [[board[x][y] for x in range(len(board))] for y in range(len(board[0]))]
    for row in board:
        if len(set(row)) == 1: # Grund-kontrollen: "genom göra board[i] till set, och kontrolera längden"
            return row[0]
    for row in flip_table:
        if len(set(row)) == 1: # Här har spelplanen roterats 90 grader för att kontrolleras.
            return row[0]
    return 0


# if-satsen i föregående programmet matar ut "X" eller "O", om 3 lika hittas. Det kontrolleras för att se vilken spelare som vinner.

def victory_for():
    global wincount, match # Global keyword visar att funktionen kan påverka parametrar utanför sig själv.
    if returnwin() == "X":
        print("You lost! ")
        match = False
    elif returnwin() == "O":
        print("You won! ")
        wincount += 1
# Frågar om spelaren vill fortsätta, samt uppdaterar "while"-villkoren för att hålla pågående spel.
        match = False

def after_victory():
    global play
    response = input("Do you want to play again? (y/n): ")
    if response != "y":
        play = False
        print(f"Thank you for playing, you won {wincount} times!")
    
#Alla print är för felsökningen
"""Game loop"""
while play:
    print("1")
    match = True
    board = new_board()
    display_board()
    print("2")

    while match and play:
        print("3")

        board = enter_move()
        victory_for()
        if not match:
            break
        print("4")

        board = draw_move()
        victory_for()
        print("5")

    if not match:
        after_victory()
        print("6")

       # continue
    
# Kan modifiera play och match, och checka mellan varje steg i game loop. 
# Men vill undvika om möjligt (if play or not match: break)


"""Att göra: 
1. Justera gameplay loop. Alla "gameplay mechanics" fungerar separat, men win condition fungerar inte.
    ska möblera om (match/play = True/False, if response mm...)
2. Diagonal board check krockar med tableflip.
3. Behöver flytta på promptsen. Ville ha en clean game loop men kanske behöver sätta några checkar
4. board återställs ej. ska utforska
5. Göra snyggare print/board

Notes: Det fanns olika metoder för 'table_flip', den jag har i koden var mest lik det min originaltanke.
Man kan även importera numpy och använda sig av 'transpose', som jag inte har prövat än.
Man kan även använda *zip. Det kan vara värt att pröva, men jag tror inte att problemen försvinner
genom att byta metod."""