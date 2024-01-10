# imports
import pandas as pd
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import csv
import numpy as np
import re
import PyPDF2

openai.api_key = "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"

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# 
# creating a pdf file object
def createCSV():

	# file_path = '.\\raw_data\\'
	# pdfFiles = [file_path+'paper-1.pdf', file_path+'paper-2.pdf']

	with open(".\\processed_data\\csv\\5000_testbank_unique.csv",  encoding='utf-8', mode='w', newline='') as f:

		writer = csv.writer(f)
		writer.writerow(['questions'])  # write headers

		#create the embeddings for the csv files
		# for pdf in pdfFiles:
		# 	pdfFileObj = open(pdf, 'rb')

		# 	# creating a pdf reader object
		# 	pdfReader = PyPDF2.PdfReader(pdfFileObj)

		# 	for i in range(1, 101):

		# 		# creating a page object
		# 		pageObj = pdfReader.pages[i]

		# 		# extracting text from page
		# 		question = pageObj.extract_text()
		# 		# print(question)

		# 		match = re.search(r"\d\.", question)

		# 		if match:
		# 			result = question[match.end():]
		# 			# print("Question: ", result)
		# 			writer.writerow([result.strip()])  # write a single row
		# 		else:
		# 			print("No match found.")
				
		# 	# closing the pdf file object
		# 	pdfFileObj.close()

		# create the embeddings for the test bank
		with open('.\\processed_data\\text\\5000_question_testbank_processed_unique.txt', 'r', encoding="utf-8") as f:
			text = f.read()
		
		paragraphs = text.split('Question\n')

		for paragraph in paragraphs:
			writer.writerow([paragraph.strip()])  # write a single row

# This may take a few minutes
def createEmbeddings():
    df = pd.read_csv('.\\processed_data\\csv\\5000_testbank_unique.csv')
    print(df.head())
    df["embedding"] = df.questions.apply(lambda x: get_embedding(x, engine=embedding_model))
    print(df.head())
    df.to_csv(".\\embeddings\\5000_testbank_embeddings.csv", index=False)
    

def searchQuestions(topic):
	df = pd.read_csv('.\\embeddings\\combined_dataset_embeddings.csv')
	df["embedding"] = df.embedding.apply(eval).apply(np.array)

	# search through the reviews for a specific product
	def search_questions(df, topic, n=3, pprint=True):
		topic_embedding = get_embedding(
			topic,
			engine="text-embedding-ada-002"
		)
		df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, topic_embedding))

		results = (
			df.sort_values("similarity", ascending=False)
			.head(n)
		)
		if pprint:
			for r in results:
				print(r)
				print()
		return results


	results = search_questions(df, topic, n=5)
	print("results: ", results)


# createCSV()
createEmbeddings()
# searchQuestions("Abdominal distension")