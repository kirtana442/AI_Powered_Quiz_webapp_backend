from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('USER','User'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = 'profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    created_at = models.DateTimeField(auto_now_add=True)

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY','Easy'),
        ("MEDIUM",'Medium'),
        ("HARD","Hard"),
    ]

    title = models.CharField(max_length=255,blank=True)

    topic = models.CharField(max_length=100)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )

    is_ai_generated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['topic','difficulty'])
        ]

class Question(models.Model):
        DIFFICULTY_CHOICES = [
            ('EASY', 'Easy'),
            ('MEDIUM', 'Medium'),
            ('HARD', 'Hard'),
        ]

        quiz = models.ForeignKey(
            Quiz,
            on_delete=models.CASCADE,
            related_name='questions'
        )

        text = models.TextField()

        difficulty = models.CharField(
            max_length=20,
            choices=DIFFICULTY_CHOICES,
            null=True,
            blank=True
        )

        points = models.IntegerField(default=1)

        explanation = models.TextField(blank=True)

        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
                constraints = [
                    models.CheckConstraint(
                        condition=models.Q(points__gte=0),
                        name='points_non_negative'
                    )
                ]
                indexes = [
                    models.Index(fields=['quiz']),
                ]

class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )

    text = models.TextField()

    is_correct = models.BooleanField(default=False)

class Attempt(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_PROGRESS'
    )

    score = models.IntegerField(null=True, blank=True)

    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quiz'],
                condition=models.Q(status='IN_PROGRESS'),
                name='unique_active_attempt'
            )
        ]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['quiz']),
        ]

class Response(models.Model):
    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE
    )

    is_correct = models.BooleanField()

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['attempt', 'question'],
                name='unique_response_per_question'
            )
        ]
        indexes = [
            models.Index(fields=['attempt']),
            models.Index(fields=['question']),
        ]

class AIRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_requests'
    )

    topic = models.CharField(max_length=100)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES
    )

    num_questions = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    response_json = models.JSONField(null=True, blank=True)

    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(num_questions__gt=0),
                name='num_questions_positive'
            )
        ]
        indexes = [
            models.Index(fields=['user']),
        ]