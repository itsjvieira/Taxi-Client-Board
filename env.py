import board
import tkinter as tk
from agents import *
from enum import Enum


class Move(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


class Environment:
    def __init__(self, board_size):
        self.board_size = board_size
        self.taxis = {}
        self.clients = {}

        self.current_ts = 1
        self.current_ts_moves = []
        self.log_text = "* TIMESTEP " + str(self.current_ts) + " *\n"

        root = tk.Tk()
        self.gui = board.Board(root, board_size)
        self.gui.update()

    def create_taxi(self, identifier, coordinates):
        x = coordinates[0]
        y = coordinates[1]

        if x < 0 or x >= self.board_size[0] or y < 0 or y >= self.board_size[1]:
            print("Invalid Coordinates")
            return

        if identifier in self.taxis.keys():
            print("Taxi ID already taken")
            return

        self.gui.update_log_text("NEW TAXI - ID: " + str(identifier) + "; (" + str(x) + ", " + str(y) + ")\n")
        self.taxis[identifier] = Taxi(x, y, identifier)

        self.gui.update_board(self.taxis)
        self.gui.update()

    def create_client(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]

        if x < 0 or x >= self.board_size[0] or y < 0 or y >= self.board_size[1]:
            print("Invalid Coordinates")
            return

        if (x, y) in self.clients.keys():
            print("Position Occupied by Another Client")
            return

        self.log_text += "NEW CLIENT - (" + str(x) + ", " + str(y) + ")\n"
        self.clients[(x, y)] = Client(x, y)
        self.gui.update()

    def go(self, identifier, move):
        if identifier in self.current_ts_moves:
            print("Invalid Move: Taxi Already Moved in The Current Time Step")
            return

        old_x = self.taxis[identifier].x
        old_y = self.taxis[identifier].y

        if move == Move.up:
            if self.taxis[identifier].y > 0:
                self.taxis[identifier].up()
            else:
                print("Invalid Move: Taxi Can Not Move Up")
                return
        elif move == Move.down:
            if self.taxis[identifier].y < self.board_size[0] - 1:
                self.taxis[identifier].down()
            else:
                print("Invalid Move: Taxi Can Not Move Down")
                return
        elif move == Move.left:
            if self.taxis[identifier].x > 0:
                self.taxis[identifier].left()
            else:
                print("Invalid Move: Taxi Can Not Move Left")
                return
        elif move == Move.right:
            if self.taxis[identifier].x < self.board_size[1] - 1:
                self.taxis[identifier].right()
            else:
                print("Invalid Move: Taxi Can Not Move Right")
                return

        self.log_text += \
            "MOVE TAXI - ID: " + str(identifier) + "; (" + \
            str(old_x) + ", " + str(old_y) + ") -> (" + \
            str(self.taxis[identifier].x) + ", " + str(self.taxis[identifier].y) + ")\n"

        self.current_ts_moves.append(identifier)
        self.gui.update()

    def pickup(self, identifier):
        x = self.taxis[identifier].x
        y = self.taxis[identifier].y

        if not (x, y) in self.clients.keys():
            print("Invalid Pickup: There is no Client at The Current Position")
            return

        if not self.taxis[identifier].state == TaxiState.free:
            print("Invalid Pickup: The Selected Taxi is Occupied")
            return

        self.log_text += "TAXI PICKUP - ID: " + str(identifier) + "\n"
        del self.clients[(x, y)]
        self.taxis[identifier].state = TaxiState.occupied
        self.gui.update()

    def free(self, identifier):
        self.log_text += "TAXI FREE - ID: " + str(identifier) + "\n"
        self.taxis[identifier].state = TaxiState.free
        self.gui.update()

    def end_timestep(self):
        self.gui.update_board(self.taxis, self.clients)
        self.gui.update_log_text(self.log_text)
        self.current_ts += 1
        self.log_text = "* TIMESTEP " + str(self.current_ts) + " *\n"
        self.current_ts_moves = []
        self.gui.update()
