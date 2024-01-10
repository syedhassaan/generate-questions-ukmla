import re
import regex as regex

letter = 0

with open('.\\raw_data\\new_data\\geekymedics.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Split the text into paragraphs
paragraphs = text.split('Question:\n')
# paragraphs.remove('')
print(len(paragraphs))


# From each paragraph remove all the text after 'Explanation:'
for i, paragraph in enumerate(paragraphs):
    paragraphs[i] = paragraph.split("Explanation:")[0]


# Fix the answers from 'Answer: Diabetes' to 'Answer: A'
for i, paragraph in enumerate(paragraphs):
    print("original paragraph:", paragraph)
    choices = re.findall('[A-E]\. \w.*\n', paragraph)
    choices_formatted = [choice[3:-1] for choice in choices]
    print(choices)
    print(choices_formatted)

    answer = re.search('Correct Answer:\w.*\n', paragraph)
    if answer:
        print(answer.group())
        answer_formated = answer.group()[15:-1]
        print(answer_formated)

        # get the correct answer choice
        for j, choice in enumerate(choices_formatted):
            if choice == answer_formated:
                answer_number = j
                print("answer_number: ", answer_number)
            
        
        if answer_number == 0:
            answer_letter = 'A'
        elif answer_number == 1:
            answer_letter = 'B'
        elif answer_number == 2:
            answer_letter = 'C'
        elif answer_number == 3:
            answer_letter = 'D'
        elif answer_number == 4:
            answer_letter = 'E'

        paragraphs[i] = re.sub('Correct Answer:\w.*\n', 'Correct Answer: ' + answer_letter, paragraphs[i])
        print(paragraphs[i])




# Join the remaining paragraphs back into a single string
filtered_text = 'Question\n'.join(paragraphs)

with open('.\\processed_data\\text\\geekymedics_processed.txt', 'w', encoding="utf-8") as f:
    f.write(filtered_text)

