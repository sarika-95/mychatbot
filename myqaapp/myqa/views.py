from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from django.views.decorators.csrf import csrf_exempt
nltk.download('punkt')
nltk.download('stopwords')
@csrf_exempt
def index(request):
    return render(request, 'index.html')
@csrf_exempt
def browse_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return render(request, 'index.html', {'file_load_message': 'File loaded successfully.', 'content': content})
    else:
        return HttpResponse("File load completed")
@csrf_exempt
def answer_question(request):
    if request.method == 'POST':
        context = request.POST.get('context', '')
        question = request.POST.get('question', '')
        if context and question:
            # Tokenize question
            question_words = set(nltk.word_tokenize(question.lower()))

            # Find the most relevant sentence based on word overlap
            sentences = nltk.sent_tokenize(context)
            max_overlap = 0
            relevant_sentence = ""

            for sent in sentences:
                sent_words = set(nltk.word_tokenize(sent.lower()))
                overlap = len(question_words.intersection(sent_words))
                if overlap > max_overlap:
                    max_overlap = overlap
                    relevant_sentence = sent

            # Display the answer
            if max_overlap > 0:
                answer = relevant_sentence
            else:
                answer = "Sorry, I don't know the answer."


            return render(request, 'index.html', {'content': context, 'question': question, 'answer': answer})
        else:
            return render(request, 'index.html', {'answer': "Please provide both context and question."})
    else:
        return HttpResponse("Invalid request method.")
