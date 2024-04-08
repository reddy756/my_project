from flask import Blueprint,redirect,url_for,render_template,request,flash,session,abort,jsonify
from database import execute_query
from sendmail import send_email
from key import add_faculty_verify,update_faculty_verify
from ctokens import create_token,verify_token
import werkzeug.security as bcrypt

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')

@admin_bp.route('/dashboard')   
def dashboard():
    if session.get('role') == 'Admin':
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_departments')
def view_departments():
    if session.get('role') == 'Admin':
        query = """
        SELECT d.department_id, d.department_name, u.name AS incharge_name
        FROM departments d
        LEFT JOIN users u ON d.incharge_user_id = u.user_id
        """
        departments_details = execute_query(query)
        return render_template('admin/view_departments.html', departments_details=departments_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_courses')
def view_courses():
    if session.get('role') == 'Admin':
        query = """
        SELECT c.course_id, c.course_name, d.department_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.department_id
        """
        course_details = execute_query(query)
        return render_template('admin/view_courses.html', course_details=course_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/add_departments', methods=['GET', 'POST'])
def add_departments():
    if session.get('role') == 'Admin':
        faculty_details = execute_query("SELECT user_id, name FROM users WHERE role = 'Faculty' OR role = 'Department Incharge'")
        if request.method == 'POST':
            dept_name = request.form.get('dept_name').strip()
            incharge_id = request.form.get('incharge_id',type=int)

            if dept_name:
                existing_dept = execute_query("SELECT COUNT(*) as count FROM departments WHERE department_name = %s", (dept_name,),fetch_one=True)
                if existing_dept['count'] == 1:
                    flash('Department name already exists.')
                    return redirect(url_for('admin.add_departments'))
                existing_incharge = execute_query("Select COUNT(*) as count FROM departments WHERE incharge_user_id=%s",(incharge_id,),fetch_one=True)
                if existing_incharge ==1:
                    flash('Incharge Already Assigned to the other Department.')
                    return(redirect(url_for('admin.add_departments')))
                execute_query("INSERT INTO departments (department_name, incharge_user_id) VALUES (%s, %s)", (dept_name, incharge_id), commit=True)

                if incharge_id:
                    execute_query("UPDATE users SET role = 'Department Incharge' WHERE user_id = %s", (incharge_id,), commit=True)
                
                flash('Department added successfully.')
                return redirect(url_for('admin.view_departments'))
            else:
                flash('Department name is required.')
                return redirect(url_for('admin.add_departments'))
        return render_template('admin/add_departments.html', faculty_details=faculty_details)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/add_courses', methods=['GET', 'POST'])
def add_courses():
    if session.get('role') == 'Admin':
        departments = execute_query("SELECT department_id, department_name FROM departments")
        if request.method == 'POST':
            course_name = request.form.get('course_name').strip()
            dept_id = request.form.get('dept_id',type=int)

            if not course_name:
                flash('Course name is required.')
                return redirect(url_for('admin.add_courses'))

            if not dept_id:
                flash('Valid department is required.')
                return redirect(url_for('admin.add_courses'))

            existing_course = execute_query("SELECT COUNT(*) as count FROM courses WHERE course_name = %s AND department_id = %s", (course_name, dept_id),fetch_one=True)
            
            if existing_course['count'] == 1:
                flash('Course already exists in the selected department.')
                return redirect(url_for('admin.add_courses'))

            execute_query("INSERT INTO courses (course_name, department_id) VALUES (%s, %s)", (course_name, dept_id), commit=True)
            flash('Course added successfully.')
            return redirect(url_for('admin.view_courses'))
        
        return render_template('admin/add_courses.html', departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/update_department/<int:dept_id>', methods=['GET', 'POST'])
def update_department(dept_id):
    if session.get('role') == 'Admin':
        dept_details = execute_query("SELECT department_id, department_name, incharge_user_id FROM departments WHERE department_id = %s", (dept_id,), fetch_one=True)
        faculty = execute_query("SELECT user_id, name FROM users WHERE role IN ('Faculty', 'Department Incharge')")

        if request.method == 'POST':
            dept_name = request.form.get('dept_name').strip()
            incharge_id = request.form.get('incharge_id',type=int)

            if not dept_name:
                flash('Department name is required.')
                return render_template('admin/update_department.html', dept_details=dept_details, faculty=faculty)

            # Check if incharge is already assigned to another department
            if incharge_id:
                existing_incharge = execute_query("SELECT COUNT(*) as count FROM departments WHERE incharge_user_id = %s AND department_id != %s", (incharge_id, dept_id),fetch_one=True)
                if existing_incharge['count'] == 1:
                    flash('This incharge is already assigned to another department.')
                    return render_template('admin/update_department.html', dept_details=dept_details, faculty=faculty)

            # Update department name and incharge
            execute_query("UPDATE departments SET department_name = %s, incharge_user_id = %s WHERE department_id = %s", (dept_name, incharge_id, dept_id), commit=True)

            # Update the role of the new incharge
            if incharge_id:
                execute_query("UPDATE users SET role = 'Department Incharge' WHERE user_id = %s", (incharge_id,), commit=True)

            # Reset the role of the old incharge if changed
            if dept_details['incharge_user_id'] and dept_details['incharge_user_id'] != incharge_id:
                execute_query("UPDATE users SET role = 'Faculty' WHERE user_id = %s", (dept_details['incharge_user_id'],), commit=True)

            flash('Department updated successfully.')
            return redirect(url_for('admin.view_departments'))
        
        return render_template('admin/update_department.html', dept_details=dept_details, faculty=faculty)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
def update_course(course_id):
    if session.get('role') == 'Admin':
        course_details = execute_query("SELECT c.course_id, c.course_name, c.department_id, d.department_name FROM courses c LEFT JOIN departments d ON c.department_id = d.department_id WHERE c.course_id = %s", (course_id,), fetch_one=True)
        departments = execute_query("SELECT department_id, department_name FROM departments")

        if request.method == 'POST':
            course_name = request.form.get('course_name').strip()
            dept_id = request.form.get('dept_id',type=int)

            if not course_name:
                flash('Course name is required.')
                return render_template('admin/update_course.html', course_details=course_details, departments=departments)

            if not dept_id:
                flash('Valid department is required.')
                return render_template('admin/update_course.html', course_details=course_details, departments=departments)

            # Update the course details
            execute_query("UPDATE courses SET course_name = %s, department_id = %s WHERE course_id = %s", (course_name, dept_id, course_id), commit=True)
            flash('Course updated successfully.')
            return redirect(url_for('admin.view_courses'))
        
        return render_template('admin/update_course.html', course_details=course_details, departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_faculty')
def view_faculty():
    if session.get('role') == 'Admin':
        query = """
        SELECT f.faculty_id, u.name, u.email, u.role, d.department_name, c.course_name,c.course_id
        FROM faculty f
        JOIN users u ON f.user_id = u.user_id
        LEFT JOIN departments d ON f.department_id = d.department_id
        LEFT JOIN courses c ON f.course_id = c.course_id;
        """
        faculty_details = execute_query(query)
        return render_template('admin/view_faculty.html', faculty_details=faculty_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/dept_course/<int:dept_id>')
def get_courses_by_department(dept_id):
    if session.get('role') == 'Admin':
        courses = execute_query("SELECT course_id, course_name FROM courses WHERE department_id = %s", (dept_id,))
        return jsonify([{'course_id': course['course_id'], 'course_name': course['course_name']} for course in courses])
    else:
        return abort(403, 'Unauthorized access')
       
@admin_bp.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if session.get('role') == 'Admin':
        departments = execute_query("SELECT department_id, department_name FROM departments")
        if request.method == 'POST':
            name = request.form.get('name', None).strip()
            email = request.form.get('email', None).strip()
            role = request.form.get('role', None).strip()
            department_id = request.form.get('department_id','Null',type=int)
            course_id = request.form.get('course_id','Null',type=int)
            hashed_password = bcrypt.generate_password_hash('asdf1234', method='pbkdf2:sha256', salt_length=16)

            # Handling for Department Incharge and Faculty roles
            if role in ['Department Incharge', 'Faculty']:
                # For Department Incharge, check if an incharge already exists
                if role == 'Department Incharge':
                    incharge_count = execute_query("SELECT COUNT(*) as count FROM departments WHERE department_id=%s AND incharge_user_id IS NOT NULL", (department_id,), fetch_one=True)
                    if incharge_count['count'] == 1:
                        flash('Incharge already assigned for this department.')
                        return redirect(url_for('admin.add_faculty'))

            email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email=%s", (email,), fetch_one=True)['count']
            if email_count== 1:
                flash('Email Already Exists!')
                return redirect(url_for('admin.add_faculty'))
                
            data = {'Name': name, 'Email': email, 'Password': hashed_password, 'Role': role,'Department_id': department_id, 'Course_id': course_id}
            
            token = create_token(data, salt=add_faculty_verify)
            verify_url = url_for('admin.faculty_verify', token=token, _external=True)
            subject = 'Activate Your Account'
            body = f"Dear {name},\n\nYour account has been created with the temporary password: asdf1234\n\nPlease activate your account and set your own password by clicking the following link:\n{verify_url}"
            send_email(receiver_email=email, subject=subject, body=body)

            flash('Faculty added and verification email sent.')
            return redirect(url_for('admin.view_faculty'))

        return render_template('admin/add_faculty.html', departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))
    
@admin_bp.route('/faculty_verify/<token>', methods=['GET', 'POST'])
def faculty_verify(token):
    data = verify_token(token, salt=add_faculty_verify, expiration=86400)  # 24 hours for token expiration
    if data:
        user_exists = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s", (data['Email'],),fetch_one=True)['count']
        if user_exists==1:
            flash('User Already Registered! Please Login.')
            return redirect(url_for('auth.login'))

        # Insert into users table
        execute_query("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)", (data['Name'], data['Email'], data['Password'], data['Role']), commit=True)

        user_id = execute_query("SELECT user_id FROM users WHERE email=%s", (data['Email'],), fetch_one=True)['user_id']

        # Handle Department Incharge and Faculty specific actions
        if data['Role'] in ['Department Incharge', 'Faculty']:
            # Insert into faculty table
            execute_query("INSERT INTO faculty (user_id,department_id,course_id) VALUES (%s,%s,%s)", (user_id,data['Department_id'],data['Course_id']), commit=True)

        if data['Role'] == 'Department Incharge':
            # Update department with incharge_user_id
            execute_query("UPDATE departments SET incharge_user_id=%s WHERE department_id=%s", (user_id, data['Department_id']), commit=True)
            flash('You were added as Department Incharge')

        flash(f"You've successfully registered as {data['Role']}")
        return redirect(url_for('auth.login'))
    else:
        flash('Verification link expired or invalid.')
        return redirect(url_for('admin.add_faculty'))

@admin_bp.route('/update_faculty/<int:faculty_id>', methods=['GET', 'POST'])
def update_faculty(faculty_id):
    if session.get('role') == 'Admin':
        faculty_details = execute_query("SELECT f.faculty_id, u.name,u.user_id, u.email, u.role, d.department_name, c.course_name,c.course_id,f.department_id,f.course_id FROM faculty f JOIN users u ON f.user_id = u.user_id LEFT JOIN departments d ON f.department_id = d.department_id LEFT JOIN courses c ON f.course_id = c.course_id where faculty_id=%s", (faculty_id,), fetch_one=True)
        departments = execute_query("SELECT department_id, department_name FROM departments")
        print(faculty_details['course_id'])
        if request.method == 'POST':
            name = request.form.get('name').strip()
            email = request.form.get('email').strip()
            role = request.form.get('role').strip()
            department_id = request.form.get('department_id', type=int)
            course_id = request.form.get('course_id',type=int)
            data = {'Name': name,'Email': email,'Role': role,'Department_id': department_id,'Course_id':course_id,'Existing_user_id': faculty_details['user_id']}

            # Handling for Department Incharge and Faculty roles
            if role in ['Department Incharge', 'Faculty']:
                # For Department Incharge, check if an incharge already exists
                if role == 'Department Incharge':
                    incharge_count = execute_query("SELECT COUNT(*) as count FROM departments WHERE department_id=%s AND incharge_user_id IS NOT NULL", (department_id,), fetch_one=True)
                    if incharge_count['count'] == 1:
                        flash('Incharge already assigned for this department.')
                        return redirect(url_for('admin.update_faculty',faculty_id=faculty_id))
                    else:
                        execute_query("update departments set incharge_user_id=%s where department_id=%s",(faculty_details['user_id'],data['Department_id']),commit=True)
            if department_id==faculty_details['department_id'] and course_id!=faculty_details['course_id']:
                execute_query("UPDATE faculty set course_id=%s where department_id=%s and faculty_id=%s",(data['Course_id'],data['Department_id'],faculty_id),commit=True)
            elif department_id!=faculty_details['department_id'] and course_id==faculty_details['course_id']:
                execute_query("UPDATE faculty set department_id=%s where course_id=%s and faculty_id=%s",(data['Department_id'],data['Course_id'],faculty_id),commit=True)
            elif department_id!=faculty_details['department_id'] and course_id!=faculty_details['course_id']:
                execute_query("UPDATE faculty set department_id=%s, course_id=%s where faculty_id=%s",(data['Department_id'],data['Course_id'],faculty_id),commit=True)

            if email != faculty_details['email']:  # Check if email has changed
                # Ensure the new email doesn't already exist in the system
                email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s AND user_id != %s", (email, faculty_details['user_id']),fetch_one=True)['count']# Send email to verify the email change
                data['Email'] = email
                if email_count == 1:
                    flash('Email Already Exists!')
                    return render_template('admin/update_faculty.html', faculty_details=faculty_details, departments=departments)
                token = create_token(data, salt=update_faculty_verify)
                verify_url = url_for('admin.faculty_update_verify', token=token, _external=True)
                subject = 'Confirm Your Email Update'
                body = f"Dear {name},\n\nPlease confirm your email update by clicking the following link:\n{verify_url}"
                send_email(receiver_email=email, subject=subject, body=body)

                flash('Email Sent to Faculty new Email to update through the link Within 24 Hours.')
                return redirect(url_for('admin.view_faculty'))

            # Update faculty details without changing email
            execute_query("UPDATE users SET name = %s, role = %s WHERE user_id = %s", (name, role,data['Existing_user_id']), commit=True)
            flash('Faculty details updated successfully.')
            return redirect(url_for('admin.view_faculty'))

        return render_template('admin/update_faculty.html', faculty_details=faculty_details, departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/faculty_update_verify/<token>', methods=['GET', 'POST'])
def faculty_update_verify(token):
    data = verify_token(token, salt=update_faculty_verify, expiration=86400)  # 24 hours for token expiration
    if data:
        # Check if the new email is already registered
        email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s AND user_id = %s", (data['Email'], data['Existing_user_id']),fetchone=True)['count']
        if email_count ==1:
            flash('New Email Already Updated.')
            return redirect(url_for('auth.login'))

        # Update the user details in the database
        execute_query("UPDATE users SET email = %s WHERE user_id = %s",
                      (data['Email'], data['Existing_user_id']), commit=True)

        flash('Faculty email update verified successfully.')
        return redirect(url_for('auth.login'))
    else:
        flash('Verification link expired or invalid.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_department/<int:dept_id>', methods=['POST'])
def delete_department(dept_id):
    if session.get('role') == 'Admin':
        # Reset incharge_user_id before deleting the department
        execute_query("UPDATE departments SET incharge_user_id = NULL WHERE department_id = %s", (dept_id,), commit=True)
        execute_query("DELETE FROM departments WHERE department_id = %s", (dept_id,), commit=True)
        flash("Department deleted successfully.")
        return redirect(url_for('admin.view_departments'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if session.get('role') == 'Admin':
        execute_query("DELETE FROM courses WHERE course_id = %s", (course_id,), commit=True)
        flash("Course deleted successfully.")
        return redirect(url_for('admin.view_courses'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_faculty/<int:faculty_id>', methods=['POST'])
def delete_faculty(faculty_id):
    if session.get('role') == 'Admin':
        # Check if the faculty is an incharge, if so, reset the department's incharge_user_id   
        user_id = execute_query("Select user_id FROM faculty WHERE faculty_id = %s", (faculty_id,), fetch_one=True)['user_id']
        execute_query("DELETE FROM users WHERE user_id = %s AND role IN ('Faculty', 'Department Incharge')", (user_id,), commit=True)
        flash("Faculty member deleted successfully.")
        return redirect(url_for('admin.view_faculty'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))


@admin_bp.route('/view_invigilation_schedule')
def view_invigilation_schedule():
    if 'role' in session and session['role'] == 'Admin':
        query = """
        SELECT invig_schedule.schedule_id, u.name AS faculty_name, c.course_name, d.department_name, invig_schedule.date, invig_schedule.time_slot, r.room_number
FROM invigilation_schedule invig_schedule
JOIN faculty f ON invig_schedule.faculty_id = f.faculty_id
JOIN users u ON f.user_id = u.user_id
JOIN courses c ON invig_schedule.course_id = c.course_id
JOIN departments d ON f.department_id = d.department_id
JOIN rooms r ON invig_schedule.room_id = r.room_id
ORDER BY invig_schedule.date, invig_schedule.time_slot
        """
        schedule = execute_query(query)
        return render_template('admin/view_invigilation_schedule.html', schedule=schedule)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))


@admin_bp.route('/assign_invigilation', methods=['GET'])
def assign_invigilation():
    if 'role' in session and session['role'] == 'Admin':
        faculty_list = execute_query("SELECT f.faculty_id, u.name FROM faculty f JOIN users u ON f.user_id = u.user_id")
        course_list = execute_query("SELECT course_id, course_name FROM courses")
        room_list = execute_query("SELECT room_id, room_number FROM rooms")
        return render_template('admin/assign_invigilation.html', faculty_list=faculty_list, course_list=course_list, room_list=room_list)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/submit_invigilation_assignment', methods=['POST'])
def submit_invigilation_assignment():
    if 'role' in session and session['role'] == 'Admin':
        faculty_id = request.form.get('faculty_id')
        course_id = request.form.get('course_id')  # Assuming you want to record which course's exam they are invigilating
        room_id = request.form.get('room_id')
        date = request.form.get('date')
        time_slot = request.form.get('time_slot')

        execute_query("INSERT INTO invigilation_schedule (faculty_id, course_id, room_id, date, time_slot) VALUES (%s, %s, %s, %s, %s)",(faculty_id, course_id, room_id, date, time_slot), commit=True)

        faculty = execute_query("SELECT u.name,u.email FROM faculty f JOIN users u ON f.user_id = u.user_id where f.faculty_id=%s",(faculty_id,),fetch_one=True)
        course = execute_query("select course_name from courses where course_id=%s",(course_id,),fetch_one=True)['course_name']
        room_num = execute_query("Select room_number from rooms where room_id=%s",(room_id,),fetch_one=True)['room_number']
        subject = "You're Assigned with Invigilation Duty"
        body = f"Hi {faculty['name']}!\n You're Assigned with Invigilation Duty for the {course} at {time_slot} on {date} in room no {room_num}."
        send_email(receiver_email=faculty['email'],subject=subject,body=body)  

        flash('Invigilation duty assigned successfully.')
        return redirect(url_for('admin.view_invigilation_schedule'))
    else:
        flash('Please login as an admin to perform this action.')
        return redirect(url_for('auth.login'))


@admin_bp.route('/view_adjustment_requests')
def view_adjustment_requests():
    if 'role' in session and session['role'] == 'Admin':
        query = """
        SELECT ar.request_id,
       u1.name AS requesting_faculty,
       u2.name AS requested_faculty,
       ar.status,
       is1.date AS original_date,
       is1.time_slot AS original_time
FROM adjustment_requests ar
JOIN invigilation_schedule is1 ON ar.original_schedule_id = is1.schedule_id
JOIN faculty f1 ON ar.requested_by = f1.faculty_id
JOIN faculty f2 ON ar.requested_to = f2.faculty_id
JOIN users u1 ON f1.user_id = u1.user_id
JOIN users u2 ON f2.user_id = u2.user_id
WHERE ar.status = 'pending';

        """
        requests = execute_query(query)
        return render_template('admin/view_adjustment_requests.html', requests=requests)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/approve_adjustment_request/<int:request_id>', methods=['POST'])
def approve_adjustment_request(request_id):
    if 'role' in session and session['role'] == 'Admin':
        execute_query("UPDATE adjustment_requests SET status = 'accepted' WHERE request_id = %s", (request_id,), commit=True)
        flash('Adjustment request approved.')
        return redirect(url_for('admin.view_adjustment_requests'))

@admin_bp.route('/reject_adjustment_request/<int:request_id>', methods=['POST'])
def reject_adjustment_request(request_id):
    if 'role' in session and session['role'] == 'Admin':
        execute_query("UPDATE adjustment_requests SET status = 'rejected' WHERE request_id = %s", (request_id,), commit=True)
        flash('Adjustment request rejected.')
        return redirect(url_for('admin.view_adjustment_requests'))

@admin_bp.route('/record_absentees', methods=['GET', 'POST'])
def record_absentees():
    if 'role' in session and session['role'] == 'Admin':
        if request.method == 'POST':
            schedule_id = request.form.get('schedule_id')
            absentee_count = request.form.get('absentee_count', type=int)
            reason = request.form.get('reason', '')

            execute_query("INSERT INTO absentee_records (schedule_id, absentee_count, reason) VALUES (%s, %s, %s)", 
                          (schedule_id, absentee_count, reason), commit=True)
            flash('Absentee record updated successfully.')
            return redirect(url_for('admin.record_absentees'))

        invigilation_schedules = execute_query("SELECT schedule_id, date, time_slot FROM invigilation_schedule ORDER BY date, time_slot")
        return render_template('admin/record_absentees.html', invigilation_schedules=invigilation_schedules)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/absentee_report')
def absentee_report():
    if 'role' in session and session['role'] == 'Admin':
        query = """
        SELECT ar.record_id, inv_sched.schedule_id, u.name AS faculty_name, inv_sched.date, inv_sched.time_slot, ar.absentee_count, ar.reason
FROM absentee_records ar
JOIN invigilation_schedule inv_sched ON ar.schedule_id = inv_sched.schedule_id
JOIN faculty f ON inv_sched.faculty_id = f.faculty_id
JOIN users u ON f.user_id = u.user_id
ORDER BY inv_sched.date, inv_sched.time_slot;

        """
        absentee_records = execute_query(query)
        return render_template('admin/absentee_report.html', absentee_records=absentee_records)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/invigilation_load_report')
def invigilation_load_report():
    if 'role' in session and session['role'] == 'Admin':
        query = """
        SELECT u.name AS faculty_name, COUNT(inv_sched.schedule_id) AS duty_count
FROM faculty f
JOIN invigilation_schedule inv_sched ON f.faculty_id = inv_sched.faculty_id
JOIN users u ON f.user_id = u.user_id
GROUP BY f.faculty_id, u.name
ORDER BY duty_count DESC;

        """
        load_report = execute_query(query)
        return render_template('admin/invigilation_load_report.html', load_report=load_report)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/invigilation_overview')
def invigilation_overview():
    if 'role' in session and session['role'] == 'Admin':
        # Sample queries for generating analytics
        adjustment_requests_query = "SELECT status, COUNT(*) as count FROM adjustment_requests GROUP BY status;"
        absentee_trends_query = """SELECT inv_sched.date, COUNT(*) AS count
FROM absentee_records ar
JOIN invigilation_schedule inv_sched ON ar.schedule_id = inv_sched.schedule_id
GROUP BY inv_sched.date
ORDER BY inv_sched.date;
"""

        adjustment_requests_stats = execute_query(adjustment_requests_query)
        absentee_trends = execute_query(absentee_trends_query)

        return render_template('admin/invigilation_overview.html',
                               adjustment_requests_stats=adjustment_requests_stats,
                               absentee_trends=absentee_trends)
    else:
        flash('Please login as an admin to view this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/automate_invigilation_allocation')
def automate_invigilation_allocation():
    if 'role' in session and session['role'] == 'Admin':
        # Fetch available faculties and invigilation slots
        faculties = execute_query("SELECT faculty_id FROM faculty WHERE is_available = 1")
        slots = execute_query("SELECT schedule_id, date, time_slot FROM invigilation_schedule WHERE faculty_id IS NULL")

        # Example of a simple allocation process
        for slot in slots:
            for faculty in faculties:
                # Check if the faculty is already assigned to the maximum number of duties
                duty_count = execute_query("SELECT COUNT(*) as count FROM invigilation_schedule WHERE faculty_id = %s", (faculty['faculty_id'],), fetch_one=True)
                
                # Assuming 'max_duties' is a field in the faculty table indicating the max number of invigilation duties allowed
                max_duties = execute_query("SELECT max_duties FROM faculty WHERE faculty_id = %s", (faculty['faculty_id'],), fetch_one=True)
                
                if duty_count['count'] < max_duties['max_duties']:
                    # Assign the faculty to this slot and break the loop to move to the next slot
                    execute_query("UPDATE invigilation_schedule SET faculty_id = %s WHERE schedule_id = %s", (faculty['faculty_id'], slot['schedule_id']), commit=True)
                    break

        flash('Invigilation duties allocated successfully.')
        return redirect(url_for('admin.dashboard'))
    else:
        flash('Please login as an admin to perform this action.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if 'role' in session and session['role'] == 'Admin':
        if request.method == 'POST':
            room_number = request.form.get('room_number')
            is_available = request.form.get('is_available', type=bool, default=True)
            # Add room data to the database
            execute_query("INSERT INTO rooms (room_number, is_available) VALUES (%s, %s)", (room_number, is_available), commit=True)
            flash('Room added successfully.')
            return redirect(url_for('admin.view_rooms'))
        return render_template('admin/add_room.html')
    else:
        flash('Access denied. Please login as an admin.')
        return redirect(url_for('auth.login'))


@admin_bp.route('/update_room/<int:room_id>', methods=['GET', 'POST'])
def update_room(room_id):
    if 'role' in session and session['role'] == 'Admin':
        room = execute_query("SELECT room_id, room_number, is_available FROM rooms WHERE room_id = %s", (room_id,), fetch_one=True)

        if request.method == 'POST':
            room_number = request.form.get('room_number')
            is_available = request.form.get('is_available', type=bool)
            
            execute_query("UPDATE rooms SET room_number = %s, is_available = %s WHERE room_id = %s", 
                          (room_number, is_available, room_id), commit=True)
            flash('Room updated successfully.')
            return redirect(url_for('admin.view_rooms'))

        return render_template('admin/update_room.html', room=room)
    else:
        flash('Access denied. Please login as an admin.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    if 'role' in session and session['role'] == 'Admin':
        execute_query("DELETE FROM rooms WHERE room_id = %s", (room_id,), commit=True)
        flash('Room deleted successfully.')
        return redirect(url_for('admin.view_rooms'))
    else:
        flash('Access denied. Please login as an admin.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_rooms')
def view_rooms():
    if 'role' in session and session['role'] == 'Admin':
        rooms = execute_query("SELECT room_id, room_number, is_available FROM rooms ORDER BY room_number")
        return render_template('admin/view_rooms.html', rooms=rooms)
    else:
        flash('Access denied. Please login as an admin.')
        return redirect(url_for('auth.login'))



@admin_bp.route('/logout')
def logout():
    if session.get('role')=='Admin':
        session.pop('role')
        session.pop('user_id')
        session.clear()
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))

