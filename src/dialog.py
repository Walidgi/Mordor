import pygame

class DialogBox:

    X_POSITION = 80
    Y_POSITION = 550

    def __init__(self):
        self.box = pygame.image.load('../dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../fonts/mono.ttf", 18)
        self.reading = False

    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog


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

class DialogBox_Info:

    X_POSITION = 500
    Y_POSITION = 10

    def __init__(self):
        self.box_info = pygame.image.load('../dialogs/dialog_box_info.png')
        self.box_info = pygame.transform.scale(self.box_info, (400, 40))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../fonts/mono.ttf", 18)
        self.reading = False

    def execute(self, dialog=[]):
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def not_execute(self):
        self.reading = False

    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box_info, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 40, self.Y_POSITION + 12))