

import os
import openai


# In[7]:

##ADD a valid Key here
some_key = ""




# In[53]:


from openai import OpenAI
 







def generate_chat_completion(article_text, min_length=200, max_length=300, model="gpt-3.5-turbo", temperature=0.2, frequency_penalty=0.0):
    max_tokens = int(max_length / .75)
    # General assistant prompt for summarizing articles with dynamic word limits
    gpt_assistant_prompt = f"I am an AI trained to summarize articles across various topics. My summaries should be between {min_length} and {max_length} words. Below is an article that needs to be summarized."
    
    # Construct the user prompt with the article text
    gpt_user_prompt = f"Article: {article_text}"
    
    # Initialize the OpenAI client with your API key
    client = openai.OpenAI(api_key=some_key)  # Ensure this line is uncommented and correct
    
    # Construct the messages list
    messages = [
        {"role": "assistant", "content": gpt_assistant_prompt},
        {"role": "user", "content": gpt_user_prompt}
    ]
    
    # Generate the chat completion
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )
    
    # Extract the summary text from the response
    # Assuming the summary is in the last message from the assistant
    summary_text = response.choices[0].message.content #if response['choices'][0]['message'] else "No summary available."
    return summary_text






