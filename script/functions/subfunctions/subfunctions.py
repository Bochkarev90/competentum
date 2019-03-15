from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def check_exists_by_xpath(driver, xpath):
    """
    Принимает драйвер браузера и путь до элемента по xpath.
    Проверяет существует ли элемент на странице.
    Возвращает True или False.
    """
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def wait(driver, xpath):
    """
    Принимает драйвер браузера и путь до элемента по xpath.
    Ждет появления указанного элемента на странице.
    Возвращает элемент.
    """
    element = WebDriverWait(driver, 15).until(ec.visibility_of_element_located((By.XPATH, xpath)))
    return element


def wait_and_click(driver, xpath):
    """
    Принимает драйвер браузера и путь до элемента по xpath.
    Вызывает функцию ожидания появления элемента на странице и
    кликает по полученному элементу.
    """
    wait(driver, xpath).click()


def wait_and_send_keys(driver, xpath, keys):
    """
    Принимает драйвер браузера и путь до элемента по xpath.
    Вызывает функцию ожидания появления элемента на странице и
    передает значения полученному элементу.
    """
    wait(driver, xpath).send_keys(keys)


def wait_and_pick_data(driver, xpath, elements=False):
    """
    Принимает драйвер браузера, путь до элемента по xpath и сколько нужно элементов (один или несколько).
    Вызывает функцию ожидания появления первого искомого элемента на странице и, если нужен один, -
    возвращает текст этого элемента, если несколько - текст всех найденных элементов.
    """
    element = wait(driver, xpath)
    if elements:
        modules_list = driver.find_elements_by_xpath(xpath)
        return [i.text for i in modules_list]
    return element.text


def chapter_nesting(modules_list):
    """
    Принимает список модулей. Если есть вложенная глава возвращает список списков модулей, если нет - ноль.
    """
    introductions = 0
    splitted_list = [[], []]
    for i in modules_list:
        if i[:i.find(":")] == 'Introduction':
            introductions += 1
        splitted_list[introductions-1].append(i)
    return splitted_list if splitted_list[1] else False


def switch_f(driver):
    """
    Ждет фрейма и переключается в него. Если backwards = True - переключается обратно.
    """
    WebDriverWait(driver, 15).until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'contentIframe')))


def title_return(driver, revel, title, title_quiz):
    """
    Возвращает название главы со страницы.
    """
    page_title = ""
    if revel and check_exists_by_xpath(driver, title_quiz):
        page_title = wait_and_pick_data(driver, title_quiz)
        if page_title[:7] == "Chapter":
            page_title = page_title[:page_title.find(" ", 8) + 1] + "Quiz: " + page_title[page_title.find(" ", 8) + 1:]
    else:
        switch_f(driver)
        if check_exists_by_xpath(driver, title):
            page_title = wait_and_pick_data(driver, title)
            if page_title[:7] == "Chapter":
                page_title = "Introduction: " + page_title[page_title.find(" ", 8) + 1:]
    return page_title
