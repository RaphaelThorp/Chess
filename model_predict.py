from random import choice
import load_chess_data as LCD
import numpy as np
from tensorflow import keras
import chess as ch
import chess.engine as eng



engine = eng.SimpleEngine.popen_uci(r'C:\Users\thera\Desktop\Python\Chess\stockfish\stockfish_14.1_win_x64_avx2')


def predict_next_move(fen):
    x = LCD.fen_to_list(fen)
    x = np.array(x)
    x = x.reshape(1,-1)

    model_path=r"C:\Users\thera\Desktop\Python\Chess\models\openings\model"
    model = keras.models.load_model(model_path)

    y = model.predict(x)
    y = np.ndarray.tolist(y)
    y = y[0]

    position =ch.Board(fen=fen)
    legal_moves = list(position.legal_moves)
    move_mse_fen = [[0,100000,0],[0,100000,0],[0,100000,0]]
    for i in range(len(legal_moves)):
        position = ch.Board(fen=fen)
        push = legal_moves[i]
        position.push(push)
        position_as_list =LCD.fen_to_list(position.fen())
        
        mse = np.mean(np.square(np.array(y[0:384])-np.array(position_as_list)))

        for i in range(3):
            if mse <= move_mse_fen[0][1]:
                move_mse_fen[0][0] = push
                move_mse_fen[0][1] = mse
                move_mse_fen[0][2] = position.fen()
            elif mse <= move_mse_fen[1][1]:
                move_mse_fen[1][0] = push
                move_mse_fen[1][1] = mse
                move_mse_fen[1][2] = position.fen()
            elif mse <= move_mse_fen[2][1]:
                move_mse_fen[2][0] = push
                move_mse_fen[2][1] = mse
                move_mse_fen[2][2] = position.fen()
    highest_score = 0
    for i in range(3):
        try:
            score= engine.Score(move_mse_fen[i][2])
        except:
            continue
        if score >= highest_score:
            highest_score=i        

    return move_mse_fen[highest_score][0]


def get_next_move(fen, percentile):
    scores = []
    position =ch.Board(fen=fen)
    legal_moves = list(position.legal_moves)
    for i in range(len(legal_moves)):
        position = ch.Board(fen=fen)
        push = legal_moves[i]
        position.push(push)
        analysis = engine.analyse(position, eng.Limit(0.1))
        score = eng.Cp(analysis['score'].relative)
        scores.append(score.score(mate_score=10000).score())
        #.score(mate_score=10000)

    best_score = max(scores)
    highest_scores = []
    highest_scores.append(best_score)
    
    for i in range(len(legal_moves)):
        if scores[i] >= percentile*best_score:
            highest_scores.append(i)
    
    move = legal_moves[choice(highest_scores)]

    return move
    



fen = 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3PB3/PPP2PPP/RN1QKBNR w KQkq - 0 1'
next_move = get_next_move(fen, 0.9)
print(next_move)