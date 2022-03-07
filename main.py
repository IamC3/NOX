from projectconstants import DIVIDER, BASE_CHANCE, GAIN, LOSS, DRAW, SURRENDER, FILE, PREF, RESET, TCOLOURS
from random import choices, randint
from re import finditer
from os import path, access, R_OK
import json

boxes = [
  ["N", "N", "N"],
  ["N", "N", "N"],
  ["N", "N", "N"]
  ]

done = False
win = False
forfeit = False
you = ""
opponent = ""
null = ""
winner = ""
playerColour = ""
opponentColour = ""
colour = 0
result = 0
cont = True
Pass = False
colourSelect = True
turn = []
coords = []
burden = []
options = []

def startupCheck():
  if not path.isfile("DATA/" + FILE) and access("DATA/" + FILE, R_OK):
    # Check if file doesn't exist 
    print ("Either file is missing or is not readable, creating file...")
    with open("DATA/" + FILE, 'w+') as outfile:  
      data = {}
      json.dump(data, outfile)


def display():
  print(" \t  a   b   c\n")
  print("1  ", end = DIVIDER)
  for b in boxes[0]:
    if b == "X":
      print(f'{PREF}0;{playerColour}' + b + RESET, end = DIVIDER)
    elif b == "O":
      print(f'{PREF}0;{opponentColour}' + b + RESET, end = DIVIDER)
    else:
      print(b + DIVIDER, end = "")
  print()
  print("2  ", end = DIVIDER)
  for b in boxes[1]:
    if b == "X":
      print(f'{PREF}0;{playerColour}' + b + RESET, end = DIVIDER)
    elif b == "O":
      print(f'{PREF}0;{opponentColour}' + b + RESET, end = DIVIDER)
    else:
      print(b + DIVIDER, end = "")
  print()
  print("3  ", end = DIVIDER)
  for b in boxes[2]:
    if b == "X":
      print(f'{PREF}0;{playerColour}' + b + RESET, end = DIVIDER)
    elif b == "O":
      print(f'{PREF}0;{opponentColour}' + b + RESET, end = DIVIDER)
    else:
      print(b + DIVIDER, end = "")
  print()
      
def players():
  global you, opponent, null, playerColour, opponentColour, colourSelect, colour
  you = "X"
  opponent = "O"
  null = "N"

  if colour == 0:
    colourSelect = True
  
  while colourSelect:
    print("Select colour:")
    print(f'{PREF}0;{TCOLOURS[0]}' + "1 - Black" + RESET)
    print(f'{PREF}0;{TCOLOURS[1]}' + "2 - Red" + RESET)
    print(f'{PREF}0;{TCOLOURS[2]}' + "3 - Green" + RESET)
    print(f'{PREF}0;{TCOLOURS[3]}' + "4 - Yellow" + RESET)
    print(f'{PREF}0;{TCOLOURS[4]}' + "5 - Blue" + RESET)
    print(f'{PREF}0;{TCOLOURS[5]}' + "6 - Magenta" + RESET)
    print(f'{PREF}0;{TCOLOURS[6]}' + "7 - Cyan" + RESET)
    print(f'{PREF}0;{TCOLOURS[7]}' + "8 - White" + RESET)
    print("9 - Random")
    colour = int(input())
    if 1 <= colour <= 9:
      colourSelect = False
  
  if colour == 9:
    playerColour = TCOLOURS[randint(0, 7)]
  else:
    playerColour = TCOLOURS[colour-1]
  
  colourSelect = True
  
  while colourSelect:
    colour2 = randint(1, 8)
    print(colour2)
    if colour2 != colour:
      opponentColour = TCOLOURS[colour2-1]
      colourSelect = False
  

def update(UIN): 
  Pass = True
  if len(UIN) == 2:
    if UIN[0].lower() == "a":
      alpha = 0
    elif UIN[0].lower() == "b":
      alpha = 1
    elif UIN[0].lower() == "c":
      alpha = 2
    else:
      alpha = -1  
    
    if UIN[1] == "1":
      numer = 0
    elif UIN[1] == "2":
      numer = 1
    elif UIN[1] == "3":
      numer = 2
    else:
      numer = -1
    
    if alpha == -1 or numer == -1:
      print("ERROR 101 - Invalid input.")
      Pass = False
      input()
    elif boxes[numer][alpha] == "N":
      boxes[numer][alpha] = "X"
    else:
      print("ERROR 102 - Space is occupied.")
      Pass = False
      input()
  else:
    print("ERROR 103 - Invalid input length.")
    Pass = False
    input()
  return Pass

def alt_update():
  global turn, forfeit
  forfeit = False
  coords = []
  burden = []
  options = []

  grid = boxes[0][0] + boxes[0][1] + boxes[0][2] + boxes[1][0] + boxes[1][1] + boxes[1][2] + boxes[2][0] + boxes[2][1] + boxes[2][2]
  
  where = [m.start() for m in finditer("N", grid)]
  for x in where:
    coords.append(position(x))

  x = 1
  with open("DATA/" + FILE, "r+") as file:
    data = json.load(file)
    for x in where:
      before = grid[:x]
      after = grid[x:]
      after = after.replace("N", "O", 1)
      n_grid = before + after
      if n_grid not in data:
        creation(n_grid)
        burden.append(BASE_CHANCE)
        options.append(n_grid)
      else:
        burden.append(data[n_grid])
        options.append(n_grid)

    print(burden)
    sum = 0
    for y in burden:
      sum += y
    if sum == SURRENDER:
      forfeit = True
      print("The Opponent Forfeits!")
      return
    dump = choices(options, weights = burden)
    check = coords[options.index(dump[0])]
    turn.append(dump)
    boxes[check[0]][check[1]] = "O"
    file.close()

def position(num):
  if num == 0:
    return [0, 0]
  elif num == 1:
    return [0, 1]
  elif num == 2:
    return [0, 2]
  elif num == 3:
    return [1, 0]
  elif num == 4:
    return [1, 1]
  elif num == 5:
    return [1, 2]
  elif num == 6:
    return [2, 0]
  elif num == 7:
    return [2, 1]
  elif num == 8:
    return [2, 2]

def win_check():
  global winner
  winner = ""
  result = 0
  win = False
  if boxes[0][0] == boxes[0][1] == boxes[0][2] != "N":
    winner = boxes[0][0]
    win = True
  elif boxes[1][0] == boxes[1][1] == boxes[1][2] != "N":
    winner = boxes[1][0]
    win = True
  elif boxes[2][0] == boxes[2][1] == boxes[2][2] != "N":
    winner = boxes[2][0]
    win = True
  elif boxes[0][0] == boxes[1][1] == boxes[2][2] != "N":
    winner = boxes[0][0]
    win = True
  elif boxes[2][0] == boxes[1][1] == boxes[0][2] != "N":
    winner = boxes[2][0]
    win = True
  elif boxes[0][0] == boxes[1][0] == boxes[2][0] != "N":
    winner = boxes[0][0]
    win = True
  elif boxes[0][1] == boxes[1][1] == boxes[2][1] != "N":
    winner = boxes[0][1]
    win = True
  elif boxes[0][2] == boxes[1][2] == boxes[2][2] != "N":
    winner = boxes[0][2]
    win = True
  elif not any("N" in sublist for sublist in boxes):
    winner = "N"
    win = True
  if win and winner == "X":
    result = 1
  elif win and winner == "O":
    result = 2
  elif win and winner == "N":
    result = 3
  return result

def creation(grid):
  new_data = {}

  new_data[grid] = BASE_CHANCE

  with open("DATA/" + FILE, "r+") as file:
    data = json.load(file)
    data.update(new_data)
    file.seek(0)
    json.dump(data, file)
    file.close()

def result(triumph):
  global turn
  with open("DATA/" + FILE, "r+") as file:
    data = json.load(file)
    if triumph == opponent:
      for x in turn:
        skip = "".join(x)
        data[skip] += GAIN
    elif triumph == you:
      skip = "".join(turn[-1]) # convert list to string
      data[skip] += LOSS
    elif triumph == null:
      for x in turn:
        skip = "".join(x)
        data[skip] += DRAW
    else:
      skip = "".join(turn[-1])
      data[skip] += LOSS
    file.close()
    turn = []
  with open("DATA/" + FILE, "w") as file:
    json.dump(data, file)
    file.close()

while cont:
  startupCheck()
  players()
  while not done and not win:
    Pass = False
    forfeit = False
    while not Pass:
      display()
      UIN = input("You are X. Enter coordinates. Alphanumeric.\n")
      Pass = update(UIN)
    end = win_check()
    if end == 1:
      display()
      print("You Win!")
      result(winner)
      break
    elif end == 3:
      display()
      print("DRAW")
      result(winner)
      break
    alt_update()
    end = win_check()
    if end == 2:
      display()
      print("You Lose...")
      result(winner)
      break
    elif end == 3:
      display()
      print("DRAW")
      result(winner)
      break
    elif forfeit:
      display()
      print("You Win!")
      result(winner)
      break
      
  if input("Do you want to continue? (y/n)\n").lower() == "n":
    cont = False
    print("FINISH")
    with open("DATA/bank.json", 'w+') as file:  
      with open("DATA/storage.json", "r") as f:
        data = json.load(f)
        json.dump(data, file)
        file.close()
      file.close()
  else:
    win = False
    done = False
    x = 0
    while x < 3:
      y = 0
      while y < 3:
        boxes[x][y] = "N"
        y += 1
      x += 1
