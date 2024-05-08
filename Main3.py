import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QScrollArea, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem, QDialog, QGridLayout
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon, QColor, QPixmap
import mysql.connector 
import pandas as pd
import pickle 
import os 
from sklearn.model_selection import train_test_split
from xgboost import DMatrix
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SurveyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Survey Application")
        self.setWindowIcon(QIcon('AnalyticsLogo.jpg'))
        self.app_icon = QApplication.instance().setWindowIcon(QIcon('AnalyticsLogo.jpg'))
        self.username = ""
        self.password = ""
        self.emp_no = None  # Initialize EmpNo
        self.is_admin = None
        self.model = None
        self.logistic_model = None
        self.sgd_model = None
        self.surveys = ["Employee Survey", "Management Survey"]
        self.selected_survey = None

        self.questions = [
            ("Revenue", "Do you think the company's revenue is sufficient for its operations?", ["Yes", "No"]),
            ("Expenses", "Are you satisfied with how the company manages its expenses?", ["Yes", "No"]),
            ("NetIncome", "Do you believe the company's net income accurately reflects its financial performance?", ["Yes", "No"]),
            ("Assets", "Do you think the company effectively utilizes its assets?", ["Yes", "No"]),
            ("Liabilities", "Are you concerned about the company's liabilities affecting its financial health?", ["No", "Yes"]),
            ("Equity", "Do you believe the company's equity adequately represents its shareholders' value?", ["Yes", "No"]),
            ("OperatingCashFlow", "Do you think the company's operating cash flow is efficiently managed?", ["Yes", "No"]),
            ("Age", "Is your age group between 25 - 45 (Lower Level) or 45 - 65(Upper Level)?", ["Lower Level", "Upper Level"]),
            ("Gender", "What is your gender?", ["Male", "Female"]),
            ("EmploymentStatus", "Should the company provide different benefits based on employment status?", ["Yes", "No"]),
            ("Compensation", "Are you satisfied with your compensation package?", ["Yes", "No"]),
            ("CompanyScale", "Do you think the company's scale impacts its agility and decision-making?", ["Yes", "No"]),
            ("LearningDevelopment", "Should the company invest more in employee learning and development?", ["No", "Yes"]),
            ("JobDemandsvsControl", "Do you feel there is a balance between job demands and control in your role?", ["Yes", "No"]),
            ("JobStrainBurnout", "Do you feel stressed or burnt out due to your job responsibilities?", ["No", "Yes"]),
            ("CustomerSegmentation", "Should the company invest in customer segmentation for targeted marketing?", ["No", "Yes"]),
            ("GeographicSegmentation", "Which part of the Global Market do you belong to?", ["East", "West"])
        ]

        self.login_layout()
        
    def login_layout(self):
        
        layout = QVBoxLayout(self)

        heading_label = QLabel("Machine Learning Framework for Multi-Level Classification of Company Revenue")
        heading_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        layout.addWidget(heading_label)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(115, 147, 179))  # Light gray background
        self.setPalette(palette)

        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("font-weight: bold; color: black;")
        self.username_entry = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("font-weight: bold; color: black;")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #f0f0f0;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

    def login(self):
        self.username = self.username_entry.text()
        self.password = self.password_entry.text()

        if not self.username or not self.password:
            self.show_message("Error", "Username and Password are required.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpana1!",
                database="survey"
            )

            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*), EmpNo FROM LoginCred WHERE Username = '{self.username}' AND Password = '{self.password}'")
            count, emp_no = cursor.fetchone()
            print(emp_no)

            if count == 1:
                self.emp_no = emp_no  # Store the EmpNo
                cursor.execute(f"SELECT WORKDEPT FROM EMPLOYEE WHERE EMPNO = {self.emp_no}")
                dept_id = cursor.fetchone()[0]
                print(dept_id)
                self.is_admin = dept_id == 105
                if self.is_admin:
                    print("In the correct If Statement")
                    self.show_admin_options()
                else:
                    print("This is where things are going wrong")
                    self.show_surveys()
                    return  # Don't proceed further if user is admin
            else:
                self.show_message("Error", "Invalid Username or Password.")

            cursor.close()

        except mysql.connector.Error as e:
            self.show_message("Error", f"Database Error: {e}")


    def show_admin_options(self):
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        heading_label = QLabel("THE ADMIN MENU")
        heading_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        layout.addWidget(heading_label)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))  # Very light gray background
        self.setPalette(palette)

        responses_button = QPushButton("Responses Collected")
        responses_button.setStyleSheet("font-weight: bold; color: black;")
        responses_button.clicked.connect(self.show_responses)
        responses_description = QLabel("The Responses collected button ensures that the data collected from the users are accurate "
                                    "and can be used to verify data accuracy.")
        layout.addWidget(responses_button)
        layout.addWidget(responses_description)

        analyze_button = QPushButton("Analyze")
        analyze_button.setStyleSheet("font-weight: bold; color: black;")
        analyze_button.clicked.connect(self.analyze_responses)
        analyze_description = QLabel("The Analyze Option will give more information about the three Machine learning models, "
                                  "by Displaying their Classification Reports and Confusion Matrix.")
        layout.addWidget(analyze_button)
        layout.addWidget(analyze_description)

        responses_button.setStyleSheet("background-color: #E57F84;")  # Light green button color
        analyze_button.setStyleSheet("background-color: #4297A0;")     # Light blue button color


    def analyze_responses(self):
        # Load models
        self.load_models()

        # Placeholder for performing analysis and gathering results
        # Replace this placeholder with actual analysis and result gathering code
        analysis_results = "Placeholder for analysis results.\nReplace this with actual analysis."
        df = pd.read_csv("Dataset9.csv")
        X = df[['Revenue', 'Expenses', 'NetIncome', 'Assets', 'Liabilities', 'Equity',
                'OperatingCashFlow', 'Age', 'Gender', 'EmploymentStatus', 'Compensation',
                'CompanyScale', 'LearningDevelopment', 'JobDemandsvsControl', 'JobStrainBurnout',
                'CustomerSegmentation', 'GeographicSegmentation']]
        Y = df["Revenue Level"]
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.3)

        dtest = DMatrix(X_Test, label=Y_Test)

        accuracy_scores = []

        xgb_pred = self.model.predict(dtest)
        xgb_accuracy = accuracy_score(Y_Test, xgb_pred)
        print(xgb_accuracy)
        accuracy_scores.append(xgb_accuracy)

        lr_pred = self.logistic_model.predict(X_Test)
        lr_accuracy = accuracy_score(Y_Test, lr_pred)
        print(lr_accuracy)
        accuracy_scores.append(lr_accuracy)

        sgd_pred = self.sgd_model.predict(X_Test)
        sgd_accuracy = accuracy_score(Y_Test, sgd_pred)
        print(sgd_accuracy)
        accuracy_scores.append(sgd_accuracy)

        # Create a new ResultsWindow
        results_window = ResultsWindow()

        # Add classification reports to the window
        results_window.add_label("Classification Report for XGBoost:")
        results_window.add_label(classification_report(Y_Test, xgb_pred))
        results_window.add_label("Confusion Matrix for XGBoost:")
        results_window.add_label(str(confusion_matrix(Y_Test, xgb_pred)))

        results_window.add_label("Classification Report for Logistic Regression:")
        results_window.add_label(classification_report(Y_Test, lr_pred, zero_division=1))
        results_window.add_label("Confusion Matrix for Logistic Regression:")
        results_window.add_label(str(confusion_matrix(Y_Test, lr_pred)))

        results_window.add_label("Classification Report for Stochastic Gradient Descent:")
        results_window.add_label(classification_report(Y_Test, sgd_pred, zero_division=1))
        results_window.add_label("Confusion Matrix for Stochastic Gradient Descent:")
        results_window.add_label(str(confusion_matrix(Y_Test, sgd_pred)))

        # Add the accuracy graph to the window
        results_window.add_image('Graph.jpg')

        # Show the results window
        results_window.show()

    def show_surveys(self):
        # Hide the login widgets
        self.username_label.hide()
        self.username_entry.hide()
        self.password_label.hide()
        self.password_entry.hide()
        self.login_button.hide()
        layout = self.layout()  # Get the existing layout

        welcome_label = QLabel("Welcome Employee!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)
        # Add the top text
        top_text = QLabel("Machine Learning Framework for Multi-Level Classification of Company Revenue")
        top_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(top_text)

        # Add about text
        about_text = QLabel("About this Software\n\nThis Software deals with the Survey data and analyzes this data to show the Revenue Level Prediction using Machine Learning")
        about_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_text)

        # Add the menu
        menu_text = QLabel("The Menu")
        menu_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(menu_text)


        # Add buttons for Employee Survey and Management Survey
        employee_button = QPushButton("Employee Survey")
        employee_button.clicked.connect(lambda: self.show_survey_questions("Employee Survey"))
        employee_button.setFixedSize(150, 30)
        layout.addWidget(employee_button, alignment=Qt.AlignCenter)
        # layout.addWidget(employee_button)

        employee_info = QLabel(
        "Employee Survey Information:\n\n"
        "The Employee Survey is designed to gather feedback and insights from employees\n "
        "about various aspects of the organization, including work environment,\n "
        "job satisfaction, company policies, and more. By taking this survey, employees\n "
        "can contribute their thoughts and suggestions, which can help the organization\n "
        "identify areas for improvement and make data-driven decisions to foster growth.\n"
        )
        employee_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(employee_info)
        employee_button.setStyleSheet("background-color: #e6f3ff;")

        management_button = QPushButton("Management Survey")
        management_button.clicked.connect(lambda: self.show_survey_questions("Management Survey"))
        management_button.setFixedSize(150, 30)
        layout.addWidget(management_button, alignment=Qt.AlignCenter)
        # layout.addWidget(management_button)

        management_info = QLabel(
        "Management Survey Information:\n\n"
        "The Management Survey is targeted towards managers and supervisors\n "
        "to evaluate leadership effectiveness, team dynamics, communication channels,\n "
        "and strategic alignment within the organization. Feedback from this survey\n "
        "helps management identify areas of strength and improvement, enabling them\n "
        "to make informed decisions and drive organizational success.\n"
        )
        management_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(management_info)
        management_button.setStyleSheet("background-color: #ccffcc;")  # Light green color



    def load_models(self):
        models = ['logistic_regression_model.pkl', 'sgd_model.pkl', 'MultiClassXGBoostModel.pkl']
        for model_file in models:
            if not os.path.isfile(model_file):
                print(f"Error: Model file '{model_file}' not found.")
            else:
                try:
                    with open(model_file, 'rb') as f:
                        if model_file == 'logistic_regression_model.pkl':
                            self.logistic_model = pickle.load(f)
                        elif model_file == 'sgd_model.pkl':
                            self.sgd_model = pickle.load(f)
                        elif model_file == 'MultiClassXGBoostModel.pkl':
                            self.model = pickle.load(f)
                    print(f"{model_file} loaded successfully!")
                except Exception as e:
                    print(f"Error loading model {model_file}: {e}")

    

    def show_responses(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpana1!",
                database="survey"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Responses")
            rows = cursor.fetchall()

            headers = ["Revenue", "Expenses", "NetIncome", "Assets", "Liabilities", "Equity", "OperatingCashFlow", "Age", "Gender", "EmploymentStatus", "Compensation", "CompanyScale", "LearningDevelopment", "JobDemandsvsControl", "JobStrainBurnout", "CustomerSegmentation", "GeographicSegmentation"]
            dialog = ResponsesDialog(rows, headers)
            dialog.exec_()

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            self.show_message("Error", f"Database Error: {e}")

    def show_survey_questions(self, survey_name):
        if survey_name != "Employee Survey":
            return

        survey_id = 98765688  # Hardcoded Survey ID for Employee Survey

        # Check if the survey has already been taken
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpana1!",
                database="survey"
            )

            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM SURVEYSTAKEN WHERE Empno = {self.emp_no} AND SURVEYID = {survey_id}")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if count == 1:
                self.show_message("Survey Already Taken", "You have already taken this survey.")
                return
        except mysql.connector.Error as e:
            self.show_message("Error", f"Database Error: {e}")

        # Survey has not been taken, proceed to display questions
        layout = self.layout()
        self.selected_survey = survey_name
        self.selected_options = {}  # Dictionary to store selected options for each question
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        scroll_layout = QVBoxLayout(scroll_widget)
    
        # Define the updated questions and options
        questions = [
            ("Revenue", "How would you rate the company's revenue growth strategy?",
            ["Strategically Aligned for Maximum Growth", "Satisfactory with Potential for Improvement",
            "Adequate for Current Operations", "Inadequate and Requires Immediate Attention"]),
            ("OperatingCashFlow", "How effectively does the company manage its operating cash flow to support its operations?",
            ["Optimally Managed to Ensure Stability and Growth", "Adequately Maintained with Room for Optimization",
            "Requires Immediate Attention to Prevent Cash Flow Issues", "Unsure or Not Applicable"]),
            ("Compensation", "How satisfied are you with your current compensation package?",
            ["Very Satisfied with Competitive Benefits and Incentives", "Satisfied, but Open to Improvement Opportunities",
            "Dissatisfied with Compensation and Seeking Adjustments", "Extremely Dissatisfied and Considering Alternatives"]),
            ("JobDemandsvsControl", "To what extent do you feel there is a balance between job demands and control in your current role?",
            ["Well-Balanced with Clear Autonomy and Supportive Environment", "Mostly Balanced, but Some Areas Could Be Improved",
            "Imbalanced with High Demands and Limited Control Over Tasks", "Severely Imbalanced, Leading to Stress and Overwhelming Workload"]),
            ("Expenses", "How effectively does the company manage its expenses to optimize profitability?",
            ["Strategically Controlled to Maximize Efficiency", "Managed Well, but Could Be Streamlined Further",
            "Excessive and Inefficient, Hindering Profitability", "Unsure or Not Applicable"]),
            ("NetIncome", "How accurately does the company's net income reflect its financial performance?",
            ["Highly Accurate Representation of Financial Health", "Generally Reflective, with Minor Discrepancies",
            "Somewhat Inaccurate and Requires Adjustment", "Completely Inaccurate, Misleading Financial Analysis"]),
            ("Assets", "How efficiently does the company utilize its assets to generate returns?",
            ["Optimally Leveraged for Maximum Returns", "Utilized Well, with Potential for Further Optimization",
            "Underutilized, Leading to Suboptimal Returns", "Unsure or Not Applicable"]),
            ("Liabilities", "To what extent are you concerned about the company's liabilities impacting its financial stability?",
            ["Confident in Managing Liabilities for Financial Stability", "Slightly Concerned, but Managed within Acceptable Limits",
            "Moderately Concerned, Potentially Affecting Financial Health", "Highly Concerned, Significantly Threatening Financial Stability"]),
            ("Equity", "How fair do you perceive the distribution of equity among shareholders?",
            ["Equitably Distributed, Ensuring Shareholder Value", "Fairly Distributed, with Some Room for Improvement",
            "Unequally Distributed, Resulting in Shareholder Discontent", "Completely Unfair, Marginalizing Certain Shareholders"]),
            ("Age", "To what extent do you believe age should be considered in determining job roles and responsibilities?",
            ["Highly Considered to Ensure Diversity and Inclusion", "Moderately Considered, Balancing Experience and Innovation",
            "Minimally Considered, Focusing on Skills and Performance", "Not Considered at All, Emphasizing Meritocracy Over Age"]),
            ("Gender", "How important do you think gender diversity is in fostering a positive workplace culture?",
            ["Extremely Important for Inclusive and Dynamic Work Environment", "Significantly Important, Enhancing Perspectives and Collaboration",
            "Moderately Important, Recognizing the Value of Diverse Teams", "Not Important, Prioritizing Skillset Regardless of Gender"]),
            ("EmploymentStatus", "Should the company provide different benefits based on an employee's employment status?",
            ["Strongly Agree to Cater to Diverse Employee Needs", "Agree, with Flexibility to Accommodate Various Employment Types",
            "Disagree, Favoring Uniform Benefits for All Employees", "Strongly Disagree, Advocating for Equal Treatment Regardless of Status"]),
            ("CompanyScale", "How do you perceive the impact of the company's scale on its agility and decision-making processes?",
            ["Highly Positive, Leveraging Scale for Competitive Advantage", "Moderately Positive, Balancing Scale with Flexibility",
            "Moderately Negative, Hindered by Bureaucracy and Complexity", "Highly Negative, Scale Impeding Innovation and Responsiveness"]),
            ("LearningDevelopment", "How much importance do you place on the company's investment in employee learning and development programs?",
            ["Very Important for Career Growth and Skill Enhancement", "Moderately Important, Recognizing Value in Continuous Learning",
            "Somewhat Unimportant, Focusing on Immediate Tasks Over Development", "Completely Unimportant, Prioritizing Operational Efficiency Over Growth"]),
            ("JobStrainBurnout", "How often do you experience feelings of stress or burnout due to your job responsibilities?",
            ["Very Rarely, Maintaining Healthy Work-Life Balance", "Rarely, with Occasional Challenges but Manageable Stress Levels",
            "Frequently, Struggling with High Workload and Pressure", "Very Frequently, Experiencing Chronic Burnout and Mental Exhaustion"]),
            ("CustomerSegmentation", "How valuable do you think customer segmentation is for the company's targeted marketing efforts?",
            ["Extremely Valuable for Personalized Customer Engagement", "Highly Valuable, Enhancing Relevance and Effectiveness of Marketing",
            "Somewhat Invaluable, Preferring Broad Marketing Strategies", "Completely Invaluable, Prioritizing Generalized Marketing Approach"]),
            ("GeographicSegmentation", "How essential do you believe geographic segmentation is for the company's expansion into new markets?",
            ["Highly Essential for Localized Market Penetration Strategies", "Moderately Essential, Tailoring Offerings to Regional Preferences",
            "Somewhat Non-Essential, Preferring Universal Market Approach", "Completely Non-Essential, Prioritizing Globalized Market Presence"])
        ]

        for question_id, question_text, options in questions:
            question_label = QLabel(question_text)
            scroll_layout.addWidget(question_label)

            option_radio_group = QButtonGroup()  # Create a button group for each question
            for option_text in options:
                option_radio = QRadioButton(option_text)
                option_radio_group.addButton(option_radio)  # Add the radio button to the button group
                scroll_layout.addWidget(option_radio)

            # Store the button group reference for the question
            self.selected_options[question_id] = option_radio_group

        submit_button = QPushButton("Submit Survey")
        submit_button.clicked.connect(self.submit_survey)
        scroll_layout.addWidget(submit_button)

    def submit_survey(self):
        # Dictionary to map option texts to their corresponding values
        option_values = {
            "Strategically Aligned for Maximum Growth": 1,
            "Satisfactory with Potential for Improvement": 2,
            "Adequate for Current Operations": 3,
            "Inadequate and Requires Immediate Attention": 4,
            "Optimally Managed to Ensure Stability and Growth": 1,
            "Adequately Maintained with Room for Optimization": 2,
            "Requires Immediate Attention to Prevent Cash Flow Issues": 3,
            "Unsure or Not Applicable": 4,
            "Very Satisfied with Competitive Benefits and Incentives": 1,
            "Satisfied, but Open to Improvement Opportunities": 2,
            "Dissatisfied with Compensation and Seeking Adjustments": 3,
            "Extremely Dissatisfied and Considering Alternatives": 4,
            "Well-Balanced with Clear Autonomy and Supportive Environment": 1,
            "Mostly Balanced, but Some Areas Could Be Improved": 2,
            "Imbalanced with High Demands and Limited Control Over Tasks": 3,
            "Severely Imbalanced, Leading to Stress and Overwhelming Workload": 4,
            "Strategically Controlled to Maximize Efficiency": 1,
            "Managed Well, but Could Be Streamlined Further": 2,
            "Excessive and Inefficient, Hindering Profitability": 3,
            "Unsure or Not Applicable": 4,
            "Highly Accurate Representation of Financial Health": 1,
            "Generally Reflective, with Minor Discrepancies": 2,
            "Somewhat Inaccurate and Requires Adjustment": 3,
            "Completely Inaccurate, Misleading Financial Analysis": 4,
            "Optimally Leveraged for Maximum Returns": 1,
            "Utilized Well, with Potential for Further Optimization": 2,
            "Underutilized, Leading to Suboptimal Returns": 3,
            "Unsure or Not Applicable": 4,
            "Confident in Managing Liabilities for Financial Stability": 1,
            "Slightly Concerned, but Managed within Acceptable Limits": 2,
            "Moderately Concerned, Potentially Affecting Financial Health": 3,
            "Highly Concerned, Significantly Threatening Financial Stability": 4,
            "Equitably Distributed, Ensuring Shareholder Value": 1,
            "Fairly Distributed, with Some Room for Improvement": 2,
            "Unequally Distributed, Resulting in Shareholder Discontent": 3,
            "Completely Unfair, Marginalizing Certain Shareholders": 4,
            "Highly Considered to Ensure Diversity and Inclusion": 1,
            "Moderately Considered, Balancing Experience and Innovation": 2,
            "Minimally Considered, Focusing on Skills and Performance": 3,
            "Not Considered at All, Emphasizing Meritocracy Over Age": 4,
            "Extremely Important for Inclusive and Dynamic Work Environment": 1,
            "Significantly Important, Enhancing Perspectives and Collaboration": 2,
            "Moderately Important, Recognizing the Value of Diverse Teams": 3,
            "Not Important, Prioritizing Skillset Regardless of Gender": 4,
            "Strongly Agree to Cater to Diverse Employee Needs": 1,
            "Agree, with Flexibility to Accommodate Various Employment Types": 2,
            "Disagree, Favoring Uniform Benefits for All Employees": 3,
            "Strongly Disagree, Advocating for Equal Treatment Regardless of Status": 4,
            "Highly Positive, Leveraging Scale for Competitive Advantage": 1,
            "Moderately Positive, Balancing Scale with Flexibility": 2,
            "Moderately Negative, Hindered by Bureaucracy and Complexity": 3,
            "Highly Negative, Scale Impeding Innovation and Responsiveness": 4,
            "Very Important for Career Growth and Skill Enhancement": 1,
            "Moderately Important, Recognizing Value in Continuous Learning": 2,
            "Somewhat Unimportant, Focusing on Immediate Tasks Over Development": 3,
            "Completely Unimportant, Prioritizing Operational Efficiency Over Growth": 4,
            "Very Rarely, Maintaining Healthy Work-Life Balance": 1,
            "Rarely, with Occasional Challenges but Manageable Stress Levels": 2,
            "Frequently, Struggling with High Workload and Pressure": 3,
            "Very Frequently, Experiencing Chronic Burnout and Mental Exhaustion": 4,
            "Extremely Valuable for Personalized Customer Engagement": 1,
            "Highly Valuable, Enhancing Relevance and Effectiveness of Marketing": 2,
            "Somewhat Invaluable, Preferring Broad Marketing Strategies": 3,
            "Completely Invaluable, Prioritizing Generalized Marketing Approach": 4,
            "Highly Essential for Localized Market Penetration Strategies": 1,
            "Moderately Essential, Tailoring Offerings to Regional Preferences": 2,
            "Somewhat Non-Essential, Preferring Universal Market Approach": 3,
            "Completely Non-Essential, Prioritizing Globalized Market Presence": 4
        }

        response_values = []
        for question_id, _, options in self.questions:
            option_radio_group = self.selected_options[question_id]
            for i, option_radio in enumerate(option_radio_group.buttons()):
                if option_radio.isChecked():
                    # Append the option's ID (1-indexed)
                    response_values.append(i + 1)

        # Insert survey responses into Responses table
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpana1!",
                database="survey"
            )

            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO Responses VALUES ({', '.join(map(str, response_values))})")
            cursor.execute(f"INSERT INTO SURVEYSTAKEN (EmpNo, SURVEYID) VALUES ({self.emp_no}, 98765688)")
            conn.commit()
            cursor.close()
            conn.close()

            self.show_message("Survey Saved", "Your survey responses have been saved.")
            self.show_surveys()  # Redirect to Surveys Available page
        except mysql.connector.Error as e:
            self.show_message("Error", f"Database Error: {e}")



    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

class ResponsesDialog(QDialog):
    def __init__(self, rows, headers):
        super().__init__()
        self.setWindowTitle("Survey Responses")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        layout = QGridLayout()
        self.setLayout(layout)

        table = QTableWidget()
        table.setRowCount(len(rows))
        table.setColumnCount(len(rows[0]))
        table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table.setItem(i, j, item)

        table.resizeColumnsToContents()
        layout.addWidget(table)

class AnalyzeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analysis Result")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        label = QLabel("Analysis Result will be displayed here.")
        layout.addWidget(label)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        super(MatplotlibWidget, self).__init__(self.fig)
        self.setParent(parent)

    def plot(self, model_names, accuracy_scores):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.bar(model_names, accuracy_scores, color=['Red', 'Green', 'Blue'])
        ax.set_ylim(0.1, 1)
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy of Different Models')
        self.canvas.draw()

class ResultsWindow(QWidget):
    def __init__(self, parent=None):
        super(ResultsWindow, self).__init__(parent)
        self.setWindowTitle("Results")
        layout = QVBoxLayout()
        self.setLayout(layout)

        software_info_label = QLabel("<div align='center'><font size='10'><b>Machine Learning Framework for Multi Level Classification of Company Revenue</b></font></div><br>"
                                    "<font size='5'>This Software deals with taking in survey responses but at the same time also comparing which type of Machine Learning model is suitable for HRM Data. Human Resource Management Data could be large</font><br>"
                                    "<font size='5'>and complex and is not something that can be dealt with by regular Data Analysis or Machine Learning models The planning and execution of a business strategy are important aspects of the </font><br>"
                                    "<font size='5'>strategic human resource management of a company. In previous studies, machine learning algorithms were used to determine the main factors correlating employees with company performance.</font><br>"
                                    "<font size='5'>In this study, we introduced a method based on machine-learning algorithms for the classifcation of company revenue.</font><br>"
                                    "<font size='5'>The performance of the proposed method was validated using six evaluation metrics:</font><br>"
                                    "<font size='5'>accuracy, precision, recall, F1-score, receiver operating characteristic curve, and area under the curve. As the project results indicate, the XGBoost classifer displayed the best classifcation performance among</font><br>"
                                    "<font size='5'>the three algorithms (XGBoost classifer, stochastic gradient descent classifer, and logistic regression) used in this study. Moreover, we confrmed the important features of the trained XGBoost model in</font><br>"
                                    "<font size='5'>accordance with variables focusing on human resource management studies.</font><br>"
                                    "<font size='4'>The Below are the Classification Reports and Confusion Matrix for the three Machine Learning model used.</font>")
        layout.addWidget(software_info_label)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow resizing of the scroll area
        layout.addWidget(scroll_area)

        # Create a widget to hold the contents
        self.scroll_content_widget = QWidget()
        scroll_area.setWidget(self.scroll_content_widget)

        # Create a layout for the content widget
        self.scroll_content_layout = QVBoxLayout()
        self.scroll_content_widget.setLayout(self.scroll_content_layout)

        # Create MatplotlibWidget instance
        self.matplotlib_widget = MatplotlibWidget()

        # Add MatplotlibWidget to scroll content layout
        self.scroll_content_layout.addWidget(self.matplotlib_widget)

    def add_label(self, text):
        label = QLabel(text)
        self.scroll_content_layout.addWidget(label)

    def add_image(self, path):
        pixmap = QPixmap(path)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        self.scroll_content_layout.addWidget(image_label)


    def add_image(self, path):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaledToWidth(600)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        self.layout().addWidget(image_label)



app = QApplication(sys.argv)
survey_app = SurveyApp()
survey_app.show()
sys.exit(app.exec_())