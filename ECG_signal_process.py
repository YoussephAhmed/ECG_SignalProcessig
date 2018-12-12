import numpy as np
import matplotlib.pyplot as plt


# getting the data from the text file part START
data1 = open("Data2.txt", "r");

lines = data1.readlines();


y_values = [];

for line in lines:
    line.rstrip();
    values = line.split();
    for value in values:
        value= float(value);
        y_values.append(value);


N = len(y_values)

Ts = 1 / 512.  # sampling freq = 512 Hz

# getting the data from the text file part END

# plotting the data START
plt.figure(1)
plt.ylabel('ECG_Signal')
plt.xlabel('Time in seconds')
t = np.arange(0., N * Ts, Ts)
plt.plot(t, y_values,'r-')
plt.show()
# plotting the data END


# The derivative of the ECG signal START

y_derivatives = []
for i in range(N):
    if i <= 1 or i >= N-2:
        y_derivative = 0
    else:
        y_derivative = (1/(8*Ts)) * (-1 * y_values[i-2] -2 *y_values[i-1]
                                  + 2 * y_values[i+1] + y_values[i+2])
    y_derivatives.append(y_derivative)

#1) The derivative of the ECG signal END


# plotting the data START
plt.figure(2)
plt.ylabel('Derivative_Signal')
plt.xlabel('Time in seconds')
t = np.arange(0., N * Ts, Ts)
plt.plot(t, y_derivatives,'r-')
plt.show()
# plotting the data END


#2) The square part of the signal START
y_squared = []
for y in y_derivatives:
    y_squared.append(y*y)
# The square part of the signal START



# plotting the data START
plt.figure(3)
plt.ylabel('Squared_Signal')
plt.xlabel('Time in seconds')
t = np.arange(0., N * Ts, Ts)
plt.plot(t, y_squared,'r-')
plt.show()
# plotting the data END

#3) smoothing average START
y_finals = []

for i in range(N):
    y_final = 0.0
    if(i>30):
        for j in range(31):
            y_final += y_squared[i-j]

        y_final /= 31.0

    y_finals.append(y_final)





# plotting the data START
plt.figure(4)
plt.ylabel('Smoothing_Signal')
plt.xlabel('Time in seconds')
t = np.arange(0., N * Ts, Ts)
plt.plot(t, y_finals,'r-')
plt.show()
# plotting the data END


#4) Auto Correleation START
auto_correlation = []
max_lag = int(N/2)
lag_values = np.arange(0., max_lag, 1)
for m in range(max_lag):
    value = 0;
    for i in range(m,N):
        value += y_finals[i] * y_finals[i-m]
    auto_correlation.append(value)

#4) Auto Correleation END


# plotting the data START
plt.figure(5)
plt.ylabel('Auto_Correlation')
plt.xlabel('Delayed_Samples')
plt.plot(lag_values, auto_correlation,'r-')
plt.show()
# plotting the data END


# The measuring part of Atrial Fibrillation STRART

# the measured value that increases with Atrial Fibrillation will be the HEART RATE!
# So first lets normalize the Correlation Curve with respect value at zero shifting
auto_correlation_normalize = [] # from 0 -> 1

for value in auto_correlation:
    normalized = value / auto_correlation[0]
    auto_correlation_normalize.append(normalized)

# plotting the data START
plt.figure(6)
plt.ylabel('Normalized_Auto_Correlation')
plt.xlabel('Delayed_Samples')
plt.plot(lag_values, auto_correlation_normalize,'r-')
plt.show()
# plotting the data END


# NOW to measure the HEART Rate we will find the first peak that passes the Threshold
# and the value just goes down that Threshold and find the max value in this interval

threshold = 0.2
flag_in = False
max_range = []

max_index = 0



for i in range(max_lag):
    if(auto_correlation_normalize[i+1] > auto_correlation_normalize[i] and auto_correlation_normalize[i] > threshold):
        flag_in = True

    if((flag_in) and (auto_correlation_normalize[i+1] < auto_correlation_normalize[i]) ):
        max_index = i
        break


for i in range (len(max_range)):
    if(auto_correlation_normalize[i] > max):
        max = auto_correlation_normalize[i]
        max_index = i

shifted_sampled = max_index

time_of_peak = Ts * shifted_sampled
time_minutes = time_of_peak / 60.
heart_rate = 1 / time_minutes

print("number of shifted samples at the peak = " , shifted_sampled)
print("time (seconds) at the peak = ", time_of_peak)
print("time (minutes) = " , time_minutes)
print("Heart Rate (bpm) = " , heart_rate)

