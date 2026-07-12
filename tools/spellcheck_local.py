# -*- coding: utf-8 -*-
"""
생기부 맞춤법 정밀 검사 도구 (로컬 실행용)
==========================================

웹 점검 시스템의 내장 사전이 잡지 못하는 오타까지 정밀 검사가 필요할 때
교사 PC에서 직접 실행하는 보조 도구입니다.

사용 라이브러리
  - py-hanspell   : 네이버 맞춤법 검사기 연동(설치: pip install git+https://github.com/ssut/py-hanspell.git)
  - pykospacing   : 띄어쓰기 교정(선택, 설치: pip install git+https://github.com/haven-jeon/PyKoSpacing.git)

⚠️ 개인정보 주의
  hanspell은 검사 텍스트를 네이버 서버로 전송합니다.
  학생 실명 등 개인정보가 포함된 문장은 이름을 지운 뒤 검사하세요.
  PyKoSpacing은 완전 로컬로 동작하므로 전송 걱정이 없습니다.

사용법
  python spellcheck_local.py 검사할파일.txt        # 파일 검사
  python spellcheck_local.py                       # 직접 입력(붙여넣기 후 Ctrl+Z, Enter)
"""

import sys
import io

# Windows 콘솔 한글 출력
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── 사전(Dictionary): 웹 시스템과 동일한 방식의 교체 단어 목록 ─────────
# 형식: "틀린표기": ("올바른표기", "수정 이유 설명")
# 여기에 항목을 추가하면 외부 전송 없이 로컬에서 우선 교정됩니다.
LOCAL_DICT = {
    "세스템": ("시스템", "'시스템(system)'의 오타입니다."),
    "비급혀": ("비급여", "'비급여(非給與)'의 오타입니다."),
    "취야 계층": ("취약 계층", "'취약(脆弱) 계층'의 오타입니다."),
    "역활": ("역할", "'역할'이 표준어입니다. ('역활'은 잘못된 표기)"),
    "합격율": ("합격률", "'ㄴ' 이외의 받침 뒤에는 '률'로 적습니다. (한글 맞춤법 제11항)"),
    "참여률": ("참여율", "받침이 없거나 'ㄴ' 받침 뒤에는 '율'로 적습니다. (한글 맞춤법 제11항)"),
    # 필요한 항목을 계속 추가하세요...
}


def check_local_dict(text):
    """로컬 사전 기반 검사: (틀린표기, 올바른표기, 이유) 목록 반환"""
    found = []
    for wrong, (right, reason) in LOCAL_DICT.items():
        if wrong in text:
            found.append((wrong, right, reason))
    return found


def check_hanspell(text):
    """네이버 맞춤법 검사(외부 전송). 실패 시 None."""
    try:
        from hanspell import spell_checker
    except ImportError:
        print("· py-hanspell 미설치 — 건너뜀 (설치: pip install git+https://github.com/ssut/py-hanspell.git)")
        return None
    try:
        results = []
        # 500자 단위로 잘라 검사(API 제한)
        for i in range(0, len(text), 500):
            chunk = text[i:i + 500]
            r = spell_checker.check(chunk)
            if r.errors:
                for wrong, right in r.words.items():
                    results.append((wrong, right))
        return results
    except Exception as e:
        print(f"· hanspell 검사 실패({e}) — 네이버 API 변경 시 발생할 수 있습니다.")
        return None


def check_spacing(text):
    """PyKoSpacing 띄어쓰기 교정(완전 로컬). 실패 시 None."""
    try:
        from pykospacing import Spacing
    except ImportError:
        print("· pykospacing 미설치 — 건너뜀 (설치: pip install git+https://github.com/haven-jeon/PyKoSpacing.git)")
        return None
    try:
        spacing = Spacing()
        return spacing(text.replace(" ", ""))
    except Exception as e:
        print(f"· 띄어쓰기 교정 실패({e})")
        return None


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            text = f.read()
    else:
        print("검사할 내용을 붙여넣고 [Ctrl+Z → Enter]를 누르세요:")
        text = sys.stdin.read()

    text = text.strip()
    if not text:
        print("입력이 비어 있습니다.")
        return

    print("\n" + "=" * 60)
    print("① 로컬 사전 검사 (외부 전송 없음)")
    print("=" * 60)
    local = check_local_dict(text)
    if local:
        for wrong, right, reason in local:
            print(f"  ✏️  {wrong} → {right}")
            print(f"      📖 이유: {reason}")
    else:
        print("  사전 등록 오타 없음")

    print("\n" + "=" * 60)
    print("② 네이버 맞춤법 검사 (⚠️ 텍스트가 외부로 전송됩니다)")
    print("=" * 60)
    ans = input("  실행할까요? 학생 이름 등 개인정보는 지웠나요? (y/N): ").strip().lower()
    if ans == "y":
        hs = check_hanspell(text)
        if hs:
            for wrong, right in hs:
                if wrong != right:
                    print(f"  ✏️  {wrong} → {right}")
        elif hs == []:
            print("  오류 없음")
    else:
        print("  건너뜀")

    print("\n" + "=" * 60)
    print("③ 띄어쓰기 교정 (PyKoSpacing, 완전 로컬)")
    print("=" * 60)
    sp = check_spacing(text)
    if sp:
        print("  교정 결과:")
        print("  " + sp)

    print("\n검사 완료.")


if __name__ == "__main__":
    main()
