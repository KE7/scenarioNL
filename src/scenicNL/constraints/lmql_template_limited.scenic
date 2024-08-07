# SCENARIO DESCRIPTION
"""
{TEXT_DESCRIPTION_TODO}
"""
# SCENARIO CODE

## SET MAP AND MODEL (i.e. definitions of all referenceable vehicle types, road library, etc)
param map = localPath(f'../../../assets/maps/CARLA/{CARLA_MAP_NAME_TODO}.xodr')
param carla_map = '{CARLA_MAP_NAME_TODO}'
param weather = '{WEATHER_PARAM_TODO}'
model scenic.simulators.carla.model

## CONSTANTS
EGO_MODEL = '{EGO_VEHICLE_BLUEPRINT_ID_TODO}'
EGO_SPEED = {EGO_VEHICLE_SPEED_TODO}
{OTHER_CONSTANTS_TODO}

## DEFINING BEHAVIORS
{VEHICLE_BEHAVIORS_TODO}

## DEFINING SPATIAL RELATIONS
{SPATIAL_RELATIONS_TODO}
