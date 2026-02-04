import streamlit as st
import os
from logic import analyze_batch, get_parameter_names, save_comprehensive_pdf, generate_proposal

# --- PAGE CONFIG ---
st.set_page_config(page_title="Water Quality Suite", page_icon="💧", layout="wide")

st.title("💧 Civil Engineering Water Suite (Web Edition)")

# --- TABS ---
tab1, tab2 = st.tabs(["Multi-Param Analysis", "Proposal Generator"])

# ==========================
# TAB 1: ANALYSIS
# ==========================
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Data")
        
        # Initialize session state for batch list
        if 'batch_list' not in st.session_state:
            st.session_state.batch_list = []
        
        # Initialize inputs if not set
        if 'input_param' not in st.session_state: st.session_state.input_param = get_parameter_names()[0]
        if 'input_val' not in st.session_state: st.session_state.input_val = 0.0

        # --- CALLBACKS ---
        def add_param_callback():
            p = st.session_state.input_param
            v = st.session_state.input_val
            
            # Check duplicate
            if any(x['name'] == p for x in st.session_state.batch_list):
                st.toast(f"⚠️ {p} is already in the list!", icon="⚠️")
            else:
                st.session_state.batch_list.append({"name": p, "value": v})
                st.toast(f"✅ Added {p}", icon="✅")
                # Reset value to 0.0
                st.session_state.input_val = 0.0

        def edit_param_callback(index):
            # 1. Get the item to edit
            item = st.session_state.batch_list[index]
            # 2. Push its values back into the input boxes
            st.session_state.input_param = item['name']
            st.session_state.input_val = item['value']
            # 3. Remove it from the list (so it doesn't duplicate)
            st.session_state.batch_list.pop(index)
            # Note: No need to call st.rerun(), callbacks trigger a rerun automatically

        def delete_param_callback(index):
            st.session_state.batch_list.pop(index)

        # --- INPUT FORM ---
        st.selectbox("Select Parameter", get_parameter_names(), key="input_param")
        st.number_input("Lab Value", step=0.1, key="input_val")
        
        st.button("Add to Batch", on_click=add_param_callback, type="primary")

        # --- LIST MANAGEMENT ---
        st.write("---")
        st.subheader("Current Batch")
        
        if st.session_state.batch_list:
            # Iterate in reverse to avoid index errors during deletion
            for i, item in reversed(list(enumerate(st.session_state.batch_list))):
                c1, c2, c3 = st.columns([3, 1, 1])
                
                c1.text(f"{item['name']}: {item['value']}")
                
                # EDIT BUTTON (Now uses on_click)
                c2.button("✏️", key=f"edit_{i}", on_click=edit_param_callback, args=(i,), help="Edit this item")

                # REMOVE BUTTON (Now uses on_click)
                c3.button("🗑️", key=f"del_{i}", on_click=delete_param_callback, args=(i,), help="Remove this item")
            
            if st.button("Clear All List"):
                st.session_state.batch_list = []
                st.rerun()
        else:
            st.info("No parameters added yet.")

    with col2:
        st.subheader("Results")
        if st.button("RUN ANALYSIS", type="primary"):
            if not st.session_state.batch_list:
                st.warning("Add parameters first!")
            else:
                gui_text, pdf_data = analyze_batch(st.session_state.batch_list)
                
                # Display results nicely
                for tag, text in gui_text:
                    if tag == "FAIL":
                        st.error(text)
                    elif tag == "PASS":
                        st.success(text)
                    elif tag == "INFO":
                        st.info(text)
                    elif tag == "SUBHEADER":
                        st.subheader(text)
                    elif tag == "HEADER":
                        st.title(text)
                    else:
                        st.text(text)
                
                # Generate PDF
                pdf_file = save_comprehensive_pdf(pdf_data)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📥 Download Report PDF",
                        data=f,
                        file_name="Water_Analysis_Report.pdf",
                        mime="application/pdf"
                    )

# ==========================
# TAB 2: PROPOSAL
# ==========================
with tab2:
    st.header("Project Proposal Wizard")
    
    with st.form("proposal_form"):
        c1, c2 = st.columns(2)
        with c1:
            prop_name = st.text_input("Project Name")
            prop_type = st.selectbox("Community Type", ["City (Geometric)", "Village (Arithmetic)"])
            prop_pop = st.number_input("Current Population", min_value=0, step=100)
        with c2:
            prop_rate = st.number_input("Growth Rate (%)", min_value=0.0, step=0.1)
            prop_source = st.selectbox("Water Source", ["River/Stream", "Groundwater (Borehole)", "Rainwater"])
            prop_years = st.number_input("Design Period (Years)", min_value=1, step=1)
            
        submitted_prop = st.form_submit_button("Generate Proposal PDF")

    if submitted_prop:
        if not prop_name or prop_pop == 0:
            st.error("Please fill in Project Name and Population.")
        else:
            inputs = {
                "name": prop_name,
                "type": prop_type,
                "pop_current": int(prop_pop),
                "growth_rate": prop_rate,
                "source": prop_source,
                "design_period": int(prop_years)
            }
            
            fname = generate_proposal(inputs)
            st.success("Proposal Generated!")
            
            with open(fname, "rb") as f:
                st.download_button(
                    label="📥 Download Proposal PDF",
                    data=f,
                    file_name=f"Proposal_{prop_name}.pdf",
                    mime="application/pdf"
                )