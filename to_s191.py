import os

def bumotec_head_block(tools):
    head_file_name = 'bumotec_head.txt'
    path = os.path.join(os.path.abspath(''), 'data', head_file_name)
    head_text = list()
    try:
        with open(path, 'r', encoding='UTF-8') as head_file:
            for line in head_file:
                head_text.append(line)
            for tool in tools:
                head_text.insert(6, tool)
    except Exception as exc:
        error_message = f'Попытка открыть {path} провалилась. '
        f'Проверьте наличие {head_file_name} на указанном пути.\n'
        add_to_error_log(exc, error_message)
    return head_text


def convert_to_normal_nc_file(path_to_folder, file_name, frame_num):
    current_path = os.path.join(path_to_folder, file_name)
    new_nc_file = list()
    tool = ''
    try:
        new_nc_file.append(frame_num)
        frame_message = ''
        start_write = False
        with open(current_path, 'r', encoding='utf-8') as file:
            for line in file:
                if start_write:
                    new_nc_file.append(line)
                if line.startswith('M53'):
                    if not start_write:
                        new_nc_file.append(frame_message)
                    start_write = True
                elif line.startswith('ON') and '(' in line:
                    frame_message = ''.join(('(', line.partition('(')[2]))

        nc_size = len(new_nc_file)
        while nc_size:
            if new_nc_file[-1].strip() in ('\n', '', 'M30', '%'):
                new_nc_file.pop()
            else:
                new_nc_file.append('M00\n')
                break
            nc_size -= 1
        for pos, line in enumerate(new_nc_file):
            if line.startswith('M6T'):
                replace_str = new_nc_file[pos-1]
                if replace_str.startswith('(T'):
                    replace_str = ''.join(('(', ' '.join(replace_str.split()[1:]), '\n'))
                    tool = replace_str
                new_nc_file[pos-1] = replace_str
                break

    except BaseException as exc:
        error_message = f'Обнаружена ошибка при попытке открыть файл {current_path}\n'
        add_to_error_log(exc, error_message)
    return new_nc_file, tool


def get_file_list(path):
    nc_files = list()
    elements_to_delete = list()
    folders = list()    
    try:
        all_files = os.listdir(path)
        for element in all_files:
            if element.lower().endswith('.nc'):
                nc_files.append(element)
            else:
                current_path = os.path.join(path, element)
                if os.path.isdir(current_path):
                    folders.append(element)
                else:
                    elements_to_delete.append(element)
        if not len(nc_files):
            raise Exception
        
    except Exception as exc:
        error_message = f'В папке {path} нет файлов с расширением *.NC\n'
        add_to_error_log(exc, error_message)

    analysis = {'nc':nc_files, 'dir':folders, 'delete':elements_to_delete}
    return analysis


def create_directories(path, direcroty_name, sub_directory_name):
    bumotec = os.path.join(path, direcroty_name[0])
    macodell = os.path.join(path, direcroty_name[1])
    if not os.path.exists(bumotec):
        os.makedirs(bumotec)
    if not os.path.exists(macodell):
        os.makedirs(macodell)
    sub_path_one = os.path.join(bumotec, sub_directory_name[0])
    sub_path_all = os.path.join(bumotec, sub_directory_name[1])
    if not os.path.exists(sub_path_one):
        os.makedirs(sub_path_one)
    if not os.path.exists(sub_path_all):
        os.makedirs(sub_path_all)
    sub_path_one = os.path.join(macodell, sub_directory_name[0])
    sub_path_all = os.path.join(macodell, sub_directory_name[1])
    if not os.path.exists(sub_path_one):
        os.makedirs(sub_path_one)
    if not os.path.exists(sub_path_all):
        os.makedirs(sub_path_all)


def add_to_error_log(exc, error):
    with open('error.log', 'a', encoding='UTF-8') as error_log:
        error_message = list()
        error_message.append('{mistake}, {comment}\n'.format(
            mistake=type(exc), comment=exc))
        error_message.append(error)
        error_message.append('\n')
        for mistakes in error_message:
            error_log.write(mistakes)


def add_multiple_bumotec_files(path, directory_name, sub_directory_name, file_name, text):
    current_path = os.path.join(path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(text)


def add_one_bumotec_files(path, directory_name, sub_directory_name, file_name, all_nc_files, tools):
    current_path = os.path.join(path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(bumotec_head_block(tools))
        for nc_file in all_nc_files:
            file.writelines(['\n', '\n'])
            file.writelines(nc_file)
        file.writelines(['M30\n', '%\n'])


def main():
    file_name = '111.NC'
    directory_name = 'Bumotec', 'Macodell'
    sub_directory_name = 'ONE_FILE', 'ALL'
    one_file_name = 'O1234.NC'
    current_path = os.path.abspath('')
    objects_in_folder = get_file_list(current_path)
    if objects_in_folder['nc']:
        create_directories(current_path, directory_name, sub_directory_name)
        all_nc_files = list()
        tools = list()
        for number, nc_file in enumerate(objects_in_folder['nc']):
            frame_num = ''.join(('N', str((number + 2)*10), '\n'))
            correct_file, nc_tool = convert_to_normal_nc_file(current_path, nc_file, frame_num)
            all_nc_files.append(correct_file)
            tools.append(nc_tool)
            add_multiple_bumotec_files(current_path, directory_name[0], sub_directory_name[1], nc_file, correct_file)
        tools = set(tools)
        add_one_bumotec_files(current_path, directory_name[0], sub_directory_name[0], one_file_name, all_nc_files, tools)


main()
