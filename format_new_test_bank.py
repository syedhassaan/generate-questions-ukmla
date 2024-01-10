import re
import regex as regex
import hashlib

letter = 0

with open('new test bank.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Replace all occurrences of 'Custom session ...' with '\n\n Question:'
initial_text = "Custom session from .*:[0-9]+"
new_text = re.sub(initial_text, '\n\n Question:', text)

def format_answer(answer):
    answer_letter = answer.group()[-1]
    return "Correct Answer: " + answer_letter + "\n"

# Replace all occurrences of 'AnswerA' with 'Correct Answer: A'
answer = "\nAnswer[A-Z]+"
new_text_1 = re.sub(answer, format_answer, new_text)

# Split the text into paragraphs
paragraphs = new_text_1.split('\n\n Question:')
# paragraphs.remove("")

# From each paragraph remove all the text after 'Explanation:'
for i, paragraph in enumerate(paragraphs):
    paragraphs[i] = paragraph.split("Explanation:")[0]

#########################
def format_choice(answer):
    global letter
    letter+=1
    # print("format_answer::::::::::")
    # print(answer.group().rstrip("0123456789%"))
    char = ""
    if letter == 1:
        char = "A"
    elif letter == 2:
        char = "B"
    elif letter == 3:
        char = "C"
    elif letter == 4:
        char = "D"
    elif letter == 5:
        char = "E"
    elif letter == 6:
        char = "F"
    elif letter == 7:
        char = "G"
    elif letter == 8:
        char = "H"

    return char + ". " + answer.group().rstrip("0123456789%")
    
for i, paragraph in enumerate(paragraphs):
    #First check if there is an answer choice on the same line
    # print("paragraph: ", paragraph)
    answer_choice_same_line = "[.!?”…][A-Z0-9].*[a-zA-Z]\d+%\n|[.!?”…][A-Z]\d+%"
    answer_choice = regex.findall(answer_choice_same_line, paragraph, overlapped=True)
    # print("answer_choice:", answer_choice)

    if answer_choice:
        # format the answer choice
        answer_choice = answer_choice[-1][1:]
        paragraphs[i] = paragraph.replace(answer_choice, '\n' + answer_choice)
        # print("paragraphs["+str(i)+"]:", paragraphs[i])

    # Now remove the %
    answer_choice = "[A-Z0-9].*[a-zA-Z]\d+%|[A-Z]\d+%"
    paragraphs[i] = re.sub(answer_choice, format_choice, paragraphs[i])
    letter = 0
    # print("paragraphs["+str(i)+"]:", paragraphs[i])

# Join the remaining paragraphs back into a single string
filtered_text = 'Question\n'.join(paragraphs)

paragraphs = filtered_text.split('Question\n')
print("# of paragraphs: ", len(paragraphs))

dict_paragraphs = {}

for paragraph in paragraphs:
    hash_object = hashlib.sha256(paragraph.encode())
    hex_dig = hash_object.hexdigest()
    
    dict_paragraphs[hex_dig] = paragraph

print("# of unique paragraphs: ", len(dict_paragraphs))

unique_text = ""
for value in dict_paragraphs.values():
    unique_text += "Question\n" + value


with open('test bank unique.txt', 'w', encoding="utf-8") as f:
    f.write(unique_text)

