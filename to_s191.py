import os


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
        for line in row_blocks:
            print(line[0])


main()
