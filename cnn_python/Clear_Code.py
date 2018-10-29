import re
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    """语法
    str.replace(old, new[, max])
    参数
    old -- 将被替换的子字符串。
    new -- 新字符串，用于替换old子字符串。
    max -- 可选字符串, 替换不超过 max 次"""
    """re.sub(pattern, repl, string, count=0, flags=0)
    pattern：表示正则表达式中的模式字符串；
    repl：被替换的字符串（既可以是字符串，也可以是函数）；
    string：要被处理的，要被替换的字符串；
    count：匹配的次数, 默认是全部替换
    flags：具体用处不详"""
    """三.strip()
    对于这个函数要记住3点：
    1. 默认删除行首或者行尾的空白符（包括'\n', '\r',  '\t',  ' ')
    2. 能使用，分隔去除多个值
    3.lstrip()表示删除左边的，rstrip()表示删除右边的"""

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
if __name__ == '__main__':
    s='dhteyu tyiu hgkyio;'
    print(clean_str(s))