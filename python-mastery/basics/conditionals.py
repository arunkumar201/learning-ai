age=12
name="Arun"

if age>=18:
    print("You are eligible to vote")
elif age<18 and age>0:
    print("You are not eligible to vote")
elif age==0:
    print("You are not eligible to vote")
elif age<0:
    print("Invalid age")
else:
    print("Invalid age")
    

# ternary operator
print("You are eligible to vote") if age>=18 else print("You are not eligible to vote")

# switch case
match age:
    case 18:
        print("You are eligible to vote")
    case 0:
        print("You are not eligible to vote")
    case _:
        print("Invalid age")
        

if age>18 and len(name)>4:
    print("You are eligible to vote")
else:
    print("You are not eligible to vote")
