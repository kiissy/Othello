
from bangtal import *
import enum
import time

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

# 장면 생성
scene = Scene("오셀로", "images/background.png")

board = Object("images/board.png")
board.locate(scene, 40, 40)

class StoneStatus(enum.Enum):
	BLANK = 1
	BLACK_POSSIBLE = 2
	WHITE_POSSIBLE = 3
	BLACK = 4
	WHITE = 5

class Turn(enum.Enum):
	BLACK = 0
	WHITE = 1

def stone_img(status):
	if status == StoneStatus.BLANK:
		img = "images/blank.png"
	elif status == StoneStatus.BLACK_POSSIBLE:
		img = "images/black possible.png"
	elif status == StoneStatus.WHITE_POSSIBLE:
		img = "images/white possible.png"
	elif status == StoneStatus.BLACK:
		img = "images/black.png"
	elif status == StoneStatus.WHITE:
		img = "images/white.png"
	return img

def num_img(num):
	num = str(num)
	img = "images/L" + num + ".png"
	return img

game_board = []
def score():
	black = 0
	white = 0
	for i in range(8):
		for j in range(8):
			if game_board[i][j].status == StoneStatus.BLACK:
				black = black + 1
			elif game_board[i][j].status == StoneStatus.WHITE:
				white = white + 1
	return black, white

turn = Turn.BLACK
black_score = 0
white_score = 0
# stone class
class Stone(Object):
	def __init__(self, file, scene, x, y, status, i, j):
		super().__init__(file)
		self.locate(scene, x, y)
		self.show()
		self.status = status
		self.i = i
		self.j = j

	def cg_status(self, status):
		self.status = status
		self.setImage(stone_img(status))

	def get_index(self):
		return self.i, self.j

	def put_stone(self, turn):
		k=-1; x=-1; y=-1
		if turn == Turn.BLACK and self.status == StoneStatus.BLACK_POSSIBLE:
			self.cg_status(StoneStatus.BLACK)
			check(self.i, self.j, turn)
			for i in range(8):
				for j in range (8):
					if game_board[i][j].status == StoneStatus.BLACK_POSSIBLE:
						game_board[i][j].cg_status(StoneStatus.BLANK)
			turn = Turn.WHITE
			for i in range(8):
				for j in range (8):
					if game_board[i][j].status == StoneStatus.WHITE:
						k_k, x_x, y_y = possible(i, j, turn)
						if k_k > k:
							k = k_k
							x = x_x
							y = y_y

			## 자동 변환
			if x == -1 or y == -1:
				turn = Turn.BLACK
				return turn
			else:
				print(x, y)
				game_board[x][y].cg_status(StoneStatus.WHITE)
				check(x, y, turn)
				for i in range(8):
					for j in range (8):
						if game_board[i][j].status == StoneStatus.WHITE_POSSIBLE:
							game_board[i][j].cg_status(StoneStatus.BLANK)
				turn = Turn.BLACK
				for i in range(8):
					for j in range (8):
						if game_board[i][j].status == StoneStatus.BLACK:
							possible(i, j, turn)
		#elif turn == Turn.WHITE and self.status == StoneStatus.WHITE_POSSIBLE:
		#	self.cg_status(StoneStatus.WHITE)
		#	check(self.i, self.j, turn)
		#	for i in range(8):
		#		for j in range (8):
		#			if game_board[i][j].status == StoneStatus.WHITE_POSSIBLE:
		#				game_board[i][j].cg_status(StoneStatus.BLANK)
		#	turn = Turn.BLACK
		#	for i in range(8):
		#		for j in range (8):
		#			if game_board[i][j].status == StoneStatus.BLACK:
		#				possible(i, j, turn)
		return turn

	def onMouseAction(self, x, y, action):
		global turn, black_score, white_score

		#put stone
		turn = self.put_stone(turn)

		# score
		black_score, white_score = score()
		display_black_score(black_score)
		display_white_score(white_score)

		# is End
		can_continue = 0
		for i in range(8):
			for j in range(8):
				if game_board[i][j].status == StoneStatus.BLACK_POSSIBLE or game_board[i][j].status == StoneStatus.WHITE_POSSIBLE:
					can_continue = can_continue + 1
		if can_continue == 0:
			showMessage("Game End!")
		
dx=[-1,-1,0,1,1,1,0,-1]
dy=[0,-1,-1,-1,0,1,1,1]

def possible(x, y, turn):
	white_k = -1
	white_x = -1
	white_y = -1
	for i in range(8):
		k = 1
		while(1):
			check_x = x + k * dx[i]
			check_y = y + k * dy[i]
			if check_x >= 0 and check_x < 8 and check_y >= 0 and check_y < 8:
				if turn == Turn.BLACK:
					if game_board[check_x][check_y].status == StoneStatus.WHITE:
						k = k + 1
					elif game_board[check_x - dx[i]][check_y - dy[i]].status == StoneStatus.WHITE and game_board[check_x][check_y].status == StoneStatus.BLANK:
						game_board[check_x][check_y].cg_status(StoneStatus.BLACK_POSSIBLE)
						break
					else: break
				elif turn == Turn.WHITE:
					if game_board[check_x][check_y].status == StoneStatus.BLACK:
						k = k + 1
					elif game_board[check_x - dx[i]][check_y - dy[i]].status == StoneStatus.BLACK and game_board[check_x][check_y].status == StoneStatus.BLANK:
						if k > white_k:
							white_k = k
							white_x = check_x
							white_y = check_y
						game_board[check_x][check_y].cg_status(StoneStatus.WHITE_POSSIBLE)
						break
					else: break
			else: break
	return white_k, white_x, white_y

# 돌 색깔 바꾸기
def check(x, y, turn):
	for i in range(8):
		k = 1
		while(1):
			check_x = x + k * dx[i]
			check_y = y + k * dy[i]
			if check_x >= 0 and check_x < 8 and check_y >= 0 and check_y < 8:
				if turn == Turn.BLACK:
					if game_board[check_x][check_y].status == StoneStatus.WHITE:
						k = k + 1
					elif game_board[check_x][check_y].status == game_board[x][y].status and game_board[check_x - dx[i]][check_y - dy[i]].status == StoneStatus.WHITE:
						for l in range(1, k):
							cg_x = x + l * dx[i]
							cg_y = y + l * dy[i]
							game_board[cg_x][cg_y].cg_status(game_board[x][y].status)
						break
					else: break
				elif turn == Turn.WHITE:
					if game_board[check_x][check_y].status == StoneStatus.BLACK:
						k = k + 1
					elif game_board[check_x][check_y].status == game_board[x][y].status and game_board[check_x - dx[i]][check_y - dy[i]].status == StoneStatus.BLACK:
						for l in range(1, k):
							cg_x = x + l * dx[i]
							cg_y = y + l * dy[i]
							game_board[cg_x][cg_y].cg_status(game_board[x][y].status)
						break
					else: break
			else: break

class Score(Object):
	def __init__(self, file, scene, x, y, num):
		super().__init__(file)
		self.locate(scene, x, y)
		self.num = num

	def cg_num(self, num):
		self.num = num
		self.setImage(num_img(num))

# 게임 보드에 stone 생성 및 배열 저장
for i in range(8):
	line = []
	for j in range(8):
		stone = Stone(stone_img(StoneStatus.BLANK), scene, 40 + 80*i, 40 + 80*j, StoneStatus.BLANK, i, j)
		line.append(stone)
	game_board.append(line)

# 초기화
b_score_1 = Score(num_img(0), scene, 750, 220, 0)
b_score_2 = Score(num_img(0), scene, 830, 220, 0)

w_score_1 = Score(num_img(0), scene, 1070, 220, 0)
w_score_2 = Score(num_img(0), scene, 1150, 220, 0)

# 점수 표시 및 정렬
def display_black_score(score):
	if score < 10:
		b_score_1.cg_num(score)
		b_score_1.show()
		b_score_2.hide()

	elif score >= 10:
		b_score_1.cg_num(score // 10)
		b_score_2.cg_num(score % 10)
		b_score_1.show()
		b_score_2.show()

def display_white_score(score):
	if score < 10:
		w_score_2.cg_num(score)
		w_score_1.hide()
		w_score_2.show()

	elif score >= 10:
		w_score_1.cg_num(score // 10)
		w_score_2.cg_num(score % 10)
		w_score_1.show()
		w_score_2.show()

game_board[3][3].cg_status(StoneStatus.BLACK)
game_board[4][4].cg_status(StoneStatus.BLACK)
game_board[3][4].cg_status(StoneStatus.WHITE)
game_board[4][3].cg_status(StoneStatus.WHITE)
black_score, white_score = score()
display_black_score(black_score)
display_white_score(white_score)

for i in range(8):
	for j in range (8):
		if game_board[i][j].status == StoneStatus.BLACK:
			possible(i, j, turn)

# 게임 시작
startGame(scene)