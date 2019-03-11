from app.common.config import sports_words_list_path


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

if __name__ == "__main__":
    input_path = 'vocabulary'
    output_path = 'w2v_vocabulary'
    get_w2v_vocabulay(input_path, output_path)