import pygame, sys,os
from PIL import Image
import pygame

pygame.init()
font = pygame.font.SysFont('Segoe', 30)

input_dir = "C:\Users\maxwe\Pictures\AnimeScreenshots\Karekano\KareKano"
output_dir = 'C:\Users\maxwe\Pictures\AnimeScreenshots\Cropped'
idx = 200

def displayImage(screen, px, topleft, bottomright, prior):
    # ensure that the rect always has positive width, height
    if topleft and bottomright:
        x, y = topleft
        width = bottomright[0] - topleft[0]
        height = bottomright[1] - topleft[1]
    elif topleft :
        x, y = topleft
        width = pygame.mouse.get_pos()[0] - topleft[0]
        height = pygame.mouse.get_pos()[1] - topleft[1]

    else :
        x, y = 0,0
        width = 0
        height = 0

    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))

    text =' Left click: Select Bounding Box \n Right click: Reset Bounding Box \n Enter: Save cropped image \n Left/Right: Prev/Next Image \n Index: '+str(idx)
    lines = text.splitlines()
    for i, l in enumerate(lines):
        text_surface=font.render(l, 0, (0,0,0),(255,170,102))
        text_surface.set_alpha(127)
        screen.blit(text_surface, (0, 0 + font.get_linesize() * i))


    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)

def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())

    pygame.display.flip()

    return screen, px

def mainLoop(screen, px):
    topleft = bottomright = prior = None
    fin=0
    dir=None

    while fin!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                topleft = None
                bottomright = None
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not topleft:
                    topleft = event.pos
                elif bottomright:
                    bottomright = None
                else:
                    bottomright = event.pos
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and topleft and bottomright:
                    fin=1
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT)) or event.type == pygame.QUIT:
                    bottomright = None
                    topleft = None
                    if event.type == pygame.QUIT:
                        dir=-1
                    elif event.key == pygame.K_LEFT:
                        dir=0
                    elif event.key == pygame.K_RIGHT:
                        dir=1
                    fin=1
        prior = displayImage(screen, px, topleft, bottomright, prior)
    test = "yes"
    return ( topleft,bottomright,dir )

if __name__ == "__main__":
    fileArr = os.listdir(input_dir)
    while 1:
        if idx<0: idx=0
        if idx>=len(fileArr): idx=len(fileArr)-1
        filename = fileArr[idx]
        f = os.path.join(input_dir, filename)

        # checking if it is a file
        if os.path.isfile(f):
            screen, px = setup(f)
            topleft,bottomright,dir = mainLoop(screen, px)

            if not topleft or not bottomright:
                if dir:
                    idx = idx+1
                elif dir==0:
                    idx = idx-1
                if dir ==-1:
                    break;
                continue

            left = topleft[0]
            upper = topleft[1]
            right = bottomright[0]
            lower = bottomright[1]
            # ensure output rect always has positive width, height
            if right < left:
                left, right = right, left
            if lower < upper:
                lower, upper = upper, lower
            im = Image.open(f)
            im = im.crop(( left, upper, right, lower))
            im.save(os.path.join(output_dir, filename))

        idx=idx+1


    pygame.display.quit()