

class RO_SHAM_BO():

	

	def __init__(self,player1,player2):

		self.player1 = player1
		self.player2 = player2
		


	def start_game():

		print("welcome to RO-SHAM-BO")
		print("The game is best 2 out of 3")
		print("options include 'rock', 'paper', 'scissors' ")
		print("you may begain")

		player1 = input("player1 enter:")
		player2 = input ("player2 enter:")

		RO_SHAM_BO.game(player1,player2)


	def set_string(player):
		RO = "rock"
		SHAM = "paper"
		BO = "scissors"
		i = 0

		if player == RO:
			i = 1
		elif player == SHAM:
			i = 2
		elif player == BO:
			i = 3 
		else:
			pass

		return i


	def game(player1,player2):

		p1 = 0 
		p2 = 0
		point = 0

		# compair the result of players input for game 

		p1 = RO_SHAM_BO.set_string(player1)
		p2 = RO_SHAM_BO.set_string(player2)



		# decide winnier and increase score
		
		if p1 < p2:
			# add point to player1
			RO_SHAM_BO.score(1,0)
		elif p1 > p2:
			# add point to player2
			RO_SHAM_BO.score(0,1)
		


	def score(p1,p2):
		# fix score list to create the list once
		scorelist = [0,0]
		temp1 = scorelist[0]
		temp2 = scorelist[1]
		scorelist[0] = temp1 + p1
		scorelist[1] = temp2 + p2 

		if scorelist[0] or scorelist[1] == 3:
			if scorelist[0] == 3:
				print("player1 wins")
				# RO_SHAM_BO.Game_over()
			elif scorelist[1] == 3:
				print("player2 wins")
				# RO_SHAM_BO.Game_over()
				
		# else:
		# 	return str(scorelist)
		# 	print("The Score is " + scorelist)
		# 	# RO_SHAM_BO.game2()
		if scorelist[0] or scorelist[1] != 3:
			
			print("The Score is " + str(scorelist[0:2]))
			RO_SHAM_BO.game2()


		

	def game2():
		player1 = input("player1 enter:")
		player2 = input ("player2 enter:")

		RO_SHAM_BO.game(player1,player2)



	def Game_over():
		print("Thank you for playing")
		return 0



	
	

test = RO_SHAM_BO.start_game()




# def start_game():

# 	print("welcome to RO-SHAM-BO")
# 	print("The game is best 2 out of 3")
# 	print("options include 'rock', 'paper', 'scissors' ")
# 	print("you may begain")


# 	player1 = input("player1 enter:")
# 	player2 = input ("player2 enter:")

# 	game(player1,player2)


# def game(player1,player2):

# 	p1 = 0
# 	p2 = 0
# 	point = 0

# 		# compair the result of players input for game 

# 	p1 = set_string(player1)
# 	p2 = set_string(player2)

# 		# decide winnier and increase score

# 	if p1 < p2:
# 			# add point to player1
# 		score(1,0)
# 	else:
# 			# add point to player2
# 		score(0,1)

# def score(p1,p2):
# 	scorelist = [0,0]
# 	temp1 = scorelist[0]
# 	temp2 = scorelist[1]
# 	scorelist[0] = temp1 + p1
# 	scorelist[1] = temp2 + p2 

# 	if scorelist[0] or scorelist[1] == 3:
# 		if scorelist[0] == 3:
# 			print("player1 wins")
# 		elif scorelist[1] == 3:
# 			print("player2 wins")

# 	else:
# 		pass


# 	print(scorelist)
# 	return scorelist

# def set_string(player):
# 	RO = "rock"
# 	SHAM = "paper"
# 	BO = "scissors"

# 	i = 0

# 	if player == RO:
# 		i = 1
# 	elif player == SHAM:
# 		i = 2
# 	elif player == BO:
# 		i = 3 
# 	else:
# 		pass

# 	return i



# start_game()

