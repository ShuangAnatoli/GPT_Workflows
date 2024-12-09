import openai
from graphviz import Digraph
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate steps from OpenAI ChatCompletion API
def generate_steps(query):
    """
    Generate step-by-step instructions for a given query using OpenAI's ChatCompletion.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that breaks down tasks into clear, step-by-step instructions."},
                {"role": "user", "content": f"How to: {query}"}
            ]
        )
        # Extract the response content
        steps = response['choices'][0]['message']['content']
        return steps
    except Exception as e:
        return f"Error: {str(e)}"

# Function to create a flowchart
def create_flowchart(steps, output_path="flowchart"):
    """
    Create a flowchart from a list of steps.
    """
    graph = Digraph(format='png')
    graph.attr(rankdir='TB')
    # Add nodes and edges for each step
    for i, step in enumerate(steps, start=1):
        graph.node(str(i), step)

        if i > 1:
            graph.edge(str(i - 1), str(i))
    file_path = graph.render(output_path, cleanup=True)
    return file_path

# Helper function to process the query and create a flowchart
def process_query(query, output_path="flowchart"):
    """
    Process the query: Generate steps and create a flowchart.
    """
    steps_text = generate_steps(query)
    steps_list = [step.strip() for step in steps_text.split("\n") if step.strip()]
    flowchart_path = create_flowchart(steps_list, output_path)
    return flowchart_path
