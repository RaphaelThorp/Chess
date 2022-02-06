import chess
import numpy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pywinauto import application
import time
import os
import sys
import glob
from get_fen import get_fen
import subprocess

subprocess.Popen('chrome.exe chess.com/play/online --remote-debugging-port=9222 --user-data-dir="C:\ChromeProfile"')

sys.path.insert(1, r'C:\Users\thera\Desktop\Python\Chess')

import model_predict as predict

running_script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(running_script_directory)

for file in glob.glob("stockfish*"):
    print("Found Stockfish binary version", file.strip("stockfish_").strip(".exe"))
    stockfish = file

mode = 'online'

board = chess.Board()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(r"C:\Users\thera\Desktop\Python\Chess\bot\src\chromedriver.exe", options=chrome_options)
with open("board.txt") as f:
    array = [i.split() for i in f]

# url = input("Enter a url\n> ")
# for pawn promotion testing
# url = "https://www.chess.com/play/computer?fen=qkb3nr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR%20w%20KQ%20-%200%201"
url = "https://www.chess.com/play/"+mode
driver.get(url)

def open_chrome():
    '''
    Funtion makes sure that Chrome is open so that check_fen can work properly.
    '''
    app = application.Application().connect(title_re ="Play Chess.*")
    app_dialog = app.top_window()
    

    if not app_dialog.has_focus():
        app_dialog.set_focus()

def check_fen(extension):
    open_chrome()
    base = get_fen(driver)
    return f"{base} {extension}"
    
        
def find_loc(piece):
    for i, row in enumerate(array):
        for j, col in enumerate(row):
            if col == piece:
                return [j+1, 8-i]



color = 'w' #input("Whose turn is it right now? Choices are 'w' for white; 'b' for black\n> ")
#print("\nCan the white king castle?\nk for king's side; q for queen's side; - for neither")
castle_w = 'KQ' #input("Choices are 'kq', 'k', 'q', or '-'\n> ").upper()

#print("\nCan the black king castle?\nk for king's side; q for queen's side; - for neither")
castle_b = 'kq' #input("Choices are 'kq', 'k', 'q', or '-'\n> ").lower()

#print("\nWhat is the en passant target square in algebraic notation?")
en_passant = '-' #input("If a pawn has just made a two-square move, this is origin square.\nIf there is no en passant or you are not sure, put '-'.\n> ").lower()
half_move = 0 #input("\nWhat is the number of half moves? Put '0' if you are not sure.\n> ")
full_move = 1 #input("\nWhat is the number of full moves? Put 1' if you are not sure.\n> ")


initial_fen = check_fen(f"{color} {castle_w}{castle_b} {en_passant} {half_move} {full_move}")

if mode == 'online':
    
    while True:
        try:
            play = driver.find_element(By.XPATH,"//button[@data-cy = 'new-game-index-play']")
            play.click()
            break
        except:
            None
    
        

print(initial_fen, "\n")
while not board.is_game_over():

    if mode == 'online':
        try:
            piece_size = driver.find_element(By.XPATH, "//chess-board[@class='board']").size["height"]/8
            player = ' w '
        except:
            piece_size = driver.find_element(By.XPATH, "//chess-board[@class='board flipped']").size["height"]/8
            player = ' b '
    else:
        piece_size = driver.find_element_by_css_selector(".layout-board.board").size["height"]/8
        player = ' w '
    while True:
        fen = check_fen(board.fen().split(" ", 1)[1])
        print(fen, "\n")
        if board.fen() != fen or board.fen() == initial_fen:
            board = chess.Board(fen)
            break


    result = predict.get_next_move(board.fen())
    if player in fen:
        origin = find_loc(str(result)[:2])
        target = find_loc(str(result)[2:4])
        offset = [a - b for a, b in zip(target, origin)]
        if player == ' w ':
            offset[0] *= piece_size
            offset[1] *= -piece_size
        if player == ' b ':
            offset[0] *= piece_size
            offset[1] *= piece_size
        
        origin_push = driver.find_element_by_xpath(f"//div[contains(@class, 'piece') and contains(@class, 'square-{origin[0]}{origin[1]}')]")
        action_chains = ActionChains(driver)
        action_chains.drag_and_drop_by_offset(origin_push, offset[0], offset[1]).perform()

        if len(str(result)) == 5:
            promotion = driver.find_element_by_css_selector("div.promotion-piece." + fen.split()[1] + str(result)[-1].lower())
            promotion.click()
            
    board.push(result)
    print(board, "\n")

    time.sleep(0.1)
