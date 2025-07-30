import streamlit as st
import json
import re
from auditor import generate_audit_prompt, get_audit_response

st.set_page_config(page_title="AI Compliance Auditor", layout="centered")

st.title("🛡️ AI Compliance Auditor")
st.markdown("Analyze your content for cultural and ethical compliance across different regions and industries.")

with st.form("audit_form"):
    text = st.text_area("📝 Enter your content here", height=200, placeholder="Paste your marketing copy, ad, or message here...")
    industry = st.selectbox("🏢 Select Industry", ["general", "marketing", "technology", "education", "finance", "healthcare"])
    regions = st.multiselect("🌍 Target Regions", ["global", "pakistan", "india", "usa", "europe"], default=["global"])
    content_type = st.radio("📄 Content Type", ["text", "image", "video"], index=0)

    submitted = st.form_submit_button("🔍 Run Audit")

if submitted:
    with st.spinner("Analyzing content..."):
        prompt = generate_audit_prompt(text, industry, regions, content_type)
        raw_response = get_audit_response(prompt)

    # Show raw AI response for debugging
    st.text_area("📦 Raw AI Response", raw_response, height=250)

    # Clean the response in case it's wrapped in ```json or has extra whitespace
    cleaned_response = raw_response.strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = re.sub(r"```json\s*|\s*```", "", cleaned_response).strip()

    try:
        audit_result = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        st.error("❌ Failed to parse AI response as JSON.")
        st.exception(e)
        st.stop()

    st.success("✅ Audit Complete")

    st.subheader("🧠 Cultural Compliance Audit Result")
    st.markdown(f"**Compliance Status:** `{audit_result['compliance_status'].upper()}`")
    st.markdown(f"**Overall Risk Score:** `{audit_result['overall_risk_score']}`")
    st.markdown(f"**Confidence Level:** `{audit_result['confidence_level']}`")

    st.markdown("### ❌ Issues Found")
    if audit_result["issues"]:
        for issue in audit_result["issues"]:
            st.write(f"- {issue}")
    else:
        st.write("No major issues found.")

    st.markdown("### ✅ Positive Aspects")
    for pos in audit_result["positive_aspects"]:
        st.write(f"- {pos}")

    st.markdown("### 🛠 Suggestions")
    st.markdown("**Conservative Version:**")
    st.info(audit_result["alternative_suggestions"]["conservative_version"])

    st.markdown("**Inclusive Version:**")
    st.info(audit_result["alternative_suggestions"]["inclusive_version"])

    if "regional_adaptations" in audit_result["alternative_suggestions"]:
        st.markdown("**Regional Adaptations:**")
        for region, adaptation in audit_result["alternative_suggestions"]["regional_adaptations"].items():
            st.write(f"📍 **{region.capitalize()}**: {adaptation}")

    st.markdown("### 📌 Industry-Specific Notes")
    st.write(audit_result["industry_specific_notes"])

    st.markdown("### ⏱ Estimated Fix Time")
    st.write(audit_result["estimated_fix_time"])

    st.markdown("### 🚨 Priority Fixes")
    if audit_result["priority_fixes"]:
        for fix in audit_result["priority_fixes"]:
            st.write(f"- {fix}")
    else:
        st.write("No urgent fixes required.")
