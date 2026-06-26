from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from langchain_core.messages import HumanMessage, SystemMessage ,ToolMessage

MODEL="google_genai:gemini-3.1-flash-lite"
MAX_ITERATIONS=3

@tool
def get_item_price(item_name:str)->float:
    """This tool takes an item name as input and provides the price of the item as output."""
    print("Executing get_item_price tool with item_name:", item_name)
    price={"laptop":500, "phone":200,"headphones":50}
    return price.get(item_name, 0)

@tool
def get_discount_rate(price:float ,discount_tier:str)->float:
    """This tool takes an item price and a discount tier as input and provides the discount rate for the item as output."""
    print("Executing get_discount_rate tool with price:", price, "and discount_tier:", discount_tier)
    discount_percent={"silver":10,"gold":15,"bronze":5}
    discount= discount_percent.get(discount_tier,0)
    final_price= price * (1 - discount / 100)
    return final_price

def run_agent(question:str):
    print("Running agent with question:", question)
    tools=[get_discount_rate, get_item_price]
    tools_dict={tool.name: tool for tool in tools}
    llm= init_chat_model(MODEL, temperature=0)
    llm_with_tools=llm.bind_tools(tools)





    messages=[
        SystemMessage(
            content=(
                    "You are a helpful shopping assistant. "
                    "You have access to a product catalog tool "
                    "and a discount tool.\n\n"
                    "STRICT RULES — you must follow these exactly:\n"
                    "1. NEVER guess or assume any product price. "
                    "You MUST call get_product_price first to get the real price.\n"
                    "2. Only call apply_discount AFTER you have received "
                    "a price from get_product_price. Pass the exact price "
                    "returned by get_product_price — do NOT pass a made-up number.\n"
                    "3. NEVER calculate discounts yourself using math. "
                    "Always use the apply_discount tool.\n"
                    "4. If the user does not specify a discount tier, "
                    "ask them which tier to use — do NOT assume one."
            )
        ),
        HumanMessage(content= question),
        # ToolMessage(content=)
    ]
    for iteration in range(1,MAX_ITERATIONS+1):
        print(f"Iteration {iteration} of {MAX_ITERATIONS}")
        Ai_message=llm_with_tools.invoke(messages)
        tool_calls=Ai_message.tool_calls
        # print(Ai_message) 

        if not tool_calls:
            print(f"\nfinal answer: {Ai_message.content}")
            return Ai_message.content
        
        tool_call=tool_calls[0]
        tool_name=tool_call.get("name")
        tool_args=tool_call.get("args",{})
        tool_call_id=tool_call.get("id")
        print(f"calling tool with name {tool_name} and parameters :{tool_args}")
        tool= tools_dict.get(tool_name)

        tool_run=tool.invoke(tool_args)
        print(f"tool_result: {tool_run}")
        messages.append(Ai_message)
        messages.append(ToolMessage(content=str(tool_run),tool_call_id=tool_call_id))




if __name__=="__main__":
    question = "What is the final price of a laptop with a gold discount?"
    run_agent(question)

