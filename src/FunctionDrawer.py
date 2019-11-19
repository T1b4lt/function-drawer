import argparse
import sys
from parser import expr
from math import *

import numpy as np
import pygame
from sklearn.preprocessing import MinMaxScaler


def to_pygame(coords, height):
	"""Convert coordinates into pygame coordinates (top-left => bottom-left)."""
	return coords[0], height - coords[1]


def norm_range(value, upper, lower):
	return lower + (upper - lower) * value


def fun_parser(str_eq):
	eq = expr(str_eq).compile()
	return eq


def main(cliargs):
	eq = fun_parser(cliargs.function)

	screen_shape = (500, 500)

	pygame.init()
	screen = pygame.display.set_mode(screen_shape)
	pygame.display.set_caption("First Pygame Application")
	screen.fill((0, 0, 0))

	start = float(cliargs.start)
	end = float(cliargs.end)
	step = float(cliargs.step)

	x_values = []
	y_values = []

	for x in np.arange(start, end, step):
		print(x, eval(eq))
		x_values.append(x)
		y_values.append(eval(eq))

	scaler_x = MinMaxScaler(feature_range=(0, 500))
	scaler_y = MinMaxScaler(feature_range=(0, 500))

	x_values = np.reshape(x_values, (len(x_values), 1))
	y_values = np.reshape(y_values, (len(y_values), 1))

	scaler_x = scaler_x.fit(x_values)
	scaler_y = scaler_y.fit(y_values)

	normalized_x = scaler_x.transform(x_values)
	normalized_y = scaler_y.transform(y_values)

	for i in range(len(normalized_x)):
		x_value, y_value = to_pygame((normalized_x[i], normalized_y[i]), screen_shape[1])
		print(x_value, y_value)
		pygame.draw.rect(screen, (255, 255, 255), (x_value, y_value, 10, 10))

	clock = pygame.time.Clock()

	while 1:
		clock.tick(1)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		pygame.display.update()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="function drawer",
		epilog="A function drawer. It draws the function you specify in tue time you specify.")

	parser.add_argument(
		"function",
		help="function to be draw",
		metavar="function-draw")
	parser.add_argument(
		"start",
		help="start x value",
		metavar="start-x")
	parser.add_argument(
		"end",
		help="end x value",
		metavar="end-x")
	parser.add_argument(
		"step",
		help="step x value",
		metavar="step-x")

	args = parser.parse_args()
	main(args)
