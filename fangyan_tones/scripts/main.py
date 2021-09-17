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


def load_and_convert():
    user_input = input()
    print(filter_chinese_specific_punctuation(chars_to_pinyin(user_input, 1)))


if __name__ == "__main__":
    load_and_convert()