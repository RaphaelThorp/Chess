
from gc import callbacks
from pickletools import optimize
import numpy as np
import pandas as pnd
import chess as ch
from matplotlib import pyplot as plt
import load_chess_data as LCD
from tensorflow import keras, data

from tensorflow.keras import layers
from keras_visualizer import visualizer as viz

import os


def graph_divergence(num, moves):
    data = pnd.read_csv(r"C:\Users\thera\Desktop\Chess_Data\games.csv", nrows=num)
    np_data = data.to_numpy()

    game_states = []
    for i in range(num):
        game_states.append(ch.Board())


    games = np.empty([num,moves])
    games[:]=np.nan
    game_history=[]
    unique_history = []

    uniqiue_positions = 0
    progress = 0

    for i in range(1,moves):
        for j in range(num):
            try:            
                push = game_states[j].parse_san(np_data[j][i])
                game_states[j].push(push)
                position = game_states[j]
                game_states[j] = position

                unique = 1
                for k in range(len(game_history)):
                    if position == game_history[k]:
                        # print('xxxxxxxxxxxxxx')
                        # print('Game: '+str(j))
                        # print('Move: '+str(i))
                        # print('History: '+str(game_history[k]))
                        # print('Position: '+str(position))
                        # print('Unique ID: ' +str(unique_history[k]))
                        
                        games[j][i] = unique_history[k]
                        unique = 0
                        break
                if unique == 1:
                    uniqiue_positions += 1
                    game_history.append(position)
                    unique_history.append(uniqiue_positions)
                    games[j][i] = unique_history[k]
                        
            except:
                continue
        progress += 1/(moves-1)*100
        print(uniqiue_positions)
        print("Progress: " + str(progress) + '%')


    for i in range(num):
        plt.plot(games[i], linewidth=0.3, alpha=0.1)

    plt.show()


def load_nn_data(num, moves, depth):
    input_data, output_data = LCD.create_next_move_array(num, moves, depth)
    return input_data,output_data

def train_keras_model(num,moves, depth):
    x_train,y_train=load_nn_data(num,moves, depth)
    #train_data = data.Dataset.from_tensors((x_train, y_train))

    callback = keras.callbacks.EarlyStopping(monitor='loss', patience=4, mode='auto')

    model = keras.Sequential(
       [    
           layers.Dense(385, activation='relu'),
           layers.Dense(64, activation='relu'),
           layers.Dense(32, activation='relu'),
           layers.Dense(64, activation='relu'),
           layers.Dense(128, activation='sigmoid'),
           layers.Dense(256, activation='sigmoid'),
           layers.Dense(385*depth, activation='sigmoid')
       ] 
    )

    epochs = 100
    batch_size = 20
    val_split = 0.1
    loss = "MSE"
    opt = "Adam"

    model.compile(loss=loss, optimizer=opt)
    
    model.fit(x_train, y_train, epochs=epochs, validation_split=val_split, batch_size=batch_size, callbacks=[callback])
    #model.summary()
    #TODO: Add summary save file

    file_name = str(num)+'_'+str(moves)+'_'+str(depth)+'--'+loss+'--'+opt+'--'+str(epochs)+'--'+str(batch_size)+'--'+str(val_split)
    save_path = "./models/"+file_name
    if os.path.isdir(save_path):
        model.save(save_path+"/model")
        viz(model, format="png", filename=(save_path+"/structure/graph"),view=True)
    else:
        os.mkdir(save_path)
        os.mkdir(save_path+"/model")
        os.mkdir(save_path+"/structure")
        model.save(save_path+"/model")
        viz(model, format="png", filename=(save_path+"/structure/graph"),view=True)

    


def use_keras_model(input):
    model = keras.load_model('model')
    output = model.predict(input)
    return output






train_keras_model(10000,45,3)
#load_nn_data(100,10)

#fen = 'rnbq1rk1/ppppbppp/5n2/4p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R w KQ - 5 5'
#next_move = get_next_move(fen)
#print(next_move)

# print(x.shape)



            

