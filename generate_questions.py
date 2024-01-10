# importing required modules
import openai
import pandas as pd
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
import time
import sys

openai.api_key = "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"

def get_relevant_context(df, topic, n=3):

	# print("get_relevant_context::df.head():", df.head())
	topic_embedding = get_embedding(
		topic,
		engine="text-embedding-ada-002"
	)
	df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, topic_embedding))

	# print("get_relevant_context::df.head():", df.head())
	results = (
		df.sort_values("similarity", ascending=False)
		.head(n)
	)
	
	# print("get_relevant_context::results:", results)
	
	context = results["questions"].tolist()
	context = [x+"\n\n" for x in context]
	return context

def create_prompt(topic, context, number):
	questions = ""
	i  = 1
	for question in context: 
		questions += str(i) + ". " + question
		i+=1
	
	# print("questions: ", questions)

	prompt = """These are some sample questions extracted from the UK Medical Licensing Examination on the topic of {topic}.

{questions}	
Generate 3 extremely difficult and lengthy questions (numbered from {start} to {end}) on the topic of '{topic}' based on the above sample questions. The length, style, difficulty level, and content should be based on the above sample questions. The generated questions should be of the highest difficulty level, make them as challenging as you can. The generated questions should be written in UK English. The questions should always have 5 options (A to E). Include the correct answer and short explanation as well. This should be the format of the generated questions:

{start}. Question text (the question text should be atleast 150 words)

A. First option
B. Second option
C. Third option
D. Fourth option
E. Fifth option

Correct Answer: X

Explanation: Explanation text""".format(topic=topic, questions=questions, start=number, end=number+2)
		
	# print("prompt: ", prompt)
	return prompt

def generate_questions(prompt):
	retries = 0
	try:
		res = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are an expert on the UK Medical Licenising Assessment."},
				{"role": "user", "content": prompt},
			],
			temperature=0.3,
			max_tokens = 2048, 
			frequency_penalty = 0.5,
			presence_penalty = 1.5, 
			logit_bias = {"30": 6, "47356":-50, "5958":-50, "27604": -20},
			n = 1
		)
		questions = res['choices'][0]['message']['content'] 
		
		# print("generated questions#############################")
		# print(questions)
		return questions
	except Exception as E:
		print("Exception: ", E)
		if retries == 5:
			print("Maximum retries attempted. Terminating program")
			sys.exit()
		
		print("Retry after 60s")
		time.sleep(60)
		print("Retrying now")
		generate_questions(prompt)

		retries+=1


# Get all the topics
df_topics = pd.read_csv('.\\information\\topics.csv', encoding="utf-8")
# print(df_topics.head())
topics = df_topics["Topics"].tolist()

# Get all the embeddings
df = pd.read_csv('.\\embeddings\\exclude_american_dataset_embeddings.csv', encoding="utf-8")
# print(df.head())
df["embedding"] = df.embedding.apply(eval).apply(np.array)
# print(df.head())

i = 0
number = 1
with open(".\\generated_data\\generated_questions_exclude_american_dataset.txt", "w", encoding="utf-8") as f:
	for topic in topics:
		topic = topic[0].lower() + topic[1:]
		print("topic #" + str(i) +  ": ", topic)
		context = get_relevant_context(df, topic)

		if context:
			prompt = create_prompt(topic, context, number)
			number+=3
			generated_questions = generate_questions(prompt)
			i+=1

			# f.write("############# Topic: " + topic + "#############\n")
			# f.write("\n")
			#############
			# f.write("############# Prompt: #############\n")
			# f.write(prompt + "\n")
			# f.write("\n")
			#############
			# f.write("############# Generated Questions: #############\n")
			f.write(generated_questions + "\n")
			f.write("\n")

		else:
			print("No relevant context found for topic:", topic)

		# if i == 10:
		# 	break