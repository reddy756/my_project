from flask import Blueprint, render_template, session, redirect, url_for, flash,request
from database import execute_query

incharge_bp = Blueprint('incharge', __name__, url_prefix='/incharge')



@incharge_bp.route('/dashboard')
def dashboard():
    department_id = execute_query("Select department_id from departments where incharge_user_id=%s",(session.get('user_id'),),fetch_one=True)['department_id']
    session['department_id'] = department_id
    return render_template('incharge/dashboard.html')

@incharge_bp.route('/view_schedule')
def view_schedule():
    if 'role' in session and session['role'] == 'Department Incharge':
        department_id = session.get('department_id')
        print(department_id)
        query = """
        SELECT inv_sched.schedule_id, u.name AS faculty_name, inv_sched.date, inv_sched.time_slot, r.room_number
FROM invigilation_schedule inv_sched
JOIN faculty f ON inv_sched.faculty_id = f.faculty_id
JOIN rooms r ON inv_sched.room_id = r.room_id
JOIN users u ON f.user_id = u.user_id
WHERE f.department_id = %s
ORDER BY inv_sched.date, inv_sched.time_slot;


        """
        schedule = execute_query(query, (department_id,))
        return render_template('incharge/view_schedule.html', schedule=schedule)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

@incharge_bp.route('/update_faculty_availability', methods=['GET', 'POST'])
def update_faculty_availability():
    if 'role' in session and session['role'] == 'Department Incharge':
        if request.method == 'POST':
            faculty_id = request.form.get('faculty_id')
            is_available = request.form.get('is_available')  # Assume this is a boolean or similar
            execute_query("UPDATE faculty SET is_available = %s WHERE faculty_id = %s", (is_available, faculty_id), commit=True)
            flash('Faculty availability updated.')
            return redirect(url_for('incharge.update_faculty_availability'))

        faculty_list = execute_query("SELECT f.faculty_id, u.name, f.is_available FROM faculty f JOIN users u ON f.user_id = u.user_id WHERE f.department_id =%s", (session.get('department_id'),))
        return render_template('incharge/update_faculty_availability.html', faculty_list=faculty_list)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

@incharge_bp.route('/adjustment_requests')
def adjustment_requests():
    if 'role' in session and session['role'] == 'Department Incharge':
        department_id = session.get('department_id')
        query = """
        SELECT ar.request_id, u1.name AS requesting_faculty, u2.name AS requested_faculty, ar.status
FROM adjustment_requests ar
JOIN faculty f1 ON ar.requested_by = f1.faculty_id
JOIN faculty f2 ON ar.requested_to = f2.faculty_id
JOIN users u1 ON f1.user_id = u1.user_id
JOIN users u2 ON f2.user_id = u2.user_id
WHERE f1.department_id = %s AND ar.status = 'pending';

        """
        requests = execute_query(query, (department_id,))
        return render_template('incharge/adjustment_requests.html', requests=requests)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

@incharge_bp.route('/record_absentee', methods=['GET', 'POST'])
def record_absentee():
    if 'role' in session and session['role'] == 'Department Incharge':
        if request.method == 'POST':
            schedule_id = request.form.get('schedule_id')
            absentee_count = request.form.get('absentee_count', type=int)
            reason = request.form.get('reason', '')

            execute_query("INSERT INTO absentee_records (schedule_id, absentee_count, reason) VALUES (%s, %s, %s)", 
                          (schedule_id, absentee_count, reason), commit=True)
            flash('Absentee recorded successfully.')
            return redirect(url_for('incharge.record_absentee'))

        schedules = execute_query("""SELECT inv_sched.schedule_id, inv_sched.date, inv_sched.time_slot
FROM invigilation_schedule inv_sched
JOIN faculty f ON inv_sched.faculty_id = f.faculty_id
WHERE f.department_id = %s
ORDER BY inv_sched.date, inv_sched.time_slot;

""", (session.get('department_id'),))
        return render_template('incharge/record_absentee.html', schedules=schedules)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

@incharge_bp.route('/department_reports')
def department_reports():
    if 'role' in session and session['role'] == 'Department Incharge':
        department_id = session.get('department_id')
        # Example query for fetching invigilation workload per faculty in the department
        query = """
        SELECT u.name, COUNT(inv_sched.schedule_id) AS duties_count
FROM faculty f
LEFT JOIN invigilation_schedule inv_sched ON f.faculty_id = inv_sched.faculty_id
JOIN users u ON f.user_id = u.user_id
WHERE f.department_id = %s
GROUP BY f.faculty_id, u.name;

        """
        workload_report = execute_query(query, (department_id,))
        return render_template('incharge/department_reports.html', workload_report=workload_report)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

@incharge_bp.route('/message_faculty', methods=['GET', 'POST'])
def message_faculty():
    if 'role' in session and session['role'] == 'Department Incharge':
        incharge_name = execute_query("SELECT u.name FROM faculty f JOIN users u ON f.user_id = u.user_id WHERE u.user_id =%s", (session.get('user_id'),),fetch_one=True)['name']
        if request.method == 'POST':
            faculty_id = request.form.get('faculty_id')
            message = request.form.get('message')
            subject = f"Message From {incharge_name}"
            faculty_email = execute_query("SELECT u.email FROM faculty f JOIN users u ON f.user_id = u.user_id WHERE f.faculty_id =%s", (faculty_id,),fetch_one=True)['email']
            # Example function to send a message (implementation depends on your system's communication method)
            send_email(receiver_email=faculty_email,subject=subject, body=message)
            flash('Message sent successfully.')
            return redirect(url_for('incharge.message_faculty'))

        faculty_list = execute_query("SELECT f.faculty_id, u.name, f.is_available FROM faculty f JOIN users u ON f.user_id = u.user_id WHERE f.department_id =%s", (session.get('department_id'),))
        return render_template('incharge/message_faculty.html', faculty_list=faculty_list)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))

        
@incharge_bp.route('/manage_rooms', methods=['GET', 'POST'])
def manage_rooms():
    if 'role' in session and session['role'] == 'Department Incharge':
        if request.method == 'POST':
            room_id = request.form.get('room_id')
            is_available = request.form.get('is_available')  # Assume this is a boolean or similar
            execute_query("UPDATE rooms SET is_available = %s WHERE room_id = %s", (is_available, room_id), commit=True)
            flash('Room status updated successfully.')
            return redirect(url_for('incharge.manage_rooms'))

        room_list = execute_query("SELECT room_id, room_number, is_available FROM rooms")
        return render_template('incharge/manage_rooms.html', room_list=room_list)
    else:
        flash('Access denied. Please login as a department incharge.')
        return redirect(url_for('auth.login'))


@incharge_bp.route('/logout')
def logout():
    if session.get('role')=='Department Incharge':
        session.pop('role')
        session.pop('user_id')
        session.clear()
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))
