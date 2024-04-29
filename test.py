# Author: Rodolfo Ferro 
# Mail: ferro@cimat.mx
# Script: Compute the Convex Hull of a set of points using the Graham Scan
EPSILON = 0.000001
import sys
import numpy as np
import matplotlib.pyplot as plt

# Function to know if we have a CCW turn
def CCW(p1, p2, p3):
	if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
		return True
	return False

# Main function:
def GiftWrapping(S):
	n = len(S)
	P = [None] * n
	l = np.where(S[:,0] == np.min(S[:,0]))
	pointOnHull = S[l[0][0]]
	i = 0
	while True:
		P[i] = pointOnHull
		endpoint = S[0]
		for j in range(1,n):
			if (abs(endpoint[0] - pointOnHull[0]) <= EPSILON and abs(endpoint[1] - pointOnHull[1]) <= EPSILON) or not CCW(S[j],P[i],endpoint):
				endpoint = S[j]
		i = i + 1
		pointOnHull = endpoint
		if endpoint[0] == P[0][0] and endpoint[1] == P[0][1]:
			break
	for i in range(n):
		if P[-1] is None:
			del P[-1]
	return np.array(P)

def main():
	INIT_POINTS = [(-49, -5),
            (0,0),
          (-5, 45),
          (5, 15),
          (21, 15)]
	# By default we build a random set of N points with coordinates in [0,300)x[0,300):
	P = np.array(INIT_POINTS)
	L = GiftWrapping(P)
	
	# Plot the computed Convex Hull:
	plt.figure()
	plt.plot(L[:,0],L[:,1], 'b-', picker=5)
	plt.plot([L[-1,0],L[0,0]],[L[-1,1],L[0,1]], 'b-', picker=5)
	plt.plot(P[:,0],P[:,1],".r")
	plt.axis('off')
	plt.show()

if __name__ == '__main__':
  main()