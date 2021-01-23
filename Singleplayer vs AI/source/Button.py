class Button:

    def __init__(self, x, y, width, height, color, font, text, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.text = text
        self.screen = screen

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        rendered_text = self.font.render(self.text, True, HTTT.WHITE)
        if self.width > rendered_text.get_rect().width:
            text_cords = [int(self.x + ((self.width-rendered_text.get_rect().width)/2)), int(self.y + ((self.height-rendered_text.get_rect().height)/1.5))] #there's a 1.5 here because the buttons look better that way
        else:
            raise Exception('The button rect must be wider than the text width')
        self.screen.blit(rendered_text, text_cords)

    def is_clicked(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            return True