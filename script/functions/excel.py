from .variables import variables as v
import xlrd

workbook = v.excel_path
book = xlrd.open_workbook(workbook)  # Адрес книги
sheet = book.sheet_by_index(0)  # Указатель страницы
chapter_number = v.chapter_number
set_number = v.set_number
chapter_list = {}


def chapter_pos(chapter_num=chapter_number, section=set_number):
    """
    Возвращает номер строки Excel-файла, в которой написано название искомой главы.
    """
    chapters_list = sheet.col_values(0)
    chapters_list = [i.strip() for i in chapters_list]
    n = 1
    for i in chapters_list:
        if i[:i.find(':')] == str(chapter_num):
            if section == 1:
                return n
            section -= 1
        n += 1
    return False


def chapter_name():
    """
    Записывает полное название главы в словарь и возвращает это название с ключом "name".
    """
    name = sheet.cell_value(chapter_pos() - 1, 0)
    chapter_list['name'] = name
    return name


def previous_chapter_name():
    """
    Возвращает название главы, идущей перед искомой.
    Функция нужна в случае, если 2 главы в одном разделе.
    """
    previous_name = sheet.cell_value(chapter_pos(v.chapter_number-1) - 1, 0)
    chapter_list['previous_name'] = previous_name
    return previous_name


def modules_names(formatted=True):
    """
    Принимает необходимость форматирования массива (форматированный идет в основной скрипт,
    неотформатированный нужен для поиска Screen Breaks в функции screen_breaks_names).
    Записывает в словарь названия всех модулей вместе с соответствующими Learning Objectives
    с ключом "modules".
    """
    modules_list = sheet.col_values(1, chapter_pos(), chapter_pos(chapter_number+1))
    if not formatted:
        return modules_list
    modules_list_formatted = [i.strip() for i in modules_list if i]
    chapter_list['modules'] = modules_list_formatted


def screen_breaks_names(without_numbers=False):
    """
    Записывает полный список модулей и Screen Breaks в словарь с ключом "breaks"
    """
    screen_breaks_list = sheet.col_values(2, chapter_pos(),
                                          chapter_pos(chapter_number+1))
    modules_list = modules_names(False)
    screen_breaks_list_formatted = []
    n = 0
    for i in modules_list:
        screen_breaks_list_formatted.append(i) if i else screen_breaks_list_formatted.append(screen_breaks_list[n])
        n += 1
    screen_breaks_list_formatted = [i for i in screen_breaks_list_formatted if i and i[0] != 'q']
    if without_numbers:  # Надо сделать!
        pass
    chapter_list['breaks'] = screen_breaks_list_formatted


def lo_list():
    """
    Записывает список модулей с соответствующими Learning Objectives в словарь с ключом "lo"
    """
    learning_objectives = sheet.col_values(4, chapter_pos(), chapter_pos(chapter_number+1))
    modules_list = modules_names(False)
    n = 0
    for i in learning_objectives:
        if i:
            learning_objectives[n] = [modules_list[n], learning_objectives[n]]
        n += 1
    learning_objectives = [i for i in learning_objectives if i]
    chapter_list['lo'] = learning_objectives


def chapter_list_return():
    modules_names()
    chapter_name()
    previous_chapter_name()
    screen_breaks_names()
    lo_list()
    return chapter_list
