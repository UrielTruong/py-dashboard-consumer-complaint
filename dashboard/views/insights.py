import streamlit as st


class InsightsView:

    def render(self, insights: list[dict]) -> None:
        if not insights:
            return
        cols = st.columns(2, gap="medium")
        for i, ins in enumerate(insights):
            with cols[i % 2]:
                tone = f" {ins['tone']}" if ins["tone"] else ""
                st.markdown(
                    f'<div class="insight{tone}">'
                    f'<div class="ins-tag">{ins["tag"]}</div>'
                    f'<h4>{ins["title"]}</h4>'
                    f'<p>{ins["body"]}</p></div>',
                    unsafe_allow_html=True)
