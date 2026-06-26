import streamlit as st
from datetime import datetime
from config import (APP_NAME, APP_VERSION, PAGE_TITLE,
                    PAGE_ICON, PAGE_LAYOUT)
from app.utils.file_handler import get_file_info, read_file_bytes
from app.core.extractor import extract_text
from app.core.preprocessor import preprocess_for_matching
from app.core.matcher import match_resume_to_job
from app.utils.report_generator import generate_report

import subprocess
import sys

@st.cache_resource
def load_spacy_model():
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run([sys.executable, "-m", "spacy",
                       "download", "en_core_web_sm"])
        import spacy
        return spacy.load("en_core_web_sm")

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)


def show_sidebar():
    with st.sidebar:
        st.title(f"{PAGE_ICON} {APP_NAME}")
        st.markdown(f"`Version {APP_VERSION}`")
        st.divider()
        st.markdown("### 📋 How to Use")
        st.markdown("""
        1. Upload your **Resume** (PDF)
        2. Upload **Job Description** (PDF/TXT)
        3. See your **Match Score**!
        4. Download your **PDF Report**!
        """)
        st.divider()
        st.markdown("### 🗺️ Project Phases")
        st.success("✅ Phase 1: Setup")
        st.success("✅ Phase 2: Extraction")
        st.success("✅ Phase 3: NLP Preprocessing")
        st.success("✅ Phase 4: Matching")
        st.success("✅ Phase 5: PDF Report")
        st.warning("🔄 Phase 6: BERT AI (Planned)")


def process_file(uploaded_file, file_label):
    file_info = get_file_info(uploaded_file)
    st.markdown(f"""
    **File:** `{file_info['name']}`
    **Size:** `{file_info['size_mb']} MB`
    **Type:** `{file_info['extension'].upper()}`
    """)
    if not file_info['is_valid']:
        st.error(file_info['message'])
        return None
    with st.spinner(f"📖 Extracting text from {file_label}..."):
        file_bytes = read_file_bytes(uploaded_file)
        result = extract_text(file_bytes, file_info['extension'])
    if not result['success']:
        st.error(f"❌ Error: {result['error']}")
        return None
    st.success(f"✅ Text extracted!")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("📝 Words", result['word_count'])
    with c2:
        st.metric("🔤 Characters", result['char_count'])
    with st.expander(f"👁️ View Raw Text — {file_label}"):
        st.text_area("", value=result['text'],
                     height=150, disabled=True)
    return result['text']


def show_match_score(result):
    st.markdown("---")
    st.markdown("## 🎯 Match Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Final Match Score",
                  f"{result['final_score']}%")
    with col2:
        st.metric("📊 TF-IDF Score",
                  f"{result['tfidf_score']}%")
    with col3:
        st.metric("🛠️ Skill Match Score",
                  f"{result['skill_score']}%")
    st.markdown("---")
    score = result['final_score']
    st.markdown(f"""
    <div style="
        background-color: {result['score_color']}22;
        border-left: 5px solid {result['score_color']};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    ">
        <h2 style="color: {result['score_color']}; margin:0;">
            {result['score_emoji']} {result['score_category']}
            — {result['final_score']}%
        </h2>
        <p style="font-size:16px; margin:8px 0 4px 0;">
            {result['score_message']}
        </p>
        <p style="font-size:14px; margin:0; opacity:0.8;">
            💡 {result['score_advice']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Match Score Breakdown")
    st.markdown("**Overall Match**")
    st.progress(min(int(score), 100) / 100)
    st.markdown(f"**TF-IDF Text Similarity** "
                f"— {result['tfidf_score']}%")
    st.progress(min(int(result['tfidf_score']), 100) / 100)
    st.markdown(f"**Skill Match** — {result['skill_score']}%")
    st.progress(min(int(result['skill_score']), 100) / 100)


def show_skills_analysis(result):
    st.markdown("---")
    st.markdown("## 🛠️ Skills Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Matching Skills",
                  result['total_matching'])
    with col2:
        st.metric("❌ Missing Skills",
                  result['total_missing'])
    with col3:
        st.metric("📋 Total Job Skills",
                  result['total_job_skills'])
    skill_col1, skill_col2 = st.columns(2)
    with skill_col1:
        st.markdown("### ✅ Matching Skills")
        if result['matching_skills']:
            for skill in result['matching_skills']:
                st.markdown(f"""
                <span style="
                    background-color:#00C85133;
                    border:1px solid #00C851;
                    padding:4px 12px;
                    border-radius:20px;
                    margin:3px;
                    display:inline-block;
                    font-size:14px;
                ">✅ {skill}</span>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching skills found!")
    with skill_col2:
        st.markdown("### ❌ Missing Skills")
        if result['missing_skills']:
            for skill in result['missing_skills']:
                st.markdown(f"""
                <span style="
                    background-color:#FF444433;
                    border:1px solid #FF4444;
                    padding:4px 12px;
                    border-radius:20px;
                    margin:3px;
                    display:inline-block;
                    font-size:14px;
                ">❌ {skill}</span>
                """, unsafe_allow_html=True)
        else:
            st.success("No missing skills! Perfect match!")
    if result['extra_skills']:
        st.markdown("### ⭐ Bonus Skills")
        bonus = "  ".join([f"`{s}`"
                           for s in result['extra_skills']])
        st.markdown(bonus)


def show_download_button(match_result,
                         resume_name, job_name):
    st.markdown("---")
    st.markdown("## 📥 Download Report")
    st.markdown(
        "Download a complete PDF report of your match analysis!"
    )
    with st.spinner("📄 Generating PDF report..."):
        pdf_bytes = generate_report(
            match_result,
            resume_filename=resume_name,
            job_filename=job_name
        )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resume_match_report_{timestamp}.pdf"
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )
    st.caption(
        f"Report will be saved as: `{filename}`"
    )


def main():
    show_sidebar()
    st.title(f"🎯 {APP_NAME}")
    st.markdown(
        "*AI-powered resume analysis and job matching*"
    )
    st.divider()
    st.markdown("### 📤 Upload Your Files")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📄 Resume")
        resume_file = st.file_uploader(
            "Upload your resume",
            type=["pdf"],
            key="resume_uploader"
        )
    with col2:
        st.markdown("### 💼 Job Description")
        job_file = st.file_uploader(
            "Upload job description",
            type=["pdf", "txt"],
            key="job_uploader"
        )
    st.divider()
    if resume_file and job_file:
        ext_col1, ext_col2 = st.columns(2)
        with ext_col1:
            st.markdown("### 📄 Resume")
            resume_text = process_file(
                resume_file, "Resume"
            )
        with ext_col2:
            st.markdown("### 💼 Job Description")
            job_text = process_file(
                job_file, "Job Description"
            )
        if resume_text and job_text:
            with st.spinner(
                "🧠 Running NLP preprocessing..."
            ):
                resume_nlp = preprocess_for_matching(
                    resume_text
                )
                job_nlp = preprocess_for_matching(job_text)
            st.success("✅ NLP Preprocessing complete!")
            with st.expander("🔍 View NLP Details"):
                n1, n2 = st.columns(2)
                with n1:
                    st.markdown("**Resume Keywords**")
                    st.markdown("  |  ".join([
                        f"`{k}`" for k in
                        resume_nlp.get('top_keywords', [])
                    ]))
                with n2:
                    st.markdown(
                        "**Job Description Keywords**"
                    )
                    st.markdown("  |  ".join([
                        f"`{k}`" for k in
                        job_nlp.get('top_keywords', [])
                    ]))
            with st.spinner(
                "🤖 Calculating match score..."
            ):
                match_result = match_resume_to_job(
                    resume_text, job_text
                )
            if match_result['success']:
                show_match_score(match_result)
                show_skills_analysis(match_result)
                show_download_button(
                    match_result,
                    resume_name=resume_file.name,
                    job_name=job_file.name
                )
                st.divider()
                st.balloons()
                st.success("""
                🎉 Analysis Complete!
                Download your PDF report above!
                Next → GitHub Setup!
                """)
            else:
                st.error(
                    f"❌ Error: {match_result['error']}"
                )
    elif not resume_file and not job_file:
        st.info(
            "👆 Upload both Resume and "
            "Job Description to begin!"
        )
    elif not resume_file:
        st.warning("⬆️ Please upload your Resume!")
    else:
        st.warning(
            "⬆️ Please upload the Job Description!"
        )


if __name__ == "__main__":
    main()