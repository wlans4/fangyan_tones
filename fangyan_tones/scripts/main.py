from fangyan_tones.utils import (
    chars_to_pinyin,
    char_to_pinyin
)

from fangyan_tones.utils import (
    filter_chinese_specific_punctuation,
    filter_english_text,
    filter_general_punctuation,
    filter_all_non_chinese_text
)

def create_table():
    return 0

def load_and_convert():
    curInput = []
    while True:
        try:
            user_input = input()
            if user_input == "Analyze":
                create_table()
            else:
                curInput += chars_to_pinyin(user_input, 1)
                print(curInput)

        except EOFError:
            break

if __name__ == "__main__":
    load_and_convert()