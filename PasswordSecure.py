characters = (('a', '@'),('i', '1'),('u', '#'),('e', '*'),('o', 'O'))
def Secure(password):
    for p,q in characters:
        password = password.replace(p, q)
    return password

a = input("Enter Your Password:")
a = Secure(a)
print("Your Password is:", a)
