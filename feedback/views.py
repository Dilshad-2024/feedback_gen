from .models import Form, Question, Response, Answer,AdditionalField, AdditionalFieldValue
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .sentiment import analyze_sentiment
from django.views.decorators.http import require_POST

@login_required
def create_form(request):

    if request.method == "POST":

        title = request.POST.get("title")

        questions = request.POST.getlist("questions[]")

        additional_fields = request.POST.getlist("fields[]")

        form = Form.objects.create(
            title=title,
            created_by=request.user
        )

        for q in questions:

            if q.strip():

                Question.objects.create(
                    form=form,
                    question_text=q
                )

        for field in additional_fields:

            if field.strip():

                AdditionalField.objects.create(
                    form=form,
                    field_name=field
                )

        return redirect(
            "form_created",
            form_id=form.id
        )

    return render(
        request,
        "feedback/create_form.html"
    )

def fill_form(request, form_id):

    form = Form.objects.get(id=form_id)

    if request.method == "POST":

        email = request.POST.get("email")
        comment = request.POST.get("comment")

        if Response.objects.filter(form=form, email=email).exists():

            return render(
                request,
                "feedback/fill_form.html",
                {
                    "form": form,
                    "error": "You have already submitted feedback for this form."
                }
            )

        total = 0
        count = 0

        ratings = {}

        for question in form.questions.all():

            rating = int(
                request.POST.get(f"question_{question.id}")
            )

            ratings[question] = rating

            total += rating
            count += 1

        overall_rating = total / count

        response = Response.objects.create(
            form=form,
            email=email,
            overall_rating=overall_rating,
            comment=comment,
        )

        # Save question ratings
        for question, rating in ratings.items():

            Answer.objects.create(
                response=response,
                question=question,
                rating=rating
            )

        # Save additional fields
        for field in form.additional_fields.all():

            value = request.POST.get(f"field_{field.id}")

            AdditionalFieldValue.objects.create(
                response=response,
                field=field,
                value=value
            )

        return redirect("feedback_submitted")

    return render(
        request,
        "feedback/fill_form.html",
        {
            "form": form
        }
    )
    
def form_created(request, form_id):

    form = Form.objects.get(id=form_id)

    return render(
        request,
        'feedback/form_created.html',
        {'form': form}
    )

def feedback_submitted(request):
    return render(request,'feedback/feedback_submitted.html')

def my_forms(request):

    forms = Form.objects.filter(
        created_by=request.user
    )

    return render(request,'feedback/my_forms.html',{'forms': forms})

def responses(request):

    forms = Form.objects.filter(
        created_by=request.user
    )

    return render(request,'feedback/responses.html',{'forms': forms})

def form_analytics(request, form_id):

    form = Form.objects.get(
        id=form_id,
        created_by=request.user
    )

    average_rating = form.responses.aggregate(
        Avg('overall_rating')
    )['overall_rating__avg']

    total_responses = form.responses.count()

    question_data = []

    for question in form.questions.all():

        avg = question.answers.aggregate(
            Avg('rating')
        )['rating__avg']

        question_data.append({
            'question': question.question_text,
            'average': round(avg or 0, 2)
        })
    five_star_comments = form.responses.filter(
    overall_rating__gte=4.5
    ).exclude(comment="")

    four_star_comments = form.responses.filter(
        overall_rating__gte=3.5,
        overall_rating__lt=4.5
    ).exclude(comment="")

    three_star_comments = form.responses.filter(
        overall_rating__gte=2.5,
        overall_rating__lt=3.5
    ).exclude(comment="")

    two_star_comments = form.responses.filter(
        overall_rating__gte=1.5,
        overall_rating__lt=2.5
    ).exclude(comment="")

    one_star_comments = form.responses.filter(
        overall_rating__lt=1.5
    ).exclude(comment="")
    comments = form.responses.exclude(
    comment=""
    )

    rating_filter = request.GET.get("rating")
    
    if rating_filter:
        rating = int(rating_filter)
        comments = form.responses.filter(
            overall_rating__gte=rating - 0.5,
            overall_rating__lt=rating + 0.5,
        ).exclude(comment="")


    return render(
        request,
        'feedback/form_analytics.html',
        {
            'form': form,
            'average_rating': average_rating,
            'total_responses': total_responses,
            'question_data': question_data,
            'five_star_comments': five_star_comments,
            'four_star_comments': four_star_comments,
            'three_star_comments': three_star_comments,
            'two_star_comments': two_star_comments,
            'one_star_comments': one_star_comments,
            'comments': comments,
            'selected_rating': rating_filter,
        }
    )

def ai_analysis(request, form_id):

    form = Form.objects.get(
        id=form_id,
        created_by=request.user
    )

    positive = 0
    negative = 0
    neutral = 0

    for response in form.responses.all():

        if response.comment.strip():

            result = analyze_sentiment(response.comment)

            if result["label"] == "POSITIVE":
                positive += 1

            elif result["label"] == "NEGATIVE":
                negative += 1

            else:
                neutral += 1

    return render(
        request,
        "feedback/ai_analysis.html",
        {
            "form": form,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        }
    )

def edit_form(request, form_id):

    form = get_object_or_404(
        Form,
        id=form_id,
        created_by=request.user
    )

    # Prevent editing if responses already exist
    if form.responses.count() > 0:
        return redirect("my_forms")

    if request.method == "POST":

        title = request.POST.get("title")
        questions = request.POST.getlist("questions[]")
        fields = request.POST.getlist("fields[]")

        # Update title
        form.title = title
        form.save()

        # Delete existing questions and additional fields
        form.questions.all().delete()
        form.additional_fields.all().delete()

        # Save questions
        for q in questions:

            if q.strip():

                Question.objects.create(
                    form=form,
                    question_text=q
                )

        # Save additional fields
        for field in fields:

            if field.strip():

                AdditionalField.objects.create(
                    form=form,
                    field_name=field
                )

        return redirect("my_forms")

    return render(
        request,
        "feedback/edit_form.html",
        {
            "form": form
        }
    )

@require_POST    
def delete_form(request, form_id):

    form = get_object_or_404(
        Form,
        id=form_id,
        created_by=request.user
    )

    form.delete()

    return redirect("my_forms")