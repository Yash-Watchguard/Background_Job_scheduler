from enums.schedule_type import ScheduleType


def get_schedule_expression(schedule_type:ScheduleType, schedule_time:str)->str:
    
    if schedule_type == ScheduleType.At:
        return f"at({schedule_time})"
    else:
        return f"cron({schedule_time})"