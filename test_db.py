from database.db import get_or_create_user, save_workout, get_history, get_summary

uid = get_or_create_user("Rahul", 70)
print("User ID:", uid)

save_workout(uid, "Squat", 12, 50, 4.5)

print("History:", get_history(uid))
print("Summary:", get_summary(uid))