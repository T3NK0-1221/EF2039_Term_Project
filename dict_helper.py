import os
from jamdict import Jamdict

def get_jamdict():
    # 1. directory setting
    base_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    
    # 2. declare data base file
    db_path = f"{base_path}/jamdict.db"
    
    # 3. load kanji dictionary
    try:
        jmd = Jamdict(db_file=db_path)
        return jmd
    except Exception as e:
        print(f"사전 연결 실패: {e}")
        return None

# test
if __name__ == "__main__":
    print("사전 연결 테스트 중...")
    jmd = get_jamdict()
    if jmd:
        print("✅ 연결 성공!")
        print(f"검색 예시 (羽織): {jmd.lookup('羽織').entries[0].senses[0]}")