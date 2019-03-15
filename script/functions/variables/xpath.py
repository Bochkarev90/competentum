from . import variables as v
from .. import excel

chapter_list_excel = excel.chapter_list_return()


def xp(tag, attribute, value):
    """
    Принимает название тега, название аттрибута и значение этого аттрибута.
    Возвращает строку - путь xpath до искомого элемента на странице.
    """
    return "//" + tag + "[@" + attribute + "='" + value + "']"


def xpc(tag, value):
    """
    Принимает название тега и текст в этом теге.
    Возвращает строку - путь xpath до искомого элемента на странице.
    """
    return "//" + tag + "[contains(text(), '" + value + "')]"


# click or send_keys
username_field = xp('input', 'name', 'username') if v.revel else xp('input', 'name', 'loginname')
password_field = xp('input', 'name', 'password')
main_button = xp('button', 'type', 'submit')
course = xpc('h4', v.course_name) + "/following-sibling::div" if v.revel else xpc('span', v.course_name)
chapter_title = xpc('div', chapter_list_excel['name']) if v.revel else xpc('span', chapter_list_excel['name'])
previous_chapter_title = xpc('div', chapter_list_excel['previous_name'])
past = xpc('*', 'Past')
upcoming = xpc('*', 'Upcoming')
account = xpc('div', 'Student1')
sign_out = xpc('a', 'Sign out')

# wait
wait_chapters = xp('div', 'class', 'upcomingItems')

# pick data
due_date = xp('div', 'class', 'dateDisplay')
page_modules = xp('div', 'class', 'labelAndQuizContainer') + "/div[2]" if v.revel \
    else xp('a', 'aria-expanded', 'true') + "/following-sibling::ul" + xp('span', 'class', 'title')
chapter_title_pick = xp('div', 'class', 'title')
module_title = "//header"  # if v.revel else "//h1"
module_title_quiz = xp('div', 'class', 'assessmentTitle')
lo = "//ol/li/p"
forward = xp('div', 'class', 'nextPage') if v.revel else xp('div', 'class', 'navigation ') + "/div[3]//span"
back = xp('div', 'class', 'previousPage  ')
