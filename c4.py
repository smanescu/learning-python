import numpy as np
import pygame
import math

ROWS = 6
COLUMNS = 7

image = pygame.image.load("pop.png")

board = np.zeros((ROWS, COLUMNS))

game_over = False
turn = 0

SLOT = 100
width = COLUMNS * SLOT
height = (ROWS+1) * SLOT
size = (width, height)

#The start position is at top left (0,0). For horizontal and vertical, it starts at 0 and goes until 700
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (128,128,128)
OFFSET = 100
RADIUS = int(SLOT/2 - 5)

def draw_board(board):
	pygame.draw.rect(window, GRAY, (0,0,width, SLOT)) 
	for c in range(COLUMNS):
		for r in range(ROWS):
			rect = (c*SLOT, r*SLOT+OFFSET, SLOT, SLOT) #it takes 4 arguments: Left position(c*SLOT size), Top position(r*SLOT+OFFSET), width of SLOT, height of SLOT 
			c1 = (int(c*SLOT+SLOT/2), int(r*SLOT+OFFSET+SLOT/2)) #defines the circle parameters, it takes two parameters (x and y positions).
			pygame.draw.rect(window, BLUE, rect) #the window we created earlier, the blue color and the circle
			pygame.draw.circle(window, GRAY, c1, RADIUS)
	for c in range(COLUMNS):
		for r in range(ROWS):
			c2 = (int(c*SLOT+SLOT/2), height-int(r*SLOT+SLOT/2)) 
			if board[r][c] == 1:
				pygame.draw.circle(window, RED, c2, RADIUS) #Whenever it finds a red circle, or player 1 slot
			elif board[r][c] == 2:
				pygame.draw.circle(window, GREEN, c2, RADIUS)#Whenever it finds a green circle, or player 2 slot
	pygame.display.update()

def is_valid_location(board, col):
	return board [ROWS-1][col] == 0

def drop_piece(board, col, piece):
	for r in range(ROWS):
			if board[r][col] == 0:
				row = r
				break
	board[row][col] = piece
def is_winning_move(board,piece):
	#Check horizontal locations for win
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board [r][c+2] == piece and board [r][c+3] == piece:
				return True
	#Check vertical locations for win
	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board [r+2][c] == piece and board [r+3][c] == piece:
				return True
	#Check for positive diagonal locations for win
	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board [r+2][c+2] == piece and board [r+3][c+3] == piece:
				return True
	#Check for negative diagonal locations for win
	for c in range(COLUMNS-3):
		for r in range(3,ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board [r-2][c+2] == piece and board [r-3][c+3] == piece:
				return True		
print(board)
pygame.init()
window = pygame.display.set_mode(size)
pygame.display.set_caption("connect 4")
font = pygame.font.SysFont("Comic Sans MS", 33, True) #3 arguments: Font, the size and Bold(=True) or not(=False)
draw_board(board)

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(window, GRAY, (0,0,width, SLOT))
			posx = event.pos[0]
			if turn %2 == 0:
				pygame.draw.circle(window, RED, (posx, int(SLOT/2)), RADIUS)
			else:
				pygame.draw.circle(window, GREEN, (posx, int(SLOT/2)), RADIUS)
		pygame.display.update()


		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.pos)

			if turn %2 == 0:
				#Ask for player 1" input
				posx = event.pos[0]
				col = math.floor(posx/SLOT)
				if is_valid_location(board,col):
					drop_piece(board,col,1)
					if is_winning_move(board, 1):
						#print("Congrats Player 1")
						label = font.render("PLAYER 1 WON!", True, RED) # 3 arguments: text written, "Smooth surface = True, color of text"
						game_over = True
				else:
					turn-=1
			else:
				#Ask for player 2"s input
				posx = event.pos[0]
				col = math.floor(posx/SLOT)
				if is_valid_location(board,col):
					drop_piece(board,col,2)
					if is_winning_move(board, 2):
						#print("Congrats Player 2")
						label = font.render("PLAYER 2 WON!", True, GREEN) # 3 arguments: text written, "Smooth surface = True, color of text"

						game_over = True
				else:
					turn-=1


			turn+=1
			print(np.flip(board,0))
			draw_board(board)

if game_over:
	window.blit(image, (120,220)) #import the image, and tell the x and y positions to put it on
	window.blit(label,(170,350))
	pygame.display.update()
	pygame.time.wait(3000) #When the flag turn true, the game will closes. This delays the shutdown so we can see the winner label