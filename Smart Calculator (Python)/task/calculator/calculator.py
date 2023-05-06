from collections import deque
import re

inp = input()

available_operations = {'+', '-', '*', '(', ')', '/'}
not_doubled = ('*', '(', ')', '/')
first_level = ('+', '-')
second_level = ('*', '/')
store_of_var = {}


def right_var(var):
    if re.fullmatch(r'[a-zA-Z ]+=[ \d]+|[a-zA-Z ]+=[ a-zA-Z]+', var):
        return True

def creating_var(string):
    lst = [i.strip() for i in string.split('=') if not i.isspace()]
    if right_var(string):
        if lst[1].isalpha():
            return {lst[0]: store_of_var[lst[1]]}
        else:
            return {lst[0]: lst[1]}
    else:
        if any([i.isdigit() for i in lst[0]]) and lst[1].isdigit():
            return 'Invalid identifier'
        else:
            return 'Invalid assignment'

def inspection(symb):
    if symb.isdigit():
        return int(symb)
    elif store_of_var.get(symb):
        return int(store_of_var.get(symb))
    else:
        return None

def formating_of_expression(line):
    lst = list(i for i in line if not i.isspace())
    lst_output = []
    elem = []
    if line.count('(') == line.count(')'):
        for i in range(len(lst)):
            if (lst[i] not in available_operations and not any([j in available_operations for j in elem])) or (
                    lst[i] in first_level and lst[i] and any([j in first_level for j in elem])):
                elem += lst[i]
            elif lst[i] in available_operations and not any([j in available_operations for j in elem]) or lst[
                i] not in available_operations and any([j in available_operations for j in elem]):
                if any([j in available_operations for j in elem]):
                    if '-' in elem:
                        if len(elem) % 2:
                            elem = ['-']
                        else:
                            elem = ['+']
                    elif '+' in elem:
                        elem = ['+']
                if all([j not in not_doubled for j in elem]):
                    lst_output.append(''.join(elem.copy()))
                else:
                    lst_output.append(' '.join(elem.copy()))
                lst_output.append(' ')
                elem.clear()
                if lst[i] != ')':
                    elem.append(lst[i])
                else:
                    lst_output.append(lst[i])
            elif lst[i] in ('(', ')'):
                for e in elem:
                    lst_output.append(f'{e} ')
                    elem.clear()
                lst_output.append(f'{lst[i]} ')
            else:
                raise Exception()
        lst_output.append(''.join(elem.copy()))
        return ''.join(lst_output)
    else:
        raise Exception()

def to_postfix(string):
    stack = deque()
    lst = [i for i in string.split(' ') if not i.isspace() and i]
    stack_of_elem = deque()
    for i in range(len(lst)):
        if lst[i] not in available_operations:
            symbol = inspection(lst[i])
            if symbol:
                stack_of_elem.append(symbol)
            else:
                return 'Invalid expression'
        else:
            if lst[i] != ')' and ((lst[i] in first_level and not len(stack)) or (lst[i] in second_level and not len(stack)) or (lst[i] in second_level and stack[-1] in first_level) or (lst[i] == '(') or (stack[-1] == '(')):
                stack.append(lst[i])
            elif (lst[i] in second_level and stack[-1] in first_level) or (lst[i] in second_level and stack[-1] in second_level) or (lst[i] in first_level and stack[-1] in first_level):
                for j in range(len(stack)):
                    stack_of_elem.append(stack.pop())
                stack.append(lst[i])
            elif (lst[i] in second_level and stack[-1] in first_level) or (lst[i] in first_level and stack[-1] in second_level)  or (lst[i] in second_level and stack[-1] in second_level) or (lst[i] in first_level and stack[-1] in first_level):
                if stack.count('('):
                    while stack[-1] != '(':
                        stack_of_elem.append(stack.pop())
                else:
                    while stack:
                        stack_of_elem.append(stack.pop())
                    stack.append(lst[i])
            else:
                if lst[i] == ')':
                    while len(stack) and stack[-1] != '(':
                        stack_of_elem.append(stack.pop())
                    if len(stack):
                        stack.pop()
    while len(stack):
        stack_of_elem.append(stack.pop())
    return stack_of_elem

def from_postfix_to_result(deq):
    lst = []
    while len(deq) != 0:
        popped_elem = deq.popleft()
        if popped_elem not in available_operations:
            lst.append(popped_elem)
        else:
            second = str(lst.pop())
            try:
                first = str(lst.pop())
                lst.append(str(eval(first+popped_elem+second)))
            except:
                lst.append(str(eval(popped_elem+second)))
    try:
        return int(lst[0])
    except:
        return int(lst[0][:lst[0].index('.')])

while inp != '/exit':
    if inp.count('='):
        try:
            result = creating_var(inp)
            if isinstance(result, dict):
                store_of_var.update(result)
            else:
                print(result)
        except:
            print('Unknown variable')
    else:
        if not (inp in store_of_var.keys()):
            if inp and not re.fullmatch(r'\/\w+', inp):
                try:
                    print(from_postfix_to_result(to_postfix(formating_of_expression(inp))))
                except AttributeError:
                    print('Unknown variable')
                except:
                    print('Invalid expression')
            elif inp == '/help':
                print('The program calculates the sum, multiplication and integer division of numbers')
            elif re.fullmatch(r'\/\w+', inp) and inp not in ('/exit', '/help'):
                print('Unknown command')
        else:
            print(store_of_var[inp])
    inp = input()
print('Bye!')
