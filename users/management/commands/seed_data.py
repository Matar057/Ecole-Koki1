from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import datetime
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Remplir la base de données avec des données exemples'

    def handle(self, *args, **kwargs):
        from academics.models import AcademicYear, Class, Section, Subject
        from students.models import Parent, Student
        from teachers.models import Teacher
        from attendance.models import Attendance
        from exams.models import Exam, ExamSubject, Mark
        from fees.models import FeeStructure, FeePayment
        from timetable.models import TimetableSlot
        from notifications.models import Announcement

        if Class.objects.filter(name='CI').exists():
            self.stdout.write(self.style.WARNING('Le seed a déjà été exécuté. Aucun utilisateur supprimé ne sera recréé.'))
            return

        self.stdout.write('Création des données exemples...')

        year, _ = AcademicYear.objects.get_or_create(
            name='2025-2026', defaults={'start_date': '2025-09-01', 'end_date': '2026-06-30', 'is_current': True}
        )

        admin, _ = User.objects.get_or_create(
            email='admin@ecole.sn',
            defaults={'username': 'admin', 'first_name': 'Amadou', 'last_name': 'Diallo', 'role': 'admin', 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin123')
        admin.save()

        classes_data = ['CI', 'CP1', 'CP2', 'CE1', 'CE2', 'CM1', 'CM2']
        classes = {}
        for name in classes_data:
            classes[name], _ = Class.objects.get_or_create(
                name=name,
                defaults={'academic_year': year, 'description': f'Classe de {name}'}
            )

        sections_data = [('A', 45), ('B', 45), ('C', 40)]
        for class_name, class_obj in classes.items():
            for name, capacity in sections_data:
                Section.objects.get_or_create(
                    name=name, class_obj=class_obj, defaults={'capacity': capacity}
                )

        subjects_data = [
            ('Français', 'FR'),
            ('Mathématiques', 'MATH'),
            ('Sciences', 'SCI'),
            ('Histoire-Géographie', 'HG'),
            ('Éducation civique', 'EC'),
            ('Éducation physique et sportive', 'EPS'),
            ('Arts', 'ART'),
            ('Langues nationales', 'LN'),
        ]
        subjects = {}
        for name, code in subjects_data:
            subjects[name], _ = Subject.objects.get_or_create(
                name=name, defaults={'code': code, 'description': f'Matière de {name}'}
            )
            for class_obj in classes.values():
                subjects[name].classes.add(class_obj)

        teachers_data = [
            ('Fatou', 'Ndiaye', 'fatou.ndiaye@ecole.sn', 'Français', 'CFEN'),
            ('Moussa', 'Sow', 'moussa.sow@ecole.sn', 'Mathématiques', 'CFEM'),
            ('Aïssatou', 'Ba', 'aissatou.ba@ecole.sn', 'Sciences', 'CFES'),
            ('Ibrahima', 'Fall', 'ibrahima.fall@ecole.sn', 'Histoire-Géographie', 'CFEG'),
            ('Mariama', 'Diallo', 'mariama.diallo@ecole.sn', 'Langues nationales', 'CFELN'),
        ]
        teachers = []
        for first, last, email, spec, qual in teachers_data:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'username': first.lower() + last.lower(), 'first_name': first, 'last_name': last, 'role': 'teacher'}
            )
            user.set_password('teacher123')
            user.save()
            teacher, _ = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'date_of_birth': '1985-01-15',
                    'gender': 'M' if first in ['Moussa', 'Ibrahima'] else 'F',
                    'qualification': qual,
                    'specialization': spec,
                    'experience_years': random.randint(3, 15),
                    'joining_date': '2020-01-01',
                    'phone': f'+221 77 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}'
                }
            )
            for subj_name, subj in subjects.items():
                if spec.lower() in subj_name.lower() or (
                    spec == 'Sciences' and subj_name in ['Sciences']
                ) or (
                    spec == 'Histoire-Géographie' and subj_name in ['Histoire-Géographie', 'Éducation civique']
                ):
                    teacher.subjects.add(subj)
            for i in range(2):
                teacher.classes_assigned.add(list(classes.values())[i])
            teachers.append(teacher)

        parents_data = [
            ('Abdoulaye', 'Touré', 'abdoulaye.toure@email.sn'),
            ('Aminata', 'Sy', 'aminata.sy@email.sn'),
            ('Ousmane', 'Mbaye', 'ousmane.mbaye@email.sn'),
            ('Khady', 'Diop', 'khady.diop@email.sn'),
            ('Cheikh', 'Gueye', 'cheikh.gueye@email.sn'),
        ]
        parents = []
        for first, last, email in parents_data:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'username': first.lower() + last.lower(), 'first_name': first, 'last_name': last, 'role': 'parent'}
            )
            user.set_password('parent123')
            user.save()
            parent, _ = Parent.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f'+221 76 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}',
                    'email': email,
                    'occupation': 'Employé'
                }
            )
            parents.append(parent)

        first_names = ['Aminata', 'Mouhamed', 'Fatoumata', 'Abdoulaye', 'Khadijetou', 'Papa Moussa',
                       'Aïssatou', 'Ibrahima', 'Mariama', 'Moussa',
                       'Ndeye Aïda', 'Oumar', 'Ramatoulaye', 'Serigne', 'Astou', 'Mamadou',
                       'Ndeye Fatou', 'Modou', 'Sokhna', 'Alioune']
        last_names = ['Ndiaye', 'Sow', 'Ba', 'Diallo', 'Fall', 'Gueye', 'Diop', 'Touré', 'Mbaye', 'Sy']
        class_names = list(classes.keys())
        students = []
        for i in range(35):
            first = first_names[i % len(first_names)]
            last = last_names[i % len(last_names)]
            email = f'{first.lower().replace(" ", ".")}.{last.lower()}{i}@eleve.ecole.sn'
            user, _ = User.objects.get_or_create(
                email=email, defaults={'username': f'eleve{i}', 'first_name': first, 'last_name': last, 'role': 'student'}
            )
            user.set_password('student123')
            user.save()
            class_obj = classes[class_names[i % len(class_names)]]
            section = Section.objects.filter(class_obj=class_obj).first()
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    'date_of_birth': datetime.date(2012 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    'gender': random.choice(['M', 'F']),
                    'blood_group': random.choice(['A+', 'B+', 'O+', 'AB+', 'A-', 'B-']),
                    'class_enrolled': class_obj,
                    'section': section,
                    'parent': random.choice(parents),
                    'address': f'Rue {random.randint(1, 50)}, Dakar',
                    'emergency_contact': f'+221 78 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}'
                }
            )
            students.append(student)

        compositions = [
            {
                'name': 'Composition 1er trimestre 2025-2026',
                'exam_type': 'compo_1',
                'start_date': '2025-10-27',
                'end_date': '2025-11-07',
                'description': 'Composition du premier trimestre',
            },
            {
                'name': 'Composition 2e trimestre 2025-2026',
                'exam_type': 'compo_2',
                'start_date': '2026-02-02',
                'end_date': '2026-02-13',
                'description': 'Composition du deuxième trimestre',
            },
            {
                'name': 'Composition 3e trimestre 2025-2026',
                'exam_type': 'compo_3',
                'start_date': '2026-05-04',
                'end_date': '2026-05-15',
                'description': 'Composition du troisième trimestre',
            },
        ]

        for compo_data in compositions:
            exam, _ = Exam.objects.get_or_create(
                name=compo_data['name'],
                defaults={
                    'exam_type': compo_data['exam_type'],
                    'academic_year': year,
                    'start_date': compo_data['start_date'],
                    'end_date': compo_data['end_date'],
                    'description': compo_data['description'],
                    'is_published': True if compo_data['exam_type'] == 'compo_1' else False,
                }
            )
            if ExamSubject.objects.filter(exam=exam).exists():
                continue
            for class_obj in classes.values():
                for subj in list(subjects.values())[:5]:
                    es = ExamSubject.objects.create(exam=exam, subject=subj, class_obj=class_obj, max_marks=20, passing_marks=10)
                    for student in students:
                        if student.class_enrolled == class_obj:
                            Mark.objects.create(
                                exam_subject=es, student=student,
                                marks_obtained=round(random.uniform(8, 19), 2), entered_by=admin
                            )

        for student in students:
            for days_back in range(5):
                date = datetime.date.today() - datetime.timedelta(days=days_back)
                Attendance.objects.create(
                    student=student, date=date,
                    status=random.choices(['present', 'absent', 'late', 'excused'], weights=[70, 15, 10, 5])[0],
                    recorded_by=admin
                )

        fee_struct, _ = FeeStructure.objects.get_or_create(
            name='Frais de scolarité T1',
            defaults={
                'class_obj': list(classes.values())[0],
                'academic_year': year,
                'amount': 25000,
                'due_date': '2025-10-01',
                'description': 'Frais de scolarité - Trimestre 1'
            }
        )
        for student in students[:15]:
            if student.class_enrolled == fee_struct.class_obj:
                FeePayment.objects.create(
                    student=student, fee_structure=fee_struct, amount_due=25000,
                    amount_paid=random.choice([0, 12500, 25000, 25000, 25000]),
                    payment_method=random.choice(['cash', 'bank_transfer', 'mobile_money']),
                    payment_date=datetime.date.today() if random.random() > 0.3 else None,
                    paid_by=admin
                )

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        times = [('08:00', '09:00'), ('09:00', '10:00'), ('10:00', '11:00'), ('11:00', '12:00'), ('13:00', '14:00'), ('14:00', '15:00')]
        class_obj = list(classes.values())[0]
        section = Section.objects.filter(class_obj=class_obj).first()
        if not TimetableSlot.objects.filter(class_obj=class_obj).exists():
            for day in days:
                for i, (start, end) in enumerate(times):
                    if i < len(teachers) and i < len(subjects):
                        subj = list(subjects.values())[i]
                        teach = teachers[i % len(teachers)]
                        TimetableSlot.objects.create(
                            class_obj=class_obj, section=section, subject=subj, teacher=teach,
                            day=day, start_time=start, end_time=end, room_number=f'{100 + i}'
                        )

        Announcement.objects.create(
            title='Bienvenue pour la nouvelle année scolaire !',
            content='Nous sommes ravis d\'accueillir tous les élèves, enseignants et parents pour l\'année scolaire 2025-2026.',
            priority='high', target_audience='all', created_by=admin, is_active=True
        )
        Announcement.objects.create(
            title='Planning des compositions 1er trimestre',
            content='Le planning des compositions du 1er trimestre a été publié. Veuillez consulter la section examens.',
            priority='medium', target_audience='students', created_by=admin, is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Données exemples créées avec succès !'))
        self.stdout.write(self.style.SUCCESS('\nIdentifiants de connexion :'))
        self.stdout.write(f'  Admin:     admin@ecole.sn / admin123')
        self.stdout.write(f'  Enseignant: fatou.ndiaye@ecole.sn / teacher123')
        self.stdout.write(f'  Élève:     aminata.ndiaye0@eleve.ecole.sn / student123')
        self.stdout.write(f'  Parent:    abdoulaye.toure@email.sn / parent123')
