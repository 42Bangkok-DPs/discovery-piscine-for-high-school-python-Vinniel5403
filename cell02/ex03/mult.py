A = int(input("Enter the first number:\n"))
B = int(input("Enter the second number:\n"))

result = A*B
print(f"{A} x {B} = {result}")
if result > 0:
    print("This number is positive.")
elif result < 0:
    print("This number is negative.")
else:
    print("This number is both positive and negative.")