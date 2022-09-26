import numpy as np
from math import *
import pygame
def camera_yaw(angle,forward,right,up):
	rotate = rotate_y(angle)
	forward = np.matmul(forward,rotate)
	right = np.matmul(right,rotate)
	up  = np.matmul(up,rotate)
	return forward,right,up

def camera_pitch(angle,forward,right,up):
	rotate = rotate_x(angle)

	forward = np.matmul(forward,rotate)
	right = np.matmul(right,rotate)
	up  = np.matmul(up,rotate)
	return forward,right,up

def translate_matrix(position,right):
	x, y, z, w = position
	return np.array([
	    [1, 0, 0, 0],
	    [0, 1, 0, 0],
	    [0, 0, 1, 0],
	    [-x, -y, -z, 1]
	])

def rotate_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(a), sin(a), 0],
        [0, -sin(a), cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotate_y(a):
    return np.array([
        [cos(a), 0, -sin(a), 0],
        [0, 1, 0, 0],
        [sin(a), 0, cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotate_matrix(right,forward,up):
	rx, ry, rz, w = right
	fx, fy, fz, w = forward
	ux, uy, uz, w = up
	return np.array([
	    [rx, ux, fx, 0],
	    [ry, uy, fy, 0],
	    [rz, uz, fz, 0],
	    [0, 0, 0, 1]
	])


def any_func(arr, a, b):
	return np.any((arr == a) | (arr == b))


def point3d(cam,screen,color,x,y,z):

	cam_pos = cam[4]

	h_fov = pi / 3
	v_fov = h_fov * (cam[2] / cam[3])
	NEAR = cam[0]
	FAR = cam[1]
	RIGHT = tan(h_fov / 2)
	LEFT = -RIGHT
	TOP = tan(v_fov / 2)
	BOTTOM = -TOP
	H_WIDTH, H_HEIGHT = cam[2] // 2, cam[3] // 2


	projection_matrix = np.array([
	    [2 / (RIGHT - LEFT), 0, 0, 0],
	    [0, 2 / (TOP - BOTTOM), 0, 0],
	    [0, 0, (FAR + NEAR) / (FAR - NEAR), 1],
	    [0, 0, -2 * NEAR * FAR / (FAR - NEAR), 0]
	])

	HW, HH = H_WIDTH, H_HEIGHT
	to_screen_matrix = np.array([
	    [HW, 0, 0, 0],
	    [0, -HH, 0, 0],
	    [0, 0, 1, 0],
	    [HW, HH, 0, 1]
	])


	vertex = [x,y,z,1.0]

	vertex = np.matmul(vertex,cam_pos) 
	vertex = np.matmul(vertex,projection_matrix)
	x,y,z,w = vertex
	vertex = x/w,y/w,z/w,1
	vertex = np.matmul(vertex,to_screen_matrix)
	vertex = vertex[:2]

	pygame.draw.circle(screen, (color), (vertex),5)







def get_object_from_file(filename):
    vertex, faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    return vertex, faces


def RenderObjet(screen,cam,name,color,px=0,py=0,pz=0):

	cam_pos = cam[4]

	h_fov = pi / 3
	v_fov = h_fov * (cam[2] / cam[3])
	NEAR = cam[0]
	FAR = cam[1]
	RIGHT = tan(h_fov / 2)
	LEFT = -RIGHT
	TOP = tan(v_fov / 2)
	BOTTOM = -TOP
	h_width, h_height = cam[2] // 2, cam[3] // 2

	projection_matrix = np.array([
	    [2 / (RIGHT - LEFT), 0, 0, 0],
	    [0, 2 / (TOP - BOTTOM), 0, 0],
	    [0, 0, (FAR + NEAR) / (FAR - NEAR), 1],
	    [0, 0, -2 * NEAR * FAR / (FAR - NEAR), 0]
	])

	hw, hh = h_width, h_height
	to_screen_matrix = np.array([
	    [hw, 0, 0, 0],
	    [0, -hh, 0, 0],
	    [0, 0, 1, 0],
	    [hw, hh, 0, 1]
	])


	vertices1, faces = get_object_from_file(name)
	vertices = []
	for i in vertices1:
		vertices.append([i[0]+px,i[1]+py,i[2]+pz,i[3]])

	faces = np.array([np.array(face) for face in faces])
	color = [(pygame.Color('orange'), face) for face in faces]


	vertices = np.matmul(vertices,cam_pos) 
	vertices = np.matmul(vertices,projection_matrix)
	vertices /= vertices[:, -1].reshape(-1, 1)
	vertices[(vertices > 2) | (vertices < -2)] = 0
	vertices = np.matmul(vertices,to_screen_matrix)
	vertices = vertices[:, :2]


	for index, color in enumerate(color):
		color, face = color
		polygon = vertices[face]
		if not any_func(polygon, h_width, h_height):
			pygame.draw.polygon(screen, color, polygon, 1)





def Camera(far,near,width,height,position,cx=0,cy=0,cz=0,rx=0,ry=0,rz=0):
	if len(position) == 3: position = np.array([*position, 1.0])
	#position = np.array([position[0],position[1],position[2],1.0])
	speed = 0.3


	forward = np.array([0, 0, 1, 1])
	up = np.array([0, 1, 0, 1])
	right = np.array([1, 0, 0, 1])

	

	position -= right * speed * cx
	position += forward * speed * cz 
	position += up * speed * cy
 

	forward,right,up = camera_yaw(ry,forward,right,up)
	forward,right,up = camera_pitch(rx,forward,right,up)
	#print (right)
	return far,near,width,height, np.matmul(translate_matrix(position,right),rotate_matrix(right,forward,up))

