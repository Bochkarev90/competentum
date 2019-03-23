import xlrd


class Excel:
    all_chapters = {
        1: {},
        2: {}
    }

    def __init__(self, path: str):
        self._chapter_info_excel = {
            'chapter_name': '',
            'modules_names': [],
            'breaks_names': [],
            'lo': []
        }
        self._sheet = xlrd.open_workbook(path).sheet_by_index(0)

    def parser(self):
        """
        Собирает данные, все строки, кроме первой, первые 5 столбцов.
        """
        all_info = [self._sheet.row_values(rownum, 0, 5) for rownum in range(1, self._sheet.nrows)]
        return all_info

    def break_add(self, all_info, set_number, chapter_index):
        """
        Добавляет название ScreenBreak-а в массив 'breaks' переданных главы и сета.
        """
        break_title = all_info[0][2]
        self.all_chapters[set_number][chapter_index]['breaks'].append(break_title)

    def module_add(self, all_info, set_number, chapter_index):
        """
        Добавляет название модуля в массив 'modules' и 'breaks' переданных главы и сета.
        """
        module_title = all_info[0][1]
        lo = all_info[0][4]
        self.all_chapters[set_number][chapter_index]['modules'].append((module_title, lo))
        self.all_chapters[set_number][chapter_index]['breaks'].append(module_title)

    def chapter_add(self, all_info, set_number):
        """
        Создает индекс главы из названия главы (первое слово или цифра).
        Индекс становится ключом в общем словаре, по которому можно получить всю информацию о главе.
        Добавляет название главы в созданный словарь.
        """
        title = all_info[0][0]
        chapter_index = title if title.find(' ') == -1 else title[:title.find(' ')]
        if chapter_index.find(':') != -1:
            chapter_index = int(chapter_index[:chapter_index.find(':')])
        self.all_chapters[set_number][chapter_index] = {
            'name': all_info[0][0],
            'modules': [],
            'breaks': []
        }
        return chapter_index

    def dictionary_create(self):
        """
        Создает большой словарь с информацией обо всех главах в книге, разбитый по сетам и индексам глав.
        """
        set_number = 1
        chapter_index = ''
        all_info = self.parser()
        count = 0
        for i in all_info:
            if i[0]:
                if i[0][:i[0].find(' ')] in self.all_chapters[set_number]:
                    set_number = 2
                chapter_index = self.chapter_add(all_info[count:], set_number)
            elif i[1]:
                self.module_add(all_info[count:], set_number, chapter_index)
            elif i[2]:
                self.break_add(all_info[count:], set_number, chapter_index)
            elif i[3]:
                pass  # надо сделать, для проверки количества вопросов
            count += 1

    def chapter_info(self, chapter_index, set_number=1):
        """
        Возвращает информацию о переданной главе в переданном сете.
        """
        if not self.all_chapters[1]:
            self.dictionary_create()
        return self.all_chapters[set_number][chapter_index]


if __name__ == '__main__':
    print(Excel('C:/work/Edwards.xlsx').chapter_info(5, 1)['breaks'])
