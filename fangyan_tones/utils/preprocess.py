from typing import String
import re
punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.".decode("utf-8")

def filter_chinese_punctuation(sentence: String) -> String:
    """Strips punctuation from an chinese sentence using regex

    Parameters
    ----------
    sentence : String
        [description]

    Returns
    -------
    String
        [description]
    """
    # TODO, test this
    return re.sub(r"[%s]+" %punc, "", sentence.decode("utf-8"))
