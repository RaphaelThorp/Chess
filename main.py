
import numpy as np
import pandas as pnd
import chess as ch
from matplotlib import pyplot as plt
import load_chess_data as LCD
from tensorflow import keras, data

from tensorflow.keras import layers
from keras_visualizer import visualizer as viz


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


def load_nn_data(num, moves):
    data = LCD.create_next_move_array(num, moves)
    return data[0],data[1]

def train_keras_model(num,moves):
    x_train,y_train=load_nn_data(num,moves)
    #train_data = data.Dataset.from_tensors((x_train, y_train))
    model = keras.Sequential(
       [    
           layers.Dense(65, activation='relu'),
           layers.Dense(64, activation='relu'),
           layers.Dense(64, activation='relu'),
           layers.Dense(64)
       ] 
    )

    epochs = 100

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    model.fit(x_train, y_train, epochs=epochs, validation_split=0.1)
    model.summary()
    model.save('model')


def use_keras_model(input):
    model = keras.load_model('model')
    output = model.predict(input)
    return output


#train_keras_model(1000,10)
#load_nn_data(100,10)

x = LCD.fen_to_list('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
x = np.array(x)
# x = x.reshape(1,-1)
#model = keras.models.load_model('model')

# y = model.predict(x)

print(x)
# print(y)

#viz(model, format="png", filename='graph',view=True)
            

