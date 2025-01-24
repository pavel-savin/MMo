from django import template
import pymorphy3
import re


register = template.Library()

# Создаем экземпляр анализатора
morph = pymorphy3.MorphAnalyzer()

# Список слов для проверки
word_check = ["редиска", "помидор", "огурец"]

@register.filter(name='filter_words')
def filter_words(text): 
    # Проверка что данные строкового типа
    if not isinstance(text, str):
        raise TypeError(f"Ожидалась строка, получили {type(text).__name__}.")
    
    # Фильтр для замены форм слов из списка на *** в принимаемом тексте
    for base_word in word_check:
        parsed_forms = morph.parse(base_word)
        all_forms = set()

        # Получаем все формы слова
        for form in parsed_forms:
            all_forms.add(form.normal_form)
            all_forms.add(form.word)
            all_forms.update([gram.word for gram in form.lexeme])

        # Создаем регулярное выражение для поиска форм слова
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, all_forms)) + r')\b', re.IGNORECASE)

        # Функция замены
        def replace_match(match):
            word = match.group(0)
            return word[0] + '*' * (len(word) - 2) + word[-1] if len(word) > 1 else word

        # Заменяем все найденные слова в тексте
        text = pattern.sub(replace_match, text)
    
    return text
