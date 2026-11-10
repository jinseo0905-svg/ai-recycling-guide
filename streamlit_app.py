import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI 맞춤형 분리수거 안내", page_icon="♻️")
st.title("♻️ AI 맞춤형 분리수거 안내")
st.write("쓰레기 사진을 올리면 AI가 종류를 분석하고 올바른 분리배출 방법을 안내합니다.")

st.info("사진은 분석 요청에 사용되며, 실제 배출 방법은 거주 지역의 지자체 안내를 우선 확인하세요.")

uploaded_file = st.file_uploader(
    "분리배출할 물건의 사진을 올려주세요.",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file:
    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or "image/jpeg"
    st.image(image_bytes, caption="업로드한 사진", use_container_width=True)

    if st.button("AI로 분리배출 방법 확인하기", type="primary"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            prompt = """
            너는 한국의 분리배출 안내 도우미야.
            사진 속 물건을 확인하고 한국에서 일반적으로 적용되는 분리배출 방법을
            한국어로 쉽게 안내해 줘.
            다음 형식을 지켜 줘.
            1. 물건 이름과 추정 재질
            2. 분리배출 분류 (종이류, 플라스틱류, 비닐류, 유리병류, 캔·고철류,
               일반쓰레기, 음식물쓰레기, 전자제품 등)
            3. 배출 전 준비 방법 (내용물 비우기, 헹구기, 라벨 제거 등)
            4. 주의할 점
            사진만으로 확실하지 않으면 추측이라고 밝히고 추가 확인이 필요하다고 말해 줘.
            지역별 배출 기준이 다를 수 있으므로 지자체 안내를 확인하라고 덧붙여 줘.
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                ],
            )
            st.subheader("분석 결과")
            st.write(response.text or "분석 결과를 가져오지 못했습니다. 다시 시도해 주세요.")
        except KeyError:
            st.error("Gemini API 키가 설정되지 않았습니다. Streamlit 앱의 Secrets에 GEMINI_API_KEY를 추가해 주세요.")
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")

st.divider()
st.caption("※ AI 분석은 참고용입니다. 오염 정도와 복합재질 여부, 지역별 수거 기준에 따라 배출 방법이 달라질 수 있습니다.")
