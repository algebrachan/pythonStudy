from math import ceil ,floor
import numpy as np
class CommonSticOp(object):
  def __init__(self,dataset):
    self.dataset = dataset
    self.interv = 1 
    self.result = []
    self.x_t = []
    self.count_list = []
    self.pdf_list = []

  def get_dist_fit(self,interv=None):
    if interv is None: 
      interv = self.interv

    data = self.dataset 
    if len(data) == 0:
      return []
    mi = floor(float(min(data))) 
    mx = ceil(float(max(data)))
    x_t = np.arange(mi, mx+interv,interv).tolist()
    mu = np.mean(data)
    sigma = np.std(data)
    # 先计算正态分布
    pdf = self.__normfun(x_t,mu,sigma)
    count_list = [0 for x in range(0,len(x_t))]
    for num in data:
      for x in x_t:
        left, right = x-interv/2,x+interv/2
        if left < float(num) <= right:
          count_list[x_t.index(x)] += 1

    self.x_t = x_t
    self.count_list = count_list
    self.pdf_list = pdf
    for i in range(0,len(x_t)):
      tp = (x_t[i],count_list[i],pdf[i])
      self.result.append(tp)
    return self.result

  def get_dist(self,interv=None):
    if interv is None: 
      interv = self.interv

    data = self.dataset 
    if len(data) == 0:
      return []
    mi = floor(float(min(data))) 
    mx = ceil(float(max(data)))
    x_t = np.arange(mi, mx+interv,interv).tolist()
    count_list = [0 for x in range(0,len(x_t))]
    for num in data:
      for x in x_t:
        left, right = x-interv/2,x+interv/2
        if left < float(num) <= right:
          count_list[x_t.index(x)] += 1

    self.x_t = x_t
    self.count_list = count_list
    for i in range(0,len(x_t)):
      tp = (x_t[i],count_list[i])
      self.result.append(tp)
    return self.result

  def __normfun(self,x, mu, sigma):
    ''' 拟合正态分布 x：横坐标,mu：均值,sigma:方差 '''
    pdf = np.exp(-((x - mu)**2)/(2*sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return pdf
  






def interval_static(data:list,interv=1):
  '''统计区间分布 ( ] 下边界不包括，上边界包括'''
  if len(data) == 0:
    return None
  try:
    mi = floor(float(min(data)))
    if mi == min(data):mi -= interv
    mx = ceil(float(max(data)))
    # 生成 区间统计
    res_dict = {}
    for i in range(ceil((mx-mi)/interv)):
      res_dict[f'{mi+i*interv}~{mi+(i+1)*interv}'] = 0
    for num in data:
      for res in res_dict:
        lr = tuple(res.split('~'))
        left , right = float(lr[0]),float(lr[1])
        if left < float(num) <= right:
          res_dict[res] +=1

    return res_dict
  except Exception as e:
    return None

def calculate_ot(data:list,wt:float):
  ''' 统计超时数量 wt:临界工时'''
  total = len(data)
  if total == 0:
    return None
  try:
    ot = 0
    for num in data:
      if float(num) > wt: ot += 1
    return (ot,total-ot)    
  except Exception as e:
    return None
    
if __name__ == '__main__':
  di = {}
  di['123'] = 1
  print(di)
    



  