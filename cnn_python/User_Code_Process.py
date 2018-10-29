import re
import os
def Code_Process(path):
    with open(path) as a:
        text= a.read()
    a.close()
    text1 = text.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    public_matched = re.findall(r'(.*public.*\(.*\).*)', text)  # 用于统计用public声明的方法
    # print(public_matched)
    private_matched = re.findall(r'(.*private.*\(.*\).*)', text)
    protected_matched = re.findall(r'(.*protected.*\(.*\).*)', text)
    everything_matched = re.findall(r'.*\(.*\).*{.*', text)
    print(everything_matched)
    new_everything_matched = []
    for key in everything_matched:
        if not re.match(r'(.*for \(.*\).*)', key):
            if not re.findall(r'(.*public.*\(.*\).*)', key):
                if not re.findall(r'(.*private.*\(.*\).*)', key):
                    if not re.findall(r'(.*protected.*\(.*\).*)', key):
                        if not re.findall(r'(.*class.*)', key):
                            if not re.findall(r'.*if.*\(.*\).*', key):
                                if not re.findall(r'(.*while \(.*\).*)', key):
                                    if not re.findall(r'(.*switch \(.*\).*)', key):
                                        if not re.findall(r'(.*foreach \(.*\).*)', key):
                                            if not re.findall(r'(.*else \(.*\).*)', key):
                                                if not re.findall(r'(.*=.*)', key):
                                                    # if not re.findall(r'(.*\..*)', key):
                                                    if not re.findall(r'(.*catch \(.*\).*)', key):
                                                        new_everything_matched.append(key)
    print(new_everything_matched)
    class_matched = re.findall(r'(.*class.*)', text)
    bracket_num = 0
    line_num = 0
    reader = open(path)
    line = reader.readline()
    word = path.split('\\')
    # print(word[-1])
    all_method_set = []  # 将所有的方法列出来
    class_list = []
    class_list.append('class' + ' ' + word[-1] + '{' + '\r\n')
    all_method_set.append(class_list)
    self_defined_method = []  # 用于自己构建方法，将所有的不属于方法中的内容全部放入此方法里面
    self_defined_method.append('public void self_Defined(){' + '\r\n')
    while line:
        line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
        if line1 in public_matched:  # 将所有的用public形式申明的方法保存下来
            print(line1)
            method_list = []  # 用于将整个方法保存下来
            # matched_num.append(line_num)
            if re.match(r'.*{.*', line1):
                method_list.append(line)
                number = 1
                while number > 0 and line:
                    line = reader.readline()
                    # print('-------------')
                    # print(line)
                    line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                    method_list.append(line)
                    if re.findall(r'.*{.*', line1):
                        number += 1
                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                        number += 1
                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                            r'.*{.*{.*{.*', line1):
                        number += 1
                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                            r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                        number += 1
                    if re.findall(r'.*}.*', line1):
                        number -= 1
                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                        number -= 1
                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                            r'.*}.*}.*}.*', line1):
                        number -= 1
                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                            r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                        number -= 1
                    if number < 0:
                        method_list.pop(-1)
                        break
                if number > 0:
                    for i in range(number):
                        method_list.append('}' + '\r\n')
                if number < 0:
                    method_list.append('}' + '\r\n')
            else:
                method_list.append(line)
                line = reader.readline()
                line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                if re.match(r'.*{.*', line1):
                    method_list.append(line)
                    number = 1
                    while number > 0 and line:
                        line = reader.readline()
                        # print('-------------')
                        # print(line)
                        line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                        method_list.append(line)
                        # if re.match(r'.*{.*', line1):
                        #     number += 1
                        # if re.match(r'.*}.*', line1):
                        #     number -= 1
                        if re.findall(r'.*{.*', line1):
                            number += 1
                        if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                            number += 1
                        if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                r'.*{.*{.*{.*', line1):
                            number += 1
                        if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                            number += 1
                        if re.findall(r'.*}.*', line1):
                            number -= 1
                        if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                            number -= 1
                        if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                r'.*}.*}.*}.*', line1):
                            number -= 1
                        if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                            number -= 1
                        if number < 0:
                            method_list.pop(-1)
                            break
                    if number > 0:
                        for i in range(number):
                            method_list.append('}' + '\r\n')
                    if number < 0:
                        method_list.append('}' + '\r\n')
            all_method_set.append(method_list)

        else:
            if line1 in protected_matched:  # 将所有用protected申明的方法保存下来
                # matched_num.append(line_num)
                if re.match(r'.*{.*', line1):
                    method_list = []  # 用于将整个方法保存下来
                    # matched_num.append(line_num)
                    if re.match(r'.*{.*', line1):
                        method_list.append(line)
                        number = 1
                        while number > 0 and line:
                            line = reader.readline()
                            # print(line)
                            line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                            method_list.append(line)
                            # if re.match(r'.*{.*', line1):
                            #     number += 1
                            # if re.match(r'.*}.*', line1):
                            #     number -= 1
                            if re.findall(r'.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                    r'.*{.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                    r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                    r'.*}.*}.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                    r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                number -= 1
                            if number < 0:
                                method_list.pop(-1)
                                break
                        if number > 0:
                            for i in range(number):
                                method_list.append('}' + '\r\n')
                        if number < 0:
                            method_list.append('}' + '\r\n')
                    all_method_set.append(method_list)
                else:
                    method_list.append(line)
                    line = reader.readline()
                    line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                    if re.match(r'.*{.*', line1):
                        method_list.append(line)
                        number = 1
                        while number > 0 and line:
                            line = reader.readline()
                            # print('-------------')
                            # print(line)
                            line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                            method_list.append(line)
                            # if re.match(r'.*{.*', line1):
                            #     number += 1
                            # if re.match(r'.*}.*', line1):
                            #     number -= 1
                            if re.findall(r'.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                    r'.*{.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                    r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                number += 1
                            if re.findall(r'.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                    r'.*}.*}.*}.*', line1):
                                number -= 1
                            if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                    r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                number -= 1
                            if number < 0:
                                method_list.pop(-1)
                                break
                        if number > 0:
                            for i in range(number):
                                method_list.append('}' + '\r\n')
                        if number < 0:
                            method_list.append('}' + '\r\n')
            else:
                if line1 in private_matched:  # 将所有的用private申明得出方法保存下来
                    # matched_num.append(line_num)
                    if re.match(r'.*{.*', line1):
                        method_list = []  # 用于将整个方法保存下来
                        # matched_num.append(line_num)
                        if re.match(r'.*{.*', line1):
                            method_list.append(line)
                            number = 1
                            while number > 0 and line:
                                line = reader.readline()
                                # print(line)
                                line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                                method_list.append(line)
                                # if re.match(r'.*{.*', line1):
                                #     number += 1
                                # if re.match(r'.*}.*', line1):
                                #     number -= 1
                                if re.findall(r'.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                        r'.*{.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                        r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                        r'.*}.*}.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                        r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                    number -= 1
                                if number < 0:
                                    method_list.pop(-1)
                                    break
                            if number > 0:
                                for i in range(number):
                                    method_list.append('}' + '\r\n')
                            if number < 0:
                                method_list.append('}' + '\r\n')
                        all_method_set.append(method_list)
                    else:
                        method_list.append(line)
                        line = reader.readline()
                        line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                        if re.match(r'.*{.*', line1):
                            method_list.append(line)
                            number = 1
                            while number > 0 and line:
                                line = reader.readline()
                                # print('-------------')
                                # print(line)
                                line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                                method_list.append(line)
                                if re.findall(r'.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                        r'.*{.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1) and re.findall(
                                        r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                    number += 1
                                if re.findall(r'.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                        r'.*}.*}.*}.*', line1):
                                    number -= 1
                                if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1) and re.findall(
                                        r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                    number -= 1
                                if number < 0:
                                    method_list.pop(-1)
                                    break
                            if number > 0:
                                for i in range(number):
                                    method_list.append('}' + '\r\n')
                            if number < 0:
                                method_list.append('}' + '\r\n')
                else:
                    if line1 in new_everything_matched:  # 将所有的用private申明得出方法保存下来
                        # matched_num.append(line_num)
                        if re.match(r'.*{.*', line1):
                            method_list = []  # 用于将整个方法保存下来
                            # matched_num.append(line_num)
                            if re.match(r'.*{.*', line1):
                                method_list.append(line)
                                number = 1
                                while number > 0 and line:
                                    line = reader.readline()
                                    # print(line)
                                    line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                                    method_list.append(line)
                                    if re.findall(r'.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*',
                                                                                  line1) and re.findall(
                                        r'.*{.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*',
                                                                                  line1) and re.findall(
                                        r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*',
                                                                                  line1) and re.findall(
                                        r'.*}.*}.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*',
                                                                                  line1) and re.findall(
                                        r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                        number -= 1
                                    if number < 0:
                                        method_list.pop(-1)
                                        break
                                if number > 0:
                                    for i in range(number):
                                        method_list.append('}' + '\r\n')
                                if number < 0:
                                    method_list.append('}' + '\r\n')
                            all_method_set.append(method_list)
                        else:
                            method_list.append(line)
                            line = reader.readline()
                            line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                            if re.match(r'.*{.*', line1):
                                method_list.append(line)
                                number = 1
                                while number > 0 and line:
                                    line = reader.readline()
                                    # print('-------------')
                                    # print(line)
                                    line1 = line.replace('\n', '').replace('\t', '').replace('\r', '')  # 去除一行中的回车换行
                                    method_list.append(line)
                                    if re.findall(r'.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*',
                                                                                  line1) and re.findall(
                                        r'.*{.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*{.*', line1) and re.findall(r'.*{.*{.*',
                                                                                  line1) and re.findall(
                                        r'.*{.*{.*{.*', line1) and re.findall(r'.*{.*{.*{.*{.*', line1):
                                        number += 1
                                    if re.findall(r'.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*',
                                                                                  line1) and re.findall(
                                        r'.*}.*}.*}.*', line1):
                                        number -= 1
                                    if re.findall(r'.*}.*', line1) and re.findall(r'.*}.*}.*',
                                                                                  line1) and re.findall(
                                        r'.*}.*}.*}.*', line1) and re.findall(r'.*}.*}.*}.*}.*', line1):
                                        number -= 1
                                    if number < 0:
                                        method_list.pop(-1)
                                        break
                                if number > 0:
                                    for i in range(number):
                                        method_list.append('}' + '\r\n')
                                if number < 0:
                                    method_list.append('}' + '\r\n')
                    else:
                        if not re.findall(r'(.*class.*)', line1):
                            self_defined_method.append(line)
                        line = reader.readline()

    self_defined_method.append('}')
    # all_method_set.append(self_defined_method)
    all_method_set.append('}')
    meth = ''
    for me in all_method_set:
        for k in me:
            meth += k
    # print(meth)
    file = open('F:/2018年暑假科研/CNN/my_clone/user_dataset/code.txt', 'w')
    file.write(meth)
if __name__ == '__main__':
    Code_Process("F:/2018年暑假科研/CNN/my_clone/origin_dataset/code.txt")