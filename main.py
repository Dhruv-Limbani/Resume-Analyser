import streamlit as st
import base64
from pyresparser import ResumeParser
import re
import pickle
import pandas as pd
import fitz
from streamlit_tags import st_tags
import nltk
nltk.download('stopwords')
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
 'PMO',
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

with open('model_pipe','rb') as f:
    model = pickle.load(f)


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def extract_data(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    return data


st.title('Resume Analyser')

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
        if data['no_of_pages'] == 1:
            cand_level = "Fresher"
            st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                        unsafe_allow_html=True)
        elif data['no_of_pages'] == 2:
            cand_level = "Intermediate"
            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                        unsafe_allow_html=True)
        elif data['no_of_pages'] >= 3:
            cand_level = "Experienced"
            st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                        unsafe_allow_html=True)
        st.subheader("**Skills Recommendation💡**")
        ## Skill shows
        keywords = st_tags(label='### Skills that you have',
                            text='See our skills recommendation',
                            value=data['skills'], key='1')

        ##  recommendation
        ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                        'streamlit']
        web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                        'javascript', 'angular js', 'c#', 'flask']
        android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
        ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
        uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                        'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                        'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                        'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                        'user research', 'user experience']
        
        recommended_skills = []
        reco_field = ''
        rec_course = ''
        # ## Courses recommendation
        # for i in data['skills']:
        #     ## Data science recommendation
        #     if i.lower() in ds_keyword:
        #         print(i.lower())
        #         reco_field = 'Data Science'
        #         st.success("** Our analysis says you are looking for Data Science Jobs.**")
        #         recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
        #                                 'Data Mining', 'Clustering & Classification', 'Data Analytics',
        #                                 'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
        #                                 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
        #                                 'Streamlit']
        #         recommended_keywords = st_tags(label='### Recommended skills for you.',
        #                                         text='Recommended skills generated from System',
        #                                         value=recommended_skills, key='2')
        #         st.markdown(
        #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
        #             unsafe_allow_html=True)
        #         rec_course = course_recommender(ds_course)
        #         break

        #     ## Web development recommendation
        #     elif i.lower() in web_keyword:
        #         print(i.lower())
        #         reco_field = 'Web Development'
        #         st.success("** Our analysis says you are looking for Web Development Jobs **")
        #         recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
        #                                 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
        #         recommended_keywords = st_tags(label='### Recommended skills for you.',
        #                                         text='Recommended skills generated from System',
        #                                         value=recommended_skills, key='3')
        #         st.markdown(
        #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
        #             unsafe_allow_html=True)
        #         rec_course = course_recommender(web_course)
        #         break

        #     ## Android App Development
        #     elif i.lower() in android_keyword:
        #         print(i.lower())
        #         reco_field = 'Android Development'
        #         st.success("** Our analysis says you are looking for Android App Development Jobs **")
        #         recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
        #                                 'Kivy', 'GIT', 'SDK', 'SQLite']
        #         recommended_keywords = st_tags(label='### Recommended skills for you.',
        #                                         text='Recommended skills generated from System',
        #                                         value=recommended_skills, key='4')
        #         st.markdown(
        #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
        #             unsafe_allow_html=True)
        #         rec_course = course_recommender(android_course)
        #         break

        #     ## IOS App Development
        #     elif i.lower() in ios_keyword:
        #         print(i.lower())
        #         reco_field = 'IOS Development'
        #         st.success("** Our analysis says you are looking for IOS App Development Jobs **")
        #         recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
        #                                 'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
        #                                 'Auto-Layout']
        #         recommended_keywords = st_tags(label='### Recommended skills for you.',
        #                                         text='Recommended skills generated from System',
        #                                         value=recommended_skills, key='5')
        #         st.markdown(
        #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
        #             unsafe_allow_html=True)
        #         rec_course = course_recommender(ios_course)
        #         break

        #     ## Ui-UX Recommendation
        #     elif i.lower() in uiux_keyword:
        #         print(i.lower())
        #         reco_field = 'UI-UX Development'
        #         st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
        #         recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
        #                                 'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
        #                                 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
        #                                 'Solid', 'Grasp', 'User Research']
        #         recommended_keywords = st_tags(label='### Recommended skills for you.',
        #                                         text='Recommended skills generated from System',
        #                                         value=recommended_skills, key='6')
        #         st.markdown(
        #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
        #             unsafe_allow_html=True)
        #         rec_course = course_recommender(uiux_course)
        #         break

        
        #st.write(data)
        doc = fitz.open('resume.pdf')
        text = ""
        for page in doc:
            text+=page.get_text()
        st.info(f"You are interested in {roles[model.predict(pd.Series([text]))[0]]}")