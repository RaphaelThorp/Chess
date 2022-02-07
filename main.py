
from gc import callbacks
from pickletools import optimize
import numpy as np
import pandas as pnd
import chess as ch
from matplotlib import pyplot as plt
import load_chess_data as LCD
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout

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
        print("Progress: " + str(progress) + '%')


    for i in range(num):
        plt.plot(games[i], linewidth=0.3, alpha=0.1)

    plt.show()

def train_keras_model(num,moves,depth):
    x_train,y_train=LCD.create_score_array(num,moves)

    callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, mode='auto')

    input_layer = Input(shape=(384,))
    layer1 = Dense(256, activation='relu')(input_layer)
    dropout1 = Dropout(0.5)(layer1)
    layer2 = Dense(128, activation='relu')(dropout1)
    #dropout2 = Dropout(0.5)(layer2)
    layer3 = Dense(64, activation='relu')(layer2)
    layer4 = Dense(16, activation='sigmoid')(layer3)
    output_layer = Dense(1, activation='linear')(layer4)
    #output_layer = Dense(384*depth, activation='linear')(layer4)

    model = Model(inputs=input_layer, outputs=output_layer)

    epochs = 100
    batch_size = 20
    val_split = 0.1
    loss = "MSE"
    opt = "Adam"

    model.compile(loss=loss, optimizer=opt)
    
    model.fit(x_train, y_train, epochs=epochs, validation_split=val_split, batch_size=batch_size, callbacks=[callback])
    #model.summary()
    #TODO: Add summary save file

    #file_name = str(num)+'_'+str(moves)+'_'+str(depth)+'--'+loss+'--'+opt+'--'+str(epochs)+'--'+str(batch_size)+'--'+str(val_split)
    file_name = 'score'
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


train_keras_model(1000,100,4)
#load_nn_data(100,10)

#fen = 'rnbq1rk1/ppppbppp/5n2/4p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R w KQ - 5 5'
#next_move = get_next_move(fen)
#print(next_move)

# print(x.shape)



            

