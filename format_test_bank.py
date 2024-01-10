import re

with open('.\\raw_data\\5000_question_testbank.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Replace all occurrences of '\n\n\n\n' with '\n\n Question:'
text = text.replace('\n\n\n\n', '\n\n Question:')

# Split the text into paragraphs
paragraphs = text.split('\n\n Question:')

# Remove paragraphs that contain the word "spam"
filtered_paragraphs = [p for p in paragraphs if 'your answer' not in p.lower()]

# Remove the explanation
for i, paragraph in enumerate(filtered_paragraphs):
    print("Original paragraph: ")
    print(paragraph)

    # Extract the correct answer
    correct_answer = re.search("Explanation\n.*\n", paragraph)
    answer_formatted = correct_answer.group()[12:-1]
    
    # Extract the choices and format them
    if '?' in paragraph:
        choices = re.search("\?\n.*\nExplanation", paragraph, re.DOTALL)
    elif ':' in paragraph:
        choices = re.search("\:\n.*\nExplanation", paragraph, re.DOTALL)
    print("choices: ", choices.group())
    choices_formatted = choices.group()[2:-12]
    choices_list = choices_formatted.split("\n")
    letter = 'A'

    for choice in choices_list: 
        print("choice: ", choice)
        choice_string = letter + ". " + choice
        print("choice_string: ", choice_string)
        filtered_paragraphs[i] = re.sub(re.escape(choice), choice_string, filtered_paragraphs[i])
        
        if answer_formatted == choice:
            answer_letter = letter
        
        letter = chr(ord(letter) + 1)
    
    # Remove the explanation and add the correct answer

    filtered_paragraphs[i] = filtered_paragraphs[i].split("Explanation")[0]
    filtered_paragraphs[i] = filtered_paragraphs[i] + "\n" + "Correct Answer: " + answer_letter

    
    print("Choices:")
    print(choices_list)

    print("New paragraph:")
    print(filtered_paragraphs[i])

    # break

# Join the remaining paragraphs back into a single string
filtered_text = '\n\n Question'.join(filtered_paragraphs)


with open('.\\processed_data\\text\\5000_question_testbank_processed.txt', 'w', encoding="utf-8") as f:
    f.write(filtered_text)
