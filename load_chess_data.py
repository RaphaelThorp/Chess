import numpy as np
import pandas as pnd
import chess as ch

def create_next_move_array(num, moves, depth):
    data = pnd.read_csv(r"C:\Users\thera\Desktop\Chess_Data\games.csv", nrows=num)
    np_data = data.to_numpy()

    move = []
    next_moves = []

    x = 0
    for j in range(num):
        ch.Board().reset()
        input_position = ch.Board()
        
        for i in range(moves):
            last_position = ch.Board.copy(input_position)
            output_positions=[]
            usable_move = True
            for k in range(depth):
                try:
                    output_positions_push = last_position.parse_san(np_data[j][i+k])
                    last_position.push(output_positions_push)
                    output_positions.extend(fen_to_list(last_position.fen()))
                    
                except:
                    usable_move = False

            if usable_move == True:
                move.append(fen_to_list(input_position.fen()))
                next_moves.append(output_positions)
    
                push = input_position.parse_san(np_data[j][i])
                input_position.push(push)


                    


        percentage = j/num*100
        print('Progress: '+str(percentage)+'%', end="\r")

    input_data=np.array(move)
    output_data=np.array(next_moves)
    # print(input_data.shape)
    # print(output_data.shape)


    return input_data,output_data
            

def create_score_array(num,moves):
    data = pnd.read_csv(r"C:\Users\thera\Desktop\Chess_Data\games.csv", nrows=num)
    np_data = data.to_numpy()

    move = []
    scores = []
    for j in range(num):
        ch.Board().reset()
        position = ch.Board()
        
        for i in range(moves):
            try:
                push = position.parse_san(np_data[j][i])
                position.push(push)
                score = float(np_data[j][i+200])
            except:
                break

            move.append(fen_to_list(position.fen()))
            scores.append(score)

        percentage = j/num*100
        print('Progress: '+str(percentage)+'%', end="\r")

    input_data=np.array(move)
    output_data=np.array(scores)

    return input_data, output_data



def fen_to_list(fen):
    if ' w ' in fen:
        dic = {
            'k':[-1,0,0,0,0,0],
            'q':[0,-1,0,0,0,0],
            'b':[0,0,-1,0,0,0],
            'n':[0,0,0,-1,0,0],
            'r':[0,0,0,0,-1,0],
            'p':[0,0,0,0,0,-1],
            'K':[1,0,0,0,0,0],
            'Q':[0,1,0,0,0,0],
            'B':[0,0,1,0,0,0],
            'N':[0,0,0,1,0,0],
            'R':[0,0,0,0,1,0],
            'P':[0,0,0,0,0,1]
            }
    else:
        dic = {
            'K':[-1,0,0,0,0,0],
            'Q':[0,-1,0,0,0,0],
            'B':[0,0,-1,0,0,0],
            'N':[0,0,0,-1,0,0],
            'R':[0,0,0,0,-1,0],
            'P':[0,0,0,0,0,-1],
            'k':[1,0,0,0,0,0],
            'q':[0,1,0,0,0,0],
            'b':[0,0,1,0,0,0],
            'n':[0,0,0,1,0,0],
            'r':[0,0,0,0,1,0],
            'p':[0,0,0,0,0,1]
            }
    list = []
    for i in range(len(fen)):
        y = fen[i]
        if y.isspace():
            break
        if y != '/':
            if y.isnumeric():
                for j in range(int(y)):
                    list.extend([0,0,0,0,0,0])
            else:
                list.extend(dic[y])

    if ' b ' in fen:
        list.reverse()
        
    return list



#print(fen_to_list(ch.Board().fen()))
#print(ch.Board().fen())
#print(create_next_move_array(10,10,1))

# fen = 'rnbq1rk1/ppppbppp/5n2/4p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R w KQ - 5 5'
# print(fen_to_list(fen))