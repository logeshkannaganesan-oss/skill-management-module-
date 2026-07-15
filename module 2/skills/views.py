from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Skill
from .forms import SkillForm

def dashboard(request):
    user_id = 1
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data['skill_name']
            skill_level = form.cleaned_data['skill_level']
            
            # Check if skill already exists for this user (case-insensitive check)
            existing_skill = Skill.objects.filter(user_id=user_id, skill_name__iexact=skill_name).first()
            
            if existing_skill:
                # Update existing skill level
                old_level = existing_skill.skill_level
                existing_skill.skill_level = skill_level
                existing_skill.save()
                messages.success(request, f"Successfully updated skill '{existing_skill.skill_name}' level from {old_level} to {skill_level}!")
            else:
                # Create and store new skill
                new_skill = Skill.objects.create(
                    user_id=user_id,
                    skill_name=skill_name,
                    skill_level=skill_level
                )
                messages.success(request, f"Successfully added new skill '{new_skill.skill_name}' as {skill_level}!")
            
            return redirect('dashboard')
    else:
        form = SkillForm()

    # Fetch all skills matching user_id = 1
    skills_list = Skill.objects.filter(user_id=user_id).order_by('skill_name')
    
    # Calculate proficiency distribution
    total_skills = skills_list.count()
    beginner_count = skills_list.filter(skill_level='Beginner').count()
    intermediate_count = skills_list.filter(skill_level='Intermediate').count()
    advanced_count = skills_list.filter(skill_level='Advanced').count()
    
    beginner_pct = int((beginner_count / total_skills) * 100) if total_skills > 0 else 0
    intermediate_pct = int((intermediate_count / total_skills) * 100) if total_skills > 0 else 0
    advanced_pct = int((advanced_count / total_skills) * 100) if total_skills > 0 else 0

    context = {
        'form': form,
        'skills': skills_list,
        'stats': {
            'total': total_skills,
            'beginner': beginner_count,
            'intermediate': intermediate_count,
            'advanced': advanced_count,
            'beginner_pct': beginner_pct,
            'intermediate_pct': intermediate_pct,
            'advanced_pct': advanced_pct,
        }
    }
    return render(request, 'skills/dashboard.html', context)

def delete_skill(request, skill_id):
    if request.method == 'POST':
        skill = get_object_or_404(Skill, skill_id=skill_id, user_id=1)
        name = skill.skill_name
        skill.delete()
        messages.success(request, f"Successfully deleted skill '{name}'.")
    return redirect('dashboard')
