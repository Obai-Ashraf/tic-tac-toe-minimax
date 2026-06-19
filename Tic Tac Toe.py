# ======================= OBAI =======================

import tkinter as tk
from tkinter import messagebox
import random

board = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' '
}

player = 'O'
computer = 'X'

buttons = {}

gameOver = False
aiMoveID = None
playerTurn = False
moveInProgress = False

difficulty = "Hard"

playerScore = 0
botScore = 0


def checkWhichMarkWon(mark):
    wins = [
        (1,2,3), (4,5,6), (7,8,9),
        (1,4,7), (2,5,8), (3,6,9),
        (1,5,9), (3,5,7)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] == mark:
            return True
    return False


def checkDraw():
    return all(board[k] != ' ' for k in board)


def updateButtons():
    for k in buttons:
        buttons[k]["text"] = board[k]


def updateStatus(text):
    statusLabel.config(text=text)


def updateScore():
    scoreLabel.config(text=f"Player ({player}): {playerScore}   |   Bot ({computer}): {botScore}")



# ======================= SHERIF =======================

def minimax(isMax):
    if checkWhichMarkWon(computer):
        return 1
    if checkWhichMarkWon(player):
        return -1
    if checkDraw():
        return 0

    if isMax:
        best = -999
        for k in board:
            if board[k] == ' ':
                board[k] = computer
                score = minimax(False)
                board[k] = ' '
                best = max(best, score)
        return best
    else:
        best = 999
        for k in board:
            if board[k] == ' ':
                board[k] = player
                score = minimax(True)
                board[k] = ' '
                best = min(best, score)
        return best


def compMove():
    global gameOver, aiMoveID, playerTurn, moveInProgress

    if gameOver:
        return

    moveInProgress = True

    move = None

    empty = [k for k in board if board[k] == ' ']

    if not empty:
        moveInProgress = False
        return

    if difficulty == "Easy":
        move = random.choice(empty)

    elif difficulty == "Medium":
        if random.random() < 0.7:
            bestScore = -999
            for k in empty:
                board[k] = computer
                score = minimax(False)
                board[k] = ' '
                if score > bestScore:
                    bestScore = score
                    move = k
        else:
            move = random.choice(empty)

    else:
        bestScore = -999
        for k in empty:
            board[k] = computer
            score = minimax(False)
            board[k] = ' '
            if score > bestScore:
                bestScore = score
                move = k

    if move is not None:
        board[move] = computer
        updateButtons()

    if checkWhichMarkWon(computer):
        gameOver = True
        global botScore
        botScore += 1
        updateStatus("Bot Wins!")
        updateScore()
        moveInProgress = False
        showGameOverMessage("Bot Wins! 🎉", f"Bot ({computer}) has won!\n\nPlayer: {playerScore}  |  Bot: {botScore}")
        return

    if checkDraw():
        gameOver = True
        updateStatus("Draw!")
        moveInProgress = False
        showGameOverMessage("It's a Draw! 🤝", f"No one wins this round!\n\nPlayer: {playerScore}  |  Bot: {botScore}")
        return

    updateButtons()

    if not gameOver:
        updateStatus(f"Player Turn ({player})")
        playerTurn = True
    
    moveInProgress = False



# ======================= YOUSSEF 1 =======================

def playerMove(pos):
    global aiMoveID, gameOver, playerScore, playerTurn, moveInProgress

    if gameOver or not playerTurn or moveInProgress:
        return

    if board[pos] == ' ':
        moveInProgress = True
        playerTurn = False
        board[pos] = player
        updateButtons()

        if checkWhichMarkWon(player):
            gameOver = True
            playerScore += 1
            updateStatus("Player Wins!")
            updateScore()
            moveInProgress = False
            showGameOverMessage("You Win! 🎊", f"Player ({player}) has won!\n\nPlayer: {playerScore}  |  Bot: {botScore}")
            return

        if checkDraw():
            gameOver = True
            updateStatus("Draw!")
            moveInProgress = False
            showGameOverMessage("It's a Draw! 🤝", f"No one wins this round!\n\nPlayer: {playerScore}  |  Bot: {botScore}")
            return

        updateStatus("Bot Thinking...")
        moveInProgress = False
        aiMoveID = root.after(500, compMove)


def showGameOverMessage(title, message):
    messagebox.showinfo(title, message)
    restartGame()


def startNewGame():
    global gameOver, aiMoveID, playerTurn, player, computer, moveInProgress

    if aiMoveID is not None:
        root.after_cancel(aiMoveID)
        aiMoveID = None

    for k in board:
        board[k] = ' '

    gameOver = False
    moveInProgress = False
    playerTurn = False
    updateButtons()
    
    if random.choice([True, False]):
        player = 'X'
        computer = 'O'
        updateScore()
        playerTurn = True
        updateStatus(f"Player Turn ({player})")
    else:
        player = 'O'
        computer = 'X'
        updateScore()
        playerTurn = False
        updateStatus("Bot Thinking...")
        aiMoveID = root.after(500, compMove)


def restartGame():
    startNewGame()



# ======================= YOUSSEF 2 =======================

root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("340x550")
root.config(bg="#f0f0f0")

titleLabel = tk.Label(root, text="Tic Tac Toe", font=('Arial', 20, 'bold'), bg="#f0f0f0")
titleLabel.pack(pady=10)

statusLabel = tk.Label(root, text="Loading...", font=('Arial', 12), bg="#f0f0f0", fg="#333")
statusLabel.pack(pady=5)

scoreLabel = tk.Label(root, text="Player (O): 0   |   Bot (X): 0", font=('Arial', 10), bg="#f0f0f0", fg="#666")
scoreLabel.pack(pady=5)

difficultyVar = tk.StringVar(value="Hard")

def setDifficulty(val):
    global difficulty
    difficulty = val

difficultyFrame = tk.Frame(root, bg="#f0f0f0")
difficultyFrame.pack(pady=10)

tk.Label(difficultyFrame, text="Difficulty:", font=('Arial', 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

tk.OptionMenu(difficultyFrame, difficultyVar, "Easy", "Medium", "Hard", command=setDifficulty).pack(side=tk.LEFT)

boardFrame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
boardFrame.pack(padx=20, pady=15)

for i in range(1, 10):
    btn = tk.Button(
        boardFrame,
        text=' ',
        width=5,
        height=2,
        font=('Arial', 18, 'bold'),
        command=lambda i=i: playerMove(i),
        bg="#ffffff",
        activebackground="#e0e0e0"
    )

    btn.grid(row=(i-1)//3, column=(i-1)%3, padx=2, pady=2)

    buttons[i] = btn

tk.Button(root, text="Restart Game", command=restartGame, font=('Arial', 10, 'bold'), 
          bg="#4CAF50", fg="white", padx=20, pady=10)\
    .pack(pady=15)

startNewGame()

root.mainloop()