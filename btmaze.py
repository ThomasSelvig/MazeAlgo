from PIL import Image, ImageGrab
import os, sys

frames = []  # to create a final GIF


class Colors:
	START = 0, 0, 255
	ROAD = 0, 0, 0
	END = 255, 0, 0

	ANIM = 255, 165, 0


def renderMaze(maze, colored, resizeFactor=1):
	pixels = maze.load()
	for px in colored:
		pixels[px] = Colors.ANIM

	if resizeFactor > 1:
		return maze.resize([i * 20 for i in maze.size], resample=Image.BILINEAR)
	return maze


def findStart(pixels, size):
	for y in range(size[1]):
		for x in range(size[0]):
			if pixels[x, y] == Colors.START:
				return x, y
	return None, None


def availNodes(x, y, pixels, size):
	nodes = []
	
	# up
	if y-1 >= 0 and y-1 < size[1] and pixels[x, y-1] in (Colors.ROAD, Colors.END):
		nodes.append((x, y - 1))
	# left
	if x-1 >= 0 and x-1 < size[0] and pixels[x-1, y] in (Colors.ROAD, Colors.END):
		nodes.append((x - 1, y))
	# down
	if y+1 >= 0 and y+1 < size[1] and pixels[x, y+1] in (Colors.ROAD, Colors.END):
		nodes.append((x, y + 1))
	# right
	if x+1 >= 0 and x+1 < size[0] and pixels[x+1, y] in (Colors.ROAD, Colors.END):
		nodes.append((x + 1, y))

	return nodes


def searchNode(x, y, maze, pixels, visited=None):
	if visited is None:
		visited = []

	frames.append(renderMaze(maze, visited+[(x, y)]))

	if pixels[x, y] == Colors.END:
		return visited + [(x, y)]

	for node in [n for n in availNodes(x, y, pixels, maze.size) if n not in visited]:
		if (search := searchNode(*node, maze.copy(), pixels, visited=visited+[(x, y)])) is not None:
			return search


def main():
	sys.setrecursionlimit(round(1e6))
	folderPath = os.path.dirname(os.path.abspath(__file__))
	maze = ImageGrab.grabclipboard()
	pixels = maze.load()
	
	x, y = findStart(pixels, maze.size)
	if x is not None:
		# recursively search from the start node
		path = searchNode(x, y, maze, pixels)
		# save gif
		frames[0].save(folderPath+"/maze.gif", duration=0.01, save_all=True, append_images=frames[1:])
		# show path, resized
		renderMaze(maze, path).resize([i * 10 for i in maze.size]).show()

	else:
		print("No startnode found")


if __name__ == '__main__':
	main()