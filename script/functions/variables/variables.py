platform = 'r'  # 'r' - Revel, 'e' - Etext
revel = 1 if platform == 'r' else 0
excel_path = 'C:/work/Manza.xlsx' if revel else 'C:/work/Yukl.xlsx'  # Путь до excel-файла
username = 'manza2.5e.cqa.student10@mailinator.com' if revel else'bpetextqaV3'
password = 'Password1' if revel else 'EtextQA3'
course_name = 'Manza_031119_TSP' if revel else 'Leadership in Organizations'  # Название курса
chapter_number = 5  # Номер проверяемой главы
set_number = 1  # Номер сета
