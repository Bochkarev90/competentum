from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .variables import xpath as x, variables as v
from script.functions.subfunctions import subfunctions as sub
from selenium.webdriver.common.action_chains import ActionChains
from . import excel
import time

chrome_options = Options()
chrome_options.add_argument("--lang=en-us")
driver = webdriver.Chrome(chrome_options=chrome_options)
chapter_list_excel = excel.chapter_list_return()
platform = 'https://revel.pearson.com/#/start' if v.revel else 'http://etext.pearson.com/eplayer/login'


def url_open():
    """
    Запускает сайт на платформе, указанной в переменных. Либо Etext (platform='e'), либо Revel (platform='r').
    """
    driver.get(platform)
    driver.maximize_window()


def login():
    """
    Берет логин и пароль из переменных и, используя их, логинится.
    """
    sub.wait_and_send_keys(driver, x.username_field, v.username)
    sub.wait_and_send_keys(driver, x.password_field, v.password)
    sub.wait_and_click(driver, x.main_button)


def course_choice():
    """
    Берет название курса из переменных и, используя его, выбирает и заходит в курс.
    """
    sub.wait(driver, x.course)
    time.sleep(1)
    sub.wait_and_click(driver, x.course)


def chapter_entry():
    """
    Получает полное название главы из excel.
    Ищет полученное название сначала на вкладке "Upcoming", если находит - заходит в главу,
    если не находит - переходит на вкладку "Past", ищет главу и заходит. Если не находит и там,
    значит уменьшает номер главы на единицу и снова ищет сначала в "Upcoming", затем в "Past".
    Записывает Due Date в словарь с ключом "due".
    """
    if v.revel:
        sub.wait(driver, x.wait_chapters)
        nested = 0  # Вложенность
        if sub.check_exists_by_xpath(driver, x.chapter_title):  # Если глава нашлась сразу в "Upcoming"
            sub.wait_and_click(driver, x.chapter_title)
        else:
            sub.wait_and_click(driver, x.past)
            if sub.check_exists_by_xpath(driver, x.chapter_title):  # Если глава нашлась сразу в "Past"
                sub.wait_and_click(driver, x.chapter_title)
            else:
                nested += 1  # Искомая глава вложена в предыдущую
                sub.wait_and_click(driver, '//span[@class="count"][1]')
                if sub.check_exists_by_xpath(driver, x.previous_chapter_title):
                    sub.wait_and_click(driver, x.previous_chapter_title)
                else:
                    sub.wait_and_click(driver, x.past)
                    sub.wait_and_click(driver, x.previous_chapter_title)
        due_date = sub.wait_and_pick_data(driver, x.due_date)
        due_date = "Due date: " + due_date[:due_date.find('\n')].capitalize() + ", " \
                   + due_date[due_date.find('\n')+1:] + "."
        chapter_list_excel['due'] = due_date
        chapter_list_excel['nested'] = nested
    else:
        sub.wait_and_click(driver, x.chapter_title)


def modules_list_compare():
    """
    Составляет список названий всех модулей. Также берет имена модулей из словаря.
    Печатает циклом каждое значение первого и второго списка и их соответствие друг другу (True, False).
    """
    page_modules_assignment = sub.wait_and_pick_data(driver, x.page_modules, True)
    excel_modules = chapter_list_excel['modules']
    if v.revel:
        nested = chapter_list_excel['nested']
        nesting = sub.chapter_nesting(page_modules_assignment)
        if not nested:
            chapter_title = sub.wait_and_pick_data(driver, x.chapter_title_pick)
            print("\n\nПроверка названия главы")
            print(chapter_title, chapter_list_excel['name'], chapter_list_excel['name'] == chapter_title)
        if nesting or nested:
            page_modules_assignment = nesting[1] if nested else nesting[0]
    print("\n\nПроверка названий модулей")
    if page_modules_assignment == excel_modules:
        print("Все верно!")
    else:
        n = 0
        for i in page_modules_assignment:
            print(i, excel_modules[n], i == excel_modules[n])
            n += 1
    chapter_list_excel['page_modules_assignment'] = page_modules_assignment


def module_titles_verification():
    """
    Заходит в каждый модуль и проверяет правильно ли привела ссылка, сравнивая названия.
    """
    print("\n\nПроверка корректности ссылок из Assignment")
    page_modules_assignment = chapter_list_excel['page_modules_assignment']
    # lo_on_pages = []
    url = driver.current_url
    for i in page_modules_assignment:
        sub.wait_and_click(driver, x.xpc('*', i[:i.find("'")]))
        time.sleep(1) if v.revel else time.sleep(4)
        page_title = sub.title_return(driver, v.revel, x.module_title, x.module_title_quiz)
        if i[0].isdigit():
            # if v.revel:
            #     lo = sub.wait_and_pick_data(driver, x.lo)
            #     lo_on_pages.append(lo)
            i = i[i.find(" ")+1:]
        if v.revel:
            driver.back()
        else:
            driver.get(url)
            sub.wait_and_click(driver, x.chapter_title)
        print(i, page_title, i == page_title)
        if i != page_title:
            print("\t", i.capitalize(), page_title.capitalize(), i.capitalize() == page_title.capitalize())
    # chapter_list_excel['lo'] = lo_on_pages


def click_through():
    """
    Заходит на первую сттраницу главы и проходит каждую страницу главы, собирая текст с кнопок "Back" и "Forward".
    Сравнивает с названиями открывающихся страниц и названиями из excel-файла.
    """
    print("\n\nПроверка порядка страниц")
    page_titles = chapter_list_excel['breaks']
    sub.wait_and_click(driver, x.page_modules)
    n = 1
    for i in range(len(page_titles)-1):
        driver.refresh()
        element = sub.wait(driver, x.forward)
        hover = ActionChains(driver).move_to_element(element)
        hover.perform()
        title_forward = sub.wait_and_pick_data(driver, x.forward)
        sub.wait_and_click(driver, x.forward)
        time.sleep(1)
        page_title = sub.title_return(driver, v.revel, x.module_title, x.module_title_quiz)
        print("\n" + title_forward, page_titles[n], title_forward == page_titles[n])
        if title_forward[0].isdigit:
            title_forward = title_forward[title_forward.find(" ")+1:]
        print(title_forward, page_title, title_forward == page_title)
        n += 1
    print("\n\nОбратно")
    for i in range(len(page_titles) - 1):
        driver.refresh()
        element = sub.wait(driver, x.back)
        hover = ActionChains(driver).move_to_element(element)
        hover.perform()
        title_back = sub.wait_and_pick_data(driver, x.back)
        sub.wait_and_click(driver, x.back)
        time.sleep(1)
        page_title = sub.title_return(driver, v.revel, x.module_title, x.module_title_quiz)
        if title_back[0].isdigit:
            title_back = title_back[title_back.find(" ") + 1:]
        print(title_back, page_title, title_back == page_title)


def logout():
    time.sleep(30)
    if v.revel:
        sub.wait_and_click(driver, x.account)
        sub.wait_and_click(driver, x.sign_out)
    driver.quit()


