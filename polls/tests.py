from django.test import TestCase
from django.utils import timezone 
from .models import Question
import datetime
from django.urls import reverse


def create_question(q_text, days):
    """"
     
    Create a question with the given `q_text` and published the given number of `days` offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(q_text=q_text, pub_date=time)

class DashboardViewTests(TestCase):

    def test_no_questions(self):
        """
        if there are no questions, an appropriate message is displayed.
        """

        response = self.client.get(reverse("polls:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Questions Available")
        self.assertQuerySetEqual(response.context['latest_questions'], [])

    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the dashnboard
        """

        question = create_question("Are you okay?", -30)
        response = self.client.get(reverse("polls:dashboard"))
        self.assertQuerySetEqual(
            response.context["latest_questions"], [question],
        )
    def test_future_question(self):

        create_question("Who is your favorite 2023 candidate?", 30)
        response = self.client.get(reverse("polls:dashboard"))
        self.assertContains(response, "No Questions Available")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_future_question_and_past_question(self):

        """
        Even if bot future and past question exist, only past ones are shown in the dashboard.
        """
        create_question("What is your age group?", 30)
        question = create_question("Chose your second best candidate", -30)

        response = self.client.get(reverse("polls:dashboard"))
        self.assertQuerySetEqual(response.context["latest_questions"],[question])

    def test_two_past_questions(self):

        """ 
        If two question are in the past then they are displayed on the dashboard
        """
        question_1 = create_question("What is your preferred pronouns?", -30)
        question_2 = create_question("What are your hobbies?", -20)

        response = self.client.get(reverse("polls:dashboard"))

        self.assertQuerySetEqual(
            response.context["latest_questions"], [question_1, question_2], ordered=False
        )
                                   
class DetailViewTests(TestCase):

    def test_future_question(self):

        """
        The details of quesitons published in the future remain hidden to the user
        returns 404 not found
        """

        future_q = create_question("What is your worst ick?", 5)
        response = self.client.get(reverse("polls:detail", args=(future_q.id,)))


        self.assertEqual(response.status_code, 404)

    def past_questions(self):
        """
        Show details if the question was already published in the past
        """

        question = create_question("What is your avg GPA?", -24)

        response = self.client.get(reverse("polls:detail", args=(question.id)))
        self.assertContains(response, question.q_text)
        

   


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)

        recent_questions = Question(pub_date=time)
        self.assertIs(recent_questions.was_published_recently(), True)


        
