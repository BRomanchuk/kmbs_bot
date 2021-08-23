# returns the list of all possible meanings of message
def get_all_message_variants(msg, list_of_programs_and_professors):
    list_of_message_variants = [get_program_from_abbreviation(msg, list_of_programs_and_professors ),
                                get_program_from_abbreviation(eng_ukr_keyboard(msg, '>'), list_of_programs_and_professors ), msg,
                                eng_ukr_keyboard(msg, '>'), eng_ukr_keyboard(msg, '<'), rus_to_ukr_keyboard(msg),
                                eng_ukr_keyboard(rus_to_ukr_keyboard(msg), '<'), eng_ukr_translit(msg, '<'),
                                eng_ukr_translit(msg, '>')]
    return list_of_message_variants


# converts word from eng to ukr keyboard or otherwise depending on direction of converting
def eng_ukr_keyboard(word, direction):

    # exception for CEO Development Program
    if 'сео' in word or 'seo' in word:
        return 'ceo development program'

    word = str.lower(word)

    eng_keyboard = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
    ukr_keyboard = "йцукенгшщзхъфівапролджєячсмитьбю.'"

    from_keyboard = ''
    to_keyboard = ''

    res_word = ''
    if direction == '>':
        from_keyboard = eng_keyboard
        to_keyboard = ukr_keyboard
    else:
        from_keyboard = ukr_keyboard
        to_keyboard = eng_keyboard

    for i in range(len(word)):
        # if character not in keyboard, return first word
        if word[i] not in from_keyboard:
            return word
        ind = from_keyboard.index(word[i])
        res_word = res_word + to_keyboard[ind]

    return res_word


# converts word written in russian keyboard into word written in ukrainian keyboard
def rus_to_ukr_keyboard(rus_word):
    rus_word = str.lower(rus_word)

    rus_unique = 'ъыэ'
    ukr_unique = 'їіє'

    ukr_word = ''
    for c in rus_word:
        if c in rus_unique:
            ukr_word = ukr_word + ukr_unique[rus_unique.index(c)]
        else:
            ukr_word = ukr_word + c

    return ukr_word


# converts word from eng to ukr transliteration or otherwise depending on direction of converting
def eng_ukr_translit(word_to_translit, direction='>'):
    word_to_translit = str.lower(word_to_translit)

    ukr_chars = 'абвґдезіклмнопрстуфх'
    eng_chars = 'abvgdeziklmnoprstufh'

    from_chars = ''
    to_chars = ''

    res_word = ''
    if direction == '>':
        from_chars = eng_chars
        to_chars = ukr_chars
    else:
        from_chars = ukr_chars
        to_chars = eng_chars

    for i in range(len(word_to_translit)):
        # if character not in char set, return first word
        if word_to_translit[i] not in from_chars:
            return word_to_translit
        ind = from_chars.index(word_to_translit[i])
        res_word = res_word + to_chars[ind]

    return res_word


# returns name of program based on its abbreviation
def get_program_from_abbreviation(abbreviation, programs_arr):
    abbr_arr = [''] * len(programs_arr)
    for i in range(len(programs_arr)):
        for word in str.split(programs_arr[i]):
            abbr_arr[i] += word[0]
        if str.lower(abbreviation) in str.lower(abbr_arr[i]):
            return programs_arr[i]
    return abbreviation
