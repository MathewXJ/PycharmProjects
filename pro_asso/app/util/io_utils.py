
def write_list_to_file(file_path, lst, lst_name):
    with open(file_path, 'w') as f:
        f.write( lst_name + ' = [' + '\n')
        for i in range(len(lst)):
            if i == len(lst) - 1:
                f.write('\'' + lst[i] + r"'" + '\n')
            else:
                f.write('\'' + lst[i] + r"'," + '\n')
        f.write(']')


def get_w2v_vocabulay(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as fr:
        vocabulay = [line.strip().split()[0] for line in fr.readlines() if line.strip() ]

    with open(output_path, 'w', encoding='utf-8') as fw:
        for w in vocabulay:
            fw.write(w + '\n')

from app.util.pre_model import INDEX_SX_APP_CONTNAME_SET
if __name__ == "__main__":
    with open("index_sx_app_content_name", 'w', encoding='utf-8') as fw:
        for w in INDEX_SX_APP_CONTNAME_SET:
            fw.write(w + '\n')