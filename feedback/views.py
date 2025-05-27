from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from .serializers import FeedbackSerializer
from .models import Feedback
from .permissions import IsParentUser

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentUser]

    def get_queryset(self):
        # Only return feedbacks submitted by the logged-in parent
        return Feedback.objects.filter(parent_email=self.request.user.email)

    def perform_create(self, serializer):
        feedback = serializer.save(parent_email=self.request.user.email)
        dean_email = self.get_dean_email(feedback.school)

        subject = f"New Parent Feedback for {feedback.school}"
        from_email = None  # uses DEFAULT_FROM_EMAIL
        to = [dean_email]

        reply_to = [feedback.parent_email]  # to choose whom the Deans can reply to, for now limited to the parent only

        sender_info = f"{feedback.parent_email}" if feedback.keep_anonymous else f"{feedback.parent_name}"  # To display only the name or email respecting the anonymity

        # Fallback plain text content
        text_content = (
            f"New Parent Feedback Received\n\n"
            f"From: {sender_info}\n"
            f"School: {feedback.get_school_display()}\n"
            f"Subject: {feedback.subject}\n"
            f"Message:\n{feedback.message}"
        )

        # Rich HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #003366;">🎓 New Parent Feedback Received</h2>
            <h3 style="color: #222;">📝 Subject: {feedback.subject}</h3>

            <p><strong>From:</strong> {sender_info}</p>
            <p><strong>School:</strong> {feedback.get_school_display()}</p>
            
            <p><strong>Message:</strong></p>
            <blockquote style="margin-left: 1em; padding: 0.5em; background-color: #f2f2f2; border-left: 4px solid #003366;">
                {feedback.message}
            </blockquote>

            <p style="margin-top: 2em; font-size: 0.9em; color: #555;">This feedback was submitted via the Parent Feedback Portal.</p>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to, reply_to=reply_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_dean_email(self, school):
        return {
            # Custom emails for testing 
            'SOT': 'deepakkumar.g_2027@woxsen.edu.in',
            'SOS': 'kshitij.moghe_2026@woxsen.edu.in'
        }.get(school, 'dean.tech@sost.in')

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Deleting feedback is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
