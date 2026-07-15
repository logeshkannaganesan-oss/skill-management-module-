from django.db import models

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    skill_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=1)  # Defaulting user_id to 1 as in SQL query example
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=50, choices=LEVEL_CHOICES)

    class Meta:
        db_table = 'skills'
        # Prevent multiple records of the same skill name for the same student
        unique_together = ('user_id', 'skill_name')

    def __str__(self):
        return f"{self.skill_name} ({self.skill_level}) for User {self.user_id}"

