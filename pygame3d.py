
import pygame
from pygame.locals import *
import numpy as np
from math import *

def translate_matrix(position):
	x, y, z = position
	return np.array([
	    [1, 0, 0, 0],
	    [0, 1, 0, 0],
	    [0, 0, 1, 0],
	    [-x, -y, -z, 1]
	])

def rotation_x(a):
	rotation_matrix = np.array([
		[1,0,0],
		[0,cos(a),-sin(a)],
		[0,sin(a),cos(a)]
	])

	return rotation_matrix






def rotation_y(a):
	rotation_matrix = [
		[cos(a),0,sin(a)],
		[0,1,0],
		[-sin(a),0,cos(a)]
	]

	return rotation_matrix

def rotation_z(a):
	rotation_matrix = [
		[cos(a),-sin(a),0],
		[sin(a),cos(a),0],
		[0,0,1]
	]

	return rotation_matrix



def rotate_x(x,y,z,a):
	mr_x = np.array([
			[1,0,0],
			[0,cos(a),sin(a)],
			[0,-sin(a),cos(a)]
		])
	return np.matmul(mr_x,[x,y,z])

def rotate_z(x,y,z,a):
	mr_z = np.array([
		[cos(a),-sin(a),0],
		[sin(a),cos(a),0],
		[0,0,1]
	])
	return np.matmul(mr_z,[x,y,z])
def rotate_y(x,y,z,a):
	mr_y = np.array([
			[cos(a),0,sin(a)],
			[0,1,0],
			[-sin(a),0,cos(a)]

		])
	return np.matmul(mr_y,[x,y,z])




def Projection(h_fov,f,n,h,w):
	


	v_fov = h_fov * (h / w)
	r = tan(h_fov / 2)
	l = -r
	t = tan(v_fov / 2)
	b = -t

	return  np.array([
	    [2 / (r - l), 0, 0, 0],
	    [0, 2 / (t - b), 0, 0],
	    [0, 0, (f + n) / (f - n), 1],
	    [0, 0, -2 * n * f / (f - n), 0]
	]), (h,w)




def LookAt(px,py,pz,rx=0,ry=0,rz=0):
	return px,py,pz,rx,ry,rz

 


"""
def Render(screen,projection,vertex,Lookat):


	projection_matrix, screen_size = projection

	h,w = screen_size
	normalize = np.array([
	    [w/2, 0, 0, 0],
	    [0, -h/2, 0, 0],
	    [0, 0, 1, 0],
	    [w/2, h/2, 0, 1]
	])


	lookat = Lookat[0]
	px,py,pz = lookat
	rotations = Lookat[1]
	rx,ry,rz = rotations
	#print (rx,ry,rz)
	#vertex = np.matmul(vertex,rotation_z(rx))
	vertex = np.matmul(vertex,rotation_y(rz))
	vertex = np.matmul(vertex,rotation_x(rx))
	print(lookat)
	#vertex = np.matmul(vertex,translate_matrix(lookat))
	for point in vertex:


		point = np.array([*point, 1.0])
		#point = np.matmul(point,translate_matrix([ 0.6,0.6, -6 ]))
		point = np.matmul(point,translate_matrix(lookat))
		v = np.matmul(projection_matrix,point)
		x,y,z,w = v
		v = x/w,y/w,z/w,1
		v = np.matmul(v,normalize)
		v = v[:2]
		#pygame.draw.rect(screen, (255,255,0), pygame.Rect(v[0],v[1],5,5))

		if (float(v[0]) < -1) or (float(v[0]) > 1):
			pass
		elif (float(v[1]) < -1) or (float(v[2]) > 1):
			pass
		else:
			pygame.draw.circle(screen, (255,0,0), (v[0],v[1]),5)

"""

def Render(screen,projection,vertex,Lookat):
	projection_matrix, screen_size = projection

	h,w = screen_size
	normalize = np.array([
	    [w/2, 0, 0, 0],
	    [0, -h/2, 0, 0],
	    [0, 0, 1, 0],
	    [w/2, h/2, 0, 1]
	])

	px,py,pz,rx,ry,rz = Lookat
	"""
	for v in vertex:
		x,y,z = v
		x = x-px
		y = y-py
		z = z-pz
		x,y,z = rotate_y(x-px,y-pz,z-pz,rx)
		x,y,z = rotate_x(x-px,y-py,z-pz,ry)
		m = np.matmul([x,y,z,-1],projection_matrix)
		x,y,z,w = m[0]/m[3],m[1]/m[3],m[2]/m[3],1.0
		if (float(x) < -1) or (float(x) > 1):
			pass
		elif (float(y) < -1) or (float(y) > 1):
			pass
		else:
			x,y,z,w = np.matmul([x,y,z,w],normalize)
			pygame.draw.circle(screen, (255,0,0), (x,y),5)
	"""
	for v in vertex:
		x,y,z = v
		vertex = convert(x,y,z,px,py,pz,rx,ry,rz,h,w,projection_matrix)
		if vertex == None:
			pass
		else:
			pygame.draw.circle(screen, (255,0,0), (vertex[0],vertex[1]),4)
	
def convert(x,y,z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix):
	x = x-camx
	y = y-camy
	z = z-camz
	#print(camdir_x)

	x,y,z = rotate_y(x-camx,y-camy,z-camz,camdir_x)
	x,y,z = rotate_x(x,y,z,camdir_y)
	m = np.matmul([x,y,z,-1],projection_matrix)
	x,y,z,wi = m[0]/m[3],m[1]/m[3],m[2]/m[3],1.0

	if (float(x) < -2) or (float(x) > 2):
		return None
	if (float(y) < -2) or (float(y) > 2):
		return None

	if (float(z) < -1) or (float(z) > 1):
		return None
	
	HW,HH = h//2,w//2
	normalize = np.array([
	    [HW, 0, 0, 0],
	    [0, -HH, 0, 0],
	    [0, 0, 1, 0],
	    [HW, HH, 0, 1]
	])
	x,y,z,w = np.matmul([x,y,z,wi],normalize)
	return x,y



def RenderTriangles(screen,color,projection,vertex,Lookat,mode=0):
	projection_matrix, screen_size = projection

	h,w = screen_size

	normalize = np.array([
	    [w/2, 0, 0, 0],
	    [0, -h/2, 0, 0],
	    [0, 0, 1, 0],
	    [w/2, h/2, 0, 1]
	])

	px,py,pz,rx,ry,rz = Lookat

	if mode == 0:
		for t in vertex:
			p1 = t[0]
			p2 = t[1]
			p3 = t[2]
			p1 = convert(p1[0],p1[1],p1[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)
			p2 = convert(p2[0],p2[1],p2[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)
			p3 = convert(p3[0],p3[1],p3[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)

			if p1 == None or p2 == None or p3 == None:
				pass
			else:
				pygame.draw.line(screen,color, p1, p2)
				pygame.draw.line(screen,color, p2, p3)
				pygame.draw.line(screen,color, p1, p3)

	if mode == 1:
		for t in vertex:
			p1 = t[0]
			p2 = t[1]
			p3 = t[2]
			p1 = convert(p1[0],p1[1],p1[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)
			p2 = convert(p2[0],p2[1],p2[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)
			p3 = convert(p3[0],p3[1],p3[2],px,py,pz,rx,ry,rz,h,w,projection_matrix)

			if p1 == None or p2 == None or p3 == None:
				pass
			else:
				#pygame.draw.line(screen,color, p1, p2)
				#pygame.draw.line(screen,color, p2, p3)
				#pygame.draw.line(screen,color, p1, p3)
				pygame.draw.polygon(screen, color,[p1, p2,p3])



def ImportObj(filename):
	vertex = []
	faces = []

	with open(filename) as file:
		for line in file:
			if line.startswith('v '):
				vertex.append([float(line.split(" ")[-3:][0]),float(line.split(" ")[-3:][1]),float(line.split(" ")[-3:][2])])
			elif line.startswith('f'):
				faces_ = line.split()[1:]
				faces.append([int(faces_[0]),int(faces_[1]),int(faces_[2])])
	return vertex,faces


def any_func(arr, a, b):
	return np.any((arr == a) | (arr == b))


def RenderObj(screen,obj,coords,projection,Lookat):
	projection_matrix, screen_size = projection
	h,w = screen_size

	x,y,z = coords
	camx,camy,camz,camdir_x,camdir_y,camdir_z = Lookat
	vertex,faces = obj

	#vertex1 = vertex
	#vertex = []
	#for v in vertex1:
	#	vertex.append([v[0]+x,v[1]+y,v[2]+z])
	"""
	vertices = []
	for v in vertex:
		vertices.append([convert(v[0],v[1],v[2],camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)])
		
	

	for v in vertex:
		#print(v[0]+x,v[1]+y,v[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)
		v = convert(v[0]+x,v[1]+y,v[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)
		if v == None:
			pass
		else:
			pygame.draw.circle(screen, (255,0,0), (v[0],v[1]),4)
	"""
	vertices = []

	"""
	for v in vertex:
		v = convert(v[0]+x,v[1]+y,v[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)
		if v == None:
			pass
		else:
			vertices.append([v[0],v[1]])
	"""
	for f in faces:
		try:
			p1 = vertex[f[0]]
			p2 = vertex[f[1]]
			p3 = vertex[f[2]]
			v1 = convert(p1[0]+x,p1[1]+y,p1[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)
			v2 = convert(p2[0]+x,p2[1]+y,p2[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)
			v3 = convert(p3[0]+x,p3[1]+y,p3[2]+z,camx,camy,camz,camdir_x,camdir_y,camdir_z,h,w,projection_matrix)

			if v1 == None or v2==None or v3 == None :
				pass
			else:
				#print(v1)
				pygame.draw.polygon(screen, color, [v1,v2,v3],1)
		except:
			pass			


	"""
	for index, color in enumerate(color):
		color, face = color
		polygon = vertices[face]
		if not any_func(polygon, h_width, h_height):
			pygame.draw.polygon(screen, color, polygon)

	"""
