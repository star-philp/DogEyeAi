import streamlit_authenticator as stauth

names = ['user1']
usernames = ['user1']
passwords = ['password1']

authenticator = stauth.Authenticate(names, usernames, passwords, 'my_cookie_name', 'my_signature_key', cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.write(f'Welcome {name}')