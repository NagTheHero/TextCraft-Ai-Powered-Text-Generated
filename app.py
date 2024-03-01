import streamlit as st
from hugchat import hugchat
from hugchat.login import Login # Import Hugging Face login module

# App title
st.set_page_config(page_title="🤗💬 TextCraft")

# Page title
st.title('🤗💬 TextCraft')

# Check if Hugging Face credentials are provided as secrets
# If not, prompt user to enter them
if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        # Credentials already provided
        #st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
else:
        # Prompt for credentials
        hf_email = 'nagendra322003@gmail.com'
        hf_pass = 'Huggingface.co1'
        #if not (hf_email and hf_pass):
            #st.warning('Please enter your credentials!', icon='⚠️')
        #else:
            #st.success('Proceed to entering your prompt message!', icon='👉')
    
# Store chat history in session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display previous chat messages 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response from Hugging Face
def generate_response(prompt_input, email, passwd):

     # Login to Hugging Face
    sign = Login(email, passwd)
    cookies = sign.login()

    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    # Generate response
    return chatbot.chat(prompt_input)

# Get user input 
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user input
    with st.chat_message("user"):
        st.write(prompt)

# Check if last message was from assistant
if st.session_state.messages[-1]["role"] != "assistant":

    # Generate response 
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # Display response
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 

    # Add response to chat history  
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
