class Game:
    def __init__(self):
        self.board = self.create_initial_board() # 2D lista koja predstavlja šahovsku ploču s figurama
        self.moveFunctions = self.create_move_functions() # dictionary koji mapira figure na njihove funkcije poteza

        #potrebni checkeri i liste za spremanje poteza
        self.white_on_move = True
        self.move_log = [] 
        self.pins_list = []
        self.checks_list = []
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.enpassant_legal_indexes = () #Tuple koji sadrži indexe na kojima je moguće izvesti en-passant potez
        self.white_king_index = (7, 4)
        self.black_king_index = (0, 4)

        #CastlingPermission je klasa koja sadrži informacije o tome može li se izvesti castling za sve 4 moguće pozicije (za bijelog i crnog kralja)
        self.castling_permissions = CastlingPermission(True, True, True, True)


    def create_initial_board(self): #funkcija koja vraća početnu šahovsku ploču s imenima figura koje su nam u folderu images da ih kasnije možemo iscrtati
        return [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def create_move_functions(self):
        return {
            "p": self.getPawnMoves,
            "R": self.getRookMoves,
            "N": self.getKnightMoves,
            "B": self.getBishopMoves,
            "Q": self.getQueenMoves,
            "K": self.getKingMoves
        }
    
    #MOVE FUNKCIJE
    def execute_normal_move(self, move):

        start_r, start_c = move.start_r, move.start_c
        end_r, end_c = move.end_r, move.end_c
        movedFigureName = move.movedFigureName

        self.board[start_r][start_c] = "empty" #makni figuru s početne pozicije
        self.board[end_r][end_c] = movedFigureName #postavi figuru na krajnju poziciju
        self.move_log.append(move) #dodaj potez u log poteza
        if self.white_on_move: #ako je bijeli na potezu, postavi da je crni na potezu
            self.white_on_move = False
        else: #ako je crni na potezu, postavi da je bijeli na potezu
            self.white_on_move = True
        self.update_king_location(move) #ako je potez pomaknuo kralja, ažuriraj njegovu poziciju (ako nije ostat će ista)

    def update_king_location(self, move): #ako je potez pomaknuo kralja, ažuriraj njegovu poziciju
        movedFigureName = move.movedFigureName
        if (movedFigureName == "wK"): #ako je bijeli kralj pomaknut, ažuriraj njegovu poziciju
            self.white_king_index = (move.end_r, move.end_c)
        elif (movedFigureName == "bK"): #ako je crni kralj pomaknut, ažuriraj njegovu poziciju
            self.black_king_index = (move.end_r, move.end_c)

    def handle_pawn_promotion(self, move): #ako je potez promocija pješaka, promijeni ime figure na ploči u kraljicu => automatski će se onda iscrtati kraljica na sljedećem pozivu drawBoard funkcije
        if move.is_pawn_promotion:
            movedFigureName = move.movedFigureName
            self.board[move.end_r][move.end_c] = movedFigureName[0] + "Q" #promijeni ime figure na ploči u kraljicu => nema biranja figure za promociju, uvijek se promovira u kraljicu jer je to najbolja opcija
        #Mogući TODO - dodati mogućnost biranja figure za promociju

    def handle_enpassant_move(self, move):
        if move.isEnpassantMove:
            self.board[move.start_r][move.end_c] = "empty" #makni pješaka koji je napravio en-passant potez
        
        movedFigureName = move.movedFigureName
        start_r, end_r = move.start_r, move.end_r
        start_c = move.start_c
        if ((movedFigureName[1] == "p") and (abs(start_r - end_r) == 2)): #ako je trenutni potez, početni potez pomaka pješaka za 2 mjesta, postavi enpassant_legal_indexe na polje iznad ili ispod pješaka koji je napravio potez
            self.enpassant_legal_indexes = ((start_r + end_r) // 2, start_c) #postavi enpassant_legal_indexes na polje iznad ili ispod pješaka koji je napravio potez
        else:
            self.enpassant_legal_indexes = ()

    def handle_castle_move(self, move):
        end_r, end_c = move.end_r, move.end_c
        if move.isCastlingMove: #ako je potez castling, izračunaj nove pozicije topa
            if ((end_c - move.start_c) == 2): #kralj ide na desnu stranu
                rook_start_c = end_c + 1
                rook_end_c = end_c - 1
            else: #kralj ide na lijevu stranu
                rook_start_c = end_c - 2
                rook_end_c = end_c + 1

            self.board[end_r][rook_end_c] = self.board[end_r][rook_start_c] #premjesti topa na odgovarajuću poziciju
            self.board[end_r][rook_start_c] = 'empty' #makni topa s početne pozicije

    def update_castling_permissions_captured_rook(self, move): #ako je top pojeden, miču se prava za castling jer ga nema
        end_c = move.end_c
        capturedFigureName = move.capturedFigureName

        if (capturedFigureName == "wR"): #ako je pojeden bijeli top
            if (end_c == 0): #ako je pojeden top s lijeve strane
                self.castling_permissions.white_queen_side = False #nema više prava za castling na lijevoj strani
            elif (end_c == 7): #ako je pojeden top s desne strane
                self.castling_permissions.white_king_side = False #nema više prava za castling na desnoj strani
        elif (capturedFigureName == "bR"): #ako je pojeden crni top
            if (end_c == 0): #ako je pojeden top s lijeve strane
                self.castling_permissions.black_queen_side = False #nema više prava za castling na lijevoj strani
            elif (end_c == 7): #ako je pojeden top s desne strane
                self.castling_permissions.black_king_side = False #nema više prava za castling na desnoj strani

    def update_castling_permissions_moved_king_or_rook(self, move): #ako je kralj ili top pomaknut, miču se prava za castling jer su se pomaknuli
        start_r, start_c = move.start_r, move.start_c
        movedFigureName = move.movedFigureName

        if ((movedFigureName == 'wK') or (movedFigureName == 'bK')): #ako je pomaknut kralj, nema više prava za castling uopce
            self.castling_permissions.white_queen_side = False
            self.castling_permissions.white_king_side = False
            self.castling_permissions.black_queen_side = False
            self.castling_permissions.black_king_side = False
        elif ((movedFigureName == 'wR') and (start_r == 7)): #ako je pomaknut bijeli top
            if (start_c == 0): #ako je pomaknut top s lijeve strane
                self.castling_permissions.white_queen_side = False #nema više prava za castling na lijevoj strani
            elif (start_c == 7): #ako je pomaknut top s desne strane
                self.castling_permissions.white_king_side = False #nema više prava za castling na desnoj strani
        elif ((movedFigureName == 'bR') and (start_r == 0)): #ako je pomaknut crni top
            if (start_c == 0): #ako je pomaknut top s lijeve strane
                self.castling_permissions.black_queen_side = False   #nema više prava za castling na lijevoj strani
            elif (start_c == 7): #ako je pomaknut top s desne strane
                self.castling_permissions.black_king_side = False #nema više prava za castling na desnoj strani

    def updateCastlingPermission(self, move):
        self.update_castling_permissions_captured_rook(move)
        self.update_castling_permissions_moved_king_or_rook(move)

    def makeMove(self, move):
        self.execute_normal_move(move)
        self.handle_pawn_promotion(move)
        self.handle_enpassant_move(move)
        self.handle_castle_move(move)
        self.updateCastlingPermission(move)

    def getPawnMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za pješaka sa (r,c)
        isPinned = False #checker je li figura pinana (tj da se ne može pomaknuti jer bi se kralj našao u šahu)
        pinDirection = () #smjer pina
        for i in range(len(self.pins_list) - 1, -1, -1): #za svaki pin u listi pinova, -1 jer idemo od kraja prema početku
            if ((self.pins_list[i][0] == r) and (self.pins_list[i][1] == c)): #ako je trenutni pin na poziciji (r,c) gdje je naš pješak
                isPinned = True #postavi da je figura pinana
                pinDirection = (self.pins_list[i][2], self.pins_list[i][3]) #dohvati smjer pina
                self.pins_list.remove(self.pins_list[i]) #makni pin iz liste jer je već provjeren
                break

        if self.white_on_move: #ako je bijeli na potezu
            moveIncrement = -1 #pješak se kreće prema gore
            start_r = 6 #početni redak za bijelog pješaka
            color_enemy = "b" #enemy je crni
            king_r, king_c = self.white_king_index #pozicija bijelog kralja
        else: #ako je crni na potezu
            moveIncrement = 1 #pješak se kreće prema dolje
            start_r = 1 #početni redak za crnog pješaka
            color_enemy = "w" #enemy je bijeli
            king_r, king_c = self.black_king_index #pozicija crnog kralja

        if (self.board[r + moveIncrement][c] == "empty"):  # ako je polje ispred pješaka prazno
            if ((not isPinned) or (pinDirection == (moveIncrement, 0))): #ako figura nije pinana ili je pinana u smjeru kretanja - jer ako je pinana u tom smjeru smije se pomaknuti jer će i dalje čuvati kralja
                moves.append(MoveSpecs((r, c), (r + moveIncrement, c), self.board)) #dodaj potez pomaka pješaka za 1 polje
                if ((r == start_r) and (self.board[r + 2 * moveIncrement][c] == "empty")):  # ako je pješak na početnoj poziciji i polje na koje bi se pomaknuo za 2 polja je prazno
                    moves.append(MoveSpecs((r, c), (r + 2 * moveIncrement, c), self.board)) #smije se pomaknuti za 2 polja
        if (c - 1 >= 0):  # jedenje lijevo
            if ((not isPinned) or (pinDirection == (moveIncrement, -1))): #ako figura nije pinana ili je pinana u smjeru kretanja - jer ako je pinana u tom smjeru smije se pomaknuti jer će i dalje čuvati kralja
                if (self.board[r + moveIncrement][c - 1][0] == color_enemy): # ako je polje lijevo od pješaka enemy figura
                    moves.append(MoveSpecs((r, c), (r + moveIncrement, c - 1), self.board)) #dodaj potez jedenja lijevo
                if ((r + moveIncrement, c - 1) == self.enpassant_legal_indexes): #ako je polje lijevo od pješaka polje na kojem je moguće izvesti en-passant potez
                    attackingFigure = False 
                    blockingFigure = False
                    if (king_r == r): #ako je kralj u istom retku kao i pješak
                        if (king_c < c):
                            inside_range = range(king_c + 1, c - 1)
                            outside_range = range(c + 1, 8)
                        else:
                            inside_range = range(king_c - 1, c, -1)
                            outside_range = range(c - 2, -1, -1)
                        for i in inside_range:
                            if (self.board[r][i] != "empty"):
                                blockingFigure = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if ((square[0] == color_enemy) and (square[1] == "R" or square[1] == "Q")):
                                attackingFigure = True
                            elif (square != "empty"):
                                blockingFigure = True
                    if ((not attackingFigure) or blockingFigure):
                        moves.append(MoveSpecs((r, c), (r + moveIncrement, c - 1), self.board, isEnpassantMove=True))
        if (c + 1 <= 7): # jedenje desno
            if ((not isPinned) or (pinDirection == (moveIncrement, +1))):
                if (self.board[r + moveIncrement][c + 1][0] == color_enemy):
                    moves.append(MoveSpecs((r, c), (r + moveIncrement, c + 1), self.board))
                if ((r + moveIncrement, c + 1) == self.enpassant_legal_indexes):
                    attackingFigure = blockingFigure = False
                    if (king_r == r):
                        if (king_c < c):
                            inside_range = range(king_c + 1, c)
                            outside_range = range(c + 2, 8)
                        else:
                            inside_range = range(king_c - 1, c + 1, -1)
                            outside_range = range(c - 1, -1, -1)
                        for i in inside_range:
                            if (self.board[r][i] != "empty"):
                                blockingFigure = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if ((square[0] == color_enemy) and (square[1] == "R" or square[1] == "Q")):
                                attackingFigure = True
                            elif (square != "empty"):
                                blockingFigure = True
                    if ((not attackingFigure) or blockingFigure):
                        moves.append(MoveSpecs((r, c), (r + moveIncrement, c + 1), self.board, isEnpassantMove=True))
    
    def getKnightMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za konja sa (r,c)
        isPinned = False # checker je li figura pinana
        for i in range(len(self.pins_list) - 1, -1, -1): #za svaki pin u listi pinova
            if ((self.pins_list[i][0] == r) and (self.pins_list[i][1] == c)): #ako je trenutni pin na poziciji (r,c) gdje je naš konj
                isPinned = True #postavi da je figura pinana
                self.pins_list.remove(self.pins_list[i]) #makni pin iz liste jer je već provjeren
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))  # mogući potezi konja

        if self.white_on_move:
            color_ally = "w"
        else:
            color_ally = "b"
        for move in knightMoves: #za svaki mogući potez konja
            end_r = r + move[0] #izračunaj krajnji redak na koji želimo pomaknuti konja
            end_c = c + move[1] #izračunaj krajnji stupac na koji želimo pomaknuti konja
            if ((0 <= end_r <= 7) and (0 <= end_c <= 7)): #ako je krajnje polje unutar ploče
                if not isPinned: #ako figura nije pinana
                    end_figure = self.board[end_r][end_c] #koja je figura na krajnjem polju
                    if (end_figure[0] != color_ally):  #ili je prazno polje ili je enemy figura
                        moves.append(MoveSpecs((r, c), (end_r, end_c), self.board)) #dodaj potez pomaka konja (ili će pojesti ili se samo pomaknuti)

    def getRookMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za topa sa (r,c)
        isPinned = False #checker je li figura pinana
        pinDirection = ()
        for i in range(len(self.pins_list) - 1, -1, -1): #za svaki pin u listi pinova
            if ((self.pins_list[i][0] == r) and (self.pins_list[i][1] == c)): #ako je trenutni pin na poziciji (r,c) gdje je naš top
                isPinned = True #postavi da je figura pinana
                pinDirection = (self.pins_list[i][2], self.pins_list[i][3]) #dohvati smjer pina
                if (self.board[r][c][1] != "Q"):  #ako je figura pinana, ali nije kraljica, onda se ne može pomaknuti jer bi se kralj našao u šahu
                    self.pins_list.remove(self.pins_list[i])
                break

        rookMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))  #mogući smjerovi za topa: gore, lijevo, dolje, desno
        if self.white_on_move: #ako je bijeli na potezu
            color_enemy = "b" #enemy je crni
        else: #ako je crni na potezu
            color_enemy = "w" #enemy je bijeli
        for move in rookMoves: #za svaki mogući smjer topa
            for i in range(1, 8): #za svaku moguću udaljenost od topa
                end_r = r + move[0] * i #izračunaj krajnji redak
                end_c = c + move[1] * i #izračunaj krajnji stupac
                if ((0 <= end_r <= 7) and (0 <= end_c <= 7)):  # provjera je li krajnje polje unutar ploče
                    if ((not isPinned) or (pinDirection == move) or (pinDirection == (-move[0], -move[1]))): #ako figura nije pinana ili je pinana u smjeru kretanja - jer ako je pinana u tom smjeru smije se pomaknuti jer će i dalje čuvati kralja
                        end_figure = self.board[end_r][end_c] #koja je figura na krajnjem polju
                        if (end_figure == "empty"):  #ako je krajnje polje prazno
                            moves.append(MoveSpecs((r, c), (end_r, end_c), self.board)) #dodaj potez pomaka topa
                        elif (end_figure[0] == color_enemy):  #ako je krajnje polje enemy figura
                            moves.append(MoveSpecs((r, c), (end_r, end_c), self.board)) #dodaj potez jedenja enemy figure
                            break
                        else:  #ally figura
                            break
                else:  # end square je izvan ploče
                    break

    def getBishopMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za lovca sa (r,c)
        isPinned = False #checker je li figura pinana
        pinDirection = () #smjer pina
        for i in range(len(self.pins_list) - 1, -1, -1): #za svaki pin u listi pinova
            if ((self.pins_list[i][0] == r) and (self.pins_list[i][1] == c)): #ako je trenutni pin na poziciji (r,c) gdje je naš lovac
                isPinned = True #postavi da je figura pinana
                pinDirection = (self.pins_list[i][2], self.pins_list[i][3]) #dohvati smjer pina
                self.pins_list.remove(self.pins_list[i]) #makni pin iz liste jer je već provjeren
                break

        bishopMoves = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # mogući smjerovi za lovca
        if self.white_on_move:
            color_enemy = "b"
        else:
            color_enemy = "w"
        for move in bishopMoves: #za svaki mogući smjer lovca
            for i in range(1, 8): #za svaku moguću udaljenost od lovca
                end_r = r + move[0] * i #izračunaj krajnji redak
                end_c = c + move[1] * i #izračunaj krajnji stupac
                if ((0 <= end_r <= 7) and (0 <= end_c <= 7)):  # provjera je li krajnje polje unutar ploče
                    if not isPinned or pinDirection == move or pinDirection == (-move[0], -move[1]): #ako figura nije pinana ili je pinana u smjeru kretanja - jer ako je pinana u tom smjeru smije se pomaknuti jer će i dalje čuvati kralja
                        end_figure = self.board[end_r][end_c] #koja je figura na krajnjem polju
                        if (end_figure == "empty"):  #ako je krajnje polje prazno
                            moves.append(MoveSpecs((r, c), (end_r, end_c), self.board)) #dodaj potez pomaka lovca
                        elif (end_figure[0] == color_enemy):  #ako je krajnje polje enemy figura
                            moves.append(MoveSpecs((r, c), (end_r, end_c), self.board)) #dodaj potez jedenja enemy figure (pojesti će)
                            break
                        else:  #ally figura
                            break
                else:  # end square je izvan ploče
                    break

    def getQueenMoves(self, r, c, moves): #kraljica je kombinacija topa i lovca pa je najlakše samo pozvati funkcije za topa i lovca

        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getPinsAndChecks(self): #funkcija koja provjerava je li trenutni igrač u šahu i ako je, provjerava je li figura pinana
        pins_list = []  # lista koja čuva polja (r,c) koja su pinana i smjer pina - PIN je kada figura ne može napraviti potez jer bi se kralj našao u šahu (tj ona čuva kralja od šaha)
        checks_list = []  # lista koja čuva polja (r,c) koja su u šahu i smjer šaha
        in_check = False # checker je li trenutni igrač u šahu
        if self.white_on_move: #bijeli na potezu
            color_enemy = "b" #enemy je crni
            color_ally = "w" #ally je bijeli
            start_r = self.white_king_index[0] #trenutni redak kralja
            start_c = self.white_king_index[1] #trenutni stupac kralja
        else: #obrnuto
            color_enemy = "w"
            color_ally = "b"
            start_r = self.black_king_index[0]
            start_c = self.black_king_index[1]
        # 8 mogućih smjerova u kojima se može napasti kralj (4 vertikalna/horizontalna i 4 dijagonalna)
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)): # za svih 8 smjerova
            direction = directions[j] #dohvati trenutni smjer
            available_pin = () #dostupni pin - prazan tupple
            for i in range(1, 8): #za svaku moguću udaljenost od kralja
                end_r = start_r + direction[0] * i #izračunaj krajnji redak
                end_c = start_c + direction[1] * i #izračunaj krajnji stupac
                if ((0 <= end_r <= 7) and (0 <= end_c <= 7)): #ako je krajnje polje unutar ploče
                    end_figure = self.board[end_r][end_c] #dohvati figuru na krajnjem polju
                    if ((end_figure[0] == color_ally) and (end_figure[1] != "K")): #ako je krajnje polje ally figura i nije kralj
                        if (available_pin == ()): 
                            available_pin = (end_r, end_c, direction[0], direction[1]) #moguće da je ta ally figura pinana od strane enemy figure
                        else:  # neka druga ally figura blokira pin ali spremamo najbližu figuru koja je pinana
                            break
                    elif (end_figure[0] == color_enemy): #ako je krajnje polje enemy figura
                        enemy_figure = end_figure[1] #dohvati koja je to figura
                        # imamo 5 mogućnosti u ovom uvjetu: 
                        # a) okomito ili vodoravno udaljeno od kralja i figura je top
                        # b) dijagonalno udaljeno od kralja i figura je lovac
                        # c) 1 polje dijagonalno udaljeno od kralja i figura je pješak
                        # d) bilo kojim smjerom i figura je kraljica
                        # e) bilo kojim smjerom ali jedno polje udaljeno i figura je kralj
                        if ((0 <= j <= 3 and enemy_figure == "R") or (4 <= j <= 7 and enemy_figure == "B") or ( i == 1 and enemy_figure == "p" and ((color_enemy == "w" and 6 <= j <= 7) or (color_enemy == "b" and 4 <= j <= 5))) or (enemy_figure == "Q") or (i == 1 and enemy_figure == "K")):
                            if (available_pin == ()):  # ništa ne blokira tj pin je prazan pa je šah
                                in_check = True #checker na True
                                checks_list.append((end_r, end_c, direction[0], direction[1])) #dodaj u listu šahova to polje i smjer šaha
                                break
                            else:  # ako available_pin nije prazan, to znači da postoji figura koja blokira šah
                                pins_list.append(available_pin) #dodaj u listu pinova to polje i smjer pina
                                break
                        else:  # enemy figura nije u mogućnosti napasti kralja
                            break
                else: #izvan ploče
                    break 
        # Za konja moramo posebno jer ima drugačije poteze

        #Svi mogući potezi konja
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knightMoves: #za svaki mogući potez konja
            end_r = start_r + move[0] #izračunaj krajnji redak na koji želimo pomaknuti kralja
            end_c = start_c + move[1] #izračunaj krajnji stupac na koji želimo pomaknuti kralja
            if ((0 <= end_r <= 7) and (0 <= end_c <= 7)): #ako je krajnje polje unutar ploče
                end_figure = self.board[end_r][end_c] #koja je figura na krajnjem polju
                if ((end_figure[0] == color_enemy) and (end_figure[1] == "N")):  #ako neprijateljski konj napada kralja
                    in_check = True #checker na True
                    checks_list.append((end_r, end_c, move[0], move[1])) #dodaj u listu šahova to polje i smjer šaha

        return in_check, pins_list, checks_list #vrati je li igrač u šahu, listu pinova i listu šahova

    def getKingMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za kralja na (r,c)
        #Kralj ima 8 mogućih poteza, 4 dijagonalna i 4 vertikalna/horizontalna
        r_moves = (-1, -1, -1, 0, 0, 1, 1, 1) 
        c_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        if self.white_on_move: #ako je bijeli na potezu, postavi ally boju na bijelo
            color_ally = "w"
        else:
            color_ally = "b" #ako je crni na potezu, postavi ally boju na crno
        for i in range(8): #za svih 8 mogućih poteza
            end_r = r + r_moves[i] #izračunaj gdje će kralj završiti s obzirom na trenutni potez (redak)
            end_c = c + c_moves[i] #izračunaj gdje će kralj završiti s obzirom na trenutni potez (stupac)
            if ((0 <= end_r <= 7) and (0 <= end_c <= 7)): #ako je kralj unutar ploče
                end_figure = self.board[end_r][end_c] #dohvati figuru na toj poziciji
                if (end_figure[0] != color_ally):  #ako je figura neprijateljska ili prazno polje
                    # trebamo staviti kralja na to end polje ako neće biti check
                    if (color_ally == "w"):
                        self.white_king_index = (end_r, end_c) #postavi bijelog kralja na novu poziciju
                    else:
                        self.black_king_index = (end_r, end_c) #postavi crnog kralja na novu poziciju
                    in_check, pins_list, checks_list = self.getPinsAndChecks() #provjeri je li kralj u šahu
                    if not in_check: #ako kralj nije u šahu, dopusti potez
                        moves.append(MoveSpecs((r, c), (end_r, end_c), self.board))
                    # ako je kralj u šahu, ne dopusti potez tj. vrati kralja na staru poziciju
                    if (color_ally == "w"): 
                        self.white_king_index = (r, c)
                    else:
                        self.black_king_index = (r, c)

    def getAllAvailableMoves(self): #funkcija koja vraća sve moguće poteze koje trenutni igrač može napraviti
        moves = [] #lista svih mogućih poteza
        for r in range(len(self.board)): #za svaki redak
            for c in range(len(self.board[r])): #za svaki stupac
                move = self.board[r][c][0] #dohvati boju figure jer su figure oblika "bR", "wK" itd. pa je [0] boja figure
                if ((move == "w" and self.white_on_move) or (move == "b" and not self.white_on_move)): #ako je trenutni igrač na potezu, dodaj sve moguće poteze za tu figuru
                    figure = self.board[r][c][1] #dohvati tip figure jer su figure oblika "bR", "wK" itd. pa je [1] tip figure
                    self.moveFunctions[figure](r, c, moves)  # gore smo napravili dictionary koji mapira figure na njihove funkcije poteza, pa sada samo pozivamo funkciju za tu figuru
        return moves

    def isSquareUnderAttack(self, r, c): #funkcija koja provjerava je li polje (r,c) napadnuto
        # Ako je bijeli na potezu, stavimo da je zapravo crni da bi mogli provjeriti je li polje napadnuto od strane crnih figura i obratno
        if self.white_on_move:
            self.white_on_move = False
        else:
            self.white_on_move = True
        # Dohvati sve moguće poteze protivnika
        enemy_moves = self.getAllAvailableMoves()
        # Vrati da je bijeli na potezu
        if self.white_on_move:
            self.white_on_move = False
        else:
            self.white_on_move = True
        
        # Provjeri je li polje napadnuto od strane protivnika
        for move in enemy_moves: #za svaki potez protivnika
            if ((move.end_r == r) and (move.end_c == c)):  #ako je krajnje polje poteza protivnika jednako polju (r,c) => polje je napadnuto
                return True
        return False

    def isInCheck(self): #funkcija koja provjerava je li trenutni igrač u šahu
        if self.white_on_move: #ako je bijeli na potezu, provjeri je li bijeli kralj napadnut
            return self.isSquareUnderAttack(self.white_king_index[0], self.white_king_index[1]) #proslijediš poziciju bijelog kralja
        else: #ako je crni na potezu, provjeri je li crni kralj napadnut
            return self.isSquareUnderAttack(self.black_king_index[0], self.black_king_index[1]) #proslijediš poziciju crnog kralja

    def getRightSideCastleMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za castling na desnoj strani
        if ((self.board[r][c + 1] == 'empty') and (self.board[r][c + 2] == 'empty')): #ako su polja između kralja i topa prazna
            if ((not self.isSquareUnderAttack(r, c + 1)) and (not self.isSquareUnderAttack(r, c + 2))): #ako nijedno polje između kralja i topa nije napadnuto
                moves.append(MoveSpecs((r, c), (r, c + 2), self.board, isCastlingMove=True)) #dodaj potez castlinga

    def getLeftSideCastleMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za castling na lijevoj strani
        if ((self.board[r][c - 1] == 'empty') and (self.board[r][c - 2] == 'empty') and (self.board[r][c - 3] == 'empty')): #ako su polja između kralja i topa prazna
            if ((not self.isSquareUnderAttack(r, c - 1)) and (not self.isSquareUnderAttack(r, c - 2))): #ako nijedno polje između kralja i topa nije napadnuto
                moves.append(MoveSpecs((r, c), (r, c - 2), self.board, isCastlingMove=True)) #dodaj potez castlinga


    def getCastlingMoves(self, r, c, moves): #funkcija koja dodaje moguće poteze za castling
        if self.isSquareUnderAttack(r, c): #prvo provjeravamo je li kralj u šahu
            return #ako je kralj u šahu, ne može se napraviti castling

        if ((self.white_on_move and self.castling_permissions.white_king_side) or (not self.white_on_move and self.castling_permissions.black_king_side)):
            #ako je bijeli na potezu i ima pravo na castling na desnoj strani ili ako je crni na potezu i ima pravo na castling na desnoj strani
            self.getRightSideCastleMoves(r, c, moves)
        if ((self.white_on_move and self.castling_permissions.white_queen_side) or (not self.white_on_move and self.castling_permissions.black_queen_side)):
            #ako je bijeli na potezu i ima pravo na castling na lijevoj strani ili ako je crni na potezu i ima pravo na castling na lijevoj strani
            self.getLeftSideCastleMoves(r, c, moves)

    def getLegalMoves(self): #funkcija koja vraća sve moguće poteze koje trenutni igrač može napraviti
        current_castling_permissions = CastlingPermission(self.castling_permissions.white_king_side, self.castling_permissions.black_king_side, self.castling_permissions.white_queen_side, self.castling_permissions.black_queen_side)
        legal_moves = [] #lista svih legalnih poteza koju ćemo vratiti
        self.in_check, self.pins_list, self.checks_list = self.getPinsAndChecks() #Uzmi polje pinova, polje šahova i checker je li trenutni igrač u šahu

        if self.white_on_move: #ako je bijeli na potezu, dohvati poziciju bijelog kralja
            king_r = self.white_king_index[0]
            king_c = self.white_king_index[1]
        else: #ako je crni na potezu, dohvati poziciju crnog kralja
            king_r = self.black_king_index[0]
            king_c = self.black_king_index[1]

        if self.in_check: #ako je trenutni igrač u šahu
            if (len(self.checks_list) == 1):  #ako samo jedna enemy figura napada kralja => može se blokirati ili pomaknuti kralja
                legal_moves = self.getAllAvailableMoves() #dohvati sve moguće poteze
                # da bi blokirali šah, moramo staviti ally figuru između kralja i figure koja napada kralja
                check = self.checks_list[0]  # dohvati poziciju figure koja napada kralja i smjer napada
                check_r = check[0] #redak figure koja napada kralja 
                check_c = check[1] #stupac figure koja napada kralja
                figureChecker = self.board[check_r][check_c] #dohvati koja je to figura koja napada kralja
                legal_squares = [] #lista u koju ćemo dodati sva polja na koja se može pomaknuti kralj ili blokirati šah
                # Ako konj radi šah mora ga se pojesti ili se mora pomaknuti kralja jer on može preskakati figure pa se ne može blokirati (pinnati)
                if (figureChecker[1] == "N"): 
                    legal_squares = [(check_r, check_c)] #legalan potez je pojesti konja
                else:
                    for i in range(1, 8): #za svaku moguću udaljenost od figure koja napada kralja
                        legal_square = (king_r + check[2] * i, king_c + check[3] * i)  # check[2] andi check[3] su check smjerovi
                        legal_squares.append(legal_square) #dodaj polje u listu legalnih polja
                        if ((legal_square[0] == check_r) and (legal_square[1] == check_c)):  #ako smo došli do figure koja napada kralja, nema smisla ići dalje
                            break
                # riješi se poteza koji ne blokiraju ili ne napadaju figuru koja napada kralja
                for i in range(len(legal_moves) - 1, -1, -1):  # iteriranje unatrag jer brisemo elemente iz liste
                    if (legal_moves[i].movedFigureName[1] != "K"):  #ako ne pomičemo kralja onda moramo blokirati ili pojesti figuru koja napada kralja
                        if not (legal_moves[i].end_r, legal_moves[i].end_c) in legal_squares:  #ako potez ne blokira ili ne napada figuru koja napada kralja
                            legal_moves.remove(legal_moves[i]) #makni taj potez
            else: 
                self.getKingMoves(king_r, king_c, legal_moves)
        else: #ako nije u šahu svi potezi su dozvoljeni
            legal_moves = self.getAllAvailableMoves() #dohvati sve moguće poteze
            if self.white_on_move:  #ako je bijeli na potezu
                self.getCastlingMoves(self.white_king_index[0], self.white_king_index[1], legal_moves) #dohvati moguće poteze za castling
            else:
                self.getCastlingMoves(self.black_king_index[0], self.black_king_index[1], legal_moves) #dohvati moguće poteze za castling

        if (len(legal_moves) == 0): #ako nema legalnih poteza
            if self.isInCheck(): #ako je u šahu
                self.checkmate = True #onda je šah mat
            else:
                self.stalemate = True # ako nema legalnih poteza a nije u šahu onda je stale mate
        else: #inače nije nijedno ni drugo
            self.checkmate = False
            self.stalemate = False

        self.castling_permissions = current_castling_permissions
        return legal_moves #vraća sve legalne poteze


class MoveSpecs: #klasa koja sadrži informacije o potezu
    def __init__(self, start_sq, end_sq, chess_board, isEnpassantMove=False, isCastlingMove=False):
        self.start_r = start_sq[0] #početni redak
        self.start_c = start_sq[1] #početni stupac
        self.end_r = end_sq[0] #završni redak
        self.end_c = end_sq[1] #završni stupac
        self.movedFigureName = chess_board[self.start_r][self.start_c] #ime figure koja se pomaknula
        self.capturedFigureName = chess_board[self.end_r][self.end_c] #ime figure koja je pojedena

        # promocija pijuna
        is_white_pawn_promotion = self.movedFigureName == "wp" and self.end_r == 0 #ako je bijeli pijun došao do kraja ploče
        is_black_pawn_promotion = self.movedFigureName == "bp" and self.end_r == 7 #ako je crni pijun došao do kraja ploče
        self.is_pawn_promotion = is_white_pawn_promotion or is_black_pawn_promotion #ako je potez promocija pijuna
        # en passant
        self.isEnpassantMove = isEnpassantMove

        if self.isEnpassantMove: #ako je potez en-passant
            if self.movedFigureName == "bp":  # ako je crni pijun pomaknut, bijeli pijun je pojeden
                self.capturedFigureName = "wp"  
            else:
                self.capturedFigureName = "bp"  # ako je bijeli pijun pomaknut, crni pijun je pojeden

        # rokada/castling
        if isCastlingMove:
            self.isCastlingMove = True
        else:
            self.isCastlingMove = False

        #kreiranje jedinstvenog pokazivača svakog poteza 
        self.MovePointer = self.start_r * 999 + self.start_c * 99 + self.end_r * 9 + self.end_c #pomoću ovog broja uspoređujemo dva poteza

    def __eq__(self, another_move): #funkcija koja uspoređuje dva poteza
        if isinstance(another_move, MoveSpecs):
            return self.MovePointer == another_move.MovePointer
        else:
            return False

class CastlingPermission: #klasa koja sadrži informacije o tome ima li igrač pravo na castling na lijevoj/desnoj strani
    def __init__(self, white_king_side, black_king_side, white_queen_side, black_queen_side):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side