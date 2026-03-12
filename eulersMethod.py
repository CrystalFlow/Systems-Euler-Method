def dx_dt(y):
    solution = -1 * y
    return solution

def dy_dt(x):
    solution = x
    return solution

"""
def x_val_approx(int index, int slope, int step_size):
    print("test")

def y_val_approx(int index, int slope, int step_size):
    print("test")
"""

step_size = 0.5

x_approx = [1] * 10
y_approx = [0] * 10

for i in range(1,10):
    x_approx[i] = x_approx[i-1] + dx_dt(x_approx[i-1]) * step_size
    y_approx[i] = y_approx[i-1] + dy_dt(y_approx[i-1]) * step_size

for i in range(10):    
    print(str(i+1) + ": " + str(x_approx[i]) + ", " + str(y_approx[i]))