import xlrd


class Excel:
    def __init__(self, path, start_of_name, set_number=1):
        self._name = str(start_of_name)
        self._set = int(set_number)
        self._sheet = xlrd.open_workbook(path).sheet_by_index(0)
        self._all_chapters_pos = {}
        self._chapter_info_excel = {
            'chapter_name': '',
            'modules_names': [],
            'breaks_names': [],
            'lo': []
        }

    def all_chapters_position(self):
        """
        Создает список всех глав в книге с номерами строк, по которым можно найти их названия.
        """
        chapters_list = self._sheet.col_values(0, 1)
        n = 0
        for i in chapters_list:
            if i:
                self._all_chapters_pos[i] = n
            n += 1
        # print(self._all_chapters_pos)

    # def chapter_pos(self):
    #     """
    #     Возвращает номер строки Excel-файла, в которой написано название искомой главы.
    #     """
    #     chapters_list = self.sheet.col_values(0)
    #     chapters_list = [i.strip() for i in chapters_list]
    #     n = 1
    #     for i in chapters_list:
    #         if i[:i.find(':')] == str(self.chapter_number):
    #             if self.set_number == 1:
    #                 return n
    #             self.set_number -= 1
    #         n += 1
    #     return False
    #
    def chapter_name(self):

        """
        Записывает полное название главы в словарь и возвращает это название с ключом "name".
        """
        self.all_chapters_position()
        for key in self._all_chapters_pos:
            print(self._all_chapters_pos[key])
            # key = key[:key.find(":")] if int(self._name) else key[:key.find(" ")]
            # print(key)
            # if key == self._name:
            #     self._chapter_info_excel['chapter_name'] = key
    #
    # def previous_chapter_name():
    #     """
    #     Возвращает название главы, идущей перед искомой.
    #     Функция нужна в случае, если 2 главы в одном разделе.
    #     """
    #     previous_name = sheet.cell_value(chapter_pos(v.chapter_number-1) - 1, 0)
    #     chapter_list['previous_name'] = previous_name
    #     return previous_name
    #
    # def modules_names(formatted=True):
    #     """
    #     Принимает необходимость форматирования массива (форматированный идет в основной скрипт,
    #     неотформатированный нужен для поиска Screen Breaks в функции screen_breaks_names).
    #     Записывает в словарь названия всех модулей вместе с соответствующими Learning Objectives
    #     с ключом "modules".
    #     """
    #     modules_list = sheet.col_values(1, chapter_pos(), chapter_pos(chapter_number+1))
    #     if not formatted:
    #         return modules_list
    #     modules_list_formatted = [i.strip() for i in modules_list if i]
    #     chapter_list['modules'] = modules_list_formatted
    #
    # def screen_breaks_names(without_numbers=False):
    #     """
    #     Записывает полный список модулей и Screen Breaks в словарь с ключом "breaks"
    #     """
    #     screen_breaks_list = sheet.col_values(2, chapter_pos(),
    #                                           chapter_pos(chapter_number+1))
    #     modules_list = modules_names(False)
    #     screen_breaks_list_formatted = []
    #     n = 0
    #     for i in modules_list:
    #         screen_breaks_list_formatted.append(i) if i else screen_breaks_list_formatted.append(screen_breaks_list[n])
    #         n += 1
    #     screen_breaks_list_formatted = [i for i in screen_breaks_list_formatted if i and i[0] != 'q']
    #     if without_numbers:  # Надо сделать!
    #         pass
    #     chapter_list['breaks'] = screen_breaks_list_formatted
    #
    # def lo_list():
    #     """
    #     Записывает список модулей с соответствующими Learning Objectives в словарь с ключом "lo"
    #     """
    #     learning_objectives = sheet.col_values(4, chapter_pos(), chapter_pos(chapter_number+1))
    #     modules_list = modules_names(False)
    #     n = 0
    #     for i in learning_objectives:
    #         if i:
    #             learning_objectives[n] = [modules_list[n], learning_objectives[n]]
    #         n += 1
    #     learning_objectives = [i for i in learning_objectives if i]
    #     chapter_list['lo'] = learning_objectives
    #

    def chapter_info(self):
        self.chapter_name()
        print(self._chapter_info_excel['chapter_name'])
        return self._chapter_info_excel


if __name__ == '__main__':
    Excel('C:/work/Edwards.xlsx', '1').chapter_info()
