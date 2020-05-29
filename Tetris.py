# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:09:22 2019

@author: Edgar
"""
import random
import copy
import time
import numpy as np
import keyboard
import os


class Tetris(object):
    def __init__(self):
        self.rows = 24
        self.columns = 10
        self.grid = self.create_grid()

        self.place_add_shape = (0, 4)

        self.shape_in_play = None
        self.coordinates_shapeip_in_grid = None
        self.origin_of_shapeip = None

        self.exit_ = False

    def create_grid(self):
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(' ')
            grid.append(row)

        return np.array(grid)

    def show_grid(self):
        print(self.grid)

    def show_grid_play(self):
        grid_play = self.grid.copy()

        for coordinate in self.coordinates_shapeip_in_grid:
            grid_play[coordinate[0]][coordinate[1]] = 1

        print(grid_play)

    def add_shape(self):
        if self.shape_in_play == None:
            self.shape_in_play = Tetris_Shape(
                random.randint(0, 6), random.randint(1, 4))
            self.coordinates_shapeip_in_grid = self.map_shape_to_grid(
                self.place_add_shape, self.shape_in_play)

            self.origin_of_shapeip = np.array(self.place_add_shape)

    def map_shape_to_grid(self, place, shape_in_play):
        if self.shape_in_play is not None:
            coordinates_in_shape = shape_in_play.coordinates

            coordinates_in_grid = []
            for shape_coordinate in coordinates_in_shape:
                coordinate_in_grid = np.array(
                    shape_coordinate) + np.array(place)
                coordinates_in_grid.append(coordinate_in_grid)

            return coordinates_in_grid

    def shape_fall(self):
        new_coordinates = []
        for coordinate in self.coordinates_shapeip_in_grid:
            new_coordinates.append(np.array(coordinate) + np.array([1, 0]))

        return new_coordinates

    def update_fall(self):
        if self.coordinates_shapeip_in_grid is not None:
            self.coordinates_shapeip_in_grid = self.shape_fall()

            self.origin_of_shapeip += np.array([1, 0])

    def connect(self):
        if self.coordinates_shapeip_in_grid is not None:
            for coordinate in self.coordinates_shapeip_in_grid:
                self.grid[coordinate[0]][coordinate[1]] = 1

            self.shape_in_play = None
            self.coordinates_shapeip_in_grid = None

    def check_collision(self):
        against_wall = False
        against_shape = False

        numbers_in_coordinates = [
            num for coordinate in self.coordinates_shapeip_in_grid for num in coordinate]

        if self.rows - 1 in numbers_in_coordinates:
            against_wall = True

        else:
            for coordinate in self.shape_fall():
                if self.grid[coordinate[0]][coordinate[1]] == '1':
                    against_shape = True

        if against_wall or against_shape:
            return True

    def flip_shape_ip(self):
        obstruction = False

        shapeip_copy = copy.copy(self.shape_in_play)

        shapeip_copy.flip(1)

        new_coordinates = self.map_shape_to_grid(
            self.origin_of_shapeip, shapeip_copy)

        for coordinate in new_coordinates:
            try:
                if self.grid[coordinate[0]][coordinate[1]] == '1':
                    obstruction = True
                    break
            except:
                obstruction = True
                break

        if not obstruction:
            self.shape_in_play = shapeip_copy
            self.coordinates_shapeip_in_grid = new_coordinates

    def move_side(self, direction):
        column_coordinates = [
            num for coordinate in self.coordinates_shapeip_in_grid for num in coordinate if num == coordinate[1]]

        if 0 in column_coordinates:
            against_wall = 'left_wall'
        elif self.columns - 1 in column_coordinates:
            against_wall = 'right_wall'
        else:
            against_wall = False

        if (direction == 'right' and against_wall != 'right_wall') or (direction == 'left' and against_wall != 'left_wall'):
            new_coordinates = []
            new_origin_shapeip = copy.copy(self.origin_of_shapeip)
            for coordinate in self.coordinates_shapeip_in_grid:
                if direction == 'left':
                    new_coordinates.append(
                        np.array(coordinate) - np.array([0, 1]))
                    new_origin_shapeip = np.array(
                        self.origin_of_shapeip) - np.array([0, 1])
                elif direction == 'right':
                    new_coordinates.append(
                        np.array(coordinate) + np.array([0, 1]))
                    new_origin_shapeip = np.array(
                        self.origin_of_shapeip) + np.array([0, 1])

            obstruction = False
            for coordinate in new_coordinates:
                if self.grid[coordinate[0]][coordinate[1]] == '1':
                    obstruction = True
                    break

            if not obstruction:
                self.coordinates_shapeip_in_grid = new_coordinates
                self.origin_of_shapeip = new_origin_shapeip

    def check_tetris(self):
        check = False
        grid_copy = self.grid.copy()
        for i in range(self.rows):
            grid_set = set(self.grid[i])
            if len(grid_set) == 1 and grid_set.pop() == '1':
                check = True
                self.grid = np.delete(self.grid, i, 0)
                self.grid = np.insert(
                    self.grid, 0, np.array([' ']*self.columns), 0)

                grid_copy[i] = np.array(['X']*self.columns)

        if check:
            print(grid_copy)
            time.sleep(0.5)

    def user_input(self):
        timeout = time.time() + 1
        while True:
            if time.time() > timeout:
                break
            time.sleep(0.05)

            if keyboard.is_pressed('escape'):
                self.exit_ = True
                break

            if keyboard.is_pressed('up'):
                self.flip_shape_ip()
                self.show_grid_play()

            if keyboard.is_pressed('down'):
                break

            if keyboard.is_pressed('right'):
                self.move_side('right')
                self.show_grid_play()

            if keyboard.is_pressed('left'):
                self.move_side('left')
                self.show_grid_play()

    def check_status(self):
        for value in self.grid[0]:
            if value == '1':
                return True

    def play(self):
        while True:
            print('\n')

            if self.shape_in_play == None:
                self.add_shape()

            self.show_grid_play()

            self.user_input()

            if self.exit_:
                print('\nThank you for playing!')
                break

            if self.check_collision():
                self.connect()
                self.check_tetris()
            else:
                self.update_fall()

            if self.check_status():
                print('Game Over!')
                print('Thank you for playing!')
                break

            os.system("CLS")


class Tetris_Shape(object):
    def __init__(self, shape_type, shift):
        self.create_shapes = {
            0: self.L_shape,
            1: self.l_shape,
            2: self.z_shape,
            3: self.hplus_shape,
            4: self.box_shape,
            5: self.bL_shape,
            6: self.bz_shape
        }

        self.shape_type = shape_type
        self.shape = self.create_shapes[shape_type]()
        self.coordinates = self.coordinates_w_1()

        self.shift = shift
        self.flip(self.shift)

    def L_shape(self):
        return np.array([[0, 0, 1], [1, 1, 1]])

    def l_shape(self):
        return np.array([[1, 1, 1, 1]])

    def z_shape(self):
        return np.array([[1, 1, 0], [0, 1, 1]])

    def hplus_shape(self):
        return np.array([[0, 1, 0], [1, 1, 1]])

    def box_shape(self):
        return np.array([[1, 1], [1, 1]])

    def bL_shape(self):
        return np.array([[1, 1, 1], [0, 0, 1]])

    def bz_shape(self):
        return np.array([[0, 1, 1], [1, 1, 0]])

    def flip(self, flips):
        if self.shape_type == 4:
            pass

        else:
            self.shape = np.rot90(self.shape, flips)
        self.coordinates = self.coordinates_w_1()

    def coordinates_w_1(self):
        coordinates = [(i, j) for i in range(self.shape.shape[0]) for j in range(
            self.shape.shape[1]) if self.shape[i][j] == 1 or self.shape[i][j] == '1']
        return coordinates


# --------------
Game = Tetris()
Game.play()
