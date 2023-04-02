from typing import Tuple
from random import randint
from . import config

left_bracket = "（("
right_bracket = "）)"
digit_char = "1234567890"
symbol = "#+-"
min_char = "MIN劣势"
max_char = "MAX优势"
dice_char = "D"
valid_char = left_bracket + right_bracket + digit_char + symbol + min_char + max_char + dice_char

def eval_dice_exp(input_str: str) -> Tuple[int,str]:
    input_str = input_str.strip().upper().replace(" ","")
    if(len(input_str)) == 0:
        return (0, "")
    i = 0
    bracket_count = 0
    has_bracket = False
    try:
        while(i < len(input_str)):
            if input_str[i] in left_bracket:
                bracket_count += 1
                has_bracket = True
            elif input_str[i] in right_bracket:
                bracket_count -= 1
                has_bracket = True
            elif bracket_count == 0 and input_str[i] in symbol:
                left = input_str[:i]
                right = input_str[i+1:]
                if(len(left) == 0 or len(right) == 0):
                    raise Exception(f"参数错误：无效的表达式\n\t>> {input_str}")
                if(input_str[i] == "+"):
                    return add(left, right)
                elif(input_str[i] == "-"):
                    return minus(left, right)
                elif(input_str[i] == "#"):
                    return repeat(left, right)
            elif input_str[i] in valid_char:
                pass
            else:
                raise Exception(f"参数错误：无效字符 '{input_str[i]}'\n\t>> {input_str}")
            i += 1
        if(bracket_count != 0):
            raise Exception(f"参数错误：括号不匹配\n\t>> {input_str}")
        if(has_bracket):
            return bracket(input_str)
        return dice(input_str)
    except Exception as e:
        raise Exception(str(e))

def dice(a: str) -> Tuple[int,str]:
    digit_result = eval_digit(a)
    if digit_result[1] == len(a):
        return (digit_result[0], a)
    i = a.find(dice_char)
    if(i == -1):
        raise Exception(f"参数错误：无效的骰子\n\t>> {a}")
    left = a[:i]
    i2 = eval_digit(a, i+len(dice_char))[1]
    mid = a[i+len(dice_char):i2]
    right = a[i2:]
    if(len(left) == 0):
        left = "1"
    if(len(mid) == 0):
        mid = str(config.default_dice)
    count = digit(left)
    if(count < 1 or count > config.max_dice):
        raise Exception(f"参数错误：骰子数量必须为1-{config.max_dice}中的整数\n\t>> {count}")
    face = digit(mid)
    if(face < 1 or face > config.max_dice_size):
        raise Exception(f"参数错误：骰子面数必须为1-{config.max_dice_size}中的整数\n\t>> {face}")
    dice_select = combine_min_max(right)
    if(abs(dice_select) > config.max_dice_select):
        raise Exception(f"参数错误：骰子优劣势骰必须为0-{config.max_dice_select}中的整数\n\t>> {abs(dice_select)}")
    dice_str_result = ""
    show_full_process = count <= config.max_repeat
    if(show_full_process and count > 1):
        dice_str_result += "("
    dice_total_result = 0
    for i in range(count):
        if(dice_select == 0):
            dice_result = randint(1, face)
            dice_total_result += dice_result
            if(show_full_process):
                dice_str_result += str(dice_result)
                if(i != count-1):
                    dice_str_result += "+"                
        else:
            if(dice_select > 0):
                raw_result = [randint(1, face) for i in range(dice_select+1)]
                dice_result = max(raw_result)
                if(show_full_process):
                    if(len(raw_result) <= config.max_repeat):
                        dice_str_result += f"{dice_result}{{"
                        for j in range(len(raw_result)):
                            dice_str_result += str(raw_result[j])
                            if(j != len(raw_result)-1):
                                dice_str_result += ","
                        dice_str_result += "}"
                    else:
                        dice_str_result += str(dice_result)
                dice_total_result += dice_result
            else:
                raw_result = [randint(1, face) for i in range(-dice_select+1)]
                dice_result = min(raw_result)
                if(show_full_process):
                    if(len(raw_result) <= config.max_repeat):
                        dice_str_result += f"{dice_result}{{"
                        for j in range(len(raw_result)):
                            dice_str_result += str(raw_result[j])
                            if(j != len(raw_result)-1):
                                dice_str_result += ","
                        dice_str_result += "}"
                    else:
                        dice_str_result += str(dice_result)
                dice_total_result += dice_result
            if(show_full_process and i != count-1):
                dice_str_result += "+"
    if(show_full_process and count > 1):
        dice_str_result += ")"
    if(not show_full_process):
        dice_str_result += str(dice_total_result)
    return (dice_total_result, dice_str_result)

def bracket(a: str) -> Tuple[int,str]:
    result = eval_dice_exp(a[1:-1])
    return (result[0], "(" + result[1] + ")")

def add(a: str, b: str) -> Tuple[int,str]:
    left = eval_dice_exp(a)
    right = eval_dice_exp(b)
    return (left[0] + right[0], left[1] + "+" + right[1])

def minus(a: str, b: str) -> Tuple[int,str]:
    left = eval_dice_exp(a)
    right = eval_dice_exp(b)
    return (left[0] - right[0], left[1] + "-" + right[1])

def repeat(a: str, b: str) -> Tuple[int,str]:
    output_left = "{"
    output_right = "{"
    count = digit(a)
    total_result = 0
    for i in range(count):
        result = eval_dice_exp(b)
        total_result += result[0]
        output_left += result[1]
        output_right += str(result[0])
        if i != count - 1:
            output_left += ","
            output_right += ","
    output_left += "}"
    output_right += "}"
    total_result /= count
    total_result = round(total_result)
    if(count <= config.max_repeat):
        return (total_result, output_left + "=" + output_right)
    else:
        return (total_result, output_right)

def combine_min_max(a: str) -> int:
    i = 0
    count = 0
    while(i < len(a)):
        if(a.startswith("MIN",i)):
            select_result = eval_digit(a, i+3)
            i = select_result[1]
            count -= select_result[0] if select_result[0] != 0 else 1
        elif(a.startswith("MAX",i)):
            select_result = eval_digit(a, i+3)
            i = select_result[1]
            count += select_result[0] if select_result[0] != 0 else 1
        elif(a.startswith("优势")):
            select_result = eval_digit(a, i+2)
            i = select_result[1]
            count += select_result[0] if select_result[0] != 0 else 1
        elif(a.startswith("劣势")):
            select_result = eval_digit(a, i+2)
            i = select_result[1]
            count -= select_result[0] if select_result[0] != 0 else 1
        else:
            raise Exception(f"参数错误：无效的骰子保留方式\n\t>> {a}")
    return count

def eval_digit(a: str, start: int = 0) -> Tuple[int, int]:
    i = start
    while(i < len(a) and a[i] in digit_char):
        i += 1
    result = 0
    if(i != start):
        result = digit(a[start:i])
    return (result, i)

def digit(a: str) -> int:
    try:
        return int(a)
    except Exception:
        raise Exception(f"参数错误：无效的数字\n\t>> {a}")