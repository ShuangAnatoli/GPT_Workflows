import openai
import csv
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# CSV file to store conversation history
CSV_FILE = "conversation_history.csv"

# Load existing conversation history from CSV
def load_conversation_from_csv(file_path):
    conversation = []
    if os.path.isfile(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                conversation.append({"role": row["role"], "content": row["content"]})
    return conversation
def save_message_to_csv(file_path, message):
    # Predefine all possible keys based on the API structure
    fieldnames = ["role", "content", "refusal", "finish_reason", "usage"]

    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file is being created
        if not file_exists:
            writer.writeheader()

        # Write the message (only include predefined fields)
        filtered_message = {key: message.get(key, "") for key in fieldnames}
        writer.writerow(filtered_message)


# ChatGPT interaction
def chat_with_openai(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']
    return assistant_reply

# Main chat function
def main():
    # Load conversation history
    conversation = load_conversation_from_csv(CSV_FILE)
    if not conversation:
        # Start with a system message if no history exists
        conversation.append({"role": "system", "content": "You are a helpful assistant."})

    print("ChatGPT is ready! Type 'exit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user message to the conversation
        user_message = {"role": "user", "content": user_input}
        conversation.append(user_message)
        save_message_to_csv(CSV_FILE, user_message)

        # Get assistant's response
        assistant_message = chat_with_openai(conversation)
        conversation.append(assistant_message)
        save_message_to_csv(CSV_FILE, assistant_message)

        # Print assistant's response
        print(f"ChatGPT: {assistant_message['content']}")

# Run the program
if __name__ == "__main__":
    main()