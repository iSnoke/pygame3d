import pygame
from pygame3d import *
pygame.init()
screen_size = 800

screen = pygame.display.set_mode( (screen_size,screen_size) )
clock = pygame.time.Clock()
FPS = 60


#cam_pos = [1,0,-10]
cam_pos = [0,0,-10]
far = 100
near = 1

cx = cy = cz = 0
rx = ry = rz = 0
#cam = Camera(far,near,screen_size,screen_size,cam_pos)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()


	screen.fill((0,0,0))

	key = pygame.key.get_pressed()
	if key[pygame.K_e]:
		cy -= 0.1
	if key[pygame.K_q]:
		cy += 0.1
	if key[pygame.K_d]:
		cx -= 0.1
	if key[pygame.K_a]:
		cx += 0.1
	if key[pygame.K_w]:
		cz += 0.1
	if key[pygame.K_s]:
		cz -= 0.1

	
	if key[pygame.K_UP]:
		rx -= 0.015
	if key[pygame.K_DOWN]:
		rx += 0.015
	if key[pygame.K_LEFT]:
		rz -= 0.015
	if key[pygame.K_RIGHT]:
		rz += 0.015

		

	cam = Camera(far,near,screen_size,screen_size,cam_pos,cx,cy,cz,rx,rz,ry)



	point3d(cam,screen,(255,0,0),0,0,0)
	point3d(cam,screen,(255,0,0),0,0,1)
	point3d(cam,screen,(255,0,0),0,1,1)
	point3d(cam,screen,(255,0,0),1,0,0)
	point3d(cam,screen,(255,0,0),1,1,0)
	point3d(cam,screen,(255,0,0),0,1,0)
	point3d(cam,screen,(255,0,0),1,0,1)
	point3d(cam,screen,(255,0,0),1,1,1)






	RenderObjet(screen,cam,"objeto.obj",(255,0,255),4,0,0)


	pygame.display.update()
	clock.tick(FPS)
