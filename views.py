###############################using with gemini api key ########################################################

# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests
# import json
# # import pathlib
# # import textwrap

# import google.generativeai as genai

# def index(request):
#     return render(request, 'chat/chat.html')

# @csrf_exempt
# def send_query(request):
#     if request.method == 'POST':
#         query = json.loads(request.body).get('query')
#         session_id = request.session.session_key
#         if not session_id:
#             request.session.create()
#             session_id = request.session.session_key
        
#         response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyAYz_SRYGUxl8Pvb08FvFQjGsTlRkRTHp4")
        
#         response_data = response.json()

#         conversation = request.session.get('conversation', [])
#         conversation.append({'query': query, 'response': response_data['response']})
#         request.session['conversation'] = conversation[-3:]

#         return JsonResponse({'response': response_data['response'], 'conversation': conversation})
#     return JsonResponse({'error': 'Invalid request'}, status=400)



############   using google-generativeai package  ####################################################################


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import google.generativeai as genai

def index(request):
    return render(request, 'chat/chat.html')

@csrf_exempt
def send_query(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if not query:
            return JsonResponse({'error': 'Query cannot be empty'}, status=400)
        
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        genai.configure(api_key=os.getenv('AIzaSyAYz_SRYGUxl8Pvb08FvFQjGsTlRkRTHp4'))
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(query)
        
        conversation = request.session.get('conversation', [])
        conversation.append({'query': query, 'response': response.text})
        request.session['conversation'] = conversation[-3:]

        return JsonResponse({'response': response.text, 'conversation': conversation})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

