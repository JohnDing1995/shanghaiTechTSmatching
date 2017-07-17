from .models import Students, Teachers, Selection

# This class is used for checking the teacher users
# update the data of teacher in the database
class TeacherHandle:
    def __init__(self, name, pwd=''):
        try:
            result = Teachers.objects.get(name=name)
            if not result:
                self.__can_login = False
            else:
                self.__name = result.name
                self.__password = result.password
                self.__id = result.id
                self.__can_login = self.__password == pwd
        except Teachers.DoesNotExist:
            self.__can_login = False

    def __str__(self):
        return self.__name

    # check the pwd of a teacher
    def can_login(self):
        return self.__can_login

    # Get information of the student
    @staticmethod
    def get_student_info(stu):
        stu_info_obj = Students.objects.get(user_name=stu.student.user_name)

        return {
            'name': stu_info_obj.name,
            'school': stu_info_obj.university,
            'GPA': stu_info_obj.gpa,
            'phone_number': stu_info_obj.phone_number,
            'we_chat': stu_info_obj.email,
            'description': stu_info_obj.comment
        }

    # Get student object
    @staticmethod
    def get_student_obj(stu):
        # Get student object
        return Students.objects.get(name=stu)

    # get the students that prefer this teacher
    def get_students(self):
        # Get the students that has not been accepted
        stu_list = Selection.objects.all().filter(student__accepted=0)

        # The result to store the students' info
        ret = []
        # Select out students that prefer this teacher now
        # we use deferred acceptance algorithm to determine which student should be expose
        # to this teacher
        # if this teacher has no more places, we'll reject all the students rest
        tea_obj = Teachers.objects.get(id=self.__id)
        if tea_obj.recruit_number <= 0:
            for stu in stu_list:
                self.reject(stu.student_id.name)
            return ret
        for stu in stu_list:
            # check if the student has selected this teacher
            # Check first choice
            if not stu.first_rejected:
                # According to DA algorithm,
                # student can apply for the teacher he prefer most,
                # while the teacher doesn't reject him
                if stu.first.name == self.__name:
                    ret.append(TeacherHandle.get_student_info(stu))
            elif not stu.second_rejected:
                if stu.second.name == self.__name:
                    ret.append(TeacherHandle.get_student_info(stu))
            elif not stu.third_rejected:
                if stu.third.ame == self.__name:
                    ret.append(TeacherHandle.get_student_info(stu))

        return ret

    # Accept the student:stu
    def accept(self, stu):
        # Get teacher object
        tea_obj = Teachers.objects.get(id=self.__id)
        # Judge whether this teacher can recruit more students
        if tea_obj.recruit_number <= 0:
            err = 'Your accepted students has up to limit, please reject one student and get to continue'
            return [False, err]

        # Get student object
        stu_obj = Students.objects.all().get(name=stu)
        # Set stu's adviser to this teacher
        stu_obj.accepted = self.__id

        # Decrease the recruit number of this teacher
        tea_obj.recruit_number = tea_obj.recruit_number - 1

        # Save all the changes
        stu_obj.save()
        tea_obj.save()

        return [True, '']

    # Reject the student stu
    def reject(self, stu):
        # Get student and teacher object
        tea_obj = Teachers.objects.get(id=self.__id)
        stu_obj = Students.objects.get(name=stu)
        # Update status of student
        stu_obj.accepted = 0
        # Update selection table
        stu_select = Selection.objects.get(student_id=stu_obj.user_name)
        if not stu_select.first_rejected:
            stu_select.first_rejected = True
        elif not stu_select.second_rejected:
            stu_select.second_rejected = True
        elif not stu_select.third_rejected:
            stu_select.third_rejected = True
        if tea_obj.recruit_number < 2:
            tea_obj.recruit_number = tea_obj.recruit_number + 1

        # Save all the changes
        stu_obj.save()
        tea_obj.save()
        stu_select.save()
