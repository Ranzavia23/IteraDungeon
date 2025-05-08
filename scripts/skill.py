class Skill:
    def __init__(self, name, required_level, description, unlocked=False):
        self.name = name
        self.required_level = required_level
        self.description = description
        self.unlocked = unlocked

    def can_unlock(self, player_level):
        return player_level >= self.required_level and not self.unlocked

    def unlock(self):
        self.unlocked = True

class SkillTree:
    def __init__(self):
        self.skills = [
            Skill("Power Strike", 1, "Deal heavy damage."),
            Skill("Swift Step", 2, "Increase speed for 3 turns."),
            Skill("Iron Guard", 3, "Increase defense temporarily."),
        ]

    def get_unlockable_skills(self, player_level):
        return [skill for skill in self.skills if skill.can_unlock(player_level)]

    def unlock_skill(self, skill_name, player_level):
        for skill in self.skills:
            if skill.name == skill_name and skill.can_unlock(player_level):
                skill.unlock()
                return True
        return False