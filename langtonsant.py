# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:26:10 2020

@author: Domenic
"""

import numpy as np
import matplotlib.pyplot as plt

class Ant:
    """ brief: A class to model Langton's ant
        member: position The position of the ant
        member: direction The direction the ant is facing
    """
    def __init__(self, position, direction):
        """ brief: Constructor
            param: position The position of the ant
            param: direction The direction the ant is facing
        """
        self.position = position
        self.direction = direction
        
    def move(self, grid_size):
        """ brief: Moves the ant depending on it's position and facing direction
            param: grid_size The size of the grid
        """
        if self.direction == 0:
            self.position = self.position - np.array([0,1])
        if self.direction == 1:
            self.position = self.position - np.array([1,0])
        if self.direction == 2:
            self.position = self.position + np.array([0,1])
        if self.direction == 3:
            self.position = self.position + np.array([1,0])
            
        #Torus topology
        self.position[0] = self.position[0] % grid_size[0]
        self.position[1] = self.position[1] % grid_size[1]
            
            
    def turn_left(self):
        """ brief: Turns the ant to the left
        """
        self.direction = (self.direction-1)%4
        
    def turn_right(self):
        """ brief: Turns the ant to the right
        """
        self.direction = (self.direction+1)%4
        
    def update(self, field):
        """ brief: Performs one update rule of the ant
            param: field The current field
            return The new field after one step
        """
        #Scan
        value = field[self.position[0], self.position[1]]
        
        #Turn
        if value == 1:
            self.turn_right()
        elif value == 0:
            self.turn_left()
            
        #Flip
        field[self.position[0], self.position[1]] = value^1 #0xor1 = 0, 1xor1 = 0 -> Flips the cell
        
        #Move
        self.move(field.shape)
        
        return field
        
def read_input(message, value_range):
    """ brief: Reads a value between the specified range
        param: message The message printed before the input
        param: value_range The desired range of the input
        return The user input
    """
    valid = False
    while not valid:
        print(message)
    
        try:
            inp = int(input())
        except ValueError:
            valid = False
        
        if inp >= value_range[0] and inp <= value_range[1]:
            valid = True
                
        if not valid:
            print("This is not a valid input, please input one of the following options:")
    
    return inp

def configure(grid_size):
    """ brief: This function initializes the field. The user has to chooses a field configuration,
               starting position and orientation
        param: grid_size The size of the grid
    """
    print("Welcome to this simulation of Langton's ant")
    
    #Let the user choose a starting field
    field_option = read_input("Please choose one of the following starting configurations by entering the number in front of the option\n(1) all white\n(2) all black\n(3) checker board\n(4) horizontal stripes\n(5) random",\
                              (1,5))
                
    field = initialize_field(field_option, grid_size).astype(np.int)
    
    #Let the user choose a x-value 
    x = read_input("Please choose the starting x value from 0 to " + str(grid_size[1]-1),\
                   (0,grid_size[1]-1))
            
    #Let the user choose a y-value
    y = read_input("Please choose the starting y value from 0 to " + str(grid_size[0]-1),\
                   (0, grid_size[0]-1))
            
    #Let the user choose a direction
    direction = read_input("Please choose the starting direction\n(1) West\n(2) North\n(3) East\n(4) South",\
                           (1,4))
    
    #Let the user choose a stepsize
    step_size = read_input("Please choose the number of updates per frame between 1 and 100 (1=realtime)", (1,100) )
            
    return field, Ant(np.array([y,x]), direction-1),step_size
    
    

def initialize_field(field_option, grid_size):
    """ brief: Initializes the starting field depending one the choosen option
        param: field_option The field option given by the user (1 to 5)
        param: grid_size The size of the grid
        return: A numpy array representing the field
    """
    
    #All white
    if field_option == 1:
        return np.ones(grid_size)
    
    #All black
    if field_option == 2:
        return np.zeros(grid_size)
    
    #Checker board
    if field_option == 3:
        field = np.zeros(grid_size)
        field[::2] = 1
        field[:,::2] = np.roll(field[:,::2], -1, axis = 0)
        field[grid_size[0]-1,::2] = 0 #Fix for last row
        return field
    
    #Horizontal stripes
    if field_option == 4:
        field = np.zeros(grid_size)
        field[::2] = 1
        return field
        
    #Random
    if field_option == 5:
        return np.random.randint(0,2,grid_size)
        
    

if __name__ == "__main__":
    grid_size = (101,82)
    field,ant,step_size = configure(grid_size)
    
    alive = []
    
    fig = plt.figure()
    plot = plt.imshow(field, cmap="gray", vmin=0, vmax = 1)

    while plt.fignum_exists(fig.number):
        #Update and count number of alive cells (0=alive)
        for i in range(step_size):
            field = ant.update(field)
            alive.append(np.where(field==0)[0].size)
        
        #Plot the new field
        plot.set_data(field)
        plt.draw()
        plt.pause(0.000000000000000000001)
    
    #Write alive cell numbers to file
    np.savetxt("alive.txt", np.array(alive).astype(int), fmt="%d")