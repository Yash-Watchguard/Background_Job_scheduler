from enums.schedule_type import ScheduleType


def get_schedule_expression(schedule_type:ScheduleType, schedule_value:str)->str:
    
    if schedule_type == ScheduleType.At:
        return f"at({schedule_value})"
    else:
        return f"cron({schedule_value})"