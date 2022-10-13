# Python program to illustrate the concept
# of threading
# importing the threading module
import threading

 
def print_cube(num):
    # function to print cube of given num
    print("Cube: {}" .format(num * num * num))
    return "Haodong LI"
 
 
def print_square(num):
    # function to print square of given num
    print("Square: {}" .format(num * num))
    return "Jiayi ZHAO"
 
 
if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_square, args=(10,))
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    a = t1.join()
    # wait until thread 2 is completely executed
    b = t2.join()

    print(a, b)
 
    # both threads completely executed
    print("Done!")
