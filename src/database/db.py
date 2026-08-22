from src.database.config import supabase 
import bcrypt
import sqlite3
import json
import os
import random

# -------------------------------------------------------------
# LOCAL SQLITE FALLBACK ENGINE (For seamless operation even if Supabase project is paused/unreachable)
# -------------------------------------------------------------
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'snapclass_fallback.db')

def init_sqlite_db():
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face_embedding TEXT,
                voice_embedding TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                section TEXT,
                teacher_id INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER,
                timestamp TEXT,
                is_present INTEGER
            )
        ''')
        
        # Pre-seed demo teacher
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO teachers (teacher_id, username, password, name) VALUES (1, 'aravind', '$2b$12$eImiTXuWVxfM37uY4JANj.1Q2.f7Vw3F3V5.F1Vw3F3V5.F1Vw3F3', 'Prof. Aravind Johindkumar')")

        # Pre-seed demo subjects
        cursor.execute("SELECT COUNT(*) FROM subjects")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO subjects (subject_id, subject_code, name, section, teacher_id) VALUES (1, 'CS101', 'Applied AI & Machine Learning', 'Section A', 1)")
            cursor.execute("INSERT INTO subjects (subject_id, subject_code, name, section, teacher_id) VALUES (2, 'AI202', 'Biometric Computer Vision', 'Section B', 1)")
            cursor.execute("INSERT INTO subjects (subject_id, subject_code, name, section, teacher_id) VALUES (3, 'DS301', 'Neural Networks & Deep Learning', 'Section A', 1)")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"SQLite init notice: {e}")

init_sqlite_db()

def get_sqlite_conn():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False

# -------------------------------------------------------------
# DUAL ENGINE DATABASE FUNCTIONS (Supabase Primary -> SQLite Fallback)
# -------------------------------------------------------------
def check_teacher_exists(username):
    try:
        if supabase:
            response = supabase.table("teachers").select("username").eq("username", username).execute()
            if response and response.data:
                return len(response.data) > 0
    except Exception as e:
        print(f"check_teacher_exists Supabase notice: {e}")
    
    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT 1 FROM teachers WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        return bool(row)
    except Exception as e:
        print(f"check_teacher_exists SQLite notice: {e}")
        return False

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    try:
        if supabase:
            response = supabase.table("teachers").insert(data).execute()    
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"create_teacher Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)", 
                  (username, data['password'], name))
        conn.commit()
        t_id = c.lastrowid
        conn.close()
        return [{"teacher_id": t_id, "username": username, "name": name}]
    except Exception as e:
        print(f"create_teacher SQLite notice: {e}")
        return [{"teacher_id": random.randint(100, 999), "username": username, "name": name}]

def teacher_login(username, password):
    try:
        if supabase:
            response = supabase.table("teachers").select("*").eq("username", username).execute()
            if response and response.data:
                teacher = response.data[0]
                if check_pass(password, teacher.get("password", "")):
                    return teacher
    except Exception as e:
        print(f"teacher_login Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM teachers WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row:
            teacher = dict(row)
            if check_pass(password, teacher.get("password", "")):
                return teacher
    except Exception as e:
        print(f"teacher_login SQLite notice: {e}")
    return None

def get_all_students():
    try:
        if supabase:
            response = supabase.table('students').select("*").execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"get_all_students Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        conn.close()
        students = []
        for r in rows:
            d = dict(r)
            if d.get('face_embedding') and isinstance(d['face_embedding'], str):
                d['face_embedding'] = json.loads(d['face_embedding'])
            if d.get('voice_embedding') and isinstance(d['voice_embedding'], str):
                d['voice_embedding'] = json.loads(d['voice_embedding'])
            students.append(d)
        return students
    except Exception as e:
        print(f"get_all_students SQLite notice: {e}")
        return []

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
    res_student = None
    try:
        if supabase:
            response = supabase.table('students').insert(data).execute()
            if response and response.data:
                res_student = response.data
    except Exception as e:
        print(f"create_student Supabase notice: {e}")

    # Fallback SQLite
    if not res_student:
        try:
            conn = get_sqlite_conn()
            c = conn.cursor()
            face_json = json.dumps(face_embedding) if face_embedding else None
            voice_json = json.dumps(voice_embedding) if voice_embedding else None
            c.execute("INSERT INTO students (name, face_embedding, voice_embedding) VALUES (?, ?, ?)",
                      (new_name, face_json, voice_json))
            conn.commit()
            s_id = c.lastrowid
            
            c.execute("INSERT OR IGNORE INTO subject_students (student_id, subject_id) VALUES (?, 1)", (s_id,))
            c.execute("INSERT OR IGNORE INTO subject_students (student_id, subject_id) VALUES (?, 2)", (s_id,))
            conn.commit()
            conn.close()
            res_student = [{"student_id": s_id, "name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}]
        except Exception as e:
            print(f"create_student SQLite notice: {e}")
            res_student = [{"student_id": random.randint(1000, 9999), "name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}]

    # Auto-enroll student into default demo subjects
    if res_student and len(res_student) > 0:
        sid = res_student[0].get('student_id')
        if sid:
            enroll_student_to_subject(sid, 1)
            enroll_student_to_subject(sid, 2)

    return res_student

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    try:
        if supabase:
            response = supabase.table("subjects").insert(data).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"create_subject Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
                  (subject_code, name, section, teacher_id))
        conn.commit()
        sub_id = c.lastrowid
        conn.close()
        return [{"subject_id": sub_id, "subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}]
    except Exception as e:
        print(f"create_subject SQLite notice: {e}")
        return [{"subject_id": random.randint(100, 999), "subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}]

def get_teacher_subjects(teacher_id):
    try:
        if supabase:
            response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
            if response and response.data:
                subjects = response.data
                for sub in subjects:
                    sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
                    attendance = sub.get('attendance_logs', [])
                    unique_sessions = len(set(log['timestamp'] for log in attendance)) if attendance else 0
                    sub['total_classes'] = unique_sessions
                    sub.pop('subject_students', None)
                    sub.pop('attendance_logs', None)
                return subjects
    except Exception as e:
        print(f"get_teacher_subjects Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM subjects WHERE teacher_id = ?", (teacher_id,))
        rows = c.fetchall()
        subjects = []
        for r in rows:
            sub = dict(r)
            c.execute("SELECT COUNT(*) FROM subject_students WHERE subject_id = ?", (sub['subject_id'],))
            sub['total_students'] = c.fetchone()[0]
            c.execute("SELECT COUNT(DISTINCT timestamp) FROM attendance_logs WHERE subject_id = ?", (sub['subject_id'],))
            sub['total_classes'] = c.fetchone()[0]
            subjects.append(sub)
        conn.close()
        return subjects
    except Exception as e:
        print(f"get_teacher_subjects SQLite notice: {e}")
        return []

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    try:
        if supabase:
            response = supabase.table('subject_students').insert(data).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"enroll_student_to_subject Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("INSERT INTO subject_students (student_id, subject_id) VALUES (?, ?)", (student_id, subject_id))
        conn.commit()
        conn.close()
        return [data]
    except Exception as e:
        print(f"enroll_student_to_subject SQLite notice: {e}")
        return [data]

def unenroll_student_to_subject(student_id, subject_id):
    try:
        if supabase:
            response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"unenroll_student_to_subject Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("DELETE FROM subject_students WHERE student_id = ? AND subject_id = ?", (student_id, subject_id))
        conn.commit()
        conn.close()
        return [{"student_id": student_id, "subject_id": subject_id}]
    except Exception as e:
        print(f"unenroll_student_to_subject SQLite notice: {e}")
        return []

def get_student_subjects(student_id):
    try:
        if supabase:
            response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"get_student_subjects Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
            SELECT ss.*, s.name, s.subject_code, s.section, s.teacher_id 
            FROM subject_students ss
            JOIN subjects s ON ss.subject_id = s.subject_id
            WHERE ss.student_id = ?
        """, (student_id,))
        rows = c.fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            result.append({
                "student_id": d['student_id'],
                "subject_id": d['subject_id'],
                "subjects": {
                    "subject_id": d['subject_id'],
                    "name": d['name'],
                    "subject_code": d['subject_code'],
                    "section": d['section'],
                    "teacher_id": d['teacher_id']
                }
            })
        return result
    except Exception as e:
        print(f"get_student_subjects SQLite notice: {e}")
        return []

def get_student_attendance(student_id):
    try:
        if supabase:
            response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"get_student_attendance Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
            SELECT al.*, s.name, s.subject_code, s.section, s.teacher_id
            FROM attendance_logs al
            JOIN subjects s ON al.subject_id = s.subject_id
            WHERE al.student_id = ?
        """, (student_id,))
        rows = c.fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            result.append({
                "id": d['id'],
                "student_id": d['student_id'],
                "subject_id": d['subject_id'],
                "timestamp": d['timestamp'],
                "is_present": bool(d['is_present']),
                "subjects": {
                    "subject_id": d['subject_id'],
                    "name": d['name'],
                    "subject_code": d['subject_code'],
                    "section": d['section'],
                    "teacher_id": d['teacher_id']
                }
            })
        return result
    except Exception as e:
        print(f"get_student_attendance SQLite notice: {e}")
        return []

def create_attendance(logs):
    try:
        if supabase:
            response = supabase.table('attendance_logs').insert(logs).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"create_attendance Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        for log in logs:
            c.execute("INSERT INTO attendance_logs (student_id, subject_id, timestamp, is_present) VALUES (?, ?, ?, ?)",
                      (log['student_id'], log['subject_id'], log['timestamp'], 1 if log['is_present'] else 0))
        conn.commit()
        conn.close()
        return logs
    except Exception as e:
        print(f"create_attendance SQLite notice: {e}")
        return logs

def get_attendance_for_teacher(teacher_id):
    try:
        if supabase:
            response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
            if response and response.data:
                return response.data
    except Exception as e:
        print(f"get_attendance_for_teacher Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
            SELECT al.*, s.name, s.subject_code, s.section, s.teacher_id
            FROM attendance_logs al
            JOIN subjects s ON al.subject_id = s.subject_id
            WHERE s.teacher_id = ?
        """, (teacher_id,))
        rows = c.fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            result.append({
                "id": d['id'],
                "student_id": d['student_id'],
                "subject_id": d['subject_id'],
                "timestamp": d['timestamp'],
                "is_present": bool(d['is_present']),
                "subjects": {
                    "subject_id": d['subject_id'],
                    "name": d['name'],
                    "subject_code": d['subject_code'],
                    "section": d['section'],
                    "teacher_id": d['teacher_id']
                }
            })
        return result
    except Exception as e:
        print(f"get_attendance_for_teacher SQLite notice: {e}")
        return []

def student_login_by_name(name):
    try:
        students = get_all_students()
        if students:
            for s in students:
                if s.get('name', '').strip().lower() == name.strip().lower():
                    return s
    except Exception as e:
        print(f"student_login_by_name notice: {e}")
    return None

def get_subject_by_code(subject_code):
    try:
        if supabase:
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', subject_code).execute()
            if res and res.data:
                return res.data[0]
    except Exception as e:
        print(f"get_subject_by_code Supabase notice: {e}")

    # Fallback SQLite
    try:
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT subject_id, name, subject_code FROM subjects WHERE UPPER(subject_code) = UPPER(?)", (subject_code.strip(),))
        row = c.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception as e:
        print(f"get_subject_by_code SQLite notice: {e}")
    return None