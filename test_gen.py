import os
import requests
import time


API_KEY_ENV_VAR = "OPENAI_API_KEY"
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-3.5-turbo-16k"
NO_FILES_FOUND_MESSAGE = "No files found in the directory."
CHOOSE_FILE_MESSAGE = "Please choose a file from the list below:"
ENTER_FILE_NUMBER_MESSAGE = "Enter the number of the file: "
INVALID_NUMBER_MESSAGE = "Invalid number, please try again."
INVALID_INPUT_MESSAGE = "Invalid input, please enter a number."
RATE_LIMIT_EXCEEDED_MESSAGE = "Rate limit exceeded. Waiting {time} seconds to retry..."
HTTP_ERROR_MESSAGE = "HTTP Error: {error}"
REQUEST_FAILED_MESSAGE = "Request failed: {error}"
SAVE_OUTPUT_PROMPT = "Would you like to save the output to a file? (y/n): "
ENTER_OUTPUT_FILENAME_PROMPT = "Please enter the output file name: "
CONTENT_WRITTEN_MESSAGE = "Content successfully written to {file}"
DISPLAY_CONTENT_MESSAGE = "Here is the content:"
GENERATED_CONTENT_HEADER = "\nGenerated Content:"
SATISFIED_PROMPT = "Are you satisfied with the output? (y/n): "
ENHANCE_PROMPT_MESSAGE = "Please provide more details to enhance the prompt: "
ADDITIONAL_DETAILS = "\n additional details to the initial request: "
CONTENT_READ_SUCCESS_MESSAGE = "File content read successfully."
INITIAL_PROMPT_MESSAGE = "Generate unit tests code in the same compute language as an input for the given input code: \n{content}"
FILE_READ_FAILURE_MESSAGE = "Failed to read file: {error}"


def choose_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    if not files:
        print(NO_FILES_FOUND_MESSAGE)
        return None

    print(CHOOSE_FILE_MESSAGE)
    for index, file in enumerate(files):
        print(f"{index + 1}: {file}")

    file_index = 0
    while True:
        try:
            file_index = int(input(ENTER_FILE_NUMBER_MESSAGE)) - 1
            if 0 <= file_index < len(files):
                break
            else:
                print(INVALID_NUMBER_MESSAGE)
        except ValueError:
            print(INVALID_INPUT_MESSAGE)

    return files[file_index]


def query_chatgpt(prompt):
    api_key = os.getenv(API_KEY_ENV_VAR)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    max_retries = 5
    backoff_factor = 2

    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json=data)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:
                sleep_time = backoff_factor ** attempt
                print(RATE_LIMIT_EXCEEDED_MESSAGE.format(time=sleep_time))
                time.sleep(sleep_time)
            else:
                print(HTTP_ERROR_MESSAGE.format(error=err))
                break
        except requests.exceptions.RequestException as err:
            print(REQUEST_FAILED_MESSAGE.format(error=err))
            break

def save_output(content):
    save_output = input(SAVE_OUTPUT_PROMPT).strip().lower()
    if save_output == 'y':
        output_file = input(ENTER_OUTPUT_FILENAME_PROMPT)
        with open(output_file, 'w') as f:
            f.write(content)
            print(CONTENT_WRITTEN_MESSAGE.format(file=output_file))
    else:
        print(DISPLAY_CONTENT_MESSAGE)
        print(content)


def interact_and_process(initial_prompt):
    current_prompt = initial_prompt
    while True:
        result = query_chatgpt(current_prompt)
        if result:
            messages = result.get('choices', [{}])[0].get('message', {})
            content = messages.get('content', 'No response found.')
            print(GENERATED_CONTENT_HEADER)
            print(content)
            user_feedback = input(SATISFIED_PROMPT).strip().lower()
            if user_feedback == 'y':
                save_output(content)
                break
            else:
                additional_input = input(ENHANCE_PROMPT_MESSAGE)
                current_prompt += ADDITIONAL_DETAILS + additional_input


def main():
    chosen_file = choose_file()
    if chosen_file:
        print(f"You selected: {chosen_file}")
        try:
            with open(chosen_file, 'r') as file:
                content = file.read()
            print(CONTENT_READ_SUCCESS_MESSAGE)
            initial_prompt = INITIAL_PROMPT_MESSAGE.format(content=content)
            interact_and_process(initial_prompt)
        except Exception as e:
            print(FILE_READ_FAILURE_MESSAGE.format(error=e))


if __name__ == "__main__":
    main()
