import pygame
    

class DialogBox ():

    X_POSITION = 140
    Y_POSITION = 760

    def __init__(self):
        self.box = pygame.image.load('assets/background/chatbox.png')
        self.box = pygame.transform.scale(self.box,(1200,180))
        self.texts = ['yo la miff','lkgfnsl','pgfn^phtrhjn','vkftbhotrnh']
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('assets/background/font.ttf',18)
        self.reading = True
 

    def render(self,screen):
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box,(self.X_POSITION,self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0,0,0))
            screen.blit(text,(self.X_POSITION + 100, self.Y_POSITION + 80))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False


