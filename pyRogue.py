"""
KENDRIYA VIDYALAYA SHALIMAR BAGH-110088
CLASS XII A COMPUTER SCIENCE PROJECT

MEMBERS:
1) NIKHIL KADIYAN (Roll no. 24) - Programming, testing, assets

The following project is a game made in Python using the tkinter module.

The game is of the genre Roguelike.

Wikipedia describes rougulike as:
'Roguelike is a subgenre of role-playing video game characterized by a dungeon crawl
through procedurally generated levels, turn-based gameplay, tile-based graphics, and permanent death of the
player character.'

This project uses a very simple algorithm to build a basic, random level everytime it is opened.

FEATURES:
1. Basic UI
2. Ranomly generated levels
3. Movement and collsions
4. Saving highscore to a text file

Concepts of syllabus used:
1. Python basics
2. 2-Dimensional arrays
3. File Handling
4. Importing modules
5. Functions
6. Error handling

CLARIFICATION:
This is an original project, and is not 'copy-pasted'. Help was taken from the internet to note basic tkinter
functions. Help was also taken from www.unity.com/learn for getting the broad idea of level generation.

Searching for pyRogue on google yield three results for me: one of the used python 2.7, one used a library called libcotd,
and one wasn't even a game. This project is not related to them in any way.

MODULES USED:
1. Tkinter
(based heavily on it, installed on standard python. If not use 'sudo apt-get install python3-tk' command)
2. Random(used for level generation)
3. winsound(only for windows, error handling used if not found)

SOFTWARE USED:
1. IDLE
2. Paint.net(since ms paint doesnt support transparent images)
3. Bfxr(free software to 'generate sounds')

I have tried to explain by comments all the tkinter functions used.
Further help can be taken from https://www.tutorialspoint.com/python/python_gui_programming.htm
"""
try :
    import tkinter
except ImportError:
    print("tkinter not installed. Use 'sudo apt-get install python3-tk' command")
import random

winsoundFound=True

try:
    import winsound
except ImportError:
    print("winsound not found, sounds won't play.")
    winsoundFound=False

#constants
spriteSize=64
levelSizeX=10
levelSizeY=10

fontName="Comic Sans MS"

#root is the window that opens
root=tkinter.Tk()
root.title("pyRogue")
#Make a window of size 640x660 at x=300 and y=0 pixels on  screen
root.geometry("640x660+300+0")
root.resizable(0,0)
#window is not resizable, because resizing breaks the look of this project 

#required to declare after defining root
stoneImage=tkinter.PhotoImage(file="Images/stone.gif")
groundImage=tkinter.PhotoImage(file="Images/ground.gif")
itemImage=tkinter.PhotoImage(file="Images/itemCherry.gif")
doorImage=tkinter.PhotoImage(file="Images/door.gif")
playerImage=tkinter.PhotoImage(file="Images/player.gif")
enemyImage=tkinter.PhotoImage(file="Images/enemy.gif")
startMenuImage=tkinter.PhotoImage(file="Images/startMenu.gif")
medalImage=tkinter.PhotoImage(file="Images/medal.gif")

#for intro images, size=256x256
intro_o_Image=tkinter.PhotoImage(file="Images/Intro/1.gif")
intro_o_Image=intro_o_Image.zoom(4)
intro_t_Image=tkinter.PhotoImage(file="Images/Intro/2.gif")
intro_t_Image=intro_t_Image.zoom(4)
intro_th_Image=tkinter.PhotoImage(file="Images/Intro/3.gif")
intro_th_Image=intro_th_Image.zoom(4)
intro_f_Image=tkinter.PhotoImage(file="Images/Intro/4.gif")
intro_f_Image=intro_f_Image.zoom(4)
intro_fv_Image=tkinter.PhotoImage(file="Images/Intro/5.gif")
intro_fv_Image=intro_fv_Image.zoom(4)

def playSound(sound):
    if winsoundFound:
        #play the sound once and dont stop the program to play sound
        winsound.PlaySound(sound,winsound.SND_FILENAME|winsound.SND_ASYNC)

#Function, that have functions within. nonlocal keyword is used that basically does the same thing
#as global keyword as described in our book,but for nested functions
def buildLevel(frame,level):
    raiseFrame(frame)
    canvas=tkinter.Canvas(frame,bg="black",height=660,width=640)
    canvas.place(x=0,y=0)
    #canvas is a rectangle that covers certain part of the window and is drawable
    #In this project, it is used to draw the game's rectangle and also to recieve input from th player
    canvas.focus_set()#set focus so keyboard inputs can be accepted
    ##########################LEVEL GENERATION################################################################
    
    #since we start at position 0,0 the corners are at 0,0  0,576  576,0 576,576 (relative to canvas) for a 10x10 level
    #Initially contains the player's position so anything dont spawn there
    #except ground tiles
    groundPositions=[[spriteSize,8*spriteSize]]
    
    for x in range(levelSizeX):
        for y in range(levelSizeY):
            curGround=canvas.create_image(x*spriteSize,y*spriteSize,image=groundImage,anchor="nw")
            #not directly saving the positions,but getting them from the created instance. Both are same
            groundPositions.append(canvas.coords(curGround))
    #Fill the border with stone
    #Things drawn later are drawn on top of the previous ones
    stonePositions=[]
    for x in range(levelSizeX):
        curStone=canvas.create_image(x*spriteSize,0,image=stoneImage,anchor="nw")
        #get stone co ordinates for later movement code, returned values are 2 memeber array of floats like 0.0 64.0 etc
        stonePositions.append(canvas.coords(curStone))
        groundPositions.remove(canvas.coords(curStone))
        curStone=canvas.create_image(x*spriteSize,(levelSizeY-1)*spriteSize,image=stoneImage,anchor="nw")
        stonePositions.append(canvas.coords(curStone))
        groundPositions.remove(canvas.coords(curStone))
    #two items less sice the above loop has alredy created corner tiles
    for y in range(levelSizeY-2):
        curStone=canvas.create_image(0,(y+1)*spriteSize,image=stoneImage,anchor="nw")
        stonePositions.append(canvas.coords(curStone))
        groundPositions.remove(canvas.coords(curStone))
        curStone=canvas.create_image((levelSizeX-1)*spriteSize,(y+1)*spriteSize,image=stoneImage,anchor="nw")
        stonePositions.append(canvas.coords(curStone))
        groundPositions.remove(canvas.coords(curStone))

    #place middle stones
    #there is a one tile gap so that all levels are passable
    for x in range(levelSizeX-4):
        for y in range(levelSizeY-4):
            shouldPlaceStone=random.randint(0,levelNum-level+1)
            #random no. from 0 to(levelNum) max
            #not shouldPlace to increase stones as level increase
            if not shouldPlaceStone:
                curStone=canvas.create_image((x+2)*spriteSize,(y+2)*spriteSize,image=stoneImage,anchor="nw")
                stonePositions.append(canvas.coords(curStone))
                groundPositions.remove(canvas.coords(curStone))

    #place door
    door=canvas.create_image((levelSizeX-2)*spriteSize,spriteSize,image=doorImage,anchor="nw")
    groundPositions.remove(canvas.coords(door))

    ##########################ENEMIES GENERATIONS###############################################################
    #use the groundPosition array declared above to generate some enemies
    enemyCount=2
    #enemyInfo is a dictionary with each item as key and positions as value
    #tkinter stores items as numbers
    #the first item formed is given number 0,second 1 and so on
    enemyInfo={}
    for x in range(enemyCount):
        enemyPosition=groundPositions[random.randint(0,(len(groundPositions)-1))]#len-1 since in randint both ranges are inclusive
        curEnemy=canvas.create_image(enemyPosition[0],enemyPosition[1],image=enemyImage,anchor="nw",tag="enemy")
        enemyInfo[curEnemy]=canvas.coords(curEnemy)
        groundPositions.remove(canvas.coords(curEnemy))

    ##########################ITEMS GENERATIONS###############################################################
    #use the groundPosition array declared above to generate some items
    itemsCount=2
    #itemInfo is a dictionary with each item as key and positions as value
    #tkinter stores items as numbers
    #the first item formed is given number 0,second 1 and so on
    itemInfo={}
    for x in range(itemsCount):
        itemPosition=groundPositions[random.randint(0,(len(groundPositions)-1))]#len-1 since in randint both ranges are inclusive
        curItem=canvas.create_image(itemPosition[0],itemPosition[1],image=itemImage,anchor="nw")#not multiplying by spriteSize
        itemInfo[curItem]=canvas.coords(curItem)
        groundPositions.remove(canvas.coords(curItem))
        
    ##########################PLAYER MOVEMENT#################################################################

    #converting a .gif file to a photoimage file that tkinter can use
    #png files are not supported
    #can't make playerPosition an array since inside function, global playerPosition[0] gives syntax error
    playerPositionX=spriteSize
    playerPositionY=8*spriteSize

    #create an instance of playerPhoto at x=0,y=576(relative to canvas) and set the anchor to top left for easy movement
    player=canvas.create_image(playerPositionX,playerPositionY,image=playerImage,anchor="nw")

    ######HUD (Heads Up Display)#######
    scoreText=tkinter.Label(canvas,text="Score : "+str(score),bg="black",fg="white")
    scoreText.place(x=0,y=640)

    healthText=tkinter.Label(canvas,text="Health : "+str(playerHealth),bg="black",fg="white")
    healthText.place(x=128,y=640)

    levelText=tkinter.Label(canvas,text="Level : "+str(level),bg="black",fg="white")
    levelText.place(x=256,y=640)

    #functions required by movement functons

    def getKeyFromValue(dictionary,value):
        #value is array for current use. All items are distinct
        for x in dictionary.keys():
            if dictionary[x]==value:
                return x

    def itemEffect():
        global playerHealth
        global score#preserve the score
        score+=50
        playerHealth+=1
        playSound("Sounds/pickup.wav")
        healthText.config(text="Health : "+str(playerHealth))
        scoreText.config(text="Score : "+str(score))

    def checkDoor():
        nonlocal playerPositionX
        nonlocal playerPositionY
        global currentLevel
        if [playerPositionX,playerPositionY]==canvas.coords(door):
            if currentLevel<(levelNum-1):
                currentLevel+=1
                buildLevel(levelFrames[currentLevel],currentLevel+1)
                playSound("Sounds/elevation.wav")
            else:
                raiseFrame(gameCompleteFrame)
                gameCompleteText.config(text="YOUR SCORE WAS : " + str(score))
                global highScore
                if score>highScore:
                    highScore=score
                    highScoreFile=open("highScore.txt","w")
                    highScoreFile.write(str(highScore))
                    highScoreFile.close()
                    highScoreFile=open("highScore.txt","r")
                    highScoreFile.close()
                    highScoreText.config(text="HIGHSCORE : " + str(highScore))

    def moveEnemy():
        #keys enemy, value position array
        for x in list(enemyInfo.keys()):
            
            if (canvas.coords(x)[0]<playerPositionX and
                [canvas.coords(x)[0]+spriteSize,canvas.coords(x)[1]] in groundPositions):
                canvas.move(x,spriteSize,0)
            
            elif (canvas.coords(x)[0]>playerPositionX and
                  [canvas.coords(x)[0]-spriteSize,canvas.coords(x)[1]] in groundPositions):
                canvas.move(x,-spriteSize,0)
            
            elif (canvas.coords(x)[1]<playerPositionY and
                  [canvas.coords(x)[0],canvas.coords(x)[1]+spriteSize] in groundPositions):
                canvas.move(x,0,spriteSize)
            
            elif (canvas.coords(x)[1]>playerPositionY and
                  [canvas.coords(x)[0],canvas.coords(x)[1]-spriteSize] in groundPositions):
                canvas.move(x,0,-spriteSize)
                    
            enemyInfo[x]=canvas.coords(x)
           
            if canvas.coords(x)==[playerPositionX,playerPositionY]:
                canvas.delete(x)
                del enemyInfo[x]
                global playerHealth
                global score
                score+=100
                scoreText.config(text="Score : "+str(score))
                playerHealth-=2
                healthText.config(text="Health : "+str(playerHealth))
                playSound("Sounds/hurt.wav")
                
                if playerHealth<=0:
                    gameOverText.config(text="YOUR SCORE WAS : "+str(score))
                    gameOver()
     
            

    #movement functions
    #There are four functions. The keyboard input only give the argument of which key is pressed. No additional arguments could be added
    #So there are 4 separate functions

    def moveRight(event):
        #we need to change the global x value
        nonlocal playerPositionX#variable from parent function
        nonlocal playerPositionY
        nonlocal player
        playerPositionX+=spriteSize
        wasItemSoundNotHeard=True#winsound cant play two audios at same time
        
        if [playerPositionX,playerPositionY] in stonePositions:
            #make variables value the original
            playerPositionX-=spriteSize
            return
        
        if [playerPositionX,playerPositionY]in list(itemInfo.values()):
            item=getKeyFromValue(itemInfo,[playerPositionX,playerPositionY])
            itemEffect()
            wasItemSoundNotHeard=False
            del itemInfo[item]#delete so a player can pick item more than once
            canvas.delete(item)

        #delete current player image and add a new one with updated position
        canvas.delete(player)
        player=canvas.create_image(playerPositionX,playerPositionY,image=playerImage,anchor="nw")
        
        if wasItemSoundNotHeard:
            playSound("Sounds/step.wav")
        checkDoor()
        moveEnemy()

    def moveLeft(event):
        nonlocal playerPositionX
        nonlocal playerPositionY
        nonlocal player
        wasItemSoundNotHeard=True
        playerPositionX-=spriteSize
        
        if [playerPositionX,playerPositionY] in stonePositions:
            playerPositionX+=spriteSize
            return
        
        if [playerPositionX,playerPositionY]in list(itemInfo.values()):
            item=getKeyFromValue(itemInfo,[playerPositionX,playerPositionY])
            itemEffect()
            wasItemSoundNotHeard=False
            del itemInfo[item]
            canvas.delete(item)
        
        canvas.delete(player)
        player=canvas.create_image(playerPositionX,playerPositionY,image=playerImage,anchor="nw")
        
        if wasItemSoundNotHeard:
            playSound("Sounds/step.wav")
        checkDoor()
        moveEnemy()

    def moveUp(event):
        nonlocal playerPositionX
        nonlocal playerPositionY
        nonlocal player
        wasItemSoundNotHeard=True
        # in computer graphics, the positive y axis is downwards
        playerPositionY-=spriteSize
        
        if [playerPositionX,playerPositionY] in stonePositions:
            playerPositionY+=spriteSize
            return
        
        if [playerPositionX,playerPositionY]in list(itemInfo.values()):
            item=getKeyFromValue(itemInfo,[playerPositionX,playerPositionY])
            itemEffect()
            wasItemSoundNotHeard=False
            del itemInfo[item]
            canvas.delete(item)
        
        canvas.delete(player)
        player=canvas.create_image(playerPositionX,playerPositionY,image=playerImage,anchor="nw")
        
        if wasItemSoundNotHeard:
            playSound("Sounds/step.wav")
        checkDoor()
        moveEnemy()

    def moveDown(event):
        nonlocal playerPositionX
        nonlocal playerPositionY
        nonlocal player
        wasItemSoundNotHeard=True
        playerPositionY+=spriteSize
        
        if [playerPositionX,playerPositionY] in stonePositions:
            playerPositionY-=spriteSize
            return
        
        #If player position matches any position in itemInfo values, i.e., item positions, then
        #it takes the key of itemInfo, i.e., the actual item and deltes it from the canvas
        if [playerPositionX,playerPositionY]in list(itemInfo.values()):
            item=getKeyFromValue(itemInfo,[playerPositionX,playerPositionY])
            itemEffect()
            wasItemSoundNotHeard=False
            del itemInfo[item]
            canvas.delete(item)
        
        canvas.delete(player)
        player=canvas.create_image(playerPositionX,playerPositionY,image=playerImage,anchor="nw")
        
        if wasItemSoundNotHeard:
            playSound("Sounds/step.wav")
        checkDoor()
        moveEnemy()

    #bind the canvas with keyboard keys to recieve input and call a function when input is given
    #It is required to place it at the end
    canvas.bind("w",moveUp)
    canvas.bind("<Up>",moveUp)#arrow key

    canvas.bind("a",moveLeft)
    canvas.bind("<Left>",moveLeft)

    canvas.bind("s",moveDown)
    canvas.bind("<Down>",moveDown)

    canvas.bind("d",moveRight)
    canvas.bind("<Right>",moveRight)

    #######################################


levelNum=5

highScoreFile=open("highScore.txt","r")
highScore=int(highScoreFile.read())
highScoreFile.close()

playerHealth=5
score=0

#frames are containers
#used here for changing 'levels'

levelFrames=[]

for x in range(levelNum):
    curFrame=tkinter.Frame(root,width=640,height=660)
    curFrame.place(x=0,y=0)
    levelFrames.append(curFrame)

currentLevel=0

#raise the current frame so that it shows up
def gameOver():
    gameOverFrame.tkraise()

def raiseFrame(frame):
    frame.tkraise()
    #change wordsOfWisdom text
    if frame==startFrame:
        global wordsOfWisdomIndex
        wordsOfWisdomIndex=random.randint(0,len(wordsOfWisdom)-1)
        wordsOfWisdomText.config(text=wordsOfWisdom[wordsOfWisdomIndex])

def startPressed():
    playSound("Sounds/select.wav")
    buildLevel(levelFrames[currentLevel],currentLevel+1)

def gameCompletePressed():
    global score
    global playerHealth
    global currentLevel
    playSound("Sounds/select.wav")
    currentLevel=0
    score=0
    playerHealth=5
    raiseFrame(startFrame)

def intro():
    playSound("Sounds/select.wav")
    raiseFrame(introFrame)

def credit():
    playSound("Sounds/select.wav")
    raiseFrame(creditFrame)

def introToMainSwitch():
    global allIntroIndex
    playSound("Sounds/select.wav")
    raiseFrame(startFrame)
    introCanvas.itemconfig(currentIntroImage,image=allIntroImages[0])
    currentIntroText.config(text=allIntroText[0])
    allIntroIndex=0

def creditToMainSwitch():
    playSound("Sounds/select.wav")
    raiseFrame(startFrame)
    
allIntroImages=[intro_o_Image,intro_t_Image,intro_th_Image,intro_f_Image,intro_fv_Image]
#use \n for newline
allIntroText=["\
Old tales claim that whoever goes into the 'Cave of Mourning'\n\
never returns. The king ordered me to go there and kill everyone\n\
present there, as I was the kingdom's assasian.",
"After hours of searching, I found the monster. He was looking into my\n\
eyes. And I was just about to take out my dagger when I saw that....",
"....he was smiling. He came to me and told me that all his friends are\n\
throwing a party tonight, and he invited me! He asked me if I could find\n\
the rest of his friends and tell them to come too.",
"These people were very friendly. To persuade them to go with you,\n\
you just have to shake hands with them. Though, I found that everytime I \n\
touch their skin, my 'health' drops, and that everytime one of them agrees\n\
to come to the party, my 'score' increases.",
"I will not let the hopes go down!"
]
allIntroIndex=0
def nextIntro():
    global allIntroIndex
    if allIntroIndex<(len(allIntroImages)-1):
        playSound("Sounds/select.wav")
        allIntroIndex+=1
        introCanvas.itemconfig(currentIntroImage,image=allIntroImages[allIntroIndex])
        currentIntroText.config(text=allIntroText[allIntroIndex])
    pass

#tkinter doesnt support taking fonts from file

gameCompleteFrame=tkinter.Frame(root,width=640,height=660)
gameCompleteFrame.place(x=0,y=0)
gameCompleteCanvas=tkinter.Canvas(gameCompleteFrame,bg="black",width=660,height=680)
gameCompleteCanvas.place(x=-10,y=-10)
gameCompleteCanvas.create_image(10,10,image=medalImage,anchor="nw")
#there is a separate function for button pressed since command function doesnt take any arguments
tkinter.Label(gameCompleteCanvas,text="YOU WON!!",fg="yellow",bg="#28208c",font=(fontName,12)).place(x=310,y=400)
gameCompleteText=tkinter.Label(gameCompleteCanvas,text="YOUR SCORE WAS : " + str(score),fg="yellow",bg="#28208c",font=(fontName,12))
gameCompleteText.place(x=280,y=460)
highScoreText=tkinter.Label(gameCompleteCanvas,text="HIGHSCORE : "+str(highScore),fg="yellow",bg="#28208c",font=(fontName,12))
highScoreText.place(x=280,y=500)
gameCompleteButton=tkinter.Button(gameCompleteCanvas,text="RETURN",width=10,fg="yellow",bg="#28208c",font=(fontName,12),command=gameCompletePressed)
gameCompleteButton.place(x=300,y=540)

gameOverFrame=tkinter.Frame(root,width=640,height=660)
gameOverFrame.place(x=0,y=0)
gameOverCanvas=tkinter.Canvas(gameOverFrame,bg="black",width=660,height=680)
gameOverCanvas.place(x=-10,y=-10)
tkinter.Label(gameOverCanvas,text="YOU LOST",fg="white",bg="black",font=(fontName,12)).place(x=310,y=200)
gameOverText=tkinter.Label(gameOverCanvas,text="YOUR SCORE WAS : " + str(score),fg="white",bg="black",font=(fontName,12))
gameOverText.place(x=280,y=260)
gameOverButton=tkinter.Button(gameOverCanvas,text="RETURN",width=10,fg="white",bg="black",font=(fontName,12),command=gameCompletePressed)
gameOverButton.place(x=300,y=320)

introFrame=tkinter.Frame(root,width=640,height=660)
introFrame.place(x=0,y=0)
introCanvas=tkinter.Canvas(introFrame,bg="black",width=660,height=680)
introCanvas.place(x=-10,y=-10)
currentIntroImage=introCanvas.create_image(80,32,image=allIntroImages[0],anchor="nw")
currentIntroText=tkinter.Label(introCanvas,text=allIntroText[0],bg="black",fg="white",font=(fontName,10))
currentIntroText.place(x=130,y=550)
nextIntro=tkinter.Button(introCanvas,text="NEXT",width=10,bg="black",fg="white",command=nextIntro,font=(fontName,8))
nextIntro.place(x=250,y=640)
introToMain=tkinter.Button(introCanvas,text="MAIN MENU",width=10,bg="black",fg="white",command=introToMainSwitch,font=(fontName,8))
introToMain.place(x=350,y=640)

creditText="1. NIKHIL KADIYAN, ROLL NO. 24\n\
 Programming, Testing, Asset making"
creditFrame=tkinter.Frame(root,width=640,height=660)
creditFrame.place(x=0,y=0)
creditCanvas=tkinter.Canvas(creditFrame,bg="black",width=660,height=680)
creditCanvas.place(x=-10,y=-10)
tkinter.Label(creditCanvas,text="THEY MADE IT(NOBODY KNOWS WHY) : ",bg="black",fg="white",font=(fontName,10)).place(x=130,y=10)
tkinter.Label(creditCanvas,text=creditText,bg="black",fg="white",font=(fontName,10)).place(x=130,y=50)
tkinter.Label(creditCanvas,text="I hope that you like it!",bg="black",fg="white",font=(fontName,10)).place(x=280,y=580)
creditToMain=tkinter.Button(creditCanvas,text="MAIN MENU",width=10,bg="black",fg="white",command=creditToMainSwitch,font=(fontName,8))
creditToMain.place(x=300,y=640)

#random quotes, inspired from Minecraft's title screen
#80 character limit
#Duplicate lines so they show more often
wordsOfWisdom=[
"This isn't even my final form.",
"All we have to do was to follow the train, CJ",
"This man makes sure that nobody steals the candle.",
"Any computer is a laptop if you are brave enough!",
"Semicolons? We don't do that here.",
"State of the art visuals.",
"It's the endgame.",
"Gamers don't die. They respawn.",
"12345 is a bad password.",
"90% bug free!",
"Any computer is a laptop if you are brave enough!",
"Where there is a code, there is a bug.",
"pyRogue!",
"Have you played Undertale?",
"Play Deltarune. It's free!",
"It's a game. Surprise!",
"Any computer is a laptop if you are brave enough!",
"Made in India",
"sqrt(-1) like you!",
"Don't kill people.",
"School project.",
"Kendriya Vidyalaya, Shalimar Bagh"]
wordsOfWisdomIndex=random.randint(0,len(wordsOfWisdom)-1)

startFrame=tkinter.Frame(root,width=640,height=660)
startFrame.place(x=0,y=0)
startCanvas=tkinter.Canvas(startFrame,bg="black",width=660,height=680)
#for some reason,there were white lines on corner of window, so
#placing the canvas to spread over the screen
startCanvas.place(x=-10,y=-10)
startCanvas.create_image(10,10,image=startMenuImage,anchor="nw")
#there is a separate function for button pressed since command function doesnt take any arguments
startButton=tkinter.Button(startCanvas,text="START",width=10,bg="#20203a",fg="yellow",command=startPressed,font=(fontName,12))
startButton.place(x=315,y=340)
introButton=tkinter.Button(startCanvas,text="INTRO",width=10,bg="#20203a",fg="yellow",command=intro,font=(fontName,12))
introButton.place(x=315,y=380)
creditButton=tkinter.Button(startCanvas,text="CREDITS",width=10,bg="#20203a",fg="yellow",command=credit,font=(fontName,12))
creditButton.place(x=315,y=420)
quitButton=tkinter.Button(startCanvas,text="QUIT",width=10,bg="#20203a",fg="yellow",font=(fontName,12),command=root.destroy)
quitButton.place(x=315,y=460)
wordsOfWisdomText=tkinter.Label(startCanvas,text=wordsOfWisdom[wordsOfWisdomIndex],bg="#20203a",fg="yellow",font=(fontName,12))
wordsOfWisdomText.place(x=10,y=620)
raiseFrame(startFrame)


#update the window
root.mainloop()
