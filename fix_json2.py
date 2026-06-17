import sys
import io

path = r"c:\Users\admin\Desktop\생활기록부\생활기록부_점검사이트.html"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

new_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    if 5886 <= line_num <= 5974:
        if line_num == 5886:
            replacement = [
                '                  "number":  24,',
                '                  "name":  "최은성",',
                '                  "class":  8,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  25,',
                '                  "name":  "한태양",',
                '                  "class":  8,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  1,',
                '                  "name":  "김나경",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  2,',
                '                  "name":  "김도현",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  3,',
                '                  "name":  "김지민",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  4,',
                '                  "name":  "김지환",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  5,',
                '                  "name":  "박시우",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  6,',
                '                  "name":  "박시은",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  7,',
                '                  "name":  "배소연",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  8,',
                '                  "name":  "배영현",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  9,',
                '                  "name":  "백민유",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  10,',
                '                  "name":  "서희원",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  11,',
                '                  "name":  "안연후",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  12,',
                '                  "name":  "유제혁",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              },',
                '              {',
                '                  "number":  13,',
                '                  "name":  "유주성",',
                '                  "class":  9,',
                '                  "grade":  3',
                '              }'
            ]
            new_lines.extend(replacement)
        continue
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines) + '\n')

print("Fixed JSON successfully.")
