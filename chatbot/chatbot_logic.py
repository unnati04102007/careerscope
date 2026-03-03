import random

def get_chat_response(message):
    msg = message.lower()
    
    if "hello" in msg or "hi" in msg:
        return "Hello! I am your CareerScope assistant. How can I help you today?"
        
    elif "career" in msg or "job" in msg:
        return "I can help you find suitable careers based on your interests. Have you taken the assessment quiz yet?"
        
    elif "college" in msg:
        return "You can explore top colleges in the 'Colleges' section. Do you have a specific location in mind?"
        
    elif "salary" in msg or "money" in msg:
        return "Salaries depend on the field. For example, Data Scientists earn avg 8-15 LPA, while CA starts around 7-10 LPA."
    
    else:
        return "I'm still learning! Please ask about careers, colleges, or subjects."
