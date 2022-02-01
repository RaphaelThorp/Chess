import numpy as np
import pandas as pnd
import chess as ch




def create_next_move_array(num, moves, depth):
    moves +=1
    data = pnd.read_csv('C:\Users\thera\Desktop\Chess_Data\games.csv', nrows=num)
    np_data = data.to_numpy()

    move = []
    next_moves = []

    for j in range(num):
        move[0].append(fen_to_list(ch.Board().fen()))
        last_position = ch.Board()


        for i in range(1,moves):
            try:
                push = last_position.parse_san(np_data[j][i])
                last_position.push(push)
                position = fen_to_list(last_position.fen())
                move.append(position)
                
            except:
                continue

        percentage = j/num*100
        print('Progress: '+str(percentage)+'%', end="\r")

        next_move_array[0].pop()
    data=np.array(next_move_array)


    return data
            

def fen_to_list(fen):
    dic = {
        'k':-6,
        'q':-5,
        'b':-4,
        'n':-3,
        'r':-2,
        'p':-1,
        'K':6,
        'Q':5,
        'B':4,
        'N':3,
        'R':2,
        'P':1,
        ' b': -7,
        ' w': 7
    }
    list = []
    for i in range(len(fen)):
        y = fen[i]
        if fen[i].isspace():
            y = y + fen[i+1]
            list.append(dic[y])
            break

        if y != '/':
            if y.isnumeric():
                for j in range(int(y)):
                    list.append(0)
            else:
                list.append(dic[y])
    return list




#fen_to_list(ch.Board().fen())
create_next_move_array(5,10)
