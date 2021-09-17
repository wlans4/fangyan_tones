from typing import String

from pypinyin import pinyin as to_pinyin
from pypinyin import Style as style

tone_styles = [style.TONE, style.TONE2, style.TONE3]


def char_to_pinyin(char: String, tone_style: int) -> String:
    """Converts a single character to pinyin
    # TODO support heteronyms

    Parameters
    ----------
    char : String
        A single chinese character
    tone_style : int
        an integeter representing the tone style to use. 0 is "zhōng" 1 is "zho1ng", 2 is "xin1"

    Returns
    -------
    String
        The pinyin representing the single chinese character
    """
    # Is created as a list of lists, so return as just string
    pinyin = to_pinyin(char, style=tone_styles[tone_style], heteronyms=False)[0][0]

def chars_to_pinyin(chars: String, tone_style: int, as_list=True) -> List[String]:
    chars_list = to_pinyin(chars, style=tone_style)

    if as_list:
        return chars_list

    # Return as space separated sentence
    return chars_list.join(" ")