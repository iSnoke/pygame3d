
import pygame3d
import pygame
from math import *
pygame.init()

h,w = 1000,1000
far,near = 100000,0.0000001


screen = pygame.display.set_mode( (h,w) )
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

cube_points = [
	[0,0,0],
	[0,0,1],
	[0,1,1],
	[1,1,0],
	[1,1,1],
	[1,0,0],
	[0,1,0],
	[1,0,1]
]


piso_puntos = []

for x in range(0,11):
	for z in range (0,11):
		piso_puntos.append([x-10,-1,z-10])


triangle = [

	[
		[0,0,1],
		[1,0,1],
		[1,1,1]
	],
	[
		[0,0,1],
		[0,1,1],
		[1,1,1]
	],
	[
		[0,0,0],
		[0,1,0],
		[0,1,1]
	],
	[
		[0,0,0],
		[0,0,1],
		[0,1,1]
	],
	[
		[0,0,0],
		[1,0,0],
		[1,1,0]
	],
	[
		[0,0,0],
		[0,1,0],
		[1,1,0]
	],

	[
		[0,0,0],
		[1,0,0],
		[1,0,1]
	],
	[
		[0,0,0],
		[0,0,1],
		[1,0,1]
	],
	[
		[1,0,0],
		[1,1,0],
		[1,1,1]
	],
	[
		[1,0,0],
		[1,0,1],
		[1,1,1]
	],
	[
		[0,1,0],
		[1,1,0],
		[1,1,1]
	],
	[
		[0,1,0],
		[0,1,1],
		[1,1,1]
	]

]

plane = [
	[-10,-1,0],
	[-10,-1,-10],
	[0,-1,0],
	[0,-1,-10]

]

piso = [
	[
		[-10,-1,0],
		[-10,-1,-10],
		[0,-1,-10]

	],
	[
		[-10,-1,0],
		[0,-1,0],
		[0,-1,-10]
	]

]




cx = 0
cy = 0
cz = -2
rx = ry = rz = 0


color = (255,255,255)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()




	screen.fill((0,0,0))

	projection = pygame3d.Projection(pi / 3,far,near,h,w)

	pygame.mouse.set_pos([h/2,w/2])

	mx,my = pygame.mouse.get_pos()

	
	rx += (h/2-mx)*0.005
	ry -= (w/2-my)*0.005
	
	key = pygame.key.get_pressed()


	

	if key[pygame.K_w]:
		cx += sin(rx)*0.1
		cz += -cos(rx)*0.1

	if key[pygame.K_s]:
		cx -= sin(rx)*0.1
		cz -= -cos(rx)*0.1	

	if key[pygame.K_d]:
		cx += -cos(rx)*0.1
		cz -= sin(rx)*0.1

	if key[pygame.K_a]:
		cx -= -cos(rx)*0.1
		cz += sin(rx)*0.1

	

	if key[pygame.K_q]:
		cy += 0.1



	if key[pygame.K_e]:
		cy -= 0.1

	if key[pygame.K_SPACE]:
		pygame.quit()




	look = pygame3d.LookAt(cx,cy,cz,rx,ry,rz)


	pygame3d.Render(screen,projection,cube_points,look)

	pygame3d.RenderTriangles(screen,color,projection,triangle,look)

	pygame3d.RenderTriangles(screen,color,projection,piso,look)


	pygame3d.Render(screen,projection,piso_puntos,look)

	pygame.display.update()

	clock.tick(60)
