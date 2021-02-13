class player(pygame.sprite.Sprite
    def __init__(mask=False, state='alive'):
        super().__init__()
        self.state=state
        self.mask=mask
        self.speedvariance=0 #i was thinking speed could change based off if someone was infected or not but this doest need to be implemented now
        self.collison=False

        self.rect.x=start[0]
        self.rect.y=start[1]

    def move(self):
        if self.state!='sick' and self.collision=False:

    def jump(self):
