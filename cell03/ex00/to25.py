#!/usr/bin/env python3
num = int(input("Enter a number less than 25\n"))
if num <= 25:
    while num <= 25:
        print(f"Inside the loop, my variable is {num}")
        num = num+1
else:
    print("ERROR")