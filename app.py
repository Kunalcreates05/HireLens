from flask import Flask,render_template,request,redirect,url_for
import pdfplumber

app=Flask(__name__)

skills_db=[

# programming
"python","java","c++","c","javascript","typescript","go","rust","kotlin","swift",

# web dev
"html","css","react","angular","vue","node","express","django","flask","spring","bootstrap","tailwind",

# data & ai
"machine learning","deep learning","data analysis","data science","nlp","computer vision",
"pandas","numpy","tensorflow","pytorch","scikit-learn","matplotlib","power bi","tableau","excel",

# database
"sql","mysql","postgresql","mongodb","firebase","oracle",

# cloud/devops
"aws","azure","gcp","docker","kubernetes","ci/cd","jenkins","linux","git","github",

# business / non-tech
"marketing","digital marketing","seo","sem","branding","sales","lead generation",
"business development","operations","management","strategy",

# content / writing
"content writing","copywriting","blog writing","technical writing","editing","proofreading","storytelling",

# soft skills
"communication","leadership","teamwork","problem solving","critical thinking","time management","adaptability",

# finance
"accounting","financial analysis","budgeting","taxation","investment","risk management",

# hr
"recruitment","talent acquisition","employee engagement","hr operations",

# design
"ui/ux","figma","adobe xd","photoshop","illustrator","canva",

# misc
"customer support","client handling","presentation","negotiation","public speaking"

]

jobs_db={
"python":["Python Developer","Backend Developer","Data Analyst"],
"javascript":["Frontend Developer","React Developer"],
"sql":["Database Developer","Backend Engineer"],
"machine learning":["ML Engineer","AI Engineer"]
}

def extract_text(file):

    text=""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            t=page.extract_text()

            if t:
                text+=t

    return text


def extract_skills(text):

    found=set()

    text=text.lower()

    for skill in skills_db:

        if skill in text:

            found.add(skill)

    return list(found)


def ats_score(skills):

    score=int((len(skills)/len(skills_db))*100)

    if score>100:
        score=100

    return score


def suggestions(skills):

    sug=[]

    # TECH TRACK
    tech_skills=["python","java","sql","machine learning","react"]

    # NON-TECH TRACK
    non_tech_skills=["marketing","seo","content","writing","sales"]

    if any(skill in skills for skill in tech_skills):

        if "sql" not in skills:
            sug.append("Add database skills like SQL")

        if "projects" not in skills:
            sug.append("Add more real-world projects")

        if len(skills)<5:
            sug.append("Add more technical skills")

    else:

        if "communication" not in skills:
            sug.append("Highlight communication skills")

        if "experience" not in skills:
            sug.append("Add more work experience")

        if len(skills)<5:
            sug.append("Add more domain-specific skills")

    return sug


def recommend_jobs(skills):

    rec=[]

    for skill in skills:

        if skill in jobs_db:

            for job in jobs_db[skill]:

                if job not in rec:

                    rec.append(job)

    # fallback if empty
    if len(rec)==0:

        rec=[
            "Content Writer",
            "Business Analyst",
            "Digital Marketing Executive",
            "Customer Support",
            "Operations Manager"
        ]

    return rec


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/signup",methods=["GET","POST"])
def signup():

    if request.method=="POST":

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():

    skills=None
    score=None
    sug=None
    jobs=None

    if request.method=="POST":

        file=request.files["resume"]

        if file:

            text=extract_text(file)

            skills=extract_skills(text)

            score=ats_score(skills)

            sug=suggestions(skills)

            jobs=recommend_jobs(skills)

    return render_template(
        "dashboard.html",
        skills=skills,
        score=score,
        suggestions=sug,
        jobs=jobs
    )


if __name__=="__main__":

    app.run(debug=True)