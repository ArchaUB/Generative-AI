from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro")

#prompt
sys_template='''
You are a chatbot for a fictional pizzeria. You need to take orders from the customers based on the menu provided as {menu}
and a chat history provided as {chats}.
First you have to ask the customer only once'what would you like to order?'.
Based on the order, you need to sum the total amount and communicate it to the customer. 
If an item is not available, inform the customer that 'The item you have just ordered is not available in our menu' and ask them to choose from the available options.
You need to show the final amount.
Keep track of the conversation.
Use proper punctuations.
Use emoji.
'''

menu={
    "Main dish":{
		"pepperoni pizza" :[ 12.95, 10.00, 7.00] ,"cheese pizza" :  [10.95, 9.25, 6.50] ,"eggplant pizza"  : [11.95, 9.75, 6.75],"fries": [4.50, 3.50] ,"greek salad": 7.25
            },
	"Toppings":{
		"extra cheese": 2.00, 'mushrooms' :1.50 ,'sausage' :3.00 ,'canadian bacon': 3.50 ,"sauce" :1.50 ,"peppers": 1.00 ,
		       },
	"Drinks":{
		"coke": [3.00, 2.00, 1.00 ],
		"sprite": [3.00, 2.00, 1.00 ],
		"bottled water" :5.00 ,
		     }
}

Prompt=ChatPromptTemplate.from_messages(
    [
        ("system",sys_template),
        ("user","{item}")
    ]
)

out=StrOutputParser()
chain= Prompt | llm | out
chats=[]

while True:
    item=input("Customer :")
    if item=="Thanks":
        print("""You are welcome.Thank you for placing your orders""")
        break
    chats.append(HumanMessage(content=item))
    response=chain.invoke({"chats":chats,"menu":menu,"item":item})
    print("Chatbot :",response)
    chats.append(AIMessage(content=response))