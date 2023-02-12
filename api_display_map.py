import requests
import pygame
import io

FrameHeight = 450
FrameWidth = 450

pygame.display.set_caption("Австралия со спутника")
screen = pygame.display.set_mode((FrameWidth,
                              FrameHeight))


class SputnikAustralia(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        req = requests.get(
            'https://static-maps.yandex.ru/1.x/?ll=139.960054%2C-28.812098&size=450,450&spn=40.016457,0.00619&l=sat'
        ).content

        self.image = pygame.image.load(io.BytesIO(
            req
        ))

        self.rect = self.image.get_rect()

sprite = SputnikAustralia()
screen.blit(sprite.image, pygame.rect.Rect(0, 0, FrameHeight, FrameWidth))
pygame.display.flip()
clock = pygame.time.Clock()
fps = 1
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    clock.tick(fps)
    sprite.update()