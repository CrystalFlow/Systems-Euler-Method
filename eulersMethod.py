import math
import matplotlib.pyplot as plt

def dx_dt(x, y):
    solution = -1 * y
    return solution

def dy_dt(x, y):
    solution = x
    return solution

def dx_dt_solution(t):
    solution = math.cos(t)
    return solution

def dy_dt_solution(t):
    solution = math.sin(t)
    return solution

step_size = 0.1
t_max = 10
n_steps = int(round(t_max / step_size)) + 1
t_values = [i * step_size for i in range(n_steps)]

x_approx = [0.0] * n_steps
y_approx = [0.0] * n_steps
x_approx[0] = 1.0

x_actual = [0.0] * n_steps
y_actual = [0.0] * n_steps
x_actual[0] = 1.0

distance_from_actual = [0.0] * n_steps

for i in range(1, n_steps):
    mk = dx_dt(x_approx[i-1], y_approx[i-1])
    nk = dy_dt(x_approx[i-1], y_approx[i-1])
    x_approx[i] = x_approx[i-1] + mk * step_size
    y_approx[i] = y_approx[i-1] + nk * step_size

    x_actual[i] = dx_dt_solution(i * step_size)
    y_actual[i] = dy_dt_solution(i * step_size)

for i in range(n_steps):
    x_approx[i] = round(x_approx[i], 2)
    y_approx[i] = round(y_approx[i], 2)

    x_actual[i] = round(x_actual[i], 2)
    y_actual[i] = round(y_actual[i], 2)
    
    distance_from_actual[i] = round(math.sqrt((x_approx[i] - x_actual[i]) ** 2 + (y_approx[i] - y_actual[i]) ** 2), 2)

plt.plot(x_actual, y_actual, label='Actual Solution', color='blue')
plt.plot(x_approx, y_approx, label='Euler Approximation', color='orange', linestyle='dashed')
plt.title("Euler's Method Approximation vs Actual Solution")
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()

# table_data = list(zip(t_values, x_approx, y_approx, x_actual, y_actual, distance_from_actual))
# fig, ax = plt.subplots()
# the_table = ax.table(
#     cellText=table_data, 
#     colLabels=['Time', 'Euler x', 'Euler y', 'Actual x', 'Actual y', 'Distance'], 
#     cellLoc='center', 
#     loc='center')
# ax.axis('off')
# the_table.auto_set_font_size(False)
# the_table.set_fontsize(14)
# the_table.scale(1.3, 1.3)
#plt.show()


# for i in range(n_steps):    
#     print(str(round(t_values[i], 1)) + "  ---  Euler approx: " + str(round(x_approx[i], 2)) + ", " + str(round(y_approx[i], 2)) 
#           + "  ---  Actual: " + str(round(x_actual[i], 2)) + ", " + str(round(y_actual[i], 2))
#           + "  ---  Distance: " + str(round(distance_from_actual[i], 2)))
