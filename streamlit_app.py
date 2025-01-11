if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        # Get the corresponding SEARCH_ON value for the selected fruit
        if fruit_chosen in pd_df['FRUIT_NAME'].values:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            
            # Fetch and display nutrition information
            st.subheader(f"{fruit_chosen} Nutrition Information")
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            if smoothiefroot_response.status_code == 200:
                st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.error(f"Failed to fetch data for {fruit_chosen}.")
        else:
            st.error(f"Fruit '{fruit_chosen}' not found in the database.")
