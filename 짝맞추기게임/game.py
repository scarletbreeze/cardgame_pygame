import random, pygame, sys
from pygame.locals import *

FPS = 30 # 초당 프레임. 프로그램의 일반속도 // 게임의 전반적인 속도
WINDOWWIDTH = 640 # 윈도우의 너비 (픽셀 단위)
WINDOWHEIGHT = 480 # 윈도우의 높이 (픽셀 단위)
HALF_WIDTH = int(WINDOWWIDTH / 2)
HALF_HEIGHT = int(WINDOWHEIGHT / 2)
REVEALSPEED = 7 # 상자가 보였다가 가려지는 속도
BOXSIZE = 60 # 상자의 너비와 높이(픽셀 단위)
GAPSIZE = 10 # 상자 사이의 간격(픽셀 단위)
BOARDWIDTH = 4 # 아이콘(상자) 가로줄 수
BOARDHEIGHT = 3 # 아이콘 세로줄 수
BOXNUMBER =  4 #처음에 뒤집히는 상자의 수


assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, '상자 갯수가 짝수가 아닙니다.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
SKYBLUE     = (155,  220, 255)

BGCOLOR = SKYBLUE
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
TEXTCOLOR = WHITE

bear = pygame.image.load('bear.png')
beartext = pygame.image.load('beartext.png')
bee = pygame.image.load('bee.png')
beetext = pygame.image.load('beetext.png')
cat =  pygame.image.load('cat.png')
cattext = pygame.image.load('cattext.png')
chicken = pygame.image.load('chicken.png')
chickentext = pygame.image.load('chickentext.png')
cow = pygame.image.load('cow.png')
cowtext = pygame.image.load('cowtext.png')
crab =  pygame.image.load('crab.png')
crabtext = pygame.image.load('crabtext.png')
deer = pygame.image.load('deer.png')
deertext = pygame.image.load('deertext.png')
dog = pygame.image.load('dog.png')
dogtext = pygame.image.load('dogtext.png')
duck = pygame.image.load('duck.png')
ducktext = pygame.image.load('ducktext.png')
elephant = pygame.image.load('elephant.png')
elephanttext = pygame.image.load('elephanttext.png')
frog = pygame.image.load('frog.png')
frogtext = pygame.image.load('frogtext.png')
giraffe =  pygame.image.load('giraffe.png')
giraffetext = pygame.image.load('giraffetext.png')
lion =  pygame.image.load('lion.png')
liontext = pygame.image.load('liontext.png')
monkey = pygame.image.load('monkey.png')
monkeytext = pygame.image.load('monkeytext.png')
mouse = pygame.image.load('mouse.png')
mousetext = pygame.image.load('mousetext.png')
owl = pygame.image.load('owl.png')
owltext = pygame.image.load('owltext.png')
penguin = pygame.image.load('penguin.png')
penguintext = pygame.image.load('penguintext.png')
pig = pygame.image.load('pig.png')
pigtext = pygame.image.load('pigtext.png')
rabbit = pygame.image.load('rabbit.png')
rabbittext = pygame.image.load('rabbittext.png')
raccoon = pygame.image.load('raccoon.png')
raccoontext = pygame.image.load('raccoontext.png')
shark =  pygame.image.load('shark.png')
sharktext = pygame.image.load('sharktext.png')
sheep = pygame.image.load('sheep.png')
sheeptext = pygame.image.load('sheeptext.png')
tiger =  pygame.image.load('tiger.png')
tigertext = pygame.image.load('tigertext.png')
whale = pygame.image.load('whale.png')
whaletext = pygame.image.load('whaletext.png')
zebra =  pygame.image.load('zebra.png')
zebratext = pygame.image.load('zebratext.png')

ALLTEXTS = (beartext, beetext, cattext, chickentext, cowtext, crabtext, dogtext, 
	 deertext ,ducktext, elephanttext , frogtext, giraffetext, liontext, monkeytext, mousetext, owltext ,
	 pigtext, penguintext, rabbittext, raccoontext, sharktext,sheeptext, tigertext, whaletext, zebratext)
ALLSHAPES = (bear, bee, cat, chicken, cow, crab,dog, deer, duck, frog, giraffe, lion, monkey, mouse, 
	 owl, penguin , pig, rabbit, raccoon, shark, sheep, tiger, whale, zebra)


assert len(ALLTEXTS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "상자의 갯수가 아이콘의 수와 맞지 않습니다."

def main():
    global FPSCLOCK, DISPLAYSURF,IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # 배경음악 추가
    pygame.mixer.music.load('BGM.wav')
    pygame.mixer.music.play(-1) #-1은 무한 재생, 0은 한번 재생

    mousex = 0 # 마우스 이벤트 발생 시 x좌표
    mousey = 0 # 마우스 이벤트 발생 시 y좌표
    pygame.display.set_caption('Matching Game')  # 이름 설정

    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    IMAGESDICT = {'title': pygame.image.load('title.png'),
                  'won' : pygame.image.load('solved.png')}

    startScreen()

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # 첫 번째 상자를 클릭했을 때 (x,y)를 저장

    DISPLAYSURF.fill(BGCOLOR) # 화면 배경 설정
    startGameAnimation(mainBoard)

    while True: # 게임 루프
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # 윈도우를 그린다.
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # 이벤트 처리 루프
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # 마우스가 현재 박스 위에 있다.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # 상자를 보이는 것으로 설정
                if firstSelection == None: # 현재의 상자가 처음 클릭한 상자
                    firstSelection = (boxx, boxy)
                else: # 현재의 상자가 두 번째 클릭한 상자라면
                    # 두 아이콘이 서로 맞는 짝인지 검사한다.
                    icon1shape = getShape(mainBoard, firstSelection[0], firstSelection[1])
                    icon2text = getShape(mainBoard, boxx, boxy)

                    if icon1shape != icon2text :
                        # 아이콘이 서로 맞지 않다면, 두 상자 모두 덮는다.
                        pygame.time.wait(100) 
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes) : # 아이콘이 서로 짝이라면
                        gameWonscreen()
                        pygame.time.wait(1000)

                        # 게임판을 재설정한다.
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # 잠시 동안 게임판의 상자를 열어서 보여준다.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # 게임 시작 애니메이션을 보여준다.
                        startGameAnimation(mainBoard)
                    firstSelection = None # 변수를 리셋한다.

        # 화면을 다시 그린 다음 시간 지연을 기다린다.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def startScreen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50
    titleRect.top = topCoord
    titleRect.centerx = HALF_WIDTH
    topCoord += titleRect.height

    instructionText = ['Mating Pictures and Texts!']

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WIDTH
        topCoord += instRect.height
        DISPLAYSURF.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPSCLOCK.tick()


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    icons = []
    for shape in ALLSHAPES:
        for shape in ALLSHAPES:
            icons.append( (shape, shape) )

    random.shuffle(icons) # 아이콘 리스트의 순서를 랜덤으로 정한다.
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # 얼마나 많은 아이콘이 필요한지 계산한다. 
    icons = icons[:numIconsUsed] * 2 # 각각의 짝을 만든다.

    random.shuffle(icons)

    # 랜덤으로 아이콘이 놓여 있는 게임판의 데이터 구조를 만든다.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # 방금 추가한 아이콘을 지운다.
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # 리스트를 2차원 리스트도 만든다. 안쪽의 리스트는 최대로
    # groupSize개 만큼의 아이템이 있다.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # 게임판 좌표계를 픽셀 좌표계로 변환한다.
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, text, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) 
    half =    int(BOXSIZE * 0.5)  

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == bear:
        DISPLAYSURF.blit(bear, (left+10, top+10))
        DISPLAYSURF.blit(beartext, (left+10, top+35))
        
    elif shape == bee:
        DISPLAYSURF.blit(bee, (left+10, top+10))
        DISPLAYSURF.blit(beetext, (left+10, top+35))

    elif shape == cat:
        DISPLAYSURF.blit(cat, (left+10, top+10))
        DISPLAYSURF.blit(cattext, (left+10, top+35))

    elif shape == chicken:
        DISPLAYSURF.blit(chicken, (left+10, top+10))
        DISPLAYSURF.blit(chickentext, (left+10, top+35))

    elif shape == cow:
        DISPLAYSURF.blit(cow, (left+10, top+10))
        DISPLAYSURF.blit(cowtext, (left+10, top+35))

    elif shape == crab:
        DISPLAYSURF.blit(crab, (left+10, top+10))
        DISPLAYSURF.blit(crabtext, (left+10, top+35))

    elif shape == dog:
        DISPLAYSURF.blit(dog, (left+10, top+10))
        DISPLAYSURF.blit(dogtext, (left+10, top+35))

    elif shape == deer:
        DISPLAYSURF.blit(deer, (left+10, top+10))
        DISPLAYSURF.blit(deertext, (left+10, top+35))

    elif shape == duck:
        DISPLAYSURF.blit(duck, (left+10, top+10))
        DISPLAYSURF.blit(ducktext, (left+10, top+30))

    elif shape == elephant:
        DISPLAYSURF.blit(elephant, (left+10, top+10))
        DISPLAYSURF.blit(elephanttext, (left+10, top+35))

    elif shape == frog:
        DISPLAYSURF.blit(frog, (left+10, top+10))
        DISPLAYSURF.blit(frogtext, (left+10, top+30))

    elif shape == giraffe:
        DISPLAYSURF.blit(giraffe, (left+10, top+10))
        DISPLAYSURF.blit(giraffetext, (left+10, top+35))

    elif shape == lion:
        DISPLAYSURF.blit(lion, (left+10, top+10))
        DISPLAYSURF.blit(liontext, (left+10, top+35))

    elif shape == monkey:
        DISPLAYSURF.blit(monkey, (left+10, top+10))
        DISPLAYSURF.blit(monkeytext, (left+10, top+28))

    elif shape == mouse:
        DISPLAYSURF.blit(mouse, (left+10, top+10))
        DISPLAYSURF.blit(mousetext, (left+10, top+27))

    elif shape == owl:
        DISPLAYSURF.blit(owl, (left+10, top+10))
        DISPLAYSURF.blit(owltext, (left+10, top+32))

    elif shape == penguin:
        DISPLAYSURF.blit(penguin, (left+10, top+10))
        DISPLAYSURF.blit(penguintext, (left+10, top+32))

    elif shape == pig:
        DISPLAYSURF.blit(pig, (left+10, top+10))
        DISPLAYSURF.blit(pigtext, (left+10, top+20))

    elif shape == rabbit:
        DISPLAYSURF.blit(rabbit, (left+10, top+10))
        DISPLAYSURF.blit(rabbittext, (left+10, top+35))

    elif shape == raccoon:
        DISPLAYSURF.blit(raccoon, (left+10, top+10))
        DISPLAYSURF.blit(raccoontext, (left+10, top+35))

    elif shape == shark:
        DISPLAYSURF.blit(shark, (left+10, top+10))
        DISPLAYSURF.blit(sharktext, (left+10, top+35))

    elif shape == sheep:
        DISPLAYSURF.blit(sheep, (left+10, top+10))
        DISPLAYSURF.blit(sheeptext, (left+10, top+33))

    elif shape == tiger:
        DISPLAYSURF.blit(tiger, (left+10, top+10))
        DISPLAYSURF.blit(tigertext, (left+10, top+35))

    elif shape == whale:
        DISPLAYSURF.blit(whale, (left+10, top+10))
        DISPLAYSURF.blit(whaletext, (left+10, top+35))

    elif shape == zebra:
        DISPLAYSURF.blit(zebra, (left+10, top+10))
        DISPLAYSURF.blit(zebratext, (left+10, top+35))


def getShape(board, boxx, boxy):
    # x,y 위치의 아이콘 형태의 값은 board[x][y][0]에 있다.
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # 닫히거나 열린 상태의 상자를 그린다.
    # 상자는 아이템 2개짜리 리스트이며 상자의 x,y 위치를 가진다.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, text = getShape(board, box[0], box[1])
        drawIcon(shape, text, box[0], box[1])
        if coverage > 0: # 닫힌 상태이면, 덮개만 그린다.
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # 상자가 열리는 애니메이션 수행
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # 상자가 닫히는 애니메이션 수행
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # 모든 상자를 상태에 맞게 그리기
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # 닫힌 상자를 그린다.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # 열린 상자, 즉 아이콘을 그린다.
                shape, text = getShape(board, boxx, boxy)
                drawIcon(shape, text, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(BOXNUMBER, boxes)     # 무작위로 한 번에 BOXNUMBER개씩 상자를 열어서 보여준다.

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonscreen():
    wonRect = IMAGESDICT['won'].get_rect()
    topCoord = 50
    wonRect.top = topCoord
    wonRect.centerx = HALF_WIDTH
    topCoord += wonRect.height

    instructionText = ['Congratulations!']
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(IMAGESDICT['won'], wonRect)

    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WIDTH
        topCoord += instRect.height
        DISPLAYSURF.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                quit()

        pygame.display.update()
        FPSCLOCK.tick()


def hasWon(revealedBoxes):
    # 모든 상자를 열었으면 True를 반환한다. 아니면 False를 반환한다.
    for i in revealedBoxes:
        if False in i:
            return False # 닫힌 상자가 있으면 False를 반환한다.
    return True


if __name__ == '__main__':
    main()