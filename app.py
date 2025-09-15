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
            file_path = "https://raw.githubusercontent.com/shanidevani/Search-Parts/main/M%20APPLICATIONS(FRAM%20ENG).csv"
            
            # Read the CSV file with 'latin-1' encoding and skip bad lines.
            df = pd.read_csv(file_path, encoding='latin-1', on_bad_lines='skip')

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

        # --- Initialize filtered DataFrame ---


        filtered_df = df.copy()
        tab1, tab2, tab3, tab4, tab5, tab6 = st.columns(6)
        
        # ------ engine Filter ------
        frame_engine_search = tab1.text_input("Enter Frame No./Engine No.")
        if frame_engine_search:
            search_text = frame_engine_search.lower().strip()
            filtered_df = filtered_df[
                (filtered_df['FRAME'].astype(str).str.lower().str.contains(search_text, na=False)) |
                (filtered_df['ENGINE'].astype(str).str.lower().str.contains(search_text, na=False))
            ]

        # ------ part Filter ------
        if frame_engine_search!="":
            part_no_search = False
            tab2.markdown("""<span style="font-weight: bold; color: red;">Part no not aplicable</span>""" , unsafe_allow_html=True)
        else:
            part_no_search = tab2.text_input("Search Part No.")

        if part_no_search:
            search_text = part_no_search.lower().strip()
            filtered_df = filtered_df[
                filtered_df['PART NO.'].astype(str).str.lower().str.contains(search_text, na=False)
            ]

        # ------ short category Filter ------
        if frame_engine_search!="":
            category = False
            tab3.markdown("""<span style="font-weight: bold; color: red;">Category not aplicable</span>""" , unsafe_allow_html=True)
        else:
            category = tab3.selectbox("Select Category (CAT)", ['All'] + sorted(filtered_df['CAT'].dropna().unique()))
        
        if category != 'All':
            filtered_df = filtered_df[filtered_df['CAT'] == category]

        
        # ------ category Filter ------
        if frame_engine_search!="":
            category_name = False
            tab4.markdown("""<span style="font-weight: bold; color: red;">Category not aplicable</span>""" , unsafe_allow_html=True)
        else:
            category_name = tab4.selectbox("Select Category", ['All'] + sorted(filtered_df['CAT NAME (PT)'].dropna().unique()))
        
        if category_name != 'All':
            filtered_df = filtered_df[filtered_df['CAT NAME (PT)'] == category_name]

        # ------ size Filter ------
        size_list = ['All'] + sorted(filtered_df['SIZE'].dropna().unique())
        if len(size_list)==1:
            size = False
            tab5.markdown("""<span style="font-weight: bold; color: red;">Size not aplicable</span>""" , unsafe_allow_html=True)
        else:
            size = tab5.selectbox("Select Size", size_list)

        if size != 'All' and size != False:
            filtered_df = filtered_df[filtered_df['SIZE'] == size]

        # ------ Front Rear Filter ------
        front_rear_list = ['All'] + sorted(filtered_df['F/R'].dropna().unique())
        if len(front_rear_list)==1:
            front_rear = False
            tab6.markdown("""<span style="font-weight: bold; color: red;">F/R (Front/Rear) not aplicable</span>""" , unsafe_allow_html=True)
        else:
            front_rear = tab6.selectbox("Select F/R (Front/Rear)", front_rear_list)
        
        if front_rear != "All" and front_rear != False:
            filtered_df = filtered_df[filtered_df['F/R'] == front_rear]

        tab1, tab2, tab3, tab4, tab5, tab6 = st.columns(6)
        # ------ Left Right Filter ------
        left_right_list = ['All'] + sorted(filtered_df['L/R'].dropna().unique())
        if len(left_right_list)>1:
            left_right = tab1.selectbox("Select L/R (Left/Right)", left_right_list)
        else:
            left_right = False
            tab1.markdown("""<span style="font-weight: bold; color: red;">L/R (Left/Right) not aplicable</span>""" , unsafe_allow_html=True)
        
        if left_right != "All" and left_right != False:
            filtered_df = filtered_df[filtered_df['L/R'] == left_right]

        # ------ Upper Lover Filter ------
        upper_lover_list = ['All'] + sorted(filtered_df['U/L'].dropna().unique())
        if len(upper_lover_list)>1:
            upper_lower = tab2.selectbox("Select U/L (Upper/Lower)", upper_lover_list)
        else:
            upper_lower = False
            tab2.markdown("""<span style="font-weight: bold; color: red;">U/L (Upper/Lower) not aplicable</span>""" , unsafe_allow_html=True)
        
        if upper_lower != "All" and upper_lower != False:
            filtered_df = filtered_df[filtered_df['U/L'] == upper_lower]

        # ------ In Out Filter ------
        in_out_list = ['All'] + sorted(filtered_df['I/O'].dropna().unique())
        if len(in_out_list)>1:
            in_out = tab3.selectbox("Select I/O (In/Out))", in_out_list)
        else:
            in_out = False
            tab3.markdown("""<span style="font-weight: bold; color: red;">I/O (In/Out)) not aplicable</span>""" , unsafe_allow_html=True)
        
        if in_out != "All" and in_out != False:
            filtered_df = filtered_df[filtered_df['I/O'] == in_out]

        # ------ Car Filter ------
        car_list = ['All'] + sorted(filtered_df['CAR'].dropna().unique())
        if len(car_list)==1:
            selected_car = False
            tab4.markdown("""<span style="font-weight: bold; color: red;">Car is not aplicable</span>""" , unsafe_allow_html=True)
        else:
            selected_car = tab4.selectbox("Select Car (CAR)", car_list)

        if selected_car != 'All' and selected_car != False:
            filtered_df = filtered_df[filtered_df['CAR'] == selected_car]

        # ------ Car model Filter ------
        
        model_list = ['All'] + sorted(filtered_df['MODEL.1'].dropna().unique())

        if len(model_list)==1:
            selected_model = False
            tab5.markdown("""<span style="font-weight: bold; color: red;">Car Model is not aplicable</span>""" , unsafe_allow_html=True)
        else:
            selected_model = tab5.selectbox("Select Model (MODEL)", model_list)

        if selected_model != 'All' and selected_model != False:
            filtered_df = filtered_df[filtered_df['MODEL.1'] == selected_model]

        # ------ model Year Filter ------
        all_years = sorted([int(y) for y in set(filtered_df['ANO DE I.'].dropna().unique()) | set(filtered_df['ANO FI.'].dropna().unique())])
        
        if len(all_years)>0:
            selected_year = tab6.selectbox("Select Year", ['All'] + all_years)
        else:
            selected_year = False
            tab6.markdown("""<span style="font-weight: bold; color: red;">Year is not aplicable</span>""" , unsafe_allow_html=True)
        
        if selected_year != 'All' and selected_year != False:
            filtered_df = filtered_df[
                (filtered_df['ANO DE I.'] <= selected_year) & 
                (filtered_df['ANO FI.'] >= selected_year)
            ]

        # Filter Group 3: Frame or Engine No.
        # with st.expander("Frame/Engine Search"):
        

        # Filter Group 4: Part No.
        # with st.expander("Part No. Search"):
        

        # --- Display Results ---
        if not filtered_df.empty:
            st.subheader("Filtered Part Numbers:")
            st.dataframe(filtered_df[['PART NO.','CAT','SIZE','F/R','L/R','U/L','I/O','CAR','MODEL','ANO DE I.','ANO FI.']].reset_index(drop=True), hide_index=True)
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
                csv_url = "https://raw.githubusercontent.com/shanidevani/service-price/main/final%20service%20data.csv"
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
                    st.markdown("""<span style="font-weight: bold; color: red;">Make is not aplicable</span>""" , unsafe_allow_html=True)
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
                    st.markdown("""<span style="font-weight: bold; color: red;">Model is not aplicable</span>""" , unsafe_allow_html=True)
                else:
                    selected_model_name = st.selectbox("Select Model Name", model_name_options)

            # Create a filtered dataframe based on the first selection
            if selected_model_name != 'All' and selected_model_name != False:
                filtered_df_step1 = filtered_df_step1[filtered_df_step1['model name'] == selected_model_name]
            
            with tab3:
                all_years = sorted([int(y) for y in set(filtered_df_step1['year start'].dropna().unique()) | set(filtered_df_step1['year end'].dropna().unique())])
                
                if len(all_years)==1:
                    selected_year = False
                    st.markdown("""<span style="font-weight: bold; color: red;">year is not aplicable</span>""" , unsafe_allow_html=True)
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
                    st.markdown("""<span style="font-weight: bold; color: red;">year is not aplicable</span>""" , unsafe_allow_html=True)
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

            st.markdown("---")
            # --- Logout button at the bottom of the page

else:
    login_page()