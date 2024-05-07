# define a text_to_sql function which takes in the system prompt and the user's question and outputs the LLM-generated Ms-SQL query. Note that since we are using Groq API's JSON mode to format our output, we must indicate our expected JSON output format in either the system or user prompt.
def text_to_sql(client, system_prompt, user_question):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        # response_format = {"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )
    return completion.choices[0].message.content