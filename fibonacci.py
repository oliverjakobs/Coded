# Function for nth fibonacci number 
def fibonacci(n): 
    if n < 0: 
        print("Incorrect input") 
    elif n == 1: # First fibonacci number is 0 
        return 0
    elif n == 2: # Second fibonacci number is 1 
        return 1
    else: 
        return fibonacci(n - 1) + fibonacci(n - 2)

n = 9

print("{0}. fibonacci number".format(n))
print(fibonacci(n)) 