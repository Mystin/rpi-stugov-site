import random
import string

from branches.models import (
    Role, 
    MemberProfile, 
    MemberRoleAssignment, 
    RolePlacement, 
    MembershipDisplay, 
    BranchPage,
    MemberListingPage,
    CommitteeIndexPage,
    CommitteePage,
    ClassCouncilIndexPage,
    ClassCouncilPage,
    FlexiblePage,
    class_choices
)

from forms_ext.models import (
    ComplaintFormPage,
    FormField
)

from records.models import (
    RecordIndexPage
)

from rep_finder.models import (
    RepsFormPage
)

from home.models import (
    SiteSettings
)

from wagtail.models import Page

db_classes = [
    Role, 
    MemberProfile, 
    MemberRoleAssignment,
    BranchPage,
    ClassCouncilPage,
    ClassCouncilIndexPage,
    MemberListingPage,
    CommitteePage,
    CommitteeIndexPage,
    RolePlacement,
    RepsFormPage,
    RecordIndexPage,
    ComplaintFormPage
]

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Seed database with randomly generated data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the existing data from the database.",
        )
        
    def handle(self, *args, **options):
        if options["clear"]:
            for db_class in db_classes:
                print(f"deleted all {db_class}")
                db_class.objects.all().delete()

        random.seed(12180)

        senators_list = []

        root_page = Page.objects.get(title="Home").specific

        senate_branch_page = BranchPage(
            branch_type="senate",
            tagline="The senate branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="gm@rpi.edu",
            meeting_schedule="",
            title="Senate",
            slug="senate",
            show_in_menus=True
        )

        root_page.add_child(instance=senate_branch_page)

        senate_member_page = MemberListingPage(
            title="Senate Member List",
            slug="senate_member_list",
            intro="The members of the Senate.",
            show_in_menus=True
        )
        
        senate_branch_page.add_child(instance=senate_member_page)

        senate_committee_page = CommitteeIndexPage(
            title="Senate Committee List",
            slug="senate_committee_list",
            intro="The committees of the Senate.",
            show_in_menus=True
        )

        senate_branch_page.add_child(instance=senate_committee_page)

        uc_branch_page = BranchPage(
            branch_type="uc",
            tagline="The undergraduate council branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="uc@rpi.edu",
            meeting_schedule="",
            title="Undergraduate Council",
            slug="uc",
            show_in_menus=True
        )

        root_page.add_child(instance=uc_branch_page)

        class_council_list_page = ClassCouncilIndexPage(
            title="Class Council Index",
            slug="class_council_index",
            intro="Index of all class councils.",
            show_in_menus=True
        )

        uc_branch_page.add_child(instance=class_council_list_page)

        uc_member_page = MemberListingPage(
            title="Undergraduate Council Member List",
            slug="uc_member_list",
            intro="The members of the Undergraduate Council.",
            show_in_menus=True
        )

        uc_branch_page.add_child(instance=uc_member_page)

        name = f"Undergraduate President"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")
        new_person = self.make_person(class_choices()[0][0])
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        RolePlacement.objects.create(
            role=role,
            display_name="President",
            tier=0,
            page=uc_member_page
        )

        name = f"Undergraduate Vice President"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")
        new_person = self.make_person(class_choices()[0][0])
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        RolePlacement.objects.create(
            role=role,
            display_name="Vice President",
            tier=1,
            page=uc_member_page
        )

        for officer in ["Secretary", "Treasurer", "Publicity Director"]:
            name = f"{officer}"
            role, created = Role.objects.update_or_create(
                role_code="uc-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": "uc-"+'-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=f"{officer}",
                tier=1,
                page=uc_member_page
            )

        for class_num, _ in class_choices():
            if class_num == "graduate": continue
            
            class_council_page = ClassCouncilPage(
                title=f"Class of {class_num} Council",
                slug=f"{class_num}_class_council",
                class_year=class_num,
                description=f"The class council for the class of {class_num}."
            )
    
            class_council_list_page.add_child(instance=class_council_page)
            
            name = f"Class of {class_num} Representative"
            role, created = Role.objects.update_or_create(
                role_code=f"{class_num}-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": f"{class_num}-"+'-'.join(name.lower().split(" ")),
                    "positions": 8,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")

            for i in range(8):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            RolePlacement.objects.create(
                role=role,
                display_name="Class Representative",
                tier=3,
                page=class_council_page
            )
            
            name = f"Class of {class_num} Senator"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 4,
                    "constituency": class_num,
                }
            )
            if created: print(f"Created {name}")

            for i in range(4):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )
                senators_list.append(new_person)
                
            RolePlacement.objects.create(
                role=role,
                display_name="Class Senator",
                tier=3,
                page=class_council_page
            )
            RolePlacement.objects.create(
                role=role,
                display_name=f"Class of {class_num} Senator",
                tier=3,
                page=senate_member_page
            )
            
            name = f"Class of {class_num} Vice President"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")

            for i in range(1):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            RolePlacement.objects.create(
                role=role,
                display_name="Class Vice President",
                tier=1,
                page=class_council_page
            )
            RolePlacement.objects.create(
                role=role,
                display_name=f"Class of {class_num} Vice President",
                tier=3,
                page=uc_member_page
            )
            
            name = f"Class of {class_num} President"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": class_num,
                }
            )
            if created: print(f"Created {name}")

            for i in range(1):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            RolePlacement.objects.create(
                role=role,
                display_name="Class President",
                tier=0,
                page=class_council_page
            )
            RolePlacement.objects.create(
                role=role,
                display_name=f"Class of {class_num} President",
                tier=3,
                page=uc_member_page
            )

            for officer_role in ["Secretary", "Treasurer", "Publicity Director"]:
                name = f"{officer_role}"
                role, created = Role.objects.update_or_create(
                    role_code=f"{class_num}-"+'-'.join(name.lower().split(" ")),
                    defaults={
                        "name": name,
                        "role_code": f"{class_num}-"+'-'.join(name.lower().split(" ")),
                        "positions": 1,
                        "constituency": 'none',
                    }
                )
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )
                RolePlacement.objects.create(
                    role=role,
                    display_name=officer_role,
                    tier=1,
                    page=class_council_page
                )
                if created: print(f"Created {name}")

        gc_branch_page = BranchPage(
            branch_type="gc",
            tagline="The graduate council branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="gc@rpi.edu",
            meeting_schedule="",
            title="Graduate Council",
            slug="gc",
            show_in_menus=True
        )

        root_page.add_child(instance=gc_branch_page)

        gc_member_page = MemberListingPage(
            title="Graduate Council Member List",
            slug="gc_member_list",
            intro="The members of the Graduate Council.",
            show_in_menus=True
        )

        gc_branch_page.add_child(instance=gc_member_page)
                        
        name = f"Graduate Representative"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 8,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")

        for i in range(8):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        RolePlacement.objects.create(
            role=role,
            display_name="Graduate Representative",
            tier=3,
            page=gc_member_page
        )
        
        name = f"Graduate Senator"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 7,
                "constituency": 'graduate',
            }
        )
        if created: print(f"Created {name}")

        for i in range(7):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
            
        RolePlacement.objects.create(
            role=role,
            display_name="Graduate Senator",
            tier=3,
            page=gc_member_page
        )
        RolePlacement.objects.create(
            role=role,
            display_name=f"Graduate Senator",
            tier=3,
            page=senate_member_page
        )
        
        name = f"Graduate Vice President"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")

        for i in range(1):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        RolePlacement.objects.create(
            role=role,
            display_name="Graduate Vice President",
            tier=1,
            page=gc_member_page
        )
        
        name = f"Graduate President"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'graduate',
            }
        )
        if created: print(f"Created {name}")

        for i in range(1):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        RolePlacement.objects.create(
            role=role,
            display_name="Graduate President",
            tier=0,
            page=gc_member_page
        )

        for officer_role in ["Secretary", "Treasurer", "Publicity Director"]:
            name = f"{officer_role}"
            role, created = Role.objects.update_or_create(
                role_code="gc-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": "gc-"+'-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=officer_role,
                tier=1,
                page=gc_member_page
            )
            if created: print(f"Created {name}")

        for officer_role in ["Secretary", "Treasurer", "Parlimenatarian"]:
            name = f"{officer_role}"
            role, created = Role.objects.update_or_create(
                role_code="senate-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": "senate-"+'-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=officer_role,
                tier=1,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

        name = f"Grand Marshall"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'none',
            }
        )
        new_person = self.make_person(class_choices()[0][0])
        MemberProfile.objects.filter(rcs_id=new_person.rcs_id).update(
            first_name = "Ben",
            last_name = "Bitdiddle",
            rcs_id = "bitdib"   
        )
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        RolePlacement.objects.create(
            role=role,
            display_name="Grand Marshall",
            tier=0,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        for vgm in ["Internal", "External"]:
            name = f"Vice Grand Marshall for {vgm} Affairs"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=name,
                tier=1,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

        name = f"FSL Senator"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 3,
                "constituency": 'associated',
            }
        )
        for i in range(3):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
        RolePlacement.objects.create(
            role=role,
            display_name=name,
            tier=3,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        name = f"Independent Senator"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 3,
                "constituency": 'independent',
            }
        )
        for i in range(3):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
        RolePlacement.objects.create(
            role=role,
            display_name=name,
            tier=3,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        for i in range(9):
            committee_name = self.gen_committee()
            name = f"{committee_name} Chair"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=name,
                tier=2,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

            committee_page = CommitteePage(
                title=committee_name,
                slug='_'.join(i.lower() for i in committee_name.split(" ")),
                show_in_menus=False,
                description=''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(1000)]),
                meeting_time=random.choice(["Monday", "Tuesday", "Wednesday", "Thursday"])+" "+str(random.choice([12,1,2,3,4,5,6]))+"pm",
                meeting_location=f"Union Room {''.join([str(random.choice(range(10))) for _ in range(4)])}"
            )
            
            senate_committee_page.add_child(instance=committee_page)

            RolePlacement.objects.create(
                role=role,
                display_name="Chair",
                tier=0,
                page=committee_page
            )

        eboard_branch_page = BranchPage(
            branch_type="eboard",
            tagline="The E-Board branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="pu@rpi.edu",
            meeting_schedule="",
            title="E-Board",
            slug="eboard",
            show_in_menus=True
        )

        root_page.add_child(instance=eboard_branch_page)

        eboard_member_page = MemberListingPage(
            title="E-Board Member List",
            slug="eboard_member_list",
            intro="The members of the E-Board.",
            show_in_menus=True
        )

        eboard_branch_page.add_child(instance=eboard_member_page)

        for officer_role in ["Secretary", "Parlimenatarian"]:
            name = f"{officer_role}"
            role, created = Role.objects.update_or_create(
                role_code="eboard-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": "eboard-"+'-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=officer_role,
                tier=1,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")

        name = f"President of the Union"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 1,
                "constituency": 'none',
            }
        )
        new_person = self.make_person(class_choices()[0][0])
        MemberProfile.objects.filter(rcs_id=new_person.rcs_id).update(
            first_name = "Alyssa P.",
            last_name = "Hacker",
            rcs_id = "hackea"   
        )
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        RolePlacement.objects.create(
            role=role,
            display_name="President of the Union",
            tier=0,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        for vp in ["Board Operations", "Club Relations", "Rules and Special Projects"]:
            name = f"Vice President for {vp}"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=name,
                tier=1,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")

        name = f"Club & Organization Representative"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 6,
                "constituency": 'none',
            }
        )
        for i in range(6):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
        RolePlacement.objects.create(
            role=role,
            display_name=name,
            tier=3,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        name = f"Member-At-Large Representative"
        role, created = Role.objects.update_or_create(
            role_code='-'.join(name.lower().split(" ")),
            defaults={
                "name": name,
                "role_code": '-'.join(name.lower().split(" ")),
                "positions": 4,
                "constituency": 'none',
            }
        )
        for i in range(4):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
        RolePlacement.objects.create(
            role=role,
            display_name=name,
            tier=3,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        for class_num, _ in class_choices():
            if class_num == "graduate": continue
            name = f"Class of {class_num} Representative"
            role, created = Role.objects.update_or_create(
                role_code="eboard-"+'-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": "eboard-"+'-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_num)
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=f"Class of {class_num} Representative",
                tier=3,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")


        eboard_committee_page = CommitteeIndexPage(
            title="E-Board Committee List",
            slug="eboard_committee_list",
            intro="The committees of E-Board.",
            show_in_menus=True
        )

        eboard_branch_page.add_child(instance=eboard_committee_page)
            
        for i in range(9):
            committee_name = self.gen_committee()
            name = f"{committee_name} Chair"
            role, created = Role.objects.update_or_create(
                role_code='-'.join(name.lower().split(" ")),
                defaults={
                    "name": name,
                    "role_code": '-'.join(name.lower().split(" ")),
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            RolePlacement.objects.create(
                role=role,
                display_name=name,
                tier=2,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")

            committee_page = CommitteePage(
                title=committee_name,
                slug='_'.join(i.lower() for i in committee_name.split(" ")),
                show_in_menus=False,
                description=''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(1000)]),
                meeting_time=random.choice(["Monday", "Tuesday", "Wednesday", "Thursday"])+" "+str(random.choice([12,1,2,3,4,5,6]))+"pm",
                meeting_location=f"Union Room {''.join([str(random.choice(range(10))) for _ in range(4)])}"
            )
            
            eboard_committee_page.add_child(instance=committee_page)

            RolePlacement.objects.create(
                role=role,
                display_name="Chair",
                tier=0,
                page=committee_page
            )

        SiteSettings.objects.update(
            box_archive_url="https://rpi.app.box.com/v/rpisg"
        )

        records_page = RecordIndexPage(
            title="Record",
            slug="the-record",
            intro="The records of student government.",
            show_in_menus=True
        )

        root_page.add_child(instance=records_page)

        complaint_form = ComplaintFormPage(
            title="Complaint Form",
            slug="complaint-form",
            intro="Submit a complaint to the government.",
            show_in_menus=True
        )

        root_page.add_child(instance=complaint_form)
        
        reps_form = RepsFormPage(
            title="Representative Finder",
            slug="find-reps",
            intro="Find your representatives!",
            show_in_menus=True
        )

        root_page.add_child(instance=reps_form)

    ids = ["bitdib", "hackea"]
    def make_id(self):
        while True:
            id = ''.join([random.choice(string.ascii_lowercase) for _ in range(6)]) + str(random.randint(2,20))
            if id not in self.ids: 
                self.ids.append(id)
                return id
    
    def make_person(self, year):
        id = self.make_id()
        person, _ = MemberProfile.objects.update_or_create(
            rcs_id=id,
            defaults={
                "first_name": ''.join([random.choice(string.ascii_lowercase) for _ in range(7)]).capitalize(),
                "last_name": ''.join([random.choice(string.ascii_lowercase) for _ in range(10)]).capitalize(),
                "rcs_id": id,
                "class_year": year,
                "major": ''.join([random.choice(string.ascii_uppercase) for _ in range(4)]),
                "bio": ''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(100)])
            }
        )
        return person

    def gen_committee(self):
        out = ""
        for i in range(3):
            out += ''.join([random.choice(string.ascii_lowercase) for _ in range([7,3,7][i])]).capitalize() +" "
        return out + "Committee"
