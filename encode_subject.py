import base64

with open(r"C:\Users\admin\Downloads\2026_나이스_바이트_계산기(교과세특).xlsm", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

with open(r"c:\Users\admin\Desktop\생활기록부\template_subject.js", "w", encoding="utf-8") as f:
    f.write(f'const TEMPLATE_SUBJECT_B64 = "{b64}";\n')

print("Done")
