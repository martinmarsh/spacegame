import pyxel
import math

# These are the 4 large blue and light blue buttons on right hand side:
GAMEPAD_1_A = 3002
GAMEPAD_1_B = 3001
GAMEPAD_1_X = 3003
GAMEPAD_1_Y = 3000

# These keys are on the top of the controller and marked l and R upper buttons
GAMEPAD_1_L = 3004
GAMEPAD_1_R = 3005

# 2 other keys on the top are marked l2 and r2 lower buttons
GAMEPAD_1_L2 = 3006
GAMEPAD_1_R2 = 3007

# These keys are marked the 4 direction key pad:
GAMEPAD_1_UP = 3014
GAMEPAD_1_RIGHT = 3015
GAMEPAD_1_DOWN = 3016
GAMEPAD_1_LEFT = 3017

LAND = 1
TANK = 2
GUN = 3

pyxel.constants.APP_SCREEN_MAX_SIZE = 320
W = pyxel.constants.APP_SCREEN_MAX_SIZE
H = pyxel.constants.APP_SCREEN_MAX_SIZE*3//4

TWO_PI = math.pi * 2
