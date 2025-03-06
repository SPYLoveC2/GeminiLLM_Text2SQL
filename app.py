import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import dotenv
import os
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  

# Define a prompt template for generating SQL from text
prompt_template = """
You are an AI assistant that translates natural language questions into SQL queries for the following database:

The database contains a table named `students` with the following columns:
- `id` (INTEGER PRIMARY KEY, AUTOINCREMENT)
- `name` (TEXT, NOT NULL)
- `class` (TEXT, NOT NULL)
- `subject` (TEXT, NOT NULL)
- `marks` (INTEGER)

Your task is to convert natural language questions into SQL queries. *Always generate a SQL query that is as simple and direct as possible*, based on the question.

### Example Queries:
1. "Show all students in the DataScience class."
   Output: SELECT * FROM students WHERE class = 'DataScience';

2. "Get all students who scored more than 80 in Mathematics."
   Output: SELECT * FROM students WHERE subject = 'Mathematics' AND marks > 80;

3. "What is the average marks of students in Physics?"
   Output: SELECT AVG(marks) FROM students WHERE subject = 'Physics';

4. "How many students are in the Art class?"
   Output: SELECT COUNT(*) FROM students WHERE class = 'Art';


{input_text}

"""

# Create a LangChain prompt template and LLM
prompt = PromptTemplate(input_variables=["input_text"], template=prompt_template)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GOOGLE_API_KEY
)
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit app
def main():
    st.title("Text to SQL Generator using LangChain and Gemini")
    
    st.markdown("""
    This app takes your natural language input and generates the equivalent SQL query using LangChain and Gemini.
    """)
    
    # Text input from the user
    input_text = st.text_area("Enter your request", height=150)
    
    if st.button("Generate SQL Query"):
        if input_text:
            # Generate SQL using LangChain with the chosen language model
            sql_query = chain.run(input_text)
            sql_query = sql_query.replace("```", "").replace("sql", "").replace("SQL", "")
            st.subheader("Generated SQL Query")
            st.code(sql_query, language='sql')
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            st.write(rows)
        else:
            st.warning("Please enter a valid input.")

if __name__ == "__main__":
    main()
