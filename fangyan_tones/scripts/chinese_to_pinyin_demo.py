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
from fangyan_tones.utils.table_generator import generate

def create_table(line_endings):
    table = dict.fromkeys(['1', '2', '3', '4', 'Neutral 1', 'Neutral 2', 'English', 'Falling Contours', 'Total'], 0)
    print(line_endings)
    for char in line_endings:
        # print(char)
        if char[-1].isdigit():
            table[char[-1]] += 1
        else:
            table['Neutral 1'] += 1
    table['Falling Contours'] = table['3'] + table['4'] + table['Neutral 1'] + table['English']
    table['Total'] = len(line_endings)
    return table

def load_and_convert():
    curPinyin = []
    line_endings = []
    # generate("", [])
    while True:
        try:
            user_input = input()
            if user_input[:7] == "Analyze":
                params = user_input[8:]
                # print(create_table(line_endings))
                table = create_table(line_endings)
                col_heads = []
                row = ["Count"]
                for (key, value) in table.items():
                    col_heads.append(key)
                    row.append(value)
                data = [
                    col_heads,
                    row
                ]
                generate(params, data)
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