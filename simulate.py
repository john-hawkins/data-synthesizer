import numpy as np
import pandas as pd

import random
import time

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start, end):
    prop = random.random()
    return str_time_prop(start, end, '%Y-%m-%d', prop)


min_dob = "1967-01-01"
max_dob = "2003-12-21"

min_reg = "2015-01-01"
max_reg = "2019-02-01"

languages = { "EN":0.81, "HI":0.07, "ZH":0.09, "AR":0.03} 

education = { "HS":0.39, "TAFE":0.31, "UG":0.27, "PG":0.03 }

educ_by_lan = {
    "EN": { "HS":0.39, "TAFE":0.31, "UG":0.27, "PG":0.03 }, 
    "HI": { "HS":0.32, "TAFE":0.29, "UG":0.34, "PG":0.04 }, 
    "ZH": { "HS":0.30, "TAFE":0.28, "UG":0.37, "PG":0.05 }, 
    "AR": { "HS":0.35, "TAFE":0.30, "UG":0.32, "PG":0.03 }, 
}

major_by_edu = {
    "UG": { "STEM":0.3, "ARTS":0.3, "OCCUP":0.4 },
    "PG": { "STEM":0.4, "ARTS":0.4, "OCCUP":0.2 }
}

# Helper Functions
import random
def sample_from_dist(a_dict):
    """
    Given a dictionary where key is the category and the value
    is the probability, we sample from the distribution of categories.
    """
    total = 0.0
    randval = random.random()
    for key, value in a_dict.items():
        total = total + value
        if randval < total:
            return key
    return key

def get_random_dob():
    return random_date(min_dob, max_dob)

def get_random_reg():
    return random_date(min_reg, max_reg)

def get_random_edu():
    return sample_from_dist(education)

def get_random_lan():
    return sample_from_dist(languages)

def get_random_edu_by_lan(lan):
    return sample_from_dist(educ_by_lan[lan])

def get_random_major(edu):
    if edu=="UG" or edu=="PG":
        return sample_from_dist(major_by_edu[edu])
    else:
        return "NONE"

from dateutil.relativedelta import relativedelta

def diff_in_years(newer, older):
    newie = pd.to_datetime(newer, format='%Y-%m-%d', errors='coerce')
    oldie = pd.to_datetime(older, format='%Y-%m-%d', errors='coerce')
    return relativedelta(newie, oldie).years

# ############################################################
# Generate the set of students

studs = []
lower_id=100000
upper_id=300002
for i in range(lower_id, upper_id):
    dob = get_random_dob()
    reg = get_random_reg()
    lan = get_random_lan()
    edu = get_random_edu_by_lan(lan)
    major = get_random_major(edu)
    age = diff_in_years(reg, dob)
    s = {
        "student_id":i,
        "dob":dob,
        "country":"AU",
        "education":edu,
        "major":major,
        "language":lan,
        "registration":reg,
        "age": age
    }
    studs.append(s)

students = pd.DataFrame(studs)

students.to_csv("students.csv", header=True, index=False)

semester_starts = [
    "2015-02-01", "2015-06-01", "2015-10-01", 
    "2016-02-01", "2016-06-01", "2016-10-01", 
    "2017-02-01", "2017-06-01", "2017-10-01", 
    "2018-02-01", "2018-06-01", "2018-10-01", 
    "2019-02-01", "2019-06-01", "2019-10-01", 
    "2020-02-01", "2020-06-01", "2020-10-01", 
]

cses = [
   {"course":10021, "title":"Introduction to Data Science", "level":1, "Math":0},
   {"course":10031, "title":"Programming in Python", "level":1, "Math":0},
   {"course":10041, "title":"Introduction to Statistics", "level":1, "Math":1},
   {"course":10051, "title":"Introduction to Machine Learning", "level":1, "Math":0},
   {"course":10061, "title":"Business Case Analysis", "level":1, "Math":0},
   {"course":20021, "title":"Data Science Project Management", "level":2, "Math":0},
   {"course":20022, "title":"Data & Feature Engineering", "level":2, "Math":0},
   {"course":20023, "title":"Data Visualization", "level":2, "Math":0},
   {"course":20024, "title":"AB Testing and Experimentation", "level":2, "Math":1},
   {"course":20025, "title":"Data Science Capstone", "level":3, "Math":1},
   {"course":20031, "title":"Agile Development Methodologies", "level":2, "Math":0},
   {"course":20051, "title":"Deep Learning Models", "level":2, "Math":1},
   {"course":20061, "title":"Presenting & Executive Briefing", "level":2, "Math":0},
   {"course":20081, "title":"Advanced Statistics", "level":3, "Math":1},
   {"course":30005, "title":"Business Process Design", "level":3, "Math":0},
   {"course":30011, "title":"Machine Learning Engineering", "level":3, "Math":0},
   {"course":30015, "title":"Machine Learning Operations", "level":3, "Math":0},
   {"course":30041, "title":"Time Series Modelling", "level":3, "Math":2},
   {"course":30051, "title":"Reinforcement Learning", "level":3, "Math":2},
   {"course":30091, "title":"Natural Language Processing", "level":3, "Math":1},
   {"course":30033, "title":"Change Management Processes", "level":3, "Math":0},
   {"course":30025, "title":"Business Analysis Capstone", "level":3, "Math":0}
]

courses = pd.DataFrame(cses)
courses.to_csv("courses.csv", header=True, index=False)
en_advantage = [10061,20021,20061,30005,30033] 
old_advantage = [10061,20021,20061,30033,30025]
youth_advantage = [10041,20051,20081,30041]

elective_probs = {
   20031:{ "STEM":0.4, "ARTS":0.5, "OCCUP":0.5, "NONE":0.3 },
   30011:{ "STEM":0.6, "ARTS":0.3, "OCCUP":0.4, "NONE":0.4 },
   20051:{ "STEM":0.4, "ARTS":0.3, "OCCUP":0.4, "NONE":0.3 },
   20061:{ "STEM":0.3, "ARTS":0.6, "OCCUP":0.7, "NONE":0.3 },
   20081:{ "STEM":0.4, "ARTS":0.1, "OCCUP":0.3, "NONE":0.2 },
   30005:{ "STEM":0.3, "ARTS":0.3, "OCCUP":0.7, "NONE":0.4 },
   30015:{ "STEM":0.4, "ARTS":0.2, "OCCUP":0.4, "NONE":0.4 },
   30041:{ "STEM":0.4, "ARTS":0.3, "OCCUP":0.5, "NONE":0.3 },
   30051:{ "STEM":0.4, "ARTS":0.2, "OCCUP":0.3, "NONE":0.2 },
   30091:{ "STEM":0.3, "ARTS":0.6, "OCCUP":0.4, "NONE":0.3 },
   30033:{ "STEM":0.3, "ARTS":0.5, "OCCUP":0.6, "NONE":0.3 },
   30025:{ "STEM":0.3, "ARTS":0.5, "OCCUP":0.6, "NONE":0.3 },
}

sequence = [ 10021,10031,10041,10051,10061,20021,20022,20023,20024,20025 ]

alternatives = {
    10021:[],
    10031:[],
    10041:[],
    10051:[],
    10061:[],
    20021:[20081,30005,30011],
    20022:[20031,30005,20051],
    20023:[30033,30005,30015],
    20024:[30041,30051,30091,20061],
    20025:[30025]
}

elective_conds = {
   20031:{10061:0.75},
   30011:{10051:0.75}, 
   20051:{10051:0.75},
   20061:{10061:0.75},
   20081:{10041:0.75},
   30005:{10061:0.75},
   30015:{30011:0.75},
   30051:{30011:0.75},
   30041:{30011:0.75},
   30091:{30011:0.75},
   30033:{20031:0.75},
   30025:{10061:0.75},
}


assess_scales = {
   10021:-0.02,
   10031:-0.02,
   10041:-0.01,
   10051:-0.02,
   10061:-0.01,
   20021:-0.01,
   20022:-0.01,
   20023:0.0,
   20024:0.0,
   20025:0.01,
   20031:-0.01,
   30011:0.0,
   30005:0.0,
   20051:0.0,
   20061:-0.01,
   20081:0.02,
   30015:0.01,
   30041:0.01,
   30051:0.02,
   30091:0.01,
   30033:0.01,
   30025:0.01,
}

assess_means = {
   10021:0.7,
   10031:0.7,
   10041:0.65,
   10051:0.65,
   10061:0.7,
   20021:0.62,
   20022:0.62,
   20023:0.62,
   20024:0.62,
   20025:0.62,
   20031:0.6,
   30011:0.57,
   30005:0.57,
   20051:0.57,
   20061:0.57,
   20081:0.55,
   30015:0.57,
   30041:0.55,
   30051:0.53,
   30091:0.55,
   30033:0.57,
   30025:0.55,
}

course_variants = {
   10021: {"STEM":0.01, "ARTS":-0.01, "OCCUP":0.01, "NONE":0.0},
   10031: {"STEM":0.05, "ARTS":-0.05, "OCCUP":0.01, "NONE":0.0},
   10041: {"STEM":0.03, "ARTS":-0.03, "OCCUP":0.03, "NONE":0.0},
   10051: {"STEM":0.03, "ARTS":-0.01, "OCCUP":0.01, "NONE":0.0},
   10061: {"STEM":-0.01, "ARTS": 0.02, "OCCUP":0.07, "NONE":0.0},
   20021: {"STEM":0.01, "ARTS": 0.01, "OCCUP":0.05, "NONE":0.0},
   20022: {"STEM":0.03, "ARTS":-0.03, "OCCUP":0.01, "NONE":0.0},
   20023: {"STEM":0.01, "ARTS": 0.02, "OCCUP":0.03, "NONE":0.0},
   20024: {"STEM":0.03, "ARTS":-0.03, "OCCUP":0.01, "NONE":0.0},
   20025: {"STEM":0.02, "ARTS":-0.03, "OCCUP":0.04, "NONE":0.0},
   20031: {"STEM":0.01, "ARTS":-0.01, "OCCUP":0.03, "NONE":0.0},
   30011: {"STEM":0.05, "ARTS":-0.05, "OCCUP":-0.02, "NONE":0.0},
   20051: {"STEM":0.05, "ARTS":-0.05, "OCCUP":0.00, "NONE":0.0},
   20061: {"STEM":-0.03, "ARTS": 0.07, "OCCUP":0.05, "NONE":0.0},
   20081: {"STEM":0.03, "ARTS":-0.04, "OCCUP":-0.02, "NONE":-0.02},
   30005: {"STEM":-0.01, "ARTS":-0.01, "OCCUP":0.05, "NONE":0.0},
   30015: {"STEM":0.04, "ARTS":-0.03, "OCCUP":0.01, "NONE":0.0},
   30041: {"STEM":0.02, "ARTS":-0.03, "OCCUP":0.04, "NONE":-0.01},
   30051: {"STEM":0.02, "ARTS":-0.04, "OCCUP":-0.02, "NONE":-0.01},
   30091: {"STEM":0.03, "ARTS":0.01, "OCCUP":0.01, "NONE":-0.01},
   30033: {"STEM":-0.03, "ARTS":0.03, "OCCUP":0.03, "NONE":0.0},
   30025: {"STEM":-0.03, "ARTS": 0.03, "OCCUP":0.05, "NONE":0.0},
}

assess_vars = {
    "HS":-0.05, "TAFE":-0.01, "UG":0.03, "PG":0.07
}


def get_enrolment(regdate):
    #print("Getting enrolment for regitration:", regdate)
    #print("Data type:", type(regdate))
    dates = [x for x in semester_starts if x > regdate]
    if len(dates) >0 :
        return min(dates)
    else:
        return None    


def get_assessment_result(course, edu, major, lan, age, mean_score, factor=0.0):
    """
    Given a students education level and the course they are taking
    return an assessment result sampled from an appropriate distribution.
    Include a feedback factor, students who did well on the last exam are
    likely to do better again.  
    """
    major_factor = course_variants[course][major]
    if course in en_advantage:
        if lan == "EN":
            major_factor += 0.02
        else:
            major_factor -= 0.02

    if course in old_advantage:
        if age > 40:
            major_factor += 0.02
        else:
            major_factor -= 0.02

    if course in youth_advantage:
        if age < 40:
            major_factor += 0.02
        else:
            major_factor -= 0.02

    if mean_score > 0.85:
        factor = factor + 0.05

    if mean_score > 0.75:
        factor = factor + 0.05

    if mean_score > 0.65:
        factor = factor + 0.01

    # Make Age contribute to the variation in scores
    # i.e younger people have a larger distribution of score
    # Older people work harder and cluster around the mean.
    if age < 25:
        scaler = +0.03
    if age < 40:
        scaler = +0.02
    else:
        scaler = -0.02

    ass_mean = assess_means[course] + factor + major_factor + assess_vars[edu]
    ass_scale = 0.12 + scaler + assess_scales[course]
    score = np.random.normal(loc=ass_mean, scale=ass_scale) + factor
    if score > 1.0:
        score = 0.99
    if score > 0.90:
        factor = 0.05
    elif score > 0.85:
        factor = 0.04
    elif score > 0.8:
        factor = 0.03
    elif score > 0.75:
        factor = 0.02

    rez = "Pass"
    if score < 0.5:
        rez = "Fail"
    return score, rez, factor


def test_for_withdrawl(score, mean_score, age, lan):
    """
    Simulate withdrawl
    """
    base_prob = 0.17
    if score < 0.3:
        base_prob += 0.1
    if score < 0.4:
        base_prob += 0.1
    if mean_score < 0.5:
        base_prob += 0.05
    if age > 40:
        base_prob -= 0.05
    else:
        base_prob += 0.05
    if age > 30:
        base_prob -= 0.05
    else:
        base_prob += 0.05
    if lan == "EN":
        base_prob += 0.05
    else:
        base_prob -= 0.1

    prop = random.random()
    if prop < base_prob:
        return True
    else:
        return False


"""
Now iterate over each student and create a series of course
enrolments and assessment results
"""
records = []
assmnts = []

for index, s in students.iterrows():
    regdate = str(s["registration"])
    student_id = s["student_id"]
    my_results = {}
    elective = "core"
    enroldate = get_enrolment(regdate)
    rec = {
        "student_id":student_id,
        "date":enroldate,
        "course":sequence[0]
    }
    records.append(rec)
    course = sequence[0]
    edu = s["education"]
    maj = s["major"]
    lan = s["language"]
    age = s["age"]
    status = "Continue"
    mean_score = 0.6
    score, result, factor = get_assessment_result( course, edu, maj, lan, age, mean_score )
    assess = {
        "student_id":student_id,
        "date":enroldate,
        "course":course,
        "type": elective,
        "score": score,
        "result":result,
        "status":status
    }
    my_results[course] = score
    assmnts.append(assess)
    mean_score = score
    c = 1
    while c < len(sequence):
        enroldate = get_enrolment(enroldate)
        if enroldate == None:
            break
        course = sequence[c]
        elective = "core"
        alts = alternatives[course]
        if len(alts)>0:
            probs = {}
            facts = {}
            elective = "elec"
            adjust = 0.0
            if mean_score > 0.8:
                adjust = 0.1
            if mean_score < 0.6:
                adjust = -0.1 
            for a in alts:
                conds = elective_conds[a]
                for k in conds.keys():
                    if k in my_results:
                        if my_results[k] > conds[k]:
                            probs[a] = elective_probs[a][maj] + adjust 
                            facts[a] = -0.02
                        else:
                            probs[a] = 0.2 * elective_probs[a][maj] + adjust
                            facts[a] = -0.04
            total = sum(probs.values())
            #print("Total prob:", total)
            if total >= 0.4:
                base = 0.1
                for k in probs.keys():
                    probs[k] = probs[k] / (total+base)
                    base = base / (total+base)
            else:
                base = 1.0 - total
            probs[course] = base
            facts[course] = 0.0
            #print("Core:", course)
            selected = sample_from_dist(probs)
            if selected != course:
                elective = "adv"
                course = selected
            factor = factor + facts[course]

            #print("Probs:", probs)
            #print("Chosen:", course)
        if course in my_results:
            factor = factor + 0.02
        rec = {
            "student_id":student_id,
            "date":enroldate,
            "course":course
        }
        records.append(rec)
        score, result, factor = get_assessment_result(course, edu, maj, lan, age, mean_score,factor)
        my_results[course] = score
        mean_score = sum(my_results.values())/len(my_results.values())
        status = "Continue"
        if result=="Fail" or mean_score < 0.55:
            if test_for_withdrawl(score, mean_score, age, lan):
                status = "Withdraw"

        assess = {
            "student_id":student_id,
            "date":enroldate,
            "course":course,
            "type": elective,
            "score":score,
            "result":result,
            "status":status
        }
        assmnts.append(assess)
        if status=="Withdraw" :
            break
        else:
            c+=1


assessments = pd.DataFrame(assmnts)

assessments = assessments.sort_values(by=['student_id','date'])

assessments.to_csv("assessments.csv", header=True, index=False)

#print(assessments.sort_values(by=['student_id','date']).head(20))



