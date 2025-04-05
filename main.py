import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, get_stylist_response
from db_utils import init_db, verify_user, save_user, save_preferences, get_preferences

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="AI Personal Stylist",
    page_icon="👔",
    layout="centered",
)
# Sidebar navigation
with st.sidebar:
    selected = option_menu('AI Personal Stylist',
                          ['Login',
                           'Style Preferences',
                           'Style Assistant'],
                          menu_icon='person-circle', 
                          icons=['key-fill', 'sliders', 'chat-dots-fill'],
                          default_index=0
                          )
with st.sidebar:
    st.markdown('<h2>🤖 Chatbot</h2>', unsafe_allow_html=True)
    st.markdown('<p>Ask me for personalized fashion advice!</p>', unsafe_allow_html=True)

# Initialize session states
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Login Page
if selected == "Login":
    st.title("👋 Welcome to AI Personal Stylist")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")
    
    with col2:
        if st.button("Register"):
            save_user(username, password)
            st.success("Registration successful!")

# Style Preferences Page
elif selected == "Style Preferences":
    if not st.session_state.username:
        st.warning("Please login first")
    else:
        st.title("🎨 Your Style Preferences")
        
        # Load existing preferences
        existing_prefs = get_preferences(st.session_state.username)
        
        # Personal Information
        st.subheader("Personal Information")
        age = st.number_input("Age", 18, 100, 
                             value=existing_prefs['age'] if existing_prefs else 18)
        gender = st.selectbox("Gender", 
                            ["Male", "Female", "Non-binary"],
                            index=["Male", "Female", "Non-binary"].index(existing_prefs['gender']) 
                            if existing_prefs and existing_prefs['gender'] else 0)
        
        # Image Upload
        st.subheader("Your Photo")
        uploaded_image = st.file_uploader("Upload a full-length photo", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.image(uploaded_image, width=300)
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    f"uploads/{st.session_state.username}_photo.jpg")
            # Convert image to RGB before saving
            image = Image.open(uploaded_image)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(image_path)
        
        # Style Preferences
        st.subheader("Style Preferences")
        style_preferences = st.multiselect(
            "Preferred Style Categories",
            ["Casual", "Formal", "Bohemian", "Minimalist", "Streetwear"],
            default=existing_prefs['style_preferences'] if existing_prefs else []
        )
        
        favorite_colors = st.multiselect(
            "Favorite Colors",
            ["Black", "White", "Blue", "Red", "Green", "Yellow", "Purple", "Pink"],
            default=existing_prefs['favorite_colors'] if existing_prefs else []
        )
        
        if st.button("Save Preferences"):
            preferences = {
                "age": age,
                "gender": gender,
                "style_preferences": style_preferences,
                "favorite_colors": favorite_colors
            }
            save_preferences(st.session_state.username, preferences, 
                           image_path if uploaded_image else None)
            st.success("Preferences saved successfully!")

# Style Assistant Chat
elif selected == "Style Assistant":
    if not st.session_state.username:
        st.warning("Please login first")
    else:
        st.title("👔 Your Personal Style Assistant")
        
        # Get user preferences for context
        user_prefs = get_preferences(st.session_state.username)
        
        # Initialize chat
        if st.session_state.chat_session is None:
            model = load_gemini_pro_model()
            st.session_state.chat_session = model.start_chat(history=[])
        
        # Chat interface
        for message in st.session_state.chat_session.history:
            with st.chat_message("assistant" if message.role == "model" else "user"):
                st.markdown(message.parts[0].text)
        
        user_prompt = st.chat_input("Ask your style question...")
        
        if user_prompt:
            st.chat_message("user").markdown(user_prompt)
            
            # Create personalized context
            context = f"""As a personal stylist, consider these preferences:
            - Age: {user_prefs['age']}
            - Gender: {user_prefs['gender']}
            - Style preferences: {', '.join(user_prefs['style_preferences'])}
            - Favorite colors: {', '.join(user_prefs['favorite_colors'])}
            
            Question: {user_prompt}"""
            
            # Check if an image is provided in preferences
            image_path = user_prefs.get('image_path')
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                response = get_stylist_response(context, image)
            else:
                response = get_stylist_response(context)
            
            st.chat_message("assistant").markdown(response)
