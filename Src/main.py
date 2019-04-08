###########################################################################
# Setup code goes below, this is called once at the start of the program: #
###########################################################################
import time
print('Hello world! I can count:')
i = 1

with open("./landing/landing.html", "r") as file:
    print(file.read())
    file.close()

