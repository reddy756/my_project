from flask import Blueprint, render_template, session, redirect, url_for, flash,request
from database import execute_query

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@faculty_bp.route('/dashboard')
def dashboard():
    faculty_id = execute_query("Select faculty_id from faculty where user_id=%s",(session.get('user_id'),),fetch_one=True)['faculty_id']
    session['faculty_id'] = faculty_id
    return render_template('faculty/dashboard.html')

@faculty_bp.route('/my_schedule')
def my_schedule():
    if 'role' in session and session['role'] == 'Faculty':
        faculty_id = session.get('faculty_id')
        print(faculty_id)
        query = """
        SELECT inv_sched.schedule_id, inv_sched.date, inv_sched.time_slot, r.room_number
FROM invigilation_schedule inv_sched
JOIN rooms r ON inv_sched.room_id = r.room_id
WHERE inv_sched.faculty_id = %s
ORDER BY inv_sched.date, inv_sched.time_slot;
        """
        schedule = execute_query(query, (faculty_id,))
        return render_template('faculty/my_schedule.html', schedule=schedule)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/request_adjustment', methods=['GET', 'POST'])
def request_adjustment():
    if 'role' in session and session['role'] == 'Faculty':
        if request.method == 'POST':
            schedule_id = request.form.get('schedule_id')
            requested_to = request.form.get('requested_to')  # faculty_id of the colleague
            reason = request.form.get('reason')
            # Insert adjustment request into the database
            execute_query("INSERT INTO adjustment_requests (original_schedule_id, requested_by, requested_to, reason) VALUES (%s, %s, %s, %s)",
                          (schedule_id, session['faculty_id'], requested_to, reason), commit=True)
            flash('Adjustment request submitted.')
            return redirect(url_for('faculty.my_schedule'))

        schedule = execute_query("SELECT schedule_id, date, time_slot FROM invigilation_schedule WHERE faculty_id = %s", (session['faculty_id'],))
        colleagues = execute_query("""SELECT f.faculty_id, u.name
FROM faculty f
JOIN users u ON f.user_id = u.user_id
WHERE f.faculty_id != %s
""", (session['faculty_id'],))
        return render_template('faculty/request_adjustment.html', schedule=schedule, colleagues=colleagues)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/report_absentee', methods=['GET', 'POST'])
def report_absentee():
    if 'role' in session and session['role'] == 'Faculty':
        if request.method == 'POST':
            schedule_id = request.form.get('schedule_id')
            absentee_count = request.form.get('absentee_count', type=int)
            reason = request.form.get('reason', '')

            execute_query("INSERT INTO absentee_records (schedule_id, absentee_count, reason) VALUES (%s, %s, %s)", 
                          (schedule_id, absentee_count, reason), commit=True)
            flash('Absentee reported successfully.')
            return redirect(url_for('faculty.my_schedule'))

        schedule = execute_query("SELECT schedule_id, date, time_slot FROM invigilation_schedule WHERE faculty_id = %s", (session['faculty_id'],))
        return render_template('faculty/report_absentee.html', schedule=schedule)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/adjustment_status')
def adjustment_status():
    if 'role' in session and session['role'] == 'Faculty':
        faculty_id = session.get('faculty_id')
        query = """
        SELECT ar.request_id, ar.status, is1.date AS original_date, is1.time_slot AS original_time
FROM adjustment_requests ar
JOIN invigilation_schedule is1 ON ar.original_schedule_id = is1.schedule_id
WHERE ar.requested_by = %s
ORDER BY ar.request_id DESC;

        """
        requests = execute_query(query, (faculty_id,))
        return render_template('faculty/adjustment_status.html', requests=requests)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/historical_records')
def historical_records():
    if 'role' in session and session['role'] == 'Faculty':
        faculty_id = session.get('faculty_id')
        query = """
        SELECT inv_sched.schedule_id, inv_sched.date, inv_sched.time_slot, r.room_number
FROM invigilation_schedule inv_sched
JOIN rooms r ON inv_sched.room_id = r.room_id
WHERE inv_sched.faculty_id = %s
ORDER BY inv_sched.date DESC, inv_sched.time_slot DESC;

        """
        history = execute_query(query, (faculty_id,))
        return render_template('faculty/historical_records.html', history=history)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'role' in session and session['role'] == 'Faculty':
        if request.method == 'POST':
            feedback = request.form.get('feedback')
            faculty_id = session.get('faculty_id')
            # Assuming there is a feedback table with columns for faculty_id, feedback, and timestamp
            execute_query("INSERT INTO feedback (faculty_id, feedback, timestamp) VALUES (%s, %s, NOW())", (faculty_id, feedback), commit=True)
            flash('Feedback submitted successfully.')
            return redirect(url_for('faculty.submit_feedback'))

        return render_template('faculty/submit_feedback.html')
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/my_statistics')
def my_statistics():
    if 'role' in session and session['role'] == 'Faculty':
        faculty_id = session.get('faculty_id')
        query = """
        SELECT COUNT(*) AS total_duties,
       SUM(TIME_TO_SEC(TIMEDIFF(STR_TO_DATE(SUBSTRING_INDEX(time_slot, '-', -1), '%H:%i'),STR_TO_DATE(SUBSTRING_INDEX(time_slot, '-', 1), '%H:%i')))/3600) AS total_hours,ROUND(AVG(TIME_TO_SEC(TIMEDIFF(STR_TO_DATE(SUBSTRING_INDEX(time_slot, '-', -1), '%H:%i'), STR_TO_DATE(SUBSTRING_INDEX(time_slot, '-', 1), '%H:%i')))/3600),2) AS average_duration FROM invigilation_schedule WHERE faculty_id = %s;
        """
        stats = execute_query(query, (faculty_id,),fetch_one=True)
        return render_template('faculty/my_statistics.html', stats=stats)
    else:
        flash('Access denied. Please login as faculty.')
        return redirect(url_for('auth.login'))

@faculty_bp.route('/logout')
def logout():
    if session.get('role')=='Faculty':
        session.pop('role')
        session.pop('user_id')
        session.clear()
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))
