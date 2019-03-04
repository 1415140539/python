import collections
import threading
import time
from multiprocessing import Process

candle = collections.deque("candle")
def burn(direction,nextsource):
    while True:
        try:
            next = nextsource()
            time.sleep(0.1)
        except IndexError:
            break
        else:
            print("%s:%s\n"%(direction,next))
    print("Done %s \n"%direction)

# 创建两个线程分别从两边去双向队列中取值
# left = threading.Thread(target = burn , args = ("left",candle.popleft))
# right = threading.Thread(target = burn , args = ("right",candle.pop))

left = Process(target = burn , args = ("left",candle.popleft))
right = Process(target = burn , args = ("right",candle.pop))

if __name__ == "__main__":
    left.start()
    right.start()

    left.join()
    right.join()