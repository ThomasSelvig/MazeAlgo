from PIL import Image, ImageDraw
import os

frames = []  # to create a final GIF


class Colors:
	START = (0, 0, 255)
	ROAD = (0, 0, 0)
	END = (255, 0, 0)

	ANIM = (0, 139, 139)


def renderMaze(maze, colored):
	pixels = maze.load()
	for px in colored:
		pixels[px] = Colors.ANIM
	return maze.resize([i * 20 for i in maze.size])


def findStart(pixels, size):
	for y in range(size[1]):
		for x in range(size[0]):
			if pixels[x, y] == Colors.START:
				return x, y


def findAvailNeig(x, y, pixels, size):
	neigh = []
	
	# up
	if y-1 >= 0 and y-1 < size[1] and pixels[x, y-1] in (Colors.ROAD, Colors.END):
		neigh.append((x, y - 1))
	# left
	if x-1 >= 0 and x-1 < size[0] and pixels[x-1, y] in (Colors.ROAD, Colors.END):
		neigh.append((x - 1, y))
	# down
	if y+1 >= 0 and y+1 < size[1] and pixels[x, y+1] in (Colors.ROAD, Colors.END):
		neigh.append((x, y + 1))
	# right
	if x+1 >= 0 and x+1 < size[0] and pixels[x+1, y] in (Colors.ROAD, Colors.END):
		neigh.append((x + 1, y))

	return neigh


def searchNode(x, y, maze, pixels, visited=None):
	if visited is None:
		visited = []

	frames.append(renderMaze(maze, visited+[(x, y)]))

	if pixels[x, y] == Colors.END:
		return visited + [(x, y)]

	for node in [n for n in findAvailNeig(x, y, pixels, maze.size) if n not in visited]:
		if (search := searchNode(*node, maze.copy(), pixels, visited=visited+[(x, y)])) is not None:
			return search


def main():
	folderPath = os.path.dirname(os.path.abspath(__file__))
	maze = Image.open((folderPath+"/maze.png") if "maze.png" in os.listdir(folderPath) else input("Maze image path: "))
	pixels = maze.load()
	
	x, y = findStart(pixels, maze.size)
	# recursively search from the start node
	path = searchNode(x, y, maze, pixels)

	
	frames[0].save(folderPath+"/maze.gif", save_all=True, append_images=frames[1:])
	
	#renderMaze(maze, path).show()


if __name__ == '__main__':
	main()