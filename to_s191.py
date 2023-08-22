import os
import datetime


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
            head_text[4] = ''.join(('(', str(datetime.date.today()), ')\n'))
    except BaseException as exc:
        error_message = f'Попытка открыть {path} провалилась. '
        f'Проверьте наличие {head_file_name} на указанном пути.\n'
        add_to_error_log(exc, error_message)
    return head_text


def macodell_head_block(tools):
    head_file_name = 'macodell_head.txt'
    path = os.path.join(os.path.abspath(''), 'data', head_file_name)
    head_text = list()
    try:
        with open(path, 'r', encoding='UTF-8') as head_file:
            for line in head_file:
                head_text.append(line)
            for tool in tools:
                head_text.insert(6, tool)
            head_text[4] = ''.join(('(', str(datetime.date.today()), ')\n'))
    except BaseException as exc:
        error_message = f'Попытка открыть {path} провалилась. '
        f'Проверьте наличие {head_file_name} на указанном пути.\n'
        add_to_error_log(exc, error_message)
    return head_text


def get_normal_num_t(line):
    t_number = ''
    line_without_t_number = line
    allow_symbols = '01213456789 '
    for symbol in line[2:]:
        if symbol in allow_symbols:
            t_number += symbol
        else:
            break
    if len(t_number) > 0:
        t_number = ''.join(('(T', t_number))
        line_without_t_number = ''.join(('(', (line.partition(t_number)[2])))
    return line_without_t_number


def convert_to_normal_nc_file(path_to_folder, file_name, frame_num):
    data = {'angle_c': '', 'angle_b': '', 'speed': '', 'tool_num': '',
            'tool_mes': '', 'frame_mes': '', 'number': ''}
    current_path = os.path.join(path_to_folder, file_name)
    new_nc_file = list()
    tool = ''
    try:
        new_nc_file.append(''.join(('N', str(frame_num*10), '\n')))
        frame_message = ''
        buffer_message = ''
        start_write = False
        add_m12 = False
        check_next_line = False
        count_g201 = 0
        with open(current_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('(') and add_m12:
                    new_nc_file.append('M12\n')
                if start_write:
                    new_nc_file.append(line)
                if check_next_line:
                    if line.startswith('('):
                        frame_message = line
                        check_next_line = False
                if line.startswith('M6T'):
                    data['tool_num'] = get_number_after_letter(line, 'T')
                    if buffer_message.startswith('(T'):
                        buffer_message = get_normal_num_t(buffer_message)
                        tool = buffer_message
                        data['tool_mes'] = buffer_message
                    if not start_write:
                        data['frame_mes'] = frame_message
                        new_nc_file.append(frame_message)
                    start_write = True
                    new_nc_file.append(buffer_message)
                    new_nc_file.append(line)
                elif line.startswith('M3S'):
                    data['speed'] = get_number_after_letter(line, 'S')
                elif line.startswith('ON'):
                    if '(' in line:
                        frame_message = ''.join(('(', line.partition('(')[2]))
                    else:
                        check_next_line = True
                elif line.startswith('M8'):
                    add_m12 = True
                elif line.startswith('G201'):
                    count_g201 += 1
                    if count_g201 == 1:
                        data['angle_b'] = get_number_after_letter(line, 'B')
                if not start_write:
                    buffer_message = line
        nc_size = len(new_nc_file)
        while nc_size:
            if new_nc_file[-1].strip() in ('\n', '', 'M30', '%'):
                new_nc_file.pop()
            else:
                new_nc_file.append('M00\n')
                break
            nc_size -= 1

        if count_g201 > 1:
            write_line = True
            multiple_nc_file = list()
            miss_symbols = ('G69', 'G49', 'G0C', 'G201', '(')
            for index, line in enumerate(new_nc_file):
                if line.startswith('M12') and new_nc_file[index + 2].startswith(miss_symbols):
                    multiple_nc_file.append('M9\n')
                    multiple_nc_file.append('G69\n')
                    multiple_nc_file.append('G49\n')
                    multiple_nc_file.append('M5\n')
                    multiple_nc_file.append('M53\n')
                    multiple_nc_file.append('M00\n')
                    multiple_nc_file.append('\n')
                    multiple_nc_file.append('\n')
                    frame_num += 1
                    multiple_nc_file.append(
                        ''.join(('N', str(frame_num*10), '\n')))
                    multiple_nc_file.append(data['frame_mes'])
                    multiple_nc_file.append(data['tool_mes'])
                    temp_mes = ''.join(('M6', data['tool_num'], 'H0B0\n'))
                    multiple_nc_file.append(temp_mes)
                    write_line = False
                else:
                    if write_line:
                        multiple_nc_file.append(line)
                    else:
                        if line.startswith('G0C'):
                            data['angle_c'] = get_number_after_letter(
                                line, 'C')
                            temp_mes = ''.join((data['frame_mes'].partition(')')[
                                               0], ' ', data['angle_c'], ')\n'))
                            mul_index = len(multiple_nc_file) - 4
                            multiple_nc_file[mul_index] = temp_mes
                        elif line.startswith('('):
                            multiple_nc_file.append(line)
                        elif not line.startswith(miss_symbols):
                            multiple_nc_file.append(
                                ''.join(('M3', data['speed'], '\n')))
                            multiple_nc_file.append(
                                ''.join(('G0', data['angle_c'], '\n')))
                            multiple_nc_file.append('G211\n')
                            multiple_nc_file.append(
                                ''.join(('G0X60Y0Z100', data['angle_b'], '\n')))
                            multiple_nc_file.append('G49\n')
                            multiple_nc_file.append(
                                ''.join(('G201X0Y0Z0', data['angle_b'], 'I#510J#511K#512\n')))
                            multiple_nc_file.append(line)
                            multiple_nc_file.append('M8M138\n')
                            write_line = True
    except BaseException as exc:
        error_message = f'Обнаружена ошибка при попытке открыть файл {current_path}\n'
        add_to_error_log(exc, error_message)
    frame_num += 1
    if count_g201 <= 1:
        return new_nc_file, tool, frame_num
    else:
        return multiple_nc_file, tool, frame_num


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

    analysis = {'nc': nc_files, 'dir': folders, 'delete': elements_to_delete}
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
    current_path = os.path.join(
        path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(text)


def add_multiple_macodell_files(path, directory_name, sub_directory_name, nc_file, file_name):
    current_path = os.path.join(
        path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(nc_file)


def add_one_bumotec_files(path, directory_name, sub_directory_name, file_name, all_nc_files, tools):
    current_path = os.path.join(
        path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(bumotec_head_block(tools))
        for nc_file in all_nc_files:
            file.writelines(['\n', '\n'])
            file.writelines(nc_file)
        file.writelines(['M30\n', '%\n'])


def add_one_macodell_files(path, directory_name, sub_directory_name, file_name, all_nc_files, tools):
    current_path = os.path.join(
        path, directory_name, sub_directory_name, file_name)
    with open(current_path, 'w', encoding='UTF-8') as file:
        file.writelines(macodell_head_block(tools))
        for nc_file in all_nc_files:
            file.writelines(['\n', '\n'])
            file.writelines(nc_file)
        file.writelines(['M30\n', '%\n'])


def get_number_after_letter(line, letter):
    value = letter
    allow_symbols = '0123456789.-'
    for symbol in line.partition(letter)[2]:
        if symbol in allow_symbols:
            value += symbol
        else:
            break
    return value


def from_bumotec_to_macodell(bumotec_block, pos):
    all_blocks = list()
    main_pos = -1
    on_g802 = False
    full_block = list()
    for element in bumotec_block:
        if element.startswith('N'):
            all_blocks.append(list())
            main_pos += 1
        all_blocks[main_pos].append(element)
    for index, item in enumerate(all_blocks):
        if index == 1:
            on_g802 = True
        full_block.extend(add_multi_angles_in_one_file(item, on_g802))
    full_block.append('M9\n')
    full_block.append('G53Z0M05\n')
    full_block.append('G53B0X0Y0\n')
    full_block.append('M00\n')
    full_block[0] = ''.join(('N', str(pos * 10), '\n'))
    return full_block


def add_multi_angles_in_one_file(bumotec_block, on_g802=False):
    macodell_block = list()
    shrink_data = list()
    write_line = True
    for pos, line in enumerate(bumotec_block):
        if line.startswith('M6T'):
            write_line = False
        if write_line:
            macodell_block.append(line)
            if line.startswith('M8'):
                macodell_block.pop()
                if not on_g802:
                    macodell_block.append('M8\n')
            elif line.startswith('M12'):
                macodell_block.pop()
                macodell_block.append('M1\n')
                macodell_block.append('M3\n')
        else:
            shrink_data.append(line)
        if line.startswith('G201'):
            shrink_data.append(bumotec_block[pos + 1])
            write_line = True
    data = {'angle_c': '', 'angle_b': '', 'speed': '', 'tool_num': '',
            'x_1': '', 'y_1': '', 'z_1': '', 'feed': '', 'special_str': '\n'}
    for index, line in enumerate(shrink_data):
        if line.startswith('M6T'):
            data['tool_num'] = get_number_after_letter(line, 'T')
            if shrink_data[index + 1].startswith('('):
                data['special_str'] = shrink_data[index + 1]
        elif line.startswith('G0C'):
            data['angle_c'] = get_number_after_letter(line, 'C')
        elif line.startswith('G201'):
            data['angle_b'] = get_number_after_letter(line, 'B')
        elif line.startswith('M3S'):
            data['speed'] = get_number_after_letter(line, 'S')
    data['x_1'] = get_number_after_letter(shrink_data[-1], 'X')
    data['y_1'] = get_number_after_letter(shrink_data[-1], 'Y')
    data['z_1'] = get_number_after_letter(shrink_data[-1], 'Z')
    data['feed'] = get_number_after_letter(shrink_data[-1], 'F')
    if not on_g802:
        new_line = ''.join((data['speed'], '\n'))
        macodell_block.insert(3, new_line)
    if not on_g802:
        new_line = ''.join(('G806', data['tool_num'], data['angle_b'], 'H11I#701J#702K#703V1',
                            data['x_1'], data['y_1'], data['z_1'], data['angle_c'],
                            'S2000', data['feed'], '\n'))
        macodell_block.insert(3, new_line)
    else:
        macodell_block.pop(2)
        new_line = ''.join(('G802', data['angle_b'], 'H11I#701J#702K#703V1',
                            data['x_1'], data['y_1'], data['z_1'], data['angle_c'],
                            data['feed'], '\n'))
        macodell_block.insert(2, new_line)
    if not on_g802:
        new_line = 'G55\n'
        macodell_block.insert(3, new_line)
    delete_symbols = ('M9', 'G69', 'G49', 'M5',
                      'M53', 'M0', '', '\n', 'M00')
    size_of_block = len(macodell_block)
    count = 0
    while count < size_of_block:
        if macodell_block[-1].strip() in delete_symbols:
            macodell_block.pop()
        else:
            break
        count += 1
    if on_g802:
        macodell_block[0] = 'M3\n'
        macodell_block.insert(1, '\n')
        macodell_block.insert(0, 'M1\n')
        macodell_block.insert(0, '\n')
        macodell_block.insert(5, data['special_str'])
    return macodell_block


def make_correct_order(names):
    new_order = dict()
    correct_list = list()
    try:
        for item in names:
            short_key = int(item[-5:].replace('_',
                                              '').replace('.NC', '').replace('.nc', ''))
            new_order[short_key] = item
        for key in sorted(new_order.keys()):
            correct_list.append(new_order[key])
    except BaseException as exc:
        error_message = f'Были обраружены проблемы с '
        f'расширением NC файлов. Проверьте расширения *.NC\n'
        add_to_error_log(exc, error_message)
    return correct_list


def get_data_from_config():
    current_path = os.path.join(os.path.abspath(''), 'data', 'config.txt')
    data = list()
    try:
        with open(current_path, 'r', encoding='UTF-8') as file:
            for line in file:
                if line.strip() != '':
                    data.append(line.partition('=')[2].strip())
    except BaseException as exc:
        error_message = f'Неверно сохранены данныек внутри config.txt или файл отсутсвует.\n'
        add_to_error_log(exc, error_message)
    return data


def load_path():
    current_path = os.path.join(os.path.abspath(''), 'data', 'config.txt')
    data = list()
    try:
        with open(current_path, 'r', encoding='UTF-8') as file:
            for line in file:
                if line.strip() != '':
                    data.append(line.partition('=')[2].strip())
        current_path = data[5]
        if not os.path.exists(current_path):
            current_path = os.path.join(os.path.abspath(''), 'CATIA')
    except BaseException as exc:
        current_path = os.path.join(os.path.abspath(''), 'CATIA')
        error_message = f'Неверно сохранены данные внутри config.txt или файл отсутсвует.\n'
        add_to_error_log(exc, error_message)
    return current_path


def save_path(last_path):
    current_path = os.path.join(os.path.abspath(''), 'data', 'config.txt')
    try:
        data = list()
        with open(current_path, 'r', encoding='UTF-8') as read_file:
            for line in read_file:
                data.append(line)
        with open(current_path, 'w', encoding='UTF-8') as write_file:
            write_file.writelines(data[:-1])
            new_path = ''.join(('path=', last_path))
            write_file.writelines(new_path)
    except BaseException as exc:
        error_message = f'Ошибка при попытке сохранить новый путь в файл config.txt.\n'
        add_to_error_log(exc, error_message)
    return data


def main(current_path):
    # Clear an error.log file before run main script
    mistakes_path = os.path.join(os.path.abspath(''), 'error.log')
    if os.path.exists(mistakes_path):
        os.remove(mistakes_path)

    # Load parametrs from data/config.txt
    data = get_data_from_config()
    if data and len(data) == 6:
        directory_name = (data[0], data[1])
        sub_directory_name = (data[2], data[3])
        one_file_name = data[4]

        # Create list of files and directories in work folder
        objects_in_folder = get_file_list(current_path)
        if objects_in_folder['nc']:
            create_directories(current_path, directory_name,
                               sub_directory_name)
            all_nc_files = list()
            tools = list()
            objects_in_folder['nc'] = make_correct_order(
                objects_in_folder['nc'])

            # for BUMOTEC nc files
            frame_num = 2
            for number, nc_file in enumerate(objects_in_folder['nc']):
                correct_file, nc_tool, frame_num = convert_to_normal_nc_file(
                    current_path, nc_file, frame_num)
                all_nc_files.append(correct_file)
                tools.append(nc_tool)
                add_multiple_bumotec_files(
                    current_path, directory_name[0], sub_directory_name[1], nc_file, correct_file)
            tools = set(tools)
            add_one_bumotec_files(
                current_path, directory_name[0], sub_directory_name[0], one_file_name, all_nc_files, tools)

            # for Macodell nc files
            for pos, element in enumerate(all_nc_files):
                all_nc_files[pos] = from_bumotec_to_macodell(element, pos + 2)
            for pos, block in enumerate(all_nc_files):
                nc_file_name = objects_in_folder['nc'][pos]
                add_multiple_macodell_files(
                    current_path, directory_name[1], sub_directory_name[1], block, nc_file_name)
            add_one_macodell_files(
                current_path, directory_name[1], sub_directory_name[0], one_file_name, all_nc_files, tools)

    # Check if error.log exist in work folder
    without_mistakes = 0
    if os.path.exists(mistakes_path):
        without_mistakes = 1
    return without_mistakes
