#request and response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
#user data parsing 1
from multiprocessing.connection import Client
#user data parsing 2
from chatbot.models import Answers, Keywords
from django.shortcuts import get_object_or_404
import random

#views
@csrf_exempt
def keyboard(request):
	my_data = {
				"type":"text",
				}
	my_data = json.dumps(my_data)
	my_data = my_data.encode('utf-8')
	response = HttpResponse(my_data, content_type='application/json; charset=utf-8')
	return response

@csrf_exempt
def message(request):
	#temp = (request.body).decode('utf-8')
	#temp2 = temp['content']
	#create Client Connect
	address = ('localhost', 65123)
	password = b'1234'
	conn = Client(address, authkey=password)
	#Get the User Data
	user_data = (request.body).decode('utf-8')
	user_data = json.loads(user_data)
	user_data = user_data['content']
	#NNG or NNP getting from the User Data
	conn.send(user_data)
	user_data2 = conn.recv()
	#if keywords is None Then return the Users Input
	temp = []
	for i in user_data2:
		try:
			temp.append(get_object_or_404(Keywords, keyword=i))
		except:
			continue
	if temp == []:
		keywordsData = str(user_data)
		return_data = {'message':{"text": keywordsData}}
		return_data = json.dumps(return_data)
		return_data = return_data.encode('utf-8')
		response = HttpResponse(return_data, content_type='application/json; charset=utf-8')
		return response
	#else, Query1 and temp is had Keyword objects
	QueryAnswers = []
	for i in temp:
		QueryAnswers.append(i.answers.filter(answer__icontains=i.keyword))
	#else, QueryAnswers is not exist then End...
	if QueryAnswers == []:
		keywordsData = str(user_data)
		return_data = {'message':{"text": keywordsData}}
		return_data = json.dumps(return_data)
		return_data = return_data.encode('utf-8')
		response = HttpResponse(return_data, content_type='application/json; charset=utf-8')
		return response
	#result...
	temp = random.choice(QueryAnswers)
	result = random.choice(temp).answer
	keywordsData = result
	return_data = {'message':{"text": keywordsData}}
	return_data = json.dumps(return_data)
	return_data = return_data.encode('utf-8')
	response = HttpResponse(return_data, content_type='application/json; charset=utf-8')
	return response