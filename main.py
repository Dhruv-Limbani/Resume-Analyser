import streamlit as st
import nltk
nltk.download('stopwords')
import base64
from pyresparser import ResumeParser
import re
import pickle
import pandas as pd
import fitz
from PIL import Image
from streamlit_tags import st_tags
import random
from courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
from skills import skills_dict
import time


roles = ['Advocate',
 'Arts',
 'Automation Testing',
 'Blockchain',
 'Business Analyst',
 'Civil Engineer',
 'Data Science',
 'Database',
 'DevOps Engineer',
 'DotNet Developer',
 'ETL Developer',
 'Electrical Engineering',
 'HR',
 'Hadoop',
 'Health and fitness',
 'Java Developer',
 'Mechanical Engineer',
 'Network Security Engineer',
 'Operations Manager',
 'PMO (Project Management office)',
 'Python Developer',
 'SAP Developer',
 'Sales',
 'Testing',
 'Web Designing']

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def trans_func(inp):
    inp = inp.apply(lambda x: cleanResume(x))
    return inp.values


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def extract_data(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    return data

def course_recommender(role):
    course_list = df[df['Sub-Category']==skills_dict[role][1]][['Title','URL']].values.tolist()
    st.subheader("Courses & Certificates:mortar_board: Recommendations")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 1000, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

st.set_page_config(
        page_title = 'Profile Builder App',
        page_icon='Parsers-Banner.png'
    )

with open('model_pipe','rb') as f:
    model = pickle.load(f)
df = pd.read_csv("Online_Courses.csv")
df = df.drop_duplicates(subset=['Title'])

st.title('Resume Analyser')
img = Image.open('Parsers-Banner.png')
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(img)



resume = st.file_uploader("Upload your resume",type=['pdf'])

if resume:
    with open('resume.pdf','wb') as f:
        f.write(resume.getbuffer())
        show_pdf("resume.pdf")
    data = extract_data("resume.pdf")
    if data:
        st.success("Hello " + data['name'])
        st.subheader("Your Basic Info")
        try:
            st.text('Name: ' + data['name'])
            st.text('Email: ' + data['email'])
            st.text('Contact: ' + data['mobile_number'])
            st.text('Resume pages: ' + str(data['no_of_pages']))
        except:
            pass
        cand_level = ''
        if data['total_experience']:
            if data['total_experience']>5:
                cand_level = "Fresher"
            elif data['total_experience']>2:
                cand_level = "Intermediate"
            else:
                cand_level = "Fresher"
        else:
            if data['no_of_pages'] == 1:
                cand_level = "Fresher"
            elif data['no_of_pages'] == 2:
                cand_level = "Intermediate"
            elif data['no_of_pages'] >= 3:
                cand_level = "Experienced"
        st.markdown(f'''<h4 style='text-align: left; color: #d73b5c;'>You are looking {cand_level}.</h4>''',
                            unsafe_allow_html=True)
        
        ## Skill shows
        keywords = st_tags(label='### Skills that you have',
                            text='See our skills recommendation',
                            value=data['skills'], key='1')

        doc = fitz.open('resume.pdf')
        text = ""
        for page in doc:
            text+=page.get_text()
        role = roles[model.predict(pd.Series([text]))[0]]
        st.success(f"According to the analysis, you are interested in {role} jobs")
        st.subheader("Skills Recommendation:brain:")
        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                            text='Recommended skills generated from System',
                                            value=skills_dict[role][0], key='2')
        st.markdown(
            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
            unsafe_allow_html=True)
        
        ### Resume writing recommendation
        st.subheader("Resume Tips & Ideas:bulb:")
        resume_score = 0
        if 'Objective' in text:
            resume_score = resume_score + 20
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                unsafe_allow_html=True)

        if 'Declaration' in text:
            resume_score = resume_score + 20
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',
                unsafe_allow_html=True)

        if 'Hobbies' or 'Interests' in text:
            resume_score = resume_score + 20
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                unsafe_allow_html=True)

        if 'Achievements' in text:
            resume_score = resume_score + 20
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                unsafe_allow_html=True)

        if 'Projects' in text:
            resume_score = resume_score + 20
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',
                unsafe_allow_html=True)

        st.subheader("Resume Score:memo:")
        st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: #d73b5c;
                }
            </style>""",
            unsafe_allow_html=True,
        )
        my_bar = st.progress(0)
        score = 0
        for percent_complete in range(resume_score):
            score += 1
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        st.success('Your Resume Writing Score: ' + str(score))
        st.warning(
            "Note: This score is calculated based on the content that you have added in your Resume")
        st.balloons()



        rec_course = course_recommender(role)