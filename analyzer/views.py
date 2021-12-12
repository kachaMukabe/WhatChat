from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatUploadForm
from .models import Conversation
import symbl
import pprint
import arrow


def index(request):
    return render(request, "analyzer/index.html")


def handle_uploaded_file(file):
    chat = file.read().decode("utf-8")
    lines = chat.splitlines()
    lines = [l.strip() for l in lines]
    messages = []
    # pprint.pprint(lines)
    cleaned_lines = []
    for x in range(len(lines)):
        if lines[x].find("[") == -1:
            cleaned_lines[-1] = f"{cleaned_lines[-1]} {lines[x]}"
            continue
        cleaned_lines.append(lines[x])
    # pprint.pprint(cleaned_lines)
    for line in cleaned_lines:
        st_dt, en_dt = line.find("["), line.find("]")
        print(line)
        # print(line[st_dt:en_dt])
        time = line[st_dt:en_dt].replace("[", "")
        # print(line[en_dt:].split(':')[0])
        name = line[en_dt:].split(":")[0].replace("]", "")
        st_m = line[en_dt:].find(":")
        # print(line[en_dt:][st_m:], type(line[en_dt:][st_m:]))
        message = line[en_dt:][st_m:].replace(":", "")
        messages.append(
            {
                "duration": {"startTime": arrow.get(time, 'M/D/YY, H:mm:ss A').format(), "endTime": arrow.get(time, 'M/D/YY, H:mm:ss A').format()},
                "payload": {"content": message, "contentType": "text/plain"},
                "from": {"name": name, "userId": name},
            }
        )
        print(time, name, message)
    print(messages)
    return {
        "name": "Business Meeting",
        "confidenceThreshold": 0.6,
        "detectPhrases": True,
        "messages": messages,
    }


class Analyze(LoginRequiredMixin, View):
    form_class = ChatUploadForm
    template_name = "analyzer/upload.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid:
            conversation = form.save(commit=False)
            conversation_request = handle_uploaded_file(request.FILES["chat"])
            conversation_object = symbl.Text.process(payload=conversation_request)
            pprint.pprint(conversation_object)
            conversation.conversation_id = conversation_object.get_conversation_id()
            conversation.owner = request.user
            conversation.save()
            return redirect("analyze")
        return redirect("analyze")


class Chat(LoginRequiredMixin, View):
    def get(self, request, pk):
        conversation = Conversation.objects.get(pk=pk)
        if not conversation.topics:
            topics = symbl.Conversations.get_topics(conversation_id=conversation.conversation_id)
            print(topics.topics,type(topics.topics))
            conversation.topics = topics.topics
            # conversation.save()
        if not conversation.actions:
            actions = symbl.Conversations.get_action_items(conversation_id=conversation.conversation_id)
            conversation.actions = actions.action_items
        return render(request, 'analyzer/chat.html', {"conversation": conversation})
