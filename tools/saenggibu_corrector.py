# -*- coding: utf-8 -*-
"""
생기부 맞춤법·띄어쓰기 교정 프로그램
=====================================

동작 순서
  1순위) 생기부 필수 어휘 사전(saenggibu_dict.json) 기반 자동 치환  ← 항상 실행(오프라인)
  2순위) py-hanspell(네이버 맞춤법 검사기)로 맞춤법·띄어쓰기 교정   ← API 원활할 때만
         API 호출이 실패하면 1순위 사전 교정 결과만으로 마무리합니다.

설치(2순위 기능을 쓸 경우에만 필요)
  pip install git+https://github.com/ssut/py-hanspell.git

사용법
  python saenggibu_corrector.py 검사할파일.txt          # 파일 교정
  python saenggibu_corrector.py 검사할파일.txt -o 결과.txt
  python saenggibu_corrector.py                          # 직접 붙여넣기(Ctrl+Z → Enter)
  python saenggibu_corrector.py --dict 다른사전.json ... # 다른 사전 파일 지정

⚠️ 개인정보 주의
  hanspell 단계는 텍스트를 네이버 서버로 전송합니다. 실행 전 확인을 받으며,
  학생 실명 등 개인정보는 반드시 지운 뒤 사용하세요. 사전 치환 단계는
  완전히 로컬에서 동작하므로 외부 전송이 없습니다.
"""

import argparse
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DEFAULT_DICT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saenggibu_dict.json")


# ──────────────────────────────────────────────────────────────
# 1순위: 사전(JSON) 기반 자동 치환 — 오프라인, 항상 실행
# ──────────────────────────────────────────────────────────────
def load_dictionary(path):
    """생기부 필수 어휘 사전(JSON)을 읽어 {틀린표기: (교정, 설명)} 으로 정규화한다.

    값 형식은 두 가지를 지원한다.
      "틀린표기": "교정어"
      "틀린표기": {"교정": "...", "설명": "..."}
    """
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    dictionary = {}
    for wrong, value in raw.items():
        if wrong.startswith("_"):          # "_설명" 같은 메타 항목은 건너뜀
            continue
        if isinstance(value, str):
            dictionary[wrong] = (value, "사전 등록 교체 어휘입니다.")
        elif isinstance(value, dict) and "교정" in value:
            dictionary[wrong] = (value["교정"], value.get("설명", "사전 등록 교체 어휘입니다."))
    return dictionary


def apply_dictionary(text, dictionary):
    """사전과 비교해 단어를 자동 치환한다.

    반환: (교정된 텍스트, [(틀린표기, 교정, 설명, 횟수), ...])
    긴 표기를 먼저 치환해 '취야 계층'이 '취야'보다 우선 적용되게 한다.
    """
    corrections = []
    for wrong in sorted(dictionary.keys(), key=len, reverse=True):
        if wrong in text:
            right, reason = dictionary[wrong]
            count = text.count(wrong)
            text = text.replace(wrong, right)
            corrections.append((wrong, right, reason, count))
    return text, corrections


# ──────────────────────────────────────────────────────────────
# 2순위: py-hanspell 맞춤법·띄어쓰기 교정 — API 원활할 때만
# ──────────────────────────────────────────────────────────────
def correct_with_hanspell(text):
    """네이버 맞춤법 검사기로 교정한다. 실패하면 None을 반환해 사전 결과로 폴백."""
    try:
        from hanspell import spell_checker
    except ImportError:
        print("  · py-hanspell 미설치 → 사전 교정 결과만 사용합니다.")
        print("    (설치: pip install git+https://github.com/ssut/py-hanspell.git)")
        return None

    corrected_parts = []
    changes = []
    try:
        # API 제한(약 500자) 때문에 줄 단위로 묶어 나눠 보낸다.
        buf = ""
        chunks = []
        for line in text.split("\n"):
            if len(buf) + len(line) + 1 > 450:
                chunks.append(buf)
                buf = line
            else:
                buf = (buf + "\n" + line) if buf else line
        if buf:
            chunks.append(buf)

        for chunk in chunks:
            result = spell_checker.check(chunk)
            corrected_parts.append(result.checked)
            for wrong, right in result.words.items():
                if isinstance(right, str) and wrong != right:
                    changes.append((wrong, right))
        return "\n".join(corrected_parts), changes
    except Exception as e:
        print(f"  · 외부 API 호출 실패({type(e).__name__}: {e})")
        print("    → 네트워크/네이버 API 변경이 원인일 수 있습니다. 사전 교정 결과만 사용합니다.")
        return None


# ──────────────────────────────────────────────────────────────
# 실행부
# ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="생기부 맞춤법·띄어쓰기 교정(사전 우선, hanspell 보조)")
    parser.add_argument("input", nargs="?", help="교정할 텍스트 파일(생략 시 직접 입력)")
    parser.add_argument("-o", "--output", help="교정 결과를 저장할 파일")
    parser.add_argument("--dict", default=DEFAULT_DICT_PATH, help="어휘 사전 JSON 경로")
    parser.add_argument("--no-api", action="store_true", help="외부 API(hanspell) 단계 건너뛰기")
    args = parser.parse_args()

    # 입력 읽기
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    else:
        print("교정할 내용을 붙여넣고 [Ctrl+Z → Enter](macOS/Linux: Ctrl+D)를 누르세요:")
        text = sys.stdin.read()
    text = text.strip()
    if not text:
        print("입력이 비어 있습니다.")
        return

    # ── 1순위: 사전 치환 ──
    print("\n" + "=" * 62)
    print("① 생기부 필수 어휘 사전 교정 (오프라인)")
    print("=" * 62)
    try:
        dictionary = load_dictionary(args.dict)
        print(f"  사전 로드: {args.dict} ({len(dictionary)}개 항목)")
    except FileNotFoundError:
        print(f"  ⚠️ 사전 파일이 없습니다: {args.dict} → 사전 단계 건너뜀")
        dictionary = {}

    text, corrections = apply_dictionary(text, dictionary)
    if corrections:
        for wrong, right, reason, count in corrections:
            times = f" ({count}회)" if count > 1 else ""
            print(f"  ✏️  {wrong} → {right}{times}")
            print(f"      📖 이유: {reason}")
    else:
        print("  사전 등록 오타 없음")

    # ── 2순위: hanspell ──
    if not args.no_api:
        print("\n" + "=" * 62)
        print("② 네이버 맞춤법·띄어쓰기 검사 (⚠️ 텍스트 외부 전송)")
        print("=" * 62)
        try:
            ans = input("  실행할까요? 학생 이름 등 개인정보는 지웠나요? (y/N): ").strip().lower()
        except EOFError:
            ans = "n"
        if ans == "y":
            result = correct_with_hanspell(text)
            if result is not None:
                text, changes = result
                if changes:
                    for wrong, right in changes:
                        print(f"  ✏️  {wrong} → {right}")
                        print("      📖 이유: 네이버 맞춤법 검사기 교정 결과입니다.")
                else:
                    print("  추가 교정 사항 없음")
        else:
            print("  건너뜀 (사전 교정 결과만 사용)")

    # ── 결과 출력/저장 ──
    print("\n" + "=" * 62)
    print("✅ 최종 교정 결과")
    print("=" * 62)
    print(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n저장 완료: {args.output}")


if __name__ == "__main__":
    main()
