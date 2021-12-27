import enum
import random


class RandomATTR(enum.EnumMeta):
    @property
    def random(self):
        return random.choice([Ships.weapon.name, Ships.hull.name, Ships.engine.name])


class Ships(enum.Enum, metaclass=RandomATTR):
    weapon = "weapon"
    hull = "hull"
    engine = "engine"


class RandomATTR(enum.EnumMeta):
    @property
    def random(self):
        return random.choice([Weapons.reload_speed.name, Weapons.rotation_speed.name,
                              Weapons.diameter.name, Weapons.power_volley.name, Weapons.count.name])


class Weapons(enum.Enum, metaclass=RandomATTR):
    reload_speed = "reload_speed"
    rotation_speed = "rotation_speed"
    diameter = "diameter"
    power_volley = "power_volley"
    count = "count"


class RandomATTR(enum.EnumMeta):
    @property
    def random(self):
        return random.choice([Hulls.armor.name, Hulls.type.name, Hulls.capacity.name])


class Hulls(enum.Enum, metaclass=RandomATTR):
    armor = "armor"
    type = "type"
    capacity = "capacity"


class RandomATTR(enum.EnumMeta):
    @property
    def random(self):
        return random.choice([Engines.power.name, Engines.type.name])


class Engines(enum.Enum, metaclass=RandomATTR):
    power = "power"
    type = "type"


def table_columns(table_name):
    global column
    if table_name == "Ships":
        column = Ships.random
    elif table_name == "Weapons":
        column = Weapons.random
    elif table_name == "Hulls":
        column = Hulls.random
    elif table_name == "Engines":
        column = Engines.random
    return column
