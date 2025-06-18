import string
import random

l1 = string.ascii_lowercase
l2 = string.ascii_uppercase
l3 = string.digits
l4 = string.punctuation

l = []

l.extend(l1)
l.extend(l2)
l.extend(l3)
l.extend(l4)
plength = int(input("Enter number of length your want:"))

random.shuffle(l)

print("".join(l[0:plength]))