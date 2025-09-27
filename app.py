import streamlit as st
import pandas as pd
import numpy as np
import io

# Sets the app to use a wide layout for a more spacious feel.
st.set_page_config(layout="wide")

# --- Login Credentials ---
LOGIN_CREDENTIALS = {
    "ARMMACHAWASASADMIN": "Smart@123456",
    "MATOLASASADMIN": "Smart@123456",
    "MATOLARIOSASADMIN": "Smart@123456",
    "MAPUTOSASADMIN": "Smart@123456",
    "CHOUPALSASADMIN": "Smart@123456",
    "MACHAWASASADMIN": "Smart@123456",
    "ARMBEIRASASADMIN": "Smart@123456",
    "BEIRASASADMIN": "Smart@123456",
    "NAMPULASASADMIN": "Smart@123456",
    "CHEMOIOSASADMIN": "Smart@123456",
}

# --- Login Page Logic ---
def login_page():
    """Displays the login form and handles authentication."""
    st.title("Login to Catalogue")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Please log in to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Log In")

        if login_button:
            if username in LOGIN_CREDENTIALS and LOGIN_CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Check if user is authenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Main Application Logic ---
if st.session_state["authenticated"]:
    # --- Logout Button ---
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
    col1, col2 = st.tabs(["Parts", "Service"])
    with col1:
        # --- Main Application Layout ---
        st.title("Search Parts")
        st.markdown("---")
        
        # --- Data Loading ---
        try:
            # Use the raw GitHub URL for the CSV file.
            file_path = "https://raw.githubusercontent.com/shanidevani/Catalogue/refs/heads/main/M%20APPLICATIONS(FRAM%20ENG).csv"
            
            # Read the CSV file with 'latin-1' encoding and skip bad lines.
            df = pd.read_csv(file_path, encoding='latin-1', on_bad_lines='skip')

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

        # --- Initialize filtered DataFrame ---


        filtered_df = df.copy()
        tab1, tab2, tab3, tab4, tab5, tab6 = st.columns(6)

        # ------ short category Filter ------
        category_list = ['All'] + sorted(filtered_df['CAT'].dropna().unique())
        with tab1:
            if len(category_list) == 1:
                category = False
                st.markdown("""<span style="font-weight: bold; color: red;">Category not applicable</span>""" , unsafe_allow_html=True)
            else:
                category = st.selectbox("Select Category (CAT)", category_list)
        
        if category != 'All':
            filtered_df = filtered_df[filtered_df['CAT'] == category]

        
        # ------ category Filter ------
        category_name_list = ['All'] + sorted(filtered_df['CAT NAME (PT)'].dropna().unique())

        with tab2:
            if len(category_name_list) == 1:
                category_name = False
                st.markdown("""<span style="font-weight: bold; color: red;">Category not applicable</span>""" , unsafe_allow_html=True)
            else:
                category_name = st.selectbox("Select Category", category_name_list)
        
        if category_name != 'All':
            filtered_df = filtered_df[filtered_df['CAT NAME (PT)'] == category_name]
        
         # ------ engine Filter ------
        with tab3:
            frame_engine_search = st.text_input("Enter Frame No./Engine No.")
        
        if frame_engine_search:
            search_text = frame_engine_search.lower().strip()
            filtered_df = filtered_df[
                (filtered_df['FRAME'].astype(str).str.lower().str.contains(search_text, na=False)) |
                (filtered_df['ENGINE'].astype(str).str.lower().str.contains(search_text, na=False))
            ]

        # ------ Car Filter ------
        car_list = ["All"] + sorted(filtered_df['CAR'].dropna().unique())
        with tab4:
            if len(car_list)==1:
                selected_car = False
                st.markdown("""<span style="font-weight: bold; color: red;">Car is not applicable</span>""" , unsafe_allow_html=True)
            else:
                selected_car = st.selectbox("Select Car (CAR)", car_list)

        if selected_car != 'All' and selected_car != False:
            filtered_df = filtered_df[filtered_df['CAR'] == selected_car]
        
        # ------ Car model Filter ------
        model_list = ["All"] + sorted(filtered_df['MODEL.1'].dropna().unique())
        with tab5:
            if len(model_list)==1:
                selected_model = False
                st.markdown("""<span style="font-weight: bold; color: red;">Car Model is not applicable</span>""" , unsafe_allow_html=True)
            else:
                selected_model = st.selectbox("Select Model (MODEL)", model_list)

        if selected_model != 'All' and selected_model != False:
            filtered_df = filtered_df[filtered_df['MODEL.1'] == selected_model]

        # ------ model Year Filter ------
        all_years = sorted([int(y) for y in set(filtered_df['ANO DE I.'].dropna().unique()) | set(filtered_df['ANO FI.'].dropna().unique())])

        with tab6:
            if len(all_years) == 1:
                selected_year = False
                st.markdown("""<span style="font-weight: bold; color: red;">Year is not applicable</span>""" , unsafe_allow_html=True)
            else:    
                selected_year = st.selectbox("Select Year", ['All'] + all_years)
        
        if selected_year != 'All' and selected_year != False:
            filtered_df = filtered_df[
                (filtered_df['ANO DE I.'] <= selected_year) & 
                (filtered_df['ANO FI.'] >= selected_year)
            ]
        
       

        

        tab1, tab2, tab3, tab4, tab5, tab6 = st.columns(6)
        # ------ size Filter ------
        size_list = ['All'] + sorted(filtered_df['SIZE'].dropna().unique())

        with tab1:
            if len(size_list)==1:
                size = False
                st.markdown("""<span style="font-weight: bold; color: red;">Size not applicable</span>""" , unsafe_allow_html=True)
            else:
                size = st.selectbox("Select Size", size_list)

        if size != 'All' and size != False:
            filtered_df = filtered_df[filtered_df['SIZE'] == size]

        # ------ Front Rear Filter ------
        with tab2:
            front_rear_list = ["All"]
            if frame_engine_search == "":
                front_rear_list = front_rear_list + sorted(filtered_df['F/R'].dropna().unique())

            if len(front_rear_list)==1:
                front_rear = False
                st.markdown("""<span style="font-weight: bold; color: red;">F/R (Front/Rear) not applicable</span>""" , unsafe_allow_html=True)
            else:
                front_rear = st.selectbox("Select F/R (Front/Rear)", front_rear_list)
        
        if front_rear != "All" and front_rear != False:
            filtered_df = filtered_df[filtered_df['F/R'] == front_rear]

        
        # ------ Left Right Filter ------
        with tab3:
            left_right_list = ["All"]
            if frame_engine_search == "":
                left_right_list = left_right_list + sorted(filtered_df['L/R'].dropna().unique())

            if len(left_right_list) == 1:
                left_right = False
                st.markdown("""<span style="font-weight: bold; color: red;">L/R (Left/Right) not applicable</span>""" , unsafe_allow_html=True)
            else:
                left_right = st.selectbox("Select L/R (Left/Right)", left_right_list)
            
        if left_right != "All" and left_right != False:
            filtered_df = filtered_df[filtered_df['L/R'] == left_right]

        # ------ Upper Lover Filter ------
        with tab4:
            upper_lover_list = ["All"]
            if frame_engine_search == "":
                upper_lover_list = upper_lover_list + sorted(filtered_df['U/L'].dropna().unique())

            if len(upper_lover_list) == 1:
                upper_lower = False
                st.markdown("""<span style="font-weight: bold; color: red;">U/L (Upper/Lower) not applicable</span>""" , unsafe_allow_html=True)
            else:
                upper_lower = st.selectbox("Select U/L (Upper/Lower)", upper_lover_list)
        
        if upper_lower != "All" and upper_lower != False:
            filtered_df = filtered_df[filtered_df['U/L'] == upper_lower]

        # ------ In Out Filter ------
        with tab5:
            in_out_list = ["All"]
            if frame_engine_search == "":
                in_out_list = in_out_list + sorted(filtered_df['I/O'].dropna().unique())
            
            if len(in_out_list) == 1:
                in_out = False
                st.markdown("""<span style="font-weight: bold; color: red;">I/O (In/Out)) not applicable</span>""" , unsafe_allow_html=True)
            else:
                in_out = st.selectbox("Select I/O (In/Out))", in_out_list)
        
        if in_out != "All" and in_out != False:
            filtered_df = filtered_df[filtered_df['I/O'] == in_out]

        # ------ part Filter ------
        with tab6:
            if frame_engine_search!="":
                part_no_search = False
                st.markdown("""<span style="font-weight: bold; color: red;">Part no not applicable</span>""" , unsafe_allow_html=True)
            else:
                part_no_search = st.text_input("Search Part No.")

        if part_no_search:
            search_text = part_no_search.lower().strip()
            filtered_df = filtered_df[
                filtered_df['PART NO.'].astype(str).str.lower().str.contains(search_text, na=False)
            ]

        

        # Filter Group 3: Frame or Engine No.
        # with st.expander("Frame/Engine Search"):
        

        # Filter Group 4: Part No.
        # with st.expander("Part No. Search"):
        

        # --- Display Results ---
        if not filtered_df.empty:
            st.subheader("Filtered Part Numbers:")
            # st.dataframe(filtered_df[['PART NO.','CAT','SIZE','F/R','L/R','U/L','I/O','CAR','MODEL','ANO DE I.','ANO FI.']].reset_index(drop=True), hide_index=True)
            st.dataframe(filtered_df[['PART NO.']].reset_index(drop=True), hide_index=True)
            st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("No part numbers found with the selected filters.")
    with col2:
        # --- Data Loading (using st.cache_data for performance)
        @st.cache_data
        def load_data():
            """
            Loads the data from the raw CSV file on GitHub.
            """
            try:
                # Correct raw URL for the GitHub CSV file.
                # The URL was changed from the web page URL to the raw content URL.
                csv_url = "https://raw.githubusercontent.com/shanidevani/Catalogue/refs/heads/main/final%20service%20data.csv"
                df = pd.read_csv(csv_url)
                print(len(df))
                print(list(df))
                return df
            except Exception as e:
                st.error(f"Error loading data: {e}. Please ensure the URL is correct and the CSV is publicly accessible.")
                return pd.DataFrame() # Return empty DataFrame on error

        df = load_data()

        print(len(df))
        print(list(df))

        if not df.empty:
            # st.title(f"Welcome, {st.session_state['username']}!")
            st.header("Service Part Filter")
            st.write("Use the dropdowns below to filter the data.")

            # --- Filter Dropdowns with cascading logic
            tab1, tab2, tab3, tab4 = st.columns(4)
            
            # Step 1: Select Code Description
            with tab1:
                make_options = ['All'] + sorted(list(df['car name'].unique()))
                if len(make_options)==1:
                    selected_make = False
                    st.markdown("""<span style="font-weight: bold; color: red;">Make is not applicable</span>""" , unsafe_allow_html=True)
                else:
                    selected_make = st.selectbox("Select Make", make_options)

            # Create a filtered dataframe based on the first selection
            filtered_df_step1 = df.copy()

            if selected_make != 'All' and selected_make != False:
                filtered_df_step1 = filtered_df_step1[filtered_df_step1['car name'] == selected_make]
            
            with tab2:
                model_name_options = ['All'] + sorted(list(filtered_df_step1['model name'].unique()))
                
                if len(model_name_options)==1:
                    selected_model_name = False
                    st.markdown("""<span style="font-weight: bold; color: red;">Model is not applicable</span>""" , unsafe_allow_html=True)
                else:
                    selected_model_name = st.selectbox("Select Model Name", model_name_options)

            # Create a filtered dataframe based on the first selection
            if selected_model_name != 'All' and selected_model_name != False:
                filtered_df_step1 = filtered_df_step1[filtered_df_step1['model name'] == selected_model_name]
            
            with tab3:
                all_years = sorted([int(y) for y in set(filtered_df_step1['year start'].dropna().unique()) | set(filtered_df_step1['year end'].dropna().unique())])
                
                if len(all_years)==1:
                    selected_year = False
                    st.markdown("""<span style="font-weight: bold; color: red;">year is not applicable</span>""" , unsafe_allow_html=True)
                else:
                    selected_year = st.selectbox("Select Year", ['All'] + all_years)

            if selected_year != 'All' and selected_year != False:
                filtered_df_step1 = filtered_df_step1[
                    (filtered_df_step1['year start'] <= selected_year) & 
                    (filtered_df_step1['year end'] >= selected_year)
                ]
            
            # Step 2: Select Service (cascading from Code Description)
            with tab4:
                service_options = ['All'] + sorted(list(filtered_df_step1['service'].unique()))
                if len(service_options)==1:
                    selected_service = False
                    st.markdown("""<span style="font-weight: bold; color: red;">year is not applicable</span>""" , unsafe_allow_html=True)
                else:
                    selected_service = st.selectbox("Select Service", service_options)

            # Create a filtered dataframe based on the second selection
            if selected_service != 'All' and selected_service != False:
                filtered_df_step1 = filtered_df_step1[filtered_df_step1['service'] == selected_service]

            # --- Final Filter the DataFrame
            filtered_df = filtered_df_step1.copy()
            if selected_model_name != 'All':
                filtered_df = filtered_df[filtered_df['model name'] == selected_model_name]
            
            # --- Display the results
            st.subheader("Filtered Results")
            
            # Before conversion, fill any NaN values in 'price' with 0
            # Then, convert the 'price' column to an integer to remove decimals
            filtered_df['price'] = filtered_df['price'].fillna(0).round(0).astype(int)

            # Display the required columns
            display_columns = ['part code', 'price', 'duracao', 'description']
            st.dataframe(filtered_df[display_columns], use_container_width=True)

            st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown("---")
            # --- Logout button at the bottom of the page

else:

    login_page()

