# Monte Carlo Review Dashboard 배포용 파일

이 폴더는 `Streamlit Community Cloud` 배포 기준으로 정리되어 있습니다.

## 포함 파일
- `app.py` : 배포용 엔트리 파일
- `requirements.txt` : 파이썬 의존성

## 로컬 실행
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud 배포
1. 이 폴더 내용을 GitHub 새 저장소에 업로드합니다.
2. Streamlit Community Cloud에 GitHub 계정을 연결합니다.
3. `Create app`를 누릅니다.
4. Repository를 선택합니다.
5. Main file path에 `app.py`를 입력합니다.
6. Deploy를 누릅니다.

## 입력 파일
앱 실행 후 엑셀 파일을 업로드합니다.
필수 시트:
- `MC_v1`
- `MC_v2`

선택 시트:
- `Specs`

## 참고
회사 데이터는 외부 공개 배포 전에 보안 정책을 확인하세요.