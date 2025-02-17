import time

# Print the current time in seconds since the Epoch
print(time.time())

# Print the current local time as a struct_time object
print(time.localtime())

# Get the current time in seconds since the Epoch
x = time.time()

# Print the local time in a human-readable format using an f-string
print(f'local time: {time.ctime(x)}')
