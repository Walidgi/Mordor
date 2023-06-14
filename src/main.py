import pygame

pygame.mixer.init()
hobbit_song = pygame.mixer.Sound("../song/hobbit_song.mp3")
hobbit_song.play()

from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()

# Game Resolution
screen_width=900
screen_height=700
screen=pygame.display.set_mode((900, 700))

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(249, 242, 14)

# Game Fonts
font = "../fonts/anirb.ttf"


# Game Framerate
clock = pygame.time.Clock()
FPS=60

# Main Menu
def main_menu():

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        game.run()
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        my_image = pygame.image.load('../map/comté.jpg')
        screen.blit(my_image, (0, 0))
        title=text_format("La Comté - Le jeu", font, 55, yellow)
        if selected=="start":
            text_start=text_format("JOUER", font, 45, white)
        else:
            text_start = text_format("JOUER", font, 45, black)
        if selected=="quit":
            text_quit=text_format("QUITTER", font, 45, white)
        else:
            text_quit = text_format("QUITTER", font, 45, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)

#Initialize the Game
main_menu()
pygame.quit()
quit()
