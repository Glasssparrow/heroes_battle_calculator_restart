from ..simulator_keywords import (
    MELEE_ACTIONS,  # Лист действий ближнего боя
    MELEE_SPELL,  # ближний бой без возможности двигаться
)


class DangerZone:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.danger_map = []
        for x in range(length):
            self.danger_map.append([0] * height)

    def __getitem__(self, item):
        if (
            item[0] >= self.length or
            item[1] >= self.height
        ):
            return 0
        return self.danger_map[item[0]][item[1]]

    def __setitem__(self, key, value):
        if not isinstance(value, (float, int)):
            raise Exception(
                f"Допустимо лишь float/int, получено - {type(value)}"
            )
        if 0 <= key[0] < self.length and 0 <= key[1] < self.height:
            self.danger_map[key[0]][key[1]] = value

    def __delitem__(self, key):
        self.danger_map[key[0]][key[1]] = 0


class DangerMap:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.melee_danger_map = []
        self.range_danger_map = []
        self.spells_danger_map = []

    def set_melee_danger_zone(self, melee_danger_map):
        self.range_danger_map = melee_danger_map

    def set_range_danger_zone(self, range_danger_map):
        self.range_danger_map = range_danger_map

    def set_spell_danger_zone(self, spells_danger_map):
        self.range_danger_map = spells_danger_map


def get_attack_area(x, y, big):
    attack_area = []
    if big:
        for dx, dy in [
            (0, 1), (1, 1), (1, 0), (1, -1),
            (0, -1), (-1, -1), (-1, 0), (-1, 1),
        ]:
            attack_area.append((x+dx, y+dy))
    else:
        for dx, dy in [
            (0, -1), (+1, -1,), (+2, -1),
            (+2, 0), (+2, +1), (+2, +2),
            (+1, +2), (0, +2), (-1, +2),
            (-1, +1), (-1, 0), (-1, -1)
        ]:
            attack_area.append((x + dx, y + dy))
    return attack_area


def get_melee_danger_zone(battle_map, unit):
    melee_danger = DangerZone(
        height=battle_map.map_height,
        length=battle_map.map_length,
    )
    available_cells = battle_map.get_available_cells(unit)
    # Выбираем сильнейшую атаку ближнего боя
    danger = 0
    for action in unit.actions:
        if (
            action.type_of_action in MELEE_ACTIONS and
            action.type_of_action != MELEE_SPELL and  # обработаем отдельно
            action.threat > danger
        ):
            danger = action.threat
    if danger == 0:  # Если не нашли рукопашных атак, значит что-то не так.
        raise Exception(
            f"{unit.name} не найдено действие рукопашной атаки."
        )
    # Заполняем melee_danger.
    # Заполняем угрозу MELEE_ACTION.
    for coord, length, path in available_cells:  # можем дойти до
        # С них можем ударить по
        attack_area = get_attack_area(
            x=coord[0], y=coord[1],
            big=unit.big,
        )
        for (x, y) in attack_area:  # можем ударить с
            melee_danger[x, y] = danger  # записываем в карту угрозы
    # добавляем угрозу от MELEE_SPELL.
    melee_spell_danger = 0
    for action in unit.actions:
        if (
                action.type_of_action == MELEE_SPELL and
                action.threat > melee_spell_danger
        ):
            melee_spell_danger = action.threat
    if melee_spell_danger > danger:
        attack_area = get_attack_area(
            x=unit.coord[0], y=unit.coord[1],
            big=unit.big,
        )
        for (x, y) in attack_area:
            melee_danger[x, y] = melee_spell_danger
    return melee_danger


def get_range_danger_zone(battle_map, unit):
    # Карта опасности дальнобойных атак.
    # Составляется для действий на которые хватает боеприпасов.
    range_danger = DangerZone(
        height=battle_map.map_height,
        length=battle_map.map_length,
    )
    return range_danger


def get_spell_danger_zone(battle_map, unit):
    # Карта опасности заклинаний.
    # Составляется для заклинаний на которые хватает маны.
    # Если заклинание стоит 0 маны, то на него маны хватает.
    # Заклинания ближнего боя уходят в карту опасности ближнего боя.
    spell_danger = DangerZone(
        height=battle_map.map_height,
        length=battle_map.map_length,
    )
    return spell_danger


def get_danger_zone(the_unit, battle_map):
    # На текущем этапе возвращает только карту опасности для ближнего боя.
    melee_danger = get_melee_danger_zone(battle_map, the_unit)
    range_danger = get_range_danger_zone(battle_map, the_unit)
    spell_danger = get_spell_danger_zone(battle_map, the_unit)
    danger_map = DangerMap(
        height=battle_map.map_height,
        length=battle_map.map_length,
    )
    danger_map.set_melee_danger_zone(melee_danger)
    danger_map.set_range_danger_zone(range_danger)
    danger_map.set_spell_danger_zone(spell_danger)
