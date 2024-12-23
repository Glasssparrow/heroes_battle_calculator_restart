from ..battle_map.get_distance import get_distance
from .common import get_hostile_units
from ..simulator_keywords import (
    MELEE_ACTIONS,  # Лист действий ближнего боя
    MELEE_SPELL,  # ближний бой без возможности двигаться
    HIT_AND_RUN_ACTION,  # Атака с возвратом на исходную позицию
    MOVEMENT_ACTIONS,  # Лист действий движения
)


class AttackPositionsForAction:
    def __init__(self, action_index, action):
        self.positions = []
        self.targets = {}
        self.action_name = action.name
        self.action_index = action_index  # position in unit's actions list.
        self.action_threat_lvl = action.threat

    def add_coord(self, coord, targets):
        x, y = coord[0], coord[1]
        self.positions.append((x, y,))
        self.targets[f"{x}:{y}"] = targets

    def get_enemies_within_reach_from_tile(self, x, y):
        return self.targets[f"{x}:{y}"]


class AttackPositions:
    def __init__(self):
        self.positions = []
        self.enemies_in_range = {}
        self.all_enemies_in_range = []

    def add_coord(self, x, y):
        self.positions.append((x,y))
        self.enemies_in_range[f"{x}:{y}"] = []

    def add_unit_to_coord(self, x, y, unit):
        if (x,y) not in self.positions:
            raise Exception(f"{x,y} не найдено в списке коорд.")
        self.enemies_in_range[f"{x}:{y}"].append(unit)
        if unit not in self.all_enemies_in_range:
            self.all_enemies_in_range.append(unit)

    def get_units(self, x, y):
        return self.enemies_in_range[f"{x}:{y}"]

    def get_all_units(self):
        pass


def get_melee_attack_positions(the_unit, battle_map):
    result_list = []  # list of AttackPositionsForAction
    available_cells = battle_map.get_available_cells(the_unit)
    enemy_units = get_hostile_units(the_unit, battle_map)

    # Находим все точки с которых можно ударить после движения.
    attack_positions = AttackPositions()
    for (x, y), length, path in available_cells:
        some_enemies_within_range = False
        for enemy in enemy_units:
            if get_distance(
                    coord1=(x, y),
                    is_big1=the_unit.big,
                    coord2=(enemy.coord[0], enemy.coord[1]),
                    is_big2=enemy.big,
            ) == 1:
                some_enemies_within_range = True
        if some_enemies_within_range:
            attack_positions.add_coord(x, y)
            for enemy in enemy_units:
                if get_distance(
                        coord1=(x, y),
                        is_big1=the_unit.big,
                        coord2=(enemy.coord[0], enemy.coord[1]),
                        is_big2=enemy.big,
                ) == 1:
                    attack_positions.add_unit_to_coord(x, y, enemy)

    # Заполняем лист result_list
    for action_index, action in enumerate(the_unit.actions):
        # Атаки после движения
        if (
            action.type_of_action in MELEE_ACTIONS and
            action.type_of_action != MELEE_SPELL
        ):
            pos_for_action = AttackPositionsForAction(
                action_index=action_index,
                action=action,
            )
            result_list.append(pos_for_action)
            for x, y in attack_positions.positions:
                pos_for_action.add_coord(
                    coord=(x, y,),
                    targets=attack_positions.get_units(x,y),
                )
            # Если можем ударить и вернуться, то
            # текущую позицию тоже добавляем.
            if (
                action.type_of_action == HIT_AND_RUN_ACTION and
                the_unit.coord not in attack_positions
            ):
                pos_for_action.add_coord(
                    coord=(the_unit.coord[0], the_unit.coord[1],),
                    targets=attack_positions.get_all_units(),
                )
        # Если можем ударить с места, то включаем
        # навыки ближнего боя, которые можно применить только с места.
        elif (
            action.type_of_action == MELEE_SPELL and
            the_unit.coord in attack_positions
        ):
            pos_for_action = AttackPositionsForAction(
                action_index=action_index,
                action=action,
            )
            result_list.append(pos_for_action)
            pos_for_action.add_coord(
                coord=(the_unit.coord[0], the_unit.coord[1],),
                targets=attack_positions.get_all_units(),
            )
        # Если это не навык ближнего боя - пропускаем.
        else:
            continue
    return result_list


def get_range_attack_positions(the_unit, battle_map):
    attack_positions = []
    return attack_positions

def get_movement_positions(the_unit, battle_map):
    movement_positions = []
    available_cells = battle_map.get_available_cells(the_unit)
    attack_positions = AttackPositions()
    for (x, y), length, path in available_cells:
        attack_positions.add_coord(x, y)
        attack_positions.add_unit_to_coord(x, y, the_unit)
    for action_index, action in enumerate(the_unit.actions):
        # Атаки после движения
        if (
            action.type_of_action in MOVEMENT_ACTIONS
        ):
            pos_for_action = AttackPositionsForAction(
                action_index=action_index,
                action=action,
            )
            movement_positions.append(pos_for_action)
            for x, y in attack_positions.positions:
                pos_for_action.add_coord(
                    coord=(x, y,),
                    targets=attack_positions.get_units(x, y),
                )
    return movement_positions
