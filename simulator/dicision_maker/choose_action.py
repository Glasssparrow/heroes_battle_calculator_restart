from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions,
    get_movement_positions,
)
from .get_danger_zone import get_danger_zone
from .common import get_hostile_units
from .choose_target import choose_target


class Decision:

    def __init__(self, action_id, action, chosen_position, target):
        # Выбранное действие
        self.action_id = action_id
        self.action = action
        # Позиция с которой действие будет применено.
        self.chosen_position = chosen_position
        # Цель навыка
        self.target = target


def choose_action(the_unit, battle_map):
    enemy_units = get_hostile_units(the_unit, battle_map)
    melee_attacks = get_melee_attack_positions(the_unit, battle_map)
    range_attacks = get_range_attack_positions(the_unit, battle_map)
    movement = get_movement_positions(the_unit, battle_map)
    # melee_attacks ,range_attacks, movement возвращает
    # list of AttackPositionsForAction

    # Выбор действия с наибольшей угрозой.
    attack_pos_for_action = None
    threat = 0
    # Выбираем действие с наибольшим уровнем угрозы
    # (из тех что можно применить).
    for pos_for_action in melee_attacks:
        # Если действие не выбрано, берем первое попавшееся.
        if not attack_pos_for_action:
            attack_pos_for_action = pos_for_action
            continue
        if pos_for_action.action.threat > threat:
            attack_pos_for_action = pos_for_action
            threat = pos_for_action.action.threat
    for pos_for_action in range_attacks:
        if pos_for_action.action.threat > threat:
            attack_pos_for_action = pos_for_action
            threat = pos_for_action.action.threat
    danger_zone = get_danger_zone(enemy_units[0], battle_map)
    if not melee_attacks and not range_attacks:
        # Если не может атаковать, выбрать клетку для перемещения.
        for pos_for_action in movement:
            attack_pos_for_action = pos_for_action
    # TODO
    # Выбор между атакой и выходом из опасной зоны.
    else:
        # Если может атаковать, то атакуем с точки наименьшей угрозы.
        pass
    return 0
