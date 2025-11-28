import io

import streamlit as st
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

st.set_page_config(page_title="PyFilterBox", page_icon="📷")

st.title("📷 PyFilterBox")
st.caption("간단한 이미지 필터 박스 (그레이스케일 / 세피아 / 블러 / 샤픈 / 밝기 / 대비 / 엣지)")

FILTER_OPTIONS = [
    "원본",
    "그레이스케일",
    "세피아",
    "블러",
    "샤픈",
    "밝기 조절",
    "대비 조절",
    "엣지 감지",
    "흑백 + 고대비",
]


def apply_sepia(image: Image.Image) -> Image.Image:
    """세피아 필터"""
    gray = ImageOps.grayscale(image)
    sepia = Image.merge(
        "RGB",
        (
            gray.point(lambda p: int(p * 240 / 255)),
            gray.point(lambda p: int(p * 200 / 255)),
            gray.point(lambda p: int(p * 145 / 255)),
        ),
    )
    return sepia


def apply_filter(image: Image.Image, filter_name: str, intensity: float) -> Image.Image:
    """
    intensity: 0.0 ~ 1.0
    """
    if filter_name == "원본":
        return image

    if filter_name == "그레이스케일":
        return ImageOps.grayscale(image).convert("RGB")

    if filter_name == "세피아":
        return apply_sepia(image)

    if filter_name == "블러":
        # radius: 0.5 ~ 5.0
        radius = 0.5 + intensity * 4.5
        return image.filter(ImageFilter.GaussianBlur(radius))

    if filter_name == "샤픈":
        # factor: 0.5 ~ 2.5
        factor = 0.5 + intensity * 2.0
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    if filter_name == "밝기 조절":
        # factor: 0.5 ~ 2.5
        factor = 0.5 + intensity * 2.0
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    if filter_name == "대비 조절":
        # factor: 0.5 ~ 2.5
        factor = 0.5 + intensity * 2.0
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    if filter_name == "엣지 감지":
        return image.filter(ImageFilter.FIND_EDGES)

    if filter_name == "흑백 + 고대비":
        gray = ImageOps.grayscale(image)
        enhancer = ImageEnhance.Contrast(gray)
        high = enhancer.enhance(2.0 + intensity * 2.0)  # 2.0 ~ 4.0
        return high.convert("RGB")

    return image


def main():
    st.sidebar.header("⚙️ 설정")

    uploaded_file = st.sidebar.file_uploader(
        "이미지 업로드 (JPG/PNG)", type=["jpg", "jpeg", "png"]
    )

    filter_name = st.sidebar.selectbox("필터 선택", FILTER_OPTIONS, index=0)
    intensity = st.sidebar.slider("강도 (필터에 따라 다르게 적용)", 0.0, 1.0, 0.5, 0.1)

    if uploaded_file is None:
        st.info("왼쪽 사이드바에서 이미지 업로드")
        return

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("원본 이미지")
        st.image(image, use_column_width=True)

    filtered_image = apply_filter(image, filter_name, intensity)

    with col2:
        st.subheader(f"필터 적용: {filter_name}")
        st.image(filtered_image, use_column_width=True)

    st.write("---")

    buffer = io.BytesIO()
    filtered_image.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="📥 필터 적용 이미지 다운로드",
        data=buffer,
        file_name=f"filtered_{filter_name}.png",
        mime="image/png",
    )


if __name__ == "__main__":
    main()
