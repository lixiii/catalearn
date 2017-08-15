import sys
sys.path.append('/Users/yuxuanliu/Desktop/Catalearn_All/catalearn')
import catalearn

@catalearn.run_on_gpu
def func():
    print('hello world')

func()



