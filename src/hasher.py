import secrets
import streamlit_authenticator as stauth
print(secrets.token_hex(32))

# passwords = ['abc', 'def'] 
# hashed_passwords = stauth.Hasher().generate(passwords)
# print(hashed_passwords)