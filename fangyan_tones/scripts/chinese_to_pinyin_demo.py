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
    cleaned_input = filter_chinese_specific_punctuation(user_input)
    pinyin = chars_to_pinyin(cleaned_input, 2, as_list=False)
    print(pinyin)


if __name__ == "__main__":
    load_and_convert()