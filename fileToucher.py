import time

f = open("msg", 'w')

for i in range(10):
    print(i)
    time.sleep(1)

f.close()