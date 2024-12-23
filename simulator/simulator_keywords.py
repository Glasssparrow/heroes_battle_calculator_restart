

# Цвет по умолчанию
DEFAULT_COLOR = "Бесцветный"

# Особенности юнитов
GHOST = "ghost"
WALL_OF_SHIELDS = "wall_of_shields"

# Условия активации навыков
ACTIVATE_BEFORE_STRIKE = "before strike"
ACTIVATE_AFTER_STRIKE = "after strike"
ACTIVATE_BEFORE_GET_HIT = "before get hit"
ACTIVATE_AFTER_GET_HIT = "after get hit"
ACTIVATE_BEFORE_SHOOT = "before shot"
ACTIVATE_AFTER_SHOOT = "after shot"
ACTIVATE_BEFORE_GET_SHOT = "before get shot"
ACTIVATE_AFTER_GET_SHOT = "after get shot"
ACTIVATE_AT_TURN_START = "turn_start"
ACTIVATE_AT_TURN_END = "turn_end"

# Метка для инициативы
INITIATIVE_MORALE = "morale_mark_for_initiative"

# Условия снятия эффектов
DISPELL_CASE_INITIATIVE = "dispel_in_initiative_package"
DISPELL_AT_TURN_START = "dispelled_at_start_of_the_turn"
DISPELL_AT_TURN_END = "dispelled_at_end_of_the_turn"
DISPELL_TEMPORARY_BLOCK_COUNTER = "dispelled_at_failed_counter"
DISPELL_AFTER_TAKING_DAMAGE = "dispelled_after_taking_damage"

# Особенности эффектов
BLOCK_ACTION = "block_action"
BLOCK_COUNTER = "block_counterattack"
TEMPORARY_BLOCK_COUNTER = "block_1_counterattack"
BASH = "bash"
ZERO_MORALE = "undead"
INVISIBILITY = "invisible"

# Иммунитеты
BASH_IMMUNE = "bash_immune"
VAMPIRISM_IMMUNE = "immune_to_vampirism"
BLIND_IMMUNE = "blind_immune"
PUSH_IMMUNE = "push_immune"
FEAR_IMMUNE = "fear_immune"

# Для словаря modifiers в классе Effect
BATTLE_FRENZY_MODIFIER = "battle_frenzy_modifier"
POISON = "poison"

# Типы действий
# Ближний бой
MELEE_ACTION = "melee"  # Атака в ближнем бою
MELEE_SPELL = "melee_spell"  # Атака в ближнем бою без возможности двигаться
HIT_AND_RUN_ACTION = "hit_and_run_melee_attack"
MELEE_ACTIONS = [MELEE_ACTION, MELEE_SPELL, HIT_AND_RUN_ACTION]
# Движение
JUST_MOVEMENT = "movement_action"  # Просто движение без атаки
MOVEMENT_ACTIONS = [JUST_MOVEMENT]

# Типы реакций
MELEE_COUNTER = "melee_counter"
