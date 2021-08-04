import threading
from datetime import datetime
from time import sleep
from random import randint
from queue import Queue

# loops = [4,2]

# def loop(nloop,nsec):
#   print('start loop',nloop,'at:',datetime.now())
#   sleep(nsec)
#   print('loop',nloop,'done at:',datetime.now())

# def main():
#   print('starting at:',datetime.now())
#   threads = []
#   nloops = range(len(loops))

#   for i in nloops:
#     t = threading.Thread(target=loop,args=(i,loops[i]))
#     threads.append(t)

#   for i in nloops:
#     threads[i].start()

#   for i in nloops:
#     threads[i].join()

#   print('all DONE at:',datetime.now())

# class ThreadFunc(object):

#   def __init__(self,func,args,name=''):
#     self.name = name
#     self.func = func
#     self.args = args
  
#   def __call__(self): # 可执行函数
#     print(self.name)
#     self.func(*self.args)

# def main():
#   print('starting at:',datetime.now())
#   threads = []
#   nloops = range(len(loops))

#   for i in nloops:
#     t = threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__))
#     threads.append(t)

#   for i in nloops:
#     threads[i].start()

#   for i in nloops:
#     threads[i].join()

#   print('all DONE at:',datetime.now())
  
# class Student(object):
#   def __init__(self,name,age):
#     self.name = name
#     self.age = age
  
#   def __call__(self):
#     print(self.name,self.age)

class MyThread(threading.Thread):
  def __init__(self,func,args,name=''):
    threading.Thread.__init__(self)
    self.name = name
    self.func = func
    self.args = args

  def run(self):
    self.func(*self.args)

def writeQ(queue):
  print('producing object for Q...')
  queue.put('xxx',1)
  print('size now',queue.qsize())

def readQ(queue):
  val = queue.get(1)
  print(val,'consumed object from Q ... size now',queue.qsize())

def writer(queue,loops):
  for i in range(loops):
    writeQ(queue)
    sleep(randint(1,3))

def reader(queue,loops):
  for i in range(loops):
    readQ(queue)
    sleep(randint(2,5))

funcs = [writer,reader]
nfuncs = range(len(funcs))

def main():
  nloops = randint(2,5)
  print('nloops',nloops)
  q = Queue(32)

  threads = []
  for i in nfuncs:
    t = MyThread(funcs[i],(q,nloops),funcs[i].__name__)
    threads.append(t)
  
  for i in nfuncs:
    threads[i].start()

  for i in nfuncs:
    threads[i].join()

  print('all DONE')







if __name__ == '__main__':
    main()
    # Student('wc',23)()
    