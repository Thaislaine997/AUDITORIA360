"""
Gamification API Router for AUDITORIA360
Implements XP, achievements, missions, and skill tree functionality
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ...models.database import get_db
from ...models.auth_models import (
    User, 
    Achievement, 
    XPHistory, 
    Skill, 
    UserSkillProgress, 
    OnboardingMission,
    user_achievements
)
from ...auth.auth_utils import get_current_user
from ..common.responses import success_response, error_response

router = APIRouter(prefix="/gamification", tags=["gamification"])


@router.get("/profile")
async def get_gamification_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's complete gamification profile"""
    try:
        # Calculate user's level (every 1000 XP = 1 level)
        current_level = (current_user.xp_points // 1000) + 1
        xp_in_current_level = current_user.xp_points % 1000
        xp_to_next_level = 1000 - xp_in_current_level
        
        # Get user's achievements
        user_achievements_query = db.query(Achievement).join(
            user_achievements
        ).filter(user_achievements.c.user_id == current_user.id).all()
        
        # Get available achievements (not yet unlocked)
        unlocked_achievement_ids = [a.id for a in user_achievements_query]
        available_achievements = db.query(Achievement).filter(
            Achievement.is_active == True,
            ~Achievement.id.in_(unlocked_achievement_ids)
        ).all()
        
        # Get user's skill progress
        skill_progress = db.query(UserSkillProgress).join(Skill).filter(
            UserSkillProgress.user_id == current_user.id
        ).all()
        
        # Get recent XP history
        recent_xp = db.query(XPHistory).filter(
            XPHistory.user_id == current_user.id
        ).order_by(desc(XPHistory.earned_at)).limit(10).all()
        
        # Get current onboarding mission
        current_mission = None
        if current_user.onboarding_status == "in_progress":
            current_mission = db.query(OnboardingMission).filter(
                OnboardingMission.id == current_user.current_mission_id
            ).first()
        
        return success_response({
            "user_id": current_user.id,
            "current_xp": current_user.xp_points,
            "current_level": current_level,
            "xp_in_current_level": xp_in_current_level,
            "xp_to_next_level": xp_to_next_level,
            "total_missions_completed": current_user.total_missions_completed,
            "achievements": {
                "unlocked": [
                    {
                        "id": achievement.id,
                        "name": achievement.name,
                        "description": achievement.description,
                        "icon": achievement.icon,
                        "badge_class": achievement.badge_class,
                        "xp_reward": achievement.xp_reward,
                    }
                    for achievement in user_achievements_query
                ],
                "available": [
                    {
                        "id": achievement.id,
                        "name": achievement.name,
                        "description": achievement.description,
                        "icon": achievement.icon,
                        "badge_class": achievement.badge_class,
                        "xp_reward": achievement.xp_reward,
                    }
                    for achievement in available_achievements
                ]
            },
            "skills": [
                {
                    "skill_id": progress.skill_id,
                    "skill_name": progress.skill.name,
                    "skill_description": progress.skill.description,
                    "skill_icon": progress.skill.icon,
                    "skill_category": progress.skill.category,
                    "current_progress": progress.current_progress,
                    "required_actions": progress.skill.required_actions,
                    "is_unlocked": progress.is_unlocked,
                    "unlocked_at": progress.unlocked_at,
                }
                for progress in skill_progress
            ],
            "recent_activity": [
                {
                    "xp_earned": xp.xp_earned,
                    "reason": xp.reason,
                    "earned_at": xp.earned_at,
                }
                for xp in recent_xp
            ],
            "current_mission": {
                "id": current_mission.id,
                "name": current_mission.name,
                "description": current_mission.description,
                "instructions": current_mission.instructions,
                "xp_reward": current_mission.xp_reward,
                "badge_reward": current_mission.badge_reward,
            } if current_mission else None,
            "onboarding_status": current_user.onboarding_status,
        })
        
    except Exception as e:
        return error_response(f"Failed to get gamification profile: {str(e)}", 500)


@router.post("/award-xp")
async def award_xp(
    xp_amount: int,
    reason: str,
    related_resource: Optional[str] = None,
    related_resource_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP to user and check for achievements"""
    try:
        # Create XP history record
        xp_history = XPHistory(
            user_id=current_user.id,
            xp_earned=xp_amount,
            reason=reason,
            related_resource=related_resource,
            related_resource_id=related_resource_id
        )
        db.add(xp_history)
        
        # Update user's XP
        old_level = (current_user.xp_points // 1000) + 1
        current_user.xp_points += xp_amount
        new_level = (current_user.xp_points // 1000) + 1
        
        # Check for level up
        level_up = new_level > old_level
        
        # Check for achievements to unlock
        new_achievements = []
        if reason == "mission_completed":
            current_user.total_missions_completed += 1
            
            # Check mission-based achievements
            mission_achievements = db.query(Achievement).filter(
                Achievement.criteria_type == "count",
                Achievement.criteria_resource == "missions",
                Achievement.criteria_target <= current_user.total_missions_completed,
                Achievement.is_active == True
            ).all()
            
            for achievement in mission_achievements:
                # Check if user already has this achievement
                existing = db.query(user_achievements).filter(
                    user_achievements.c.user_id == current_user.id,
                    user_achievements.c.achievement_id == achievement.id
                ).first()
                
                if not existing:
                    # Award achievement
                    db.execute(
                        user_achievements.insert().values(
                            user_id=current_user.id,
                            achievement_id=achievement.id
                        )
                    )
                    new_achievements.append(achievement)
                    current_user.xp_points += achievement.xp_reward
        
        db.commit()
        
        return success_response({
            "xp_awarded": xp_amount,
            "total_xp": current_user.xp_points,
            "old_level": old_level,
            "new_level": new_level,
            "level_up": level_up,
            "new_achievements": [
                {
                    "id": achievement.id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "xp_reward": achievement.xp_reward,
                }
                for achievement in new_achievements
            ]
        })
        
    except Exception as e:
        db.rollback()
        return error_response(f"Failed to award XP: {str(e)}", 500)


@router.post("/complete-mission/{mission_id}")
async def complete_mission(
    mission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete an onboarding mission"""
    try:
        # Get the mission
        mission = db.query(OnboardingMission).filter(
            OnboardingMission.id == mission_id,
            OnboardingMission.is_active == True
        ).first()
        
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not found"
            )
        
        # Check if mission is appropriate for user's profile
        if mission.profile_target != "all" and mission.profile_target != current_user.user_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mission not available for your profile"
            )
        
        # Award XP for mission completion
        xp_result = await award_xp(
            xp_amount=mission.xp_reward,
            reason="mission_completed",
            related_resource="onboarding_mission",
            related_resource_id=str(mission_id),
            current_user=current_user,
            db=db
        )
        
        # Update user's onboarding progress
        next_mission = db.query(OnboardingMission).filter(
            OnboardingMission.order_sequence > mission.order_sequence,
            OnboardingMission.profile_target.in_(["all", current_user.user_profile]),
            OnboardingMission.is_active == True
        ).order_by(OnboardingMission.order_sequence).first()
        
        if next_mission:
            current_user.current_mission_id = next_mission.id
        else:
            # All missions completed
            current_user.onboarding_status = "completed"
            current_user.onboarding_completed_at = func.now()
            current_user.current_mission_id = None
        
        db.commit()
        
        return success_response({
            "mission_completed": {
                "id": mission.id,
                "name": mission.name,
                "xp_reward": mission.xp_reward,
                "badge_reward": mission.badge_reward,
            },
            "xp_result": xp_result,
            "next_mission": {
                "id": next_mission.id,
                "name": next_mission.name,
                "description": next_mission.description,
            } if next_mission else None,
            "onboarding_completed": current_user.onboarding_status == "completed"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return error_response(f"Failed to complete mission: {str(e)}", 500)


@router.get("/leaderboard")
async def get_team_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get team leaderboard (for managers)"""
    try:
        # Check if user is a manager/gestor
        if current_user.user_profile not in ["gestor", "administrador"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers can view leaderboard"
            )
        
        # Get team members (users in the same company/department)
        team_members = db.query(User).filter(
            User.department == current_user.department,
            User.status == "active"
        ).order_by(desc(User.xp_points)).limit(20).all()
        
        return success_response({
            "leaderboard": [
                {
                    "rank": index + 1,
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "xp_points": user.xp_points,
                    "level": (user.xp_points // 1000) + 1,
                    "total_missions_completed": user.total_missions_completed,
                    "position": user.position,
                }
                for index, user in enumerate(team_members)
            ]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        return error_response(f"Failed to get leaderboard: {str(e)}", 500)


@router.post("/update-skill-progress")
async def update_skill_progress(
    skill_id: int,
    progress_increment: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's progress on a specific skill"""
    try:
        # Get or create skill progress
        skill_progress = db.query(UserSkillProgress).filter(
            UserSkillProgress.user_id == current_user.id,
            UserSkillProgress.skill_id == skill_id
        ).first()
        
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found"
            )
        
        if not skill_progress:
            skill_progress = UserSkillProgress(
                user_id=current_user.id,
                skill_id=skill_id,
                current_progress=0,
                is_unlocked=False
            )
            db.add(skill_progress)
        
        # Update progress
        skill_progress.current_progress += progress_increment
        
        # Check if skill should be unlocked
        skill_unlocked = False
        if not skill_progress.is_unlocked and skill_progress.current_progress >= skill.required_actions:
            skill_progress.is_unlocked = True
            skill_progress.unlocked_at = func.now()
            skill_unlocked = True
            
            # Award XP for skill unlock (optional)
            await award_xp(
                xp_amount=100,  # Fixed XP for skill unlock
                reason="skill_unlocked",
                related_resource="skill",
                related_resource_id=str(skill_id),
                current_user=current_user,
                db=db
            )
        
        db.commit()
        
        return success_response({
            "skill_id": skill_id,
            "skill_name": skill.name,
            "current_progress": skill_progress.current_progress,
            "required_actions": skill.required_actions,
            "is_unlocked": skill_progress.is_unlocked,
            "skill_unlocked": skill_unlocked,
        })
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return error_response(f"Failed to update skill progress: {str(e)}", 500)


@router.get("/achievements")
async def get_available_achievements(
    db: Session = Depends(get_db)
):
    """Get all available achievements"""
    try:
        achievements = db.query(Achievement).filter(
            Achievement.is_active == True
        ).all()
        
        return success_response([
            {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "icon": achievement.icon,
                "badge_class": achievement.badge_class,
                "xp_reward": achievement.xp_reward,
                "criteria_type": achievement.criteria_type,
                "criteria_target": achievement.criteria_target,
                "criteria_resource": achievement.criteria_resource,
            }
            for achievement in achievements
        ])
        
    except Exception as e:
        return error_response(f"Failed to get achievements: {str(e)}", 500)


@router.get("/missions")
async def get_onboarding_missions(
    profile: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get onboarding missions for user's profile"""
    try:
        user_profile = profile or current_user.user_profile
        
        missions = db.query(OnboardingMission).filter(
            OnboardingMission.is_active == True,
            OnboardingMission.profile_target.in_(["all", user_profile])
        ).order_by(OnboardingMission.order_sequence).all()
        
        return success_response([
            {
                "id": mission.id,
                "name": mission.name,
                "description": mission.description,
                "instructions": mission.instructions,
                "order_sequence": mission.order_sequence,
                "profile_target": mission.profile_target,
                "xp_reward": mission.xp_reward,
                "badge_reward": mission.badge_reward,
                "completion_criteria": mission.completion_criteria,
                "is_optional": mission.is_optional,
            }
            for mission in missions
        ])
        
    except Exception as e:
        return error_response(f"Failed to get missions: {str(e)}", 500)