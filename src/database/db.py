from src.database.config import supabase 
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False

def check_teacher_exists(username):
    try:
        if not supabase:
            return False
        response = supabase.table("teachers").select("username").eq("username", username).execute()
        return len(response.data) > 0 if response and response.data else False
    except Exception as e:
        print(f"check_teacher_exists error: {e}")
        return False

def create_teacher(username, password, name):
    try:
        if not supabase:
            return None
        data = {"username": username, "password": hash_pass(password), "name": name}
        response = supabase.table("teachers").insert(data).execute()    
        return response.data if response else None
    except Exception as e:
        print(f"create_teacher error: {e}")
        raise e

def teacher_login(username, password):
    try:
        if not supabase:
            return None
        response = supabase.table("teachers").select("*").eq("username", username).execute()
        if response and response.data:
            teacher = response.data[0]
            if check_pass(password, teacher.get("password", "")):
                return teacher
    except Exception as e:
        print(f"teacher_login error: {e}")
    return None

def get_all_students():
    try:
        if not supabase:
            return []
        response = supabase.table('students').select("*").execute()
        return response.data if response and response.data else []
    except Exception as e:
        print(f"get_all_students error: {e}")
        return []

def create_student(new_name, face_embedding=None, voice_embedding=None):
    try:
        if not supabase:
            return None
        data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
        response = supabase.table('students').insert(data).execute()
        return response.data if response else None
    except Exception as e:
        print(f"create_student error: {e}")
        return None

def create_subject(subject_code, name, section, teacher_id):
    try:
        if not supabase:
            return None
        data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
        response = supabase.table("subjects").insert(data).execute()
        return response.data if response else None
    except Exception as e:
        print(f"create_subject error: {e}")
        return None

def get_teacher_subjects(teacher_id):
    try:
        if not supabase:
            return []
        response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
        subjects = response.data if response and response.data else []

        for sub in subjects:
            sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
            attendance = sub.get('attendance_logs', [])
            unique_sessions = len(set(log['timestamp'] for log in attendance)) if attendance else 0
            sub['total_classes'] = unique_sessions

            sub.pop('subject_students', None)
            sub.pop('attendance_logs', None)

        return subjects
    except Exception as e:
        print(f"get_teacher_subjects error: {e}")
        return []

def enroll_student_to_subject(student_id, subject_id):
    try:
        if not supabase:
            return None
        data = {'student_id': student_id, "subject_id": subject_id}
        response = supabase.table('subject_students').insert(data).execute()
        return response.data if response else None
    except Exception as e:
        print(f"enroll_student_to_subject error: {e}")
        return None

def unenroll_student_to_subject(student_id, subject_id):
    try:
        if not supabase:
            return None
        response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
        return response.data if response else None
    except Exception as e:
        print(f"unenroll_student_to_subject error: {e}")
        return None

def get_student_subjects(student_id):
    try:
        if not supabase:
            return []
        response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data if response and response.data else []
    except Exception as e:
        print(f"get_student_subjects error: {e}")
        return []

def get_student_attendance(student_id):
    try:
        if not supabase:
            return []
        response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data if response and response.data else []
    except Exception as e:
        print(f"get_student_attendance error: {e}")
        return []

def create_attendance(logs):
    try:
        if not supabase:
            return None
        response = supabase.table('attendance_logs').insert(logs).execute()
        return response.data if response else None
    except Exception as e:
        print(f"create_attendance error: {e}")
        return None

def get_attendance_for_teacher(teacher_id):
    try:
        if not supabase:
            return []
        response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
        return response.data if response and response.data else []
    except Exception as e:
        print(f"get_attendance_for_teacher error: {e}")
        return []

def student_login_by_name(name):
    try:
        students = get_all_students()
        if students:
            for s in students:
                if s.get('name', '').strip().lower() == name.strip().lower():
                    return s
    except Exception as e:
        print(f"student_login_by_name error: {e}")
    return None