from PIL import Image
import random, sys


def availNodes(x, y, visited, pixels, size):
	w, h = size
	nodes = []  # ((x, y), (x1, y1)) where x,y is the "destination node" (the one checked) and x1,y1 is the "road node" bridging the dest node and "parameter given" node
	
	# up
	if y-2 >= 0 and y-2 < h and pixels[x, y-2] == (0xff, 0xff, 0xff):
		nodes.append(((x, y - 2), (x, y - 1)))
	# left
	if x-2 >= 0 and x-2 < w and pixels[x-2, y] == (0xff, 0xff, 0xff):
		nodes.append(((x - 2, y), (x - 1, y)))
	# down
	if y+2 >= 0 and y+2 < h and pixels[x, y+2] == (0xff, 0xff, 0xff):
		nodes.append(((x, y + 2), (x, y + 1)))
	# right
	if x+2 >= 0 and x+2 < w and pixels[x+2, y] == (0xff, 0xff, 0xff):
		nodes.append(((x + 2, y), (x + 1, y)))

	return [node for node in nodes if node[0] not in visited]


def nodeAction(x, y, maze, pixels, visited=None):
	if visited is None:
		visited = []

	while nodes := availNodes(x, y, visited, pixels, maze.size):
		node, middleNode = random.choice(nodes)
		# draw a road
		pixels[node] = 0, 0, 0
		pixels[middleNode] = 0, 0, 0
		# do it again
		nodeAction(*node, maze, pixels, visited=visited+[(x, y)])

		if len(nodes) == 1:
			return x, y


def main():
	sys.setrecursionlimit(round(1e6))
	rootSize = 151
	maze = Image.new(size=(rootSize, rootSize), mode="RGB", color=(0xff, 0xff, 0xff))
	pixels = maze.load()

	pixels[rootSize // 2, rootSize // 2] = 0, 0, 0xff
	nodeAction(rootSize // 2, rootSize // 2, maze, pixels)
	pixels[rootSize - 2, 1] = 0xff, 0, 0

	maze.save("maze.png")


if __name__ == '__main__':
	main()
