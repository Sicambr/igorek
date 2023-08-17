import os


def get_number_after_letter(line, letter):
    numerals = '0123456789.-'
    number = letter
    for symbol in line.partition(letter)[2]:
        if symbol in numerals:
            number += symbol
        else:
            break
    return number


def create_normal_blocks(row_blocks):
    original_par = {
        'frame_num': 'N10',
        'tool_num': '',
        'angle_b': '',
        'angle_c': '',
        'speed': '',
        'operation_mes': '',
        'tool_mes': ''
    }
    if row_blocks[0][1].startswith('ON') and '(' in row_blocks[0][1]:
        original_par['operation_mes'] = '(' + \
            row_blocks[0][1].partition('(')[2]

    chaneged_blocks = list()
    allow_symbols = ('%', 'ON', "#", 'M', 'G', '(')
    frame_number = 10

    for pos, block in enumerate(row_blocks):
        count = 0
        if row_blocks[pos][0].startswith('(T'):
            original_par['tool_mes'] = row_blocks[pos][0]
        if row_blocks[pos][0].startswith('(N'):
            temp_message = '(' + " ".join(row_blocks[pos][0].split()[1:])
            original_par['operation_mes'] = temp_message
            original_par['tool_mes'] = row_blocks[pos][1]
        for pos_2, line in enumerate(block):
            if not line.startswith(allow_symbols):
                count += 1
            else:
                if line.startswith('M6T'):
                    original_par['tool_num'] = get_number_after_letter(
                        line, 'T')
                elif line.startswith('G201'):
                    original_par['angle_b'] = get_number_after_letter(
                        line, 'B')
                    if block[pos_2 - 1].startswith('G0C'):
                        original_par['angle_c'] = get_number_after_letter(
                            block[pos_2 - 1], 'C')
                elif line.startswith('M3S'):
                    original_par['speed'] = line
                    if block[pos_2 + 1].startswith('G0C'):
                        original_par['angle_c'] = get_number_after_letter(
                            block[pos_2 + 1], 'C')

        if count:
            print(original_par)
            frame_number += 10
            original_par['frame_num'] = ''.join(('N', str(frame_number), '\n'))
            chaneged_blocks.append(1)


def read_catia_file(path_to_folder, file_name):
    current_path = os.path.join(path_to_folder, file_name)
    blocks = None
    try:
        blocks = list()
        position = 0
        blocks.append(list())
        with open(current_path, 'r', encoding='utf-8') as file:
            for line in file:
                blocks[position].append(line)
                if line.startswith('M53'):
                    blocks.append(list())
                    position += 1
    except BaseException as exc:
        path_for_log = os.path.join(path_to_folder, 'error.log')
        with open(path_for_log, 'a', encoding='utf-8') as error_log:
            error_message = list()
            error_message.append(
                f'Обнаружена ошибка при попытке открыть файл {file_name}\n')
            error_message.append('{mistake}, {comment}\n'.format(
                mistake=type(exc), comment=exc))
            for element in error_message:
                error_log.write(element)
        if error_log and not error_log.closed:
            error_log.close()
    return blocks


def main():
    file_name = '111.NC'
    current_path = os.path.abspath('')
    row_blocks = read_catia_file(current_path, file_name)
    if row_blocks:
        create_normal_blocks(row_blocks[:])


main()
