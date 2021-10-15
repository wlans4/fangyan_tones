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

def create_table(line_endings):
    table = dict.fromkeys(['1', '2', '3', '4', 'Neutral', 'Total'], 0)
    for char in line_endings:
        # print(char)
        if char[-1].isdigit():
            table[char[-1]] += 1
        else:
            table['Neutral'] += 1
    table['Total'] = len(line_endings)
    return table

def load_and_convert():
    curPinyin = []
    line_endings = []
    while True:
        try:
            user_input = input()
            if user_input == "Analyze":
                print(create_table(line_endings))
            else:
                cleaned_input = filter_chinese_specific_punctuation(user_input)
                pinyin = chars_to_pinyin(cleaned_input, 2, as_list=True)
                curPinyin += pinyin
                if pinyin:
                    line_endings.append(pinyin[-1])
                # print(curPinyin)
                # print(line_endings)
        except EOFError:
            break

if __name__ == "__main__":
    load_and_convert()