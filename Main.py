import pygame as p
import Game
import sys

# Inicijalne dimenzije za igru
WIDTH = 512
HEIGHT = 512
DIM = 8
SQUARESIZE = HEIGHT // DIM
FIGURE = {}
MAX_FPS = 15
playername_1 = ""
playername_2 = ""
imena_upisana = False
score_player1 = 0
score_player2 = 0

button_predaja1 = p.Rect(440, 18, 65, 20)
button_predaja2 = p.Rect(440, 586, 65, 20)

button_revans1 = p.Rect(358, 18, 65, 20)
button_revans2 = p.Rect(358, 586, 65, 20)

tick_mark_rect1 = p.Rect(200, 582, 40, 30) # donji tickmark rect
deny_mark_rect1 = p.Rect(250, 582, 40, 30) # donji denymark rect

tick_mark_rect2 = p.Rect(200, 13, 40, 30) # gornji tickmark rect
deny_mark_rect2 = p.Rect(250, 13, 40, 30) # gornji denymark rect

def loadFigures():
    piece_names = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in piece_names:
        image_path = f"images/{piece}.png"
        piece_image = p.image.load(image_path)
        scaled_image = p.transform.scale(piece_image, (SQUARESIZE, SQUARESIZE))
        FIGURE[piece] = scaled_image


def main():

    global playername_1, playername_2, imena_upisana, score_player1, score_player2, tick_mark_rect1, deny_mark_rect1, tick_mark_rect2, deny_mark_rect2
    p.init()
    start_screen = p.display.set_mode((860, 540))
    start_image = p.image.load('images/startscreen.png')
    start_screen.blit(start_image, (0, 0))

    font = p.font.SysFont('arial', 65, bold=True)
    text = font.render('Šah', True, p.Color('white'))
    text_rect = text.get_rect(center=(75, 65))
    start_screen.blit(text, text_rect)

    font2 = p.font.SysFont('arial', 30, bold=True, italic=True)
    text2 = font2.render('Upišite imena igrača:', True, p.Color('white'))
    text_rect2 = text2.get_rect(center=(150, 135))
    start_screen.blit(text2, text_rect2)

    font3 = p.font.SysFont('arial', 16, bold=True)
    text3 = font3.render('David Matej Vnuk © Mathos', True, p.Color('#717171'))
    text_rect3 = text3.get_rect(center=(95, 525))
    start_screen.blit(text3, text_rect3)

    outer_border_color = p.Color('#0d2d4f')
    background_color = p.Color('#3c528e')
    border_color = p.Color('#0d2d4f')
    button_color = p.Color('#8bc8db')
    outer_border_rect = p.Rect(30, 325, 260, 80)
    background_rect = p.Rect(35, 330, 250, 70)
    border_rect = p.Rect(40, 335, 240, 60)
    button_rect = p.Rect(45, 340, 230, 50)
    corner_radius = 25
    corner_radius_button = 20
    #p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
    #p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
    #p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
    #p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
    font4 = p.font.Font(None, 40)
    text4 = font4.render('IGRAJ', True, p.Color('black'))
    text_rect4 = text4.get_rect(center=button_rect.center)
    start_screen.blit(text4, text_rect4)

    # Bijeli pravokutnici iza input boxova
    white_rec1 = p.Rect(28, 180, 260, 40)
    #p.draw.rect(start_screen, "white", white_rec1)

    white_rec2 = p.Rect(28, 250, 260, 40)
    #p.draw.rect(start_screen, "white", white_rec2)

    # Input boxovi
    input_box1 = p.Rect(28, 180, 260, 40)
    input_box2 = p.Rect(28, 250, 260, 40)
    color_inactive = p.Color('#0d2d4f')
    color_active = p.Color('dodgerblue2')
    color1 = color_active
    color2 = color_active
    active_box = None
    border_thickness = 5

    p.display.flip()
    start_game = False
    while ((not start_game) and (imena_upisana == False)):
        for e in p.event.get():
            if (e.type == p.QUIT):
                p.quit()
                sys.exit()
            elif (e.type == p.MOUSEBUTTONDOWN):
                if input_box1.collidepoint(e.pos):
                    active_box = 1
                elif input_box2.collidepoint(e.pos):
                    active_box = 2
                elif button_rect.collidepoint(e.pos) and playername_1 and playername_2:
                    start_game = True
                else:
                    active_box = None
            elif (e.type == p.KEYDOWN):
                if (active_box == 1):
                    if (e.key == p.K_RETURN):
                        active_box = None
                    elif (e.key == p.K_BACKSPACE):
                        playername_1 = playername_1[:-1]
                    else:
                        playername_1 += e.unicode
                elif active_box == 2:
                    if (e.key == p.K_RETURN):
                        active_box = None
                    elif (e.key == p.K_BACKSPACE):
                        playername_2 = playername_2[:-1]
                    else:
                        playername_2 += e.unicode

        start_screen.blit(start_image, (0, 0))
        start_screen.blit(text, text_rect)
        start_screen.blit(text2, text_rect2)
        start_screen.blit(text3, text_rect3)
        p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
        p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
        p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
        p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
        p.draw.rect(start_screen, "white", white_rec1)
        p.draw.rect(start_screen, "white", white_rec2)

        start_screen.blit(text4, text_rect4)
        p.draw.rect(start_screen, color1 if active_box == 1 else color_inactive, input_box1, border_thickness)
        p.draw.rect(start_screen, color2 if active_box == 2 else color_inactive, input_box2, border_thickness)
        text_surface1 = font2.render(playername_1, True, p.Color('black'))
        text_surface2 = font2.render(playername_2, True, p.Color('black'))

        start_screen.blit(text_surface1, (input_box1.x + 10, input_box1.y + 2))
        start_screen.blit(text_surface2, (input_box2.x + 10, input_box2.y + 2))

        p.display.flip()

    imena_upisana = True #Da kad kasnije pokrećemo main iz score_screena ne ulazi opet u crtanje imena
    screen = p.display.set_mode((WIDTH+16, HEIGHT+112))
    clock = p.time.Clock()
    screen.fill(p.Color("#1e4072"))
    game = Game.Game()
    legal_moves = game.getLegalMoves()
    move_done = False  
    animation = False  
    loadFigures() 
    run = True
    sel_square = ()  # zadnji klik korisnika (tuple(row,col))
    player_clicks = []  # dva klika korisnika, prvi je selekcija, drugi je destinacija poteza (tuple(row,col))
    game_over = False
    score_screen = False
    isRevansPressed1 = False
    isRevansPressed2 = False

    while run:
        for e in p.event.get():
            if (e.type == p.QUIT):
                p.quit()
                sys.exit()
            elif (e.type == p.MOUSEBUTTONDOWN and button_predaja1.collidepoint(e.pos)): #PREDAJA GORNJEG IGRAČA
                score_player1+=1 #increment na scoru
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))

                #Tekst da je predaja
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('PREDAJA', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()
                text_rect11.topleft = (80, 10)
                screen.blit(text11, text_rect11)

                #Tekst taj i taj igrač je izgubio
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text6 = font.render(playername_2, True, p.Color('white'))
                text_rect6 = text6.get_rect() 
                text_rect6.topleft = (80, 70)
                screen.blit(text6, text_rect6)    

                text1 = font.render('je izgubio', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(180, 130))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect() 
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect() 
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect() 
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect() 
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect() 
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                #resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()

            elif (e.type == p.MOUSEBUTTONDOWN and button_predaja2.collidepoint(e.pos)): #PREDAJA DONJEG IGRAČA
                score_player2+=1 #increment na scoru
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))
                
                #Tekst da je predaja
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('PREDAJA', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()  
                text_rect11.topleft = (80, 10)
                screen.blit(text11, text_rect11)

                #Tekst taj i taj igrač je izgubio
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text6 = font.render(playername_1, True, p.Color('white'))
                text_rect6 = text6.get_rect()  
                text_rect6.topleft = (80, 70)
                screen.blit(text6, text_rect6)    

                text1 = font.render('je izgubio', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(180, 130))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect()  
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect()  
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect()  
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                # resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()
            
            #AKO PRITISNE REMI PRIKAZI TICK I DENY MARK
            elif ((e.type == p.MOUSEBUTTONDOWN) and button_revans1.collidepoint(e.pos)): #REVANS OD GORNJEG IGRAČA
                #Tick_mark rect koji se crta prvi da je ispod njega i da možemo detektirati da smo ga stisnuli jer image nema collidepoint izgleda

                p.draw.rect(start_screen, "#1e4072", tick_mark_rect1)

                #Deny_mark rect koji se crta prvi da je ispod njega i da možemo detektirati da smo ga stisnuli jer image nema collidepoint izgleda
                
                p.draw.rect(start_screen, "#1e4072", deny_mark_rect1)

                #Nacrtaj tick mark i deny mark kod suprotnog, tj dolje
                tick_mark = p.image.load('images/tickmark.png')
                new_width = tick_mark.get_width() // 100
                new_height = tick_mark.get_height() // 100
                # resize
                prihvacanje = p.transform.scale(tick_mark, (new_width, new_height))
                
                screen.blit(tick_mark, (200, 578))

                deny_mark = p.image.load('images/denymark.png')
                new_width = deny_mark.get_width() // 100
                new_height = deny_mark.get_height() // 100
                # resize
                odbijanje = p.transform.scale(deny_mark, (new_width, new_height))
                
                screen.blit(deny_mark, (250, 585))
                isRevansPressed1 = True
            
            #AKO PRIHVATI PRIKAZI REMI SCREEN
            elif ((e.type == p.MOUSEBUTTONDOWN) and tick_mark_rect1.collidepoint(e.pos) and isRevansPressed1):
                isRevansPressed1 = False #prvo ih resetamo, ne resetamo jer ide screen za neriješeno
                print("blabla")
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))
                        
                #Tekst da je remi
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('REMI', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()  
                text_rect11.topleft = (130, 10)
                screen.blit(text11, text_rect11)
    
                #Tekst da je neriješeno
                text1 = font.render('Neriješeno', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(175, 110))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect()  
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect()  
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect()  
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                # resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()
            #AKO ODBIJE
            elif ((e.type == p.MOUSEBUTTONDOWN) and deny_mark_rect1.collidepoint(e.pos) and isRevansPressed1):
                isRevansPressed1 = False #prvo ih resetamo
                prekrivanje_dolje = p.Rect(200, 581, 100, 32) #prekrijemo tick mark i deny mark jer je korisnik odlučio
                p.draw.rect(start_screen, "#1e4072", prekrivanje_dolje)

            #AKO PRITISNE REMI PRIKAZI TICK I DENYMARK
            elif ((e.type == p.MOUSEBUTTONDOWN) and button_revans2.collidepoint(e.pos)): #REVANS OD DONJEG IGRAČA
                #Tick_mark rect koji se crta prvi da je ispod njega i da možemo detektirati da smo ga stisnuli jer image nema collidepoint izgleda
                p.draw.rect(start_screen, "#1e4072", tick_mark_rect2)

                #Deny_mark rect koji se crta prvi da je ispod njega i da možemo detektirati da smo ga stisnuli jer image nema collidepoint izgleda
                p.draw.rect(start_screen, "#1e4072", deny_mark_rect2)
            
                #Nacrtaj tick mark i deny mark kod suprotnog, tj gore
                tick_mark = p.image.load('images/tickmark.png')
                new_width = tick_mark.get_width() // 100
                new_height = tick_mark.get_height() // 100
                # resize
                prihvacanje = p.transform.scale(tick_mark, (new_width, new_height))
                
                screen.blit(tick_mark, (200, 10))

                deny_mark = p.image.load('images/denymark.png')
                new_width = deny_mark.get_width() // 100
                new_height = deny_mark.get_height() // 100
                # resize
                odbijanje = p.transform.scale(deny_mark, (new_width, new_height))
                
                screen.blit(deny_mark, (250, 15))
                isRevansPressed2 = True
            
            #AKO PRIHVATI POKAZI SCREEN REMI
            elif ((e.type == p.MOUSEBUTTONDOWN) and tick_mark_rect2.collidepoint(e.pos) and isRevansPressed2):
                isRevansPressed2 = False #prvo ih resetamo, ne resetamo jer ide screen za neriješeno
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))
                        
                #Tekst da je remi
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('REMI', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()  
                text_rect11.topleft = (130, 10)
                screen.blit(text11, text_rect11)
    
                #Tekst da je neriješeno
                text1 = font.render('Neriješeno', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(175, 110))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect()  
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect()  
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect()  
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                # resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()

            #AKO ODBIJE SAMO PREKRI
            elif ((e.type == p.MOUSEBUTTONDOWN) and deny_mark_rect2.collidepoint(e.pos) and isRevansPressed2):
                isRevansPressed2 = False #prvo ih resetamo
                prekrivanje_gore = p.Rect(200, 13, 100, 32) #prekrijemo tick mark i deny mark jer je korisnik odlučio
                p.draw.rect(start_screen, "#1e4072", prekrivanje_gore)


            elif (e.type == p.MOUSEBUTTONDOWN) and not (isRevansPressed1 or isRevansPressed2):  #Uvjet da može raditi potez samo ako nitko nije zatražio revanš => u tom slučaju mora odabrati pristaje li ili odbija
                if not game_over:
                    mouse_x, mouse_y = p.mouse.get_pos()
                    col = (mouse_x - 8) // SQUARESIZE
                    row = (mouse_y - 56) // SQUARESIZE

                    # Provjera da li je kliknuti kvadrat unutar ploče
                    if 0 <= col < DIM and 0 <= row < DIM:
                        if sel_square == (row, col):  # Kliknio je na isti kvadrat ili negdje izvan
                            sel_square = ()  # Deselectaj
                            player_clicks = []  # Obriši klikove
                        else: # Kliknuo je na novi kvadrat
                            sel_square = (row, col)
                            player_clicks.append(sel_square) #dodajemo klik u listu klikova

                        if len(player_clicks) == 2:  #nakon što je kliknuo na dva kvadrata
                            start_square, end_square = player_clicks # Dohvati početni i krajnji kvadrat
                            move = Game.MoveSpecs(start_square, end_square, game.board) # Stvori objekt poteza
                            for legal_move in legal_moves: # Provjeri da li je potez legalan
                                if move == legal_move: # Ako je legalan, napravi potez
                                    game.makeMove(legal_move) # Napravi potez
                                    move_done = True 
                                    animation = True
                                    sel_square = ()  # Deselectaj kvadrat
                                    player_clicks = [] # Obriši klikove
                                    break
                            if not move_done: 
                                player_clicks = [sel_square]

            
        if move_done: # Ako je potez napravljen
            if animation: #Napravi animaciju ako nije napravljena
                moveAnimation(game.move_log[-1], screen, game.board, clock)
            legal_moves = game.getLegalMoves()
            animation = False
            move_done = False

        if (score_screen == False): #ako je score_screen ne crtaj ponovo ploču jer je igra završila, ili se netko predao ili je izgubio
            drawGame(screen, game, legal_moves, sel_square)

        if game.checkmate: #ako je šah mat
            game_over = True 
            if game.white_on_move: #Ako je bijeli na potezu
                p.time.wait(4000) #Da pričeka da se reviewa zadnja pozicija figura
                score_player2+=1 #increment na scoru
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))

                #Tekst da je šah mat
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('ŠAH-MAT', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()  
                text_rect11.topleft = (80, 10)
                screen.blit(text11, text_rect11)

                #Tekst taj i taj igrač je izgubio
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text6 = font.render(playername_1, True, p.Color('white'))
                text_rect6 = text6.get_rect()  
                text_rect6.topleft = (80, 70)
                screen.blit(text6, text_rect6)    

                text1 = font.render('je izgubio', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(180, 130))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect()  
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect()  
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect()  
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                # resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()

            else: #Ako je crni na potezu i ŠAH-MAT je
                p.time.wait(4000)
                score_player1+=1 #increment na scoru
                score_screen = True 
                p.init()
                score_screen = p.display.set_mode((860, 540))
                score_image = p.image.load('images/startscreen.png')
                score_screen.blit(score_image, (0, 0))

                #Tekst da je šah mat
                font = p.font.SysFont('arial', 45, bold=True, italic = True)
                text11 = font.render('ŠAH-MAT', True, p.Color('#0a2262'))
                text_rect11 = text11.get_rect()  
                text_rect11.topleft = (80, 10)
                screen.blit(text11, text_rect11)

                #Tekst taj i taj igrač je izgubio
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text6 = font.render(playername_2, True, p.Color('white'))
                text_rect6 = text6.get_rect()  
                text_rect6.topleft = (80, 70)
                screen.blit(text6, text_rect6)    

                text1 = font.render('je izgubio', True, p.Color('white'))
                text_rect1 = text1.get_rect(center=(180, 130))
                score_screen.blit(text1, text_rect1)

                #Imena igrača za score i dvotočka
                font = p.font.SysFont('arial', 35, bold=True, italic = True)
                text7 = font.render(playername_1, True, p.Color('white'))
                text_rect7 = text7.get_rect()  
                text_rect7.topleft = (60, 270)
                screen.blit(text7, text_rect7) 
                text8 = font.render(playername_2, True, p.Color('white'))
                text_rect8 = text8.get_rect()  
                text_rect8.topleft = (180, 270)
                screen.blit(text8, text_rect8)
                #Dvotočka
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(':', True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (155, 165)
                screen.blit(text9, text_rect9)

                #ISPIS SCOROVA
                font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
                text9 = font2.render(str(score_player1), True, p.Color('white'))
                text_rect9 = text9.get_rect()  
                text_rect9.topleft = (100, 165)
                screen.blit(text9, text_rect9)
                text10 = font2.render(str(score_player2), True, p.Color('white'))
                text_rect10 = text10.get_rect()  
                text_rect10.topleft = (200, 165)
                screen.blit(text10, text_rect10)

                #Tekst kao dugme izlaz
                font = p.font.SysFont('arial', 20, bold=True)
                text = font.render('Izlaz', True, p.Color('white'))
                text_rect = text.get_rect(center=(48, 520))
                score_screen.blit(text, text_rect)

                #Strelica iznad izlaza
                izlaz_strelica = p.image.load('images/strelica.png')
                new_width = izlaz_strelica.get_width() // 8
                new_height = izlaz_strelica.get_height() // 8
                # resize
                izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
                
                score_screen.blit(izlaz_strelica, (8, 470))

                #Dugme revanš

                outer_border_color = p.Color('#0d2d4f')
                background_color = p.Color('#3c528e')
                border_color = p.Color('#0d2d4f')
                button_color = p.Color('#8bc8db')
                outer_border_rect = p.Rect(30, 325, 260, 80)
                background_rect = p.Rect(35, 330, 250, 70)
                border_rect = p.Rect(40, 335, 240, 60)
                button_rect = p.Rect(45, 340, 230, 50)
                corner_radius = 25
                corner_radius_button = 20
                p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
                p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
                p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
                font4 = p.font.Font(None, 40)
                text4 = font4.render('REVANŠ', True, p.Color('black'))
                text_rect4 = text4.get_rect(center=button_rect.center)
                score_screen.blit(text4, text_rect4)

                p.display.flip()
                start_game = False
                while not start_game:
                    for e in p.event.get():
                        if (e.type == p.QUIT):
                            p.quit()
                            sys.exit()
                        elif (e.type == p.MOUSEBUTTONDOWN):
                            if button_rect.collidepoint(e.pos):
                                start_game = True
                            elif text_rect.collidepoint(e.pos):
                                p.quit()
                                sys.exit()
                main()

        elif game.stalemate: #Ako je stale-mate
            game_over = True
            score_screen = True 
            p.time.wait(4000)
            p.init()
            score_screen = p.display.set_mode((860, 540))
            score_image = p.image.load('images/startscreen.png')
            score_screen.blit(score_image, (0, 0))

            #Tekst da je stale-mate
            font = p.font.SysFont('arial', 45, bold=True, italic = True)
            text11 = font.render('STALE-MATE', True, p.Color('#0a2262'))
            text_rect11 = text11.get_rect()  
            text_rect11.topleft = (70, 10)
            screen.blit(text11, text_rect11)
  
            #Tekst da je neriješeno
            text1 = font.render('Neriješeno', True, p.Color('white'))
            text_rect1 = text1.get_rect(center=(175, 110))
            score_screen.blit(text1, text_rect1)

            #Imena igrača za score i dvotočka
            font = p.font.SysFont('arial', 35, bold=True, italic = True)
            text7 = font.render(playername_1, True, p.Color('white'))
            text_rect7 = text7.get_rect()  
            text_rect7.topleft = (60, 270)
            screen.blit(text7, text_rect7) 
            text8 = font.render(playername_2, True, p.Color('white'))
            text_rect8 = text8.get_rect()  
            text_rect8.topleft = (180, 270)
            screen.blit(text8, text_rect8)
            #Dvotočka
            font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
            text9 = font2.render(':', True, p.Color('white'))
            text_rect9 = text9.get_rect()  
            text_rect9.topleft = (155, 165)
            screen.blit(text9, text_rect9)

            #ISPIS SCOROVA
            font2 = p.font.SysFont('arial', 70, bold=True, italic = True)
            text9 = font2.render(str(score_player1), True, p.Color('white'))
            text_rect9 = text9.get_rect()  
            text_rect9.topleft = (100, 165)
            screen.blit(text9, text_rect9)
            text10 = font2.render(str(score_player2), True, p.Color('white'))
            text_rect10 = text10.get_rect()  
            text_rect10.topleft = (200, 165)
            screen.blit(text10, text_rect10)

            #Tekst kao dugme izlaz
            font = p.font.SysFont('arial', 20, bold=True)
            text = font.render('Izlaz', True, p.Color('white'))
            text_rect = text.get_rect(center=(48, 520))
            score_screen.blit(text, text_rect)

            #Strelica iznad izlaza
            izlaz_strelica = p.image.load('images/strelica.png')
            new_width = izlaz_strelica.get_width() // 8
            new_height = izlaz_strelica.get_height() // 8
            # resize
            izlaz_strelica = p.transform.scale(izlaz_strelica, (new_width, new_height))
            
            score_screen.blit(izlaz_strelica, (8, 470))

            #Dugme revanš

            outer_border_color = p.Color('#0d2d4f')
            background_color = p.Color('#3c528e')
            border_color = p.Color('#0d2d4f')
            button_color = p.Color('#8bc8db')
            outer_border_rect = p.Rect(30, 325, 260, 80)
            background_rect = p.Rect(35, 330, 250, 70)
            border_rect = p.Rect(40, 335, 240, 60)
            button_rect = p.Rect(45, 340, 230, 50)
            corner_radius = 25
            corner_radius_button = 20
            p.draw.rect(start_screen, outer_border_color, outer_border_rect, border_radius=30)
            p.draw.rect(start_screen, background_color, background_rect, border_radius=corner_radius)
            p.draw.rect(start_screen, border_color, border_rect, border_radius=corner_radius)
            p.draw.rect(start_screen, button_color, button_rect, border_radius=corner_radius_button)
            font4 = p.font.Font(None, 40)
            text4 = font4.render('REVANŠ', True, p.Color('black'))
            text_rect4 = text4.get_rect(center=button_rect.center)
            score_screen.blit(text4, text_rect4)

            p.display.flip()
            start_game = False
            while not start_game:
                for e in p.event.get():
                    if (e.type == p.QUIT):
                        p.quit()
                        sys.exit()
                    elif (e.type == p.MOUSEBUTTONDOWN):
                        if button_rect.collidepoint(e.pos):
                            start_game = True
                        elif text_rect.collidepoint(e.pos):
                            p.quit()
                            sys.exit()
            main()

        clock.tick(MAX_FPS)
        p.display.flip()


def drawBoard(screen): # Funkcija za crtanje ploče
    left_margin = 8 # Margina s lijeve strane gdje su nam samo bijele linije (obrubi)
    top_margin = 56 # Margina s gornje strane gdje su nam imena igrača i score i gumbi
    for r in range(DIM): 
        for c in range(DIM): 
            if (((r + c) % 2) == 0): # Ako je zbroj reda i stupca paran, onda je kvadrat bijele boje
                color = p.Color("#eae9d2")
            else:
                color = p.Color("#4b7399") #inače je plave
            p.draw.rect(screen, color, p.Rect(c * SQUARESIZE + left_margin, r * SQUARESIZE + top_margin, SQUARESIZE, SQUARESIZE))

def squareMarker(screen, game, legal_moves, sel_square): # Funkcija za markiranje kvadrata (koji smo odabrali, koji je zadnji potez i koji su legalni potezi)
    left_margin = 8 # Margina s lijeve strane gdje su nam samo bijele linije (obrubi)
    top_margin = 56 # Margina s gornje strane gdje su nam imena igrača i score i gumbi

    def highlight_square(row, col, color, alpha=100): # Funkcija za markiranje kvadrata, tj ispunjavanje bojom
        overlay = p.Surface((SQUARESIZE, SQUARESIZE))
        overlay.set_alpha(alpha)
        overlay.fill(p.Color(color))
        screen.blit(overlay, (col * SQUARESIZE + left_margin, row * SQUARESIZE + top_margin))

    if game.move_log: # Ako postoji neki potez u logu, tj zadnji potez markiraj sa tamno zelenom
        last_move = game.move_log[-1]
        highlight_square(last_move.end_r, last_move.end_c, 'darkgreen')

    if sel_square: # Ako je kvadrat odabran, tj ako je kliknut na kvadrat, markiraj ga sa svijetlo zelenom
        r, c = sel_square
        current_piece = game.board[r][c][0]
        if game.white_on_move:
            piece_color = 'w'
        else:
            piece_color = 'b'

        if (current_piece == piece_color): 
            highlight_square(r, c, 'green')
            
            # Loadamo sliku kojom označavamo legalne poteze
            grey_dot = p.image.load("images/greydot.png")
            grey_dot = p.transform.scale(grey_dot, (SQUARESIZE, SQUARESIZE))
            grey_dot.set_alpha(128)  # setamo alfa da bude polu-prozirno
            
            for move in legal_moves: # Prolazimo kroz sve legalne poteze i označavamo kvadrate sa sivim točkama
                if ((move.start_r == r) and (move.start_c == c)):
                    screen.blit(grey_dot, (move.end_c * SQUARESIZE + left_margin, move.end_r * SQUARESIZE + top_margin))

def drawFigure(screen, board): # Funkcija za crtanje figura na ploči
    left_margin = 8 # Margina s lijeve strane gdje su nam samo bijele linije (obrubi)
    top_margin = 56 # Margina s gornje strane gdje su nam imena igrača i score i gumbi
    for r in range(DIM):
        for c in range(DIM):
            piece = board[r][c] #Dohvat figure sa ploče da znamo koju sliku koristimo
            if (piece != "empty"): #Ako nije prazno polje, tj ako je figura na ploči crtaj tu figuru iz liste FIGURE
                screen.blit(FIGURE[piece], p.Rect(c * SQUARESIZE + left_margin, r * SQUARESIZE + top_margin, SQUARESIZE, SQUARESIZE))

def drawGame(screen, game, legal_moves, sel_square): # Funkcija za crtanje igre

    drawBoard(screen)  #poziv funkcije za crtanje ploče
    squareMarker(screen, game, legal_moves, sel_square) #poziv funkcije za markanje
    drawFigure(screen, game.board)  # poziv funkcije za crtanje figura na ploči

    #Ispisivanje imena
    font = p.font.SysFont('arial', 25)
    text = font.render(playername_2, True, p.Color('white'))
    text_rect = text.get_rect()  
    text_rect.topleft = (16, 13)
    screen.blit(text, text_rect)
    #Crtanje bijelog obruba desno od imena točno za 8 pixela
    rect_right = p.Rect(text_rect.right + 8, 0, 8, 56)
    p.draw.rect(screen, p.Color('white'), rect_right)
    
    # text za score_player2
    score_font = p.font.SysFont('arial', 25)
    score_text = score_font.render(str(score_player2), True, p.Color('white'))
    score_text_rect = score_text.get_rect()

    score_text_rect.topleft = (rect_right.right + 8, 13)
    screen.blit(score_text, score_text_rect)

    # Crtanje bijelog obruba desno od score_player2 točno za 8 pixela
    score_rect_right = p.Rect(score_text_rect.right + 8, 0, 8, 56)
    p.draw.rect(screen, p.Color('white'), score_rect_right)

    # Ispis imena igrača 1
    text2 = font.render(playername_1, True, p.Color('white'))
    text_rect2 = text2.get_rect()  
    text_rect2.topleft = (16, 580)
    screen.blit(text2, text_rect2)

    # crtanje bijelog obruba desno od imena igrača 1 točno za 8 pixela
    rect2_right = p.Rect(text_rect2.right + 8, 572, 8, 56)
    p.draw.rect(screen, p.Color('white'), rect2_right)

    # Ispis score_player1
    score_font2 = p.font.SysFont('arial', 25)
    score_text2 = score_font2.render(str(score_player1), True, p.Color('white'))
    score_text_rect2 = score_text2.get_rect()

    score_text_rect2.topleft = (rect2_right.right + 8, 580)
    screen.blit(score_text2, score_text_rect2)

    # Crtanje bijelog obruba desno od score_player1 točno za 8 pixela
    score_rect_right2 = p.Rect(score_text_rect2.right + 8, 572, 8, 56)
    p.draw.rect(screen, p.Color('white'), score_rect_right2)


    #528x624 je naš screen
    rect_left = p.Rect(0, 0, 8, 624)
    p.draw.rect(screen, "white", rect_left)
    rect_right = p.Rect(520, 0, 8, 624)
    p.draw.rect(screen, "white", rect_right)

    rect_top1 = p.Rect(0,0, 528, 8)
    p.draw.rect(screen, "white", rect_top1)
    rect_top2 = p.Rect(0,48, 528, 8)
    p.draw.rect(screen, "white", rect_top2)

    rect_bottom1 = p.Rect(0,616, 528, 8)
    p.draw.rect(screen, "white", rect_bottom1)
    rect_bottom2 = p.Rect(0,568, 528, 8)
    p.draw.rect(screen, "white", rect_bottom2)

    #Button predaja gornji
    button_predaja_border_1 = p.Rect(437, 15, 71, 26)
    p.draw.rect(screen, "black", button_predaja_border_1, border_radius=30)

    global button_predaja1
    p.draw.rect(screen, "white", button_predaja1, border_radius=30)
    font5 = p.font.SysFont('arial', 18, bold=True)
    text5 = font5.render('Predaj', True, p.Color('black'))
    text_rect5 = text5.get_rect(center=button_predaja1.center)
    screen.blit(text5, text_rect5)

    #Button predaja donji
    button_predaja_border_2 = p.Rect(437, 583, 71, 26)
    p.draw.rect(screen, "black", button_predaja_border_2, border_radius=30)

    global button_predaja2
    p.draw.rect(screen, "white", button_predaja2, border_radius=30)
    font6 = p.font.SysFont('arial', 18, bold=True)
    text6 = font6.render('Predaj', True, p.Color('black'))
    text_rect6 = text6.get_rect(center=button_predaja2.center)
    screen.blit(text6, text_rect6)

    #Button revans gornji
    button_revans_border_1 = p.Rect(355, 15, 71, 26)
    p.draw.rect(screen, "black", button_revans_border_1, border_radius=30)

    global button_revans1
    p.draw.rect(screen, "white", button_revans1, border_radius=30)
    font7 = p.font.SysFont('arial', 18, bold=True)
    text7 = font7.render('Remi', True, p.Color('black'))
    text_rect7 = text7.get_rect(center=button_revans1.center)
    screen.blit(text7, text_rect7)

    # Crtanje bijelog obruba lijevo od button_revans1
    rect1_left = p.Rect(text_rect7.left - 32, 572, 8, 56)
    p.draw.rect(screen, p.Color('white'), rect1_left)

    #Button revans donji
    button_revans_border_2 = p.Rect(355, 583, 71, 26)
    p.draw.rect(screen, "black", button_revans_border_2, border_radius=30)

    global button_revans2
    p.draw.rect(screen, "white", button_revans2, border_radius=30)
    font8 = p.font.SysFont('arial', 18, bold=True)
    text8 = font8.render('Remi', True, p.Color('black'))
    text_rect8 = text8.get_rect(center=button_revans2.center)
    screen.blit(text8, text_rect8)

    # Crtanje bijelog obruba lijevo od button_revans2
    rect2_left = p.Rect(text_rect8.left - 32, 0, 8, 56)
    p.draw.rect(screen, p.Color('white'), rect2_left)
        
def moveAnimation(move, screen, board, clock): # Funkcija za animaciju poteza
    left_margin = 8 # Margina s lijeve strane gdje su nam samo bijele linije (obrubi)
    top_margin = 56 # Margina s gornje strane gdje su nam imena igrača i score i gumbi
    delta_row = move.end_r - move.start_r # Razlika redova
    delta_col = move.end_c - move.start_c # Razlika stupaca
    frames_per_square = 10  # Broj frameova po kvadratu
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square # Ukupan broj frameova za potez
    
    for frame in range(frame_count + 1): # Prolazimo kroz sve frameove i crtamo non stop ploču i figure ali sa promjenjenim pozicijama i moramo crtati figuru koja će biti pojedena da bi se vidjelo kako polako nestaje tj da ju ova prekriva
        r, c = (move.start_r + delta_row * frame / frame_count, move.start_c + delta_col * frame / frame_count) # Trenutna pozicija figure
        drawBoard(screen)  #Crtamo ponovo ploču
        drawFigure(screen, board)  #Crtamo ponovo figure

        # Računamo trenutnu poziciju i konačnu s obzirom na margine
        x_pos = int(c * SQUARESIZE + left_margin)
        y_pos = int(r * SQUARESIZE + top_margin)
        end_x = move.end_c * SQUARESIZE + left_margin
        end_y = move.end_r * SQUARESIZE + top_margin

        # Računamo boju kvadrata na kojem će se nalaziti figura
        if (move.end_r + move.end_c) % 2 == 0:
            color = p.Color("#eae9d2")
        else:
            color = p.Color("#4b7399")
        end_square = p.Rect(end_x, end_y, SQUARESIZE, SQUARESIZE)
        p.draw.rect(screen, color, end_square) # Crtamo kvadrat na kojem će se nalaziti figura

        #Crtanje figure koja će biti pojedena na taj kvadrat da ne bude da odma nestane nego da se polako prekriva sa figurom koja se pomjera
        if (move.capturedFigureName != 'empty'): # Ako je figura pojedena, tj ako je potez bio napad na figuru
            if move.isEnpassantMove: # Ako je potez bio en passant
                if (move.capturedFigureName[0] == 'b'): # Ako je crni napadnut
                    enpassant_row_offset = 1 # Pomičemo se dolje 
                else:
                    enpassant_row_offset = -1 # Inače se pomičemo gore
                enpassant_row = move.end_r + enpassant_row_offset # Računamo red u kojem se nalazi figura koja je pojedena
                enpassant_y = (enpassant_row * SQUARESIZE) + top_margin # Računamo y koordinatu kvadrata na kojem se nalazi figura koja je pojedena 
                end_square = p.Rect(end_x, enpassant_y, SQUARESIZE, SQUARESIZE) # Kvadrat na kojem se nalazi figura koja je pojedena
            screen.blit(FIGURE[move.capturedFigureName], end_square) # Crtamo figuru koja je pojedena

        # Crtanje figure koja se pomjera na kraju jer ona mora biti na vrhu tj prekrivati figuru koja će biti pojedena
        moving_piece_image = FIGURE[move.movedFigureName] # Dohvat slike figure
        moving_piece_rect = p.Rect(x_pos, y_pos, SQUARESIZE, SQUARESIZE) 
        screen.blit(moving_piece_image, moving_piece_rect) #na točnom kvadratu crtamo sliku figure
        
        p.display.flip()
        clock.tick(60)  #brzina animacije

if __name__ == "__main__":
    main()
