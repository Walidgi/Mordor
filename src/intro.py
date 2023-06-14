import pygame

class DialogBox_Intro:

    X_POSITION = 80
    Y_POSITION = 550

    def __init__(self):
        self.box = pygame.image.load('../dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = ["Bienvenue à La Comté ! Appuie sur ESPACE", "Tu peux aller visiter les maisons des Hobbits", "Tu peux aussi t'aventurer au-delà de la Comté...", "Mais attention à toi, c'est dangereux !", "Si tu rencontres un Hobbit et qu'il s'arrête...","...il veut sûrement te dire quelque chose...", "Alors appuie sur espace pour l'écouter :)"]
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../fonts/mono.ttf", 18)
        self.reading = True

    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 40))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            #fermer dialog
            self.reading = False