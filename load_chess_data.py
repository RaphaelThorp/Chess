import numpy as np
import pandas as pnd
import chess as ch




def create_next_move_array(num, moves, depth):
    moves +=1
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
    x=1



def fen_to_list(fen):
    dic = {
        'k':[0,0,0,1,1,0],
        'q':[0,0,0,1,0,1],
        'b':[0,0,0,1,0,0],
        'n':[0,0,0,0,1,1],
        'r':[0,0,0,0,1,0],
        'p':[0,0,0,0,0,1],
        'K':[1,1,0,0,0,0],
        'Q':[1,0,1,0,0,0],
        'B':[1,0,0,0,0,0],
        'N':[0,1,1,0,0,0],
        'R':[0,1,0,0,0,0],
        'P':[0,0,1,0,0,0],
        ' b': [0],
        ' w': [1]
    }
    list = []
    for i in range(len(fen)):
        y = fen[i]
        if fen[i].isspace():
            y = y + fen[i+1]
            list.extend(dic[y])
            break

        if y != '/':
            if y.isnumeric():
                for j in range(int(y)):
                    list.extend([0,0,0,0,0,0])
            else:
                list.extend(dic[y])
    return list



#fen_to_list(ch.Board().fen())
create_next_move_array(10,10,5)
