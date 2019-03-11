lst = [
'a',
'b',
'c',
'd',
'e'
]

from app.util.pre_model import W2V_VOCABULARY_SET
import time

time1 = time.time()
str = '战狼'
if str in W2V_VOCABULARY_SET:
    print('in')
else:
    print('not in')
time2 = time.time()
print('costs: %s ms' % ((time2-time1)*1000))