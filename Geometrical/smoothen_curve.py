import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Sample data
x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([1,4,9,3,6,1])

def smoothen_func(x:np.array,y:np.array, points_between:int):
    """Takes in a limited x and y array with points which are then smoothend out
    
    args:
        x: the array along the x axis
        y: the array along the y axis
        points_between: how much you want to smoothen out and increase with points between
    
    return:
        (x_array_smoothen, y_array_smoothen)"""
    # Create spline interpolation
    spline = UnivariateSpline(x, y, k=3, s=0)  # k=3 for cubic spline
    # Smoothed data points
    points_between = 10
    x_smooth = np.linspace(x.min(), x.max(), x.min()*x.max()*points_between)
    y_smooth = spline(x_smooth)
    return x_smooth, y_smooth

def view(x,y,x_smooth, y_smooth):
    """Views the smoothen and the normal graph"""
    plt.plot(x, y, label='Original Data', color='blue')
    plt.plot(x, y,'o', label='Points', color='green')
    plt.plot(x_smooth, y_smooth, label='Smoothed Curve', color='red')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.title('Smoothing with Spline Interpolation')
    plt.show()


x_smooth, y_smooth = smoothen_func(x,y,5)
view(x,y, x_smooth,y_smooth)
# Plot original and smoothed data
