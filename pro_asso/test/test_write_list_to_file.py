from app.util.io_utils import write_list_to_file
from test import lst
print(lst)

lst = [
    'a',
    'b',
    'c',
    'd',
    'e'
]

path = 'G:\\PycharmProjects\\pro_asso\\test\\test.py'

write_list_to_file(path, lst, 'lst')

# with open('G:\\PycharmProjects\\pro_asso\\test\\test.py', 'w') as f:
#     f.write('lst = ['+'\n')
#     for i in range(len(lst)):
#         if i == len(lst)-1:
#             f.write('\'' + lst[i] +r"'"+'\n')
#         else:
#             f.write('\'' + lst[i] +r"',"+'\n')
#     f.write(']')

from test import lst
print(lst)