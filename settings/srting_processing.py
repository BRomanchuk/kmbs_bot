def get_message_variants(msg, programs_and_staff):
    """
    returns the list of all possible meanings of message
    :param msg: str
    :param programs_and_staff: np.array
    :return: list
    """
    list_of_message_variants = [
        __get_program_from_abbreviation(msg, programs_and_staff),
        __get_program_from_abbreviation(__eng_ukr_keyboard(msg, '>'), programs_and_staff),
        msg,
        __eng_ukr_keyboard(msg, '>'),
        __eng_ukr_keyboard(msg, '<'),
        __rus_to_ukr_keyboard(msg),
        __eng_ukr_keyboard(__rus_to_ukr_keyboard(msg), '<'),
        __eng_ukr_transliteration(msg, '<'),
        __eng_ukr_transliteration(msg, '>')
    ]
    return list_of_message_variants


# converts word from eng to ukr keyboard or otherwise depending on direction of converting
def __eng_ukr_keyboard(word, direction):
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
def __rus_to_ukr_keyboard(rus_word):
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
def __eng_ukr_transliteration(word_to_transliterate, direction='>'):
    word_to_transliterate = str.lower(word_to_transliterate)

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

    for i in range(len(word_to_transliterate)):
        # if character not in char set, return first word
        if word_to_transliterate[i] not in from_chars:
            return word_to_transliterate
        ind = from_chars.index(word_to_transliterate[i])
        res_word = res_word + to_chars[ind]

    return res_word


# returns name of program based on its abbreviation
def __get_program_from_abbreviation(abbreviation, programs_arr):
    abbr_arr = [''] * len(programs_arr)
    for i in range(len(programs_arr)):
        for word in str.split(programs_arr[i]):
            abbr_arr[i] += word[0]
        if str.lower(abbreviation) in str.lower(abbr_arr[i]):
            return programs_arr[i]
    return abbreviation
