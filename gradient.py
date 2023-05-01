import numpy as np
import matplotlib.pyplot as plt

# Define the function f(x,y) = x^2 + y^2
def f(x,y):
    return x**2 + y**2

# Define the gradient of f(x,y)
def grad_f(x,y):
    return np.array([2*x, 2*y])

# Define the learning rate
alpha = 0.1

# Define the initial point
x = 1
y = 1

# Create a list to store the points
points = [(x,y)]

# Run the gradient descent for 10 iterations
for i in range(10):
    # Update x and y by subtracting alpha times the gradient
    x = x - alpha * grad_f(x,y)[0]
    y = y - alpha * grad_f(x,y)[1]
    # Append the new point to the list
    points.append((x,y))

# Convert the list of points to a numpy array
points = np.array(points)

# Create a meshgrid for plotting
X,Y = np.meshgrid(np.linspace(-1,1,100), np.linspace(-1,1,100))

# Plot the contour of f(x,y)
plt.contour(X,Y,f(X,Y), levels=20)
# Plot the points obtained from gradient descent
plt.plot(points[:,0], points[:,1], 'ro-')
# Label the axes and show the plot
plt.xlabel('x')
plt.ylabel('y')
plt.show()