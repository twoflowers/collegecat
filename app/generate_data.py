import sys
sys.path.append("..")

from app import app
import sqlalchemy
import models
import csv
import time
import random

data_file = '../ksmo_names.csv'
csv_file = csv.DictReader(open(data_file, 'rb'), delimiter=',', quotechar='"')
db = models.db
db.drop_all()
db.create_all()

subjects = [
    'Academic Achievement Center',
    'Accounting',
    'Algebra',
    'Administration of Justice',
    'American Sign Language',
    'Animation',
    'Anthropology',
    'Architecture',
    'Art',
    'Art History',
    'Astronomy',
    'Automotive Technology',
    'Biology',
    'Biotechnology',
    'Business',
    'Business Office Technology',
    'Calculus',
    'Chemistry',
    'Civil Engineering Technology',
    'Computer Desktop Publishing',
    'Computer Information Systems',
    'Computer Personal Computer App',
    'Computer Science',
    'Computer Web',
    'Cosmetology',
    'Cosmetology - Esthetics',
    'Credit Course Descriptions',
    'Dental Hygiene',
    'Dietary Managers',
    'Drafting/CAD/AutoCAD',
    'Economics',
    'Education and Early Childhood',
    'Electrical Technology',
    'Electronics',
    'Emergency Medical Science/MICT',
    'Energy Perform & Resource Mgmt',
    'Engineering',
    'English',
    'English for Academic Purposes',
    'Entrepreneurship',
    'Fashion Merchandising/Design',
    'Fire Services Administration',
    'Floriculture',
    'Foreign Language',
    'Game Development',
    'Geoscience',
    'Global & International Studies',
    'Goat Herding',
    'Graphic Design',
    'Health Care',
    'Health Care Info Systems',
    'Health Care Interpreting',
    'Health Occupations',
    'Heating,Vent.,Air Conditioning',
    'History',
    'Home Economics',
    'Honors Program',
    'Horticulture',
    'Hospitality Management',
    'Hospitality Mgt Pastry Baking',
    'Humanities',
    'Industrial Technology',
    'Information Technology',
    'Interactive Media',
    'Interior Design',
    'International Studies Abroad',
    'Interpreter Training',
    'Journalism/Media Communication',
    'Leadership',
    'Learning Communities',
    'Learning Strategies',
    'Legal Interpreting',
    'Legal Studies',
    'Library',
    'Marketing Management',
    'Mathematics',
    'Med Info & Revenue Management',
    'Metal Fabrication and Welding',
    'Music',
    'Nursing',
    'Philosophy',
    'PHP',
    'Photography',
    'Physical Ed, Health & Rec',
    'Physical Science',
    'Physics',
    'Political Science',
    'Polysomnography/Sleep Tech',
    'Practical Nursing',
    'Psychology',
    'Python',
    'Railroad Conductor',
    'Railroad Electronics',
    'Railroad Industrial Technology',
    'Railroad Operations-Mechanical',
    'Railroad Operations',
    'Reading',
    'Religion',
    'Respiratory Care',
    'Science',
    'Sociology',
    'Speech/Debate',
    'Theater',
    'Underwater Basket Weaving',
    'Women and Gender Studies',
    'World of Warcraft'
]

bios = [
    'Thinker. Introvert. Gamer. Alcohol ninja. Friendly tv fan. Amateur internet trailblazer. Hipster-friendly music junkie.',
    'Unapologetic problem solver. Amateur entrepreneur. Explorer. Gamer. Devoted alcohol nerd. Professional introvert. Wannabe troublemaker.',
    'Hipster-friendly music fan. Social media advocate. Avid pop culture maven. Troublemaker. Web aficionado. Thinker.',
    'Award-winning thinker. Social mediaholic. Gamer. Twitter lover. Organizer.',
    'Web aficionado. Zombie guru. Bacon fan. Entrepreneur. Award-winning pop culture advocate. Reader.',
    'Alcohol aficionado. Web buff. Wannabe music enthusiast. Student. Travel fanatic. Professional tv evangelist. Typical social media scholar. Twitter lover.',
    'Analyst. Alcohol buff. Award-winning travel expert. Zombie aficionado. Evil tv nerd.',
    'Music fanatic. Hardcore introvert. Travel aficionado. Web ninja. Beer enthusiast. Entrepreneur. Food buff. Incurable pop culture scholar.',
    'Freelance pop culture ninja. Infuriatingly humble beer maven. Alcohol aficionado. Extreme writer. Web nerd. Certified communicator.',
    'Bacon fanatic. Friendly introvert. Travel nerd. Infuriatingly humble student. Total alcohol geek. Passionate problem solver. Analyst.',
    'Web lover. Alcohol fanatic. Bacon maven. Travel aficionado. Zombie fanatic. Unapologetic student.',
    'Typical gamer. Pop culture enthusiast. Communicator. Tv fanatic. Total organizer. Future teen idol. Professional webaholic.',
    'Wannabe foodaholic. Social media lover. Bacon ninja. Zombie enthusiast. Travel maven. Beer fan.',
    "Avatar, Entertainer, Green building lover, Man of Winter, Han Solo's College Roommate. In Russia, car drives you!"
]

users_added = 0
tags_added = 0
ratings_added = 0

for row in csv_file:
    newLoc = models.Location(
        street=row['StreetAddress'],
        city=row['City'],
        state=row['State'],
        zip=row['ZipCode'],
        gps="%s,%s" % (row['Latitude'], row['Longitude'])
    )

    newUser = models.User(
        name="%s %s" % (row['GivenName'], row['Surname']),
        username=row['Username'].lower(),
        password="password", #row['Password'],
        email=row['EmailAddress'],
        phone=row['TelephoneNumber'],
        payment='B6Epo8Kn'
    )
    newUser.loc.append(newLoc)
    newUser.bio = random.choice(bios)
    db.session.add(newLoc)
    db.session.add(newUser)
    try:
        db.session.commit()
        users_added += 1
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        continue

    tags = random.sample(subjects, random.randint(0, 6))
    if newUser.username == 'santov':
        tags.append('Bulgarian')
        tags.append('Goat Herding')
    elif newUser.username == 'marcs':
        tags.append('Spanish')
        tags.append('Chupacabras')
    elif newUser.username == 'tmartin':
        tags.append('Underwater Basket Weaving')

    for tag in tags:
        try:
            newTag = models.Tag(tag)
            newUser.tags.append(newTag)
            db.session.commit()
            tags_added += 1
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            try:
                newTag = models.Tag.query.filter_by(name=tag).first()
                newUser.tags.append(newTag)
                db.session.commit()
                sys.stdout.write("+")
            except:
                db.session.rollback()
                continue
            continue

        try:
            newPrice = models.Price(price=random.randint(500, 4200), tag=newTag.id, user_id=newUser.id)
            db.session.add(newPrice)
            db.session.commit()
        except Exception as e:
            print "There was an exception adding a price because %r " % e
            db.session.rollback()

    # print "Adding course tags: %s" % tags

    total_users = db.session.query(models.User).count()
    if random.randint(0, 1000) > 500:
        is_good = random.randint(0, 1000) < 500
        # Randomly decide whether they get any ratings at all
        for rating_no in range(0, random.randint(0, 13)):
            if is_good:
                max_rating = 5
                min_rating = 3
            else:
                max_rating = 3
                min_rating = 0

            try:
                # print "Adding rating # %s" % rating_no
                ratingUser = models.User.query.get(random.randint(1, total_users))
                newRating = models.Rating(
                    user=ratingUser.id,
                    tutor=newUser.id,
                    rating=random.randint(min_rating, max_rating),
                    comment=""
                )
                db.session.add(newRating)
                db.session.commit()
                ratings_added += 1
            except Exception as e:
                #print "Exception: %r" % e
                db.session.rollback()
                continue

        sys.stdout.write(".")
        sys.stdout.flush()

print ""
print "Added Users: %s Ratings: %s Tags: %s" % (
    users_added,
    ratings_added,
    tags_added
)
