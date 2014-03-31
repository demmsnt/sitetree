#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Разные работы со строками"""

def jsonrus(s):
    """В json строке заменит все \u0422 символы их значениями
    """
    table = {'\u0410': 'А',
                '\u0411': 'Б',
                '\u0412': 'В',
                '\u0413': 'Г',
                '\u0414': 'Д',
                '\u0415': 'Е',
                '\u0416': 'Ж',
                '\u0417': 'З',
                '\u0418': 'И',
                '\u0419': 'Й',
                '\u041a': 'К',
                '\u041b': 'Л',
                '\u041c': 'М',
                '\u041d': 'Н',
                '\u041e': 'О',
                '\u041f': 'П',
                '\u0420': 'Р',
                '\u0421': 'С',
                '\u0422': 'Т',
                '\u0423': 'У',
                '\u0424': 'Ф',
                '\u0425': 'Х',
                '\u0426': 'Ц',
                '\u0427': 'Ч',
                '\u0428': 'Ш',
                '\u0429': 'Щ',
                '\u042a': 'Ъ',
                '\u042b': 'Ы',
                '\u042c': 'Ь',
                '\u042d': 'Э',
                '\u042e': 'Ю',
                '\u042f': 'Я',
                '\u0430': 'а',
                '\u0431': 'б',
                '\u0432': 'в',
                '\u0433': 'г',
                '\u0434': 'д',
                '\u0435': 'е',
                '\u0436': 'ж',
                '\u0437': 'з',
                '\u0438': 'и',
                '\u0439': 'й',
                '\u043a': 'к',
                '\u043b': 'л',
                '\u043c': 'м',
                '\u043d': 'н',
                '\u043e': 'о',
                '\u043f': 'п',
                '\u0440': 'р',
                '\u0441': 'с',
                '\u0442': 'т',
                '\u0443': 'у',
                '\u0444': 'ф',
                '\u0445': 'х',
                '\u0446': 'ц',
                '\u0447': 'ч',
                '\u0448': 'ш',
                '\u0449': 'щ',
                '\u044a': 'ъ',
                '\u044b': 'ы',
                '\u044c': 'ь',
                '\u044d': 'э',
                '\u044e': 'ю',
                '\u044f': 'я'}
    for k, v in table.items():
       s = s.replace(k,v)
    return s

jasonrus = jsonrus # tupo!
