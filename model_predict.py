import load_chess_data as LCD
import numpy as np
from tensorflow import keras
import chess as ch
import chess.engine as engine

def get_next_move(fen):
    x = LCD.fen_to_list(fen)
    x = np.array(x)
    x = x.reshape(1,-1)

    model_path=r"C:\Users\thera\Desktop\Python\Chess\models\10000_45_3--MSE--Adam--100--20--0.1\model"
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
        
        mse = np.mean(np.square(np.array(y[0:385])-np.array(position_as_list)))

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

fen = 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3PB3/PPP2PPP/RN1QKBNR w KQkq - 0 1'
next_move = get_next_move(fen)
print(next_move)