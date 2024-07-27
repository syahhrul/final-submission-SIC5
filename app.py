import pandas as pd
import streamlit as st

# Load the datasets
scholarships_file_path = 'scholarships_300.csv'  # Adjust the path as needed
users_file_path = 'users.csv'  # Path to the users data CSV

scholarships_df = pd.read_csv(scholarships_file_path)
users_df = pd.read_csv(users_file_path)

# Print the content of users_df for debugging purposes
# st.write("Data pengguna:")
# st.write(users_df)

# Function to get user details based on RFID
def get_user_details(rfid):
    user_details = users_df[users_df['rfid'].astype(str) == str(rfid)]
    if user_details.empty:
        return None
    else:
        return user_details.iloc[0]

# Function to get scholarship recommendations based on user input
def get_scholarship_recommendations(education_level, gpa, field_of_study, location):
    filtered_df = scholarships_df[
        (scholarships_df['education_level_required'] == education_level) &
        (scholarships_df['gpa_required'] <= gpa) &
        (scholarships_df['field_of_study_required'].str.contains(field_of_study, case=False, na=False)) &
        (scholarships_df['location_preference'].str.contains(location, case=False, na=False))
    ]
    
    if filtered_df.empty:
        return "Tidak ada rekomendasi beasiswa yang sesuai dengan kriteria Anda."
    else:
        recommendations = filtered_df[['scholarship_name', 'provider', 'amount']]#.to_string(index=False)
        return recommendations

# Streamlit interface
def main():
    st.title("Sistem Rekomendasi Beasiswa")
    st.write("Masukkan RFID Anda untuk mendapatkan rekomendasi beasiswa yang sesuai.")

    # User input
    rfid = st.text_input("RFID")

    if st.button("Dapatkan Rekomendasi"):
        user_details = get_user_details(rfid)
        if user_details is not None:
            education_level = user_details['education_level']
            gpa = user_details['gpa']
            field_of_study = user_details['field_of_study']
            location = user_details['location']
            
            st.write("Detail Pengguna:")
            st.write(f"Tingkat Pendidikan: {education_level}")
            st.write(f"IPK (GPA): {gpa}")
            st.write(f"Bidang Studi: {field_of_study}")
            st.write(f"Lokasi: {location}")
            
            recommendations = get_scholarship_recommendations(education_level, gpa, field_of_study, location)
            st.write("Rekomendasi Beasiswa:")
            st.write(recommendations)
        else:
            st.write("RFID tidak ditemukan. Silakan coba lagi.")

if __name__ == "__main__":
    main()
