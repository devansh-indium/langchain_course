# from dotenv import load_dotenv
# import os
# load_dotenv()

# def main():
#     print("Hello, World!")
#     print(os.environ.get("GOOGLE_API_KEY"))

# if __name__ == "__main__":
#     main()    


from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
load_dotenv()
def main():
    Information = '''my name is devansh'''
    prompt_template='''here is the info about user{Information} answer the user query using this information '''
    final_template=PromptTemplate(
        input_variables=["Information"], template=prompt_template
    )
    llm= ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )
    chain=final_template|llm
    response= chain.invoke(input={"Information":Information})
    print(response)

if __name__ == "__main__":
    main()



# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0.5,
# )

# response = llm.invoke("Explain LangChain in one sentence.")

# print(response.content)








# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# load_dotenv()

# llm = ChatOpenAI(
#     model="adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic",
#     temperature=0.5,
# )

# response = llm.invoke("Give a Python Fizzbuzz solution in one line of code?")

# print(response.content)



# from openai import OpenAI

# client = OpenAI(
#     base_url="https://hermes.ai.unturf.com/v1",
#     api_key="choose-any-value"
# )

# response = client.chat.completions.create(
#     model="adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic",
#     messages=[{"role": "user", "content": "Hello"}]
# )

# print(response.choices[0].message.content)



# from openai import OpenAI

# client = OpenAI(base_url="https://hermes.ai.unturf.com/v1", api_key="choose-any-value")

# MODEL = "adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic"

# messages = [{"role": "user", "content": "Give a Python Fizzbuzz solution in one line of code?"}]

# response = client.chat.completions.create(
#     model=MODEL,
#     messages=messages,
#     temperature=0.5,
#     max_tokens=150
# )

# print(response.choices[0].message.content)