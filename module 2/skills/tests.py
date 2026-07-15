from django.test import TestCase, Client
from django.urls import reverse
from .models import Skill

class SkillModelTest(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(user_id=1, skill_name="Python", skill_level="Intermediate")
        self.assertEqual(skill.skill_name, "Python")
        self.assertEqual(skill.skill_level, "Intermediate")
        self.assertEqual(skill.user_id, 1)
        self.assertEqual(str(skill), "Python (Intermediate) for User 1")

class SkillViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_get_empty(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No skills registered yet")
        self.assertEqual(response.context['stats']['total'], 0)

    def test_add_new_skill(self):
        response = self.client.post(self.dashboard_url, {
            'skill_name': 'Python',
            'skill_level': 'Intermediate'
        })
        self.assertRedirects(response, self.dashboard_url)
        
        # Verify db entry
        skill = Skill.objects.get(user_id=1, skill_name="Python")
        self.assertEqual(skill.skill_level, "Intermediate")
        
        # Verify statistics update
        response_get = self.client.get(self.dashboard_url)
        self.assertEqual(response_get.context['stats']['total'], 1)
        self.assertEqual(response_get.context['stats']['intermediate'], 1)
        self.assertEqual(response_get.context['stats']['intermediate_pct'], 100)

    def test_upsert_existing_skill(self):
        # Insert initial skill
        Skill.objects.create(user_id=1, skill_name="Python", skill_level="Beginner")
        
        # Post request to update same skill to 'Advanced'
        response = self.client.post(self.dashboard_url, {
            'skill_name': 'Python',
            'skill_level': 'Advanced'
        })
        self.assertRedirects(response, self.dashboard_url)
        
        # Check skill level is updated to Advanced
        skill = Skill.objects.get(user_id=1, skill_name="Python")
        self.assertEqual(skill.skill_level, "Advanced")
        self.assertEqual(Skill.objects.filter(user_id=1, skill_name="Python").count(), 1)

    def test_empty_skill_name_validation(self):
        response = self.client.post(self.dashboard_url, {
            'skill_name': '   ',
            'skill_level': 'Advanced'
        })
        # Should stay on page and show form error
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'skill_name', 'Skill name cannot be empty.')
        self.assertEqual(Skill.objects.count(), 0)

    def test_delete_skill(self):
        skill = Skill.objects.create(user_id=1, skill_name="JavaScript", skill_level="Beginner")
        delete_url = reverse('delete_skill', args=[skill.skill_id])
        
        response = self.client.post(delete_url)
        self.assertRedirects(response, self.dashboard_url)
        
        # Verify skill is deleted
        self.assertFalse(Skill.objects.filter(skill_id=skill.skill_id).exists())

