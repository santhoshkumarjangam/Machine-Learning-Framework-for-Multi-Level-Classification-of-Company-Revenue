USE SURVEY;

-- Create the user_responses table
CREATE TABLE user_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    response TEXT NOT NULL,
    UNIQUE KEY unique_response (user_id, question_id),
    FOREIGN KEY (user_id) REFERENCES USERS(EmpNo),
    FOREIGN KEY (question_id) REFERENCES survey_questions(id)
);

-- Create the survey_questions table
CREATE TABLE survey_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL
);

DROP TABLE surveys;


SHOW TABLES;

-- Create the user_responses table
CREATE TABLE user_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    response TEXT NOT NULL,
    UNIQUE KEY unique_response (user_id, question_id),
    FOREIGN KEY (user_id) REFERENCES USERS(EmpNo),
    FOREIGN KEY (question_id) REFERENCES survey_questions(id)
);

-- Create the survey_questions table
CREATE TABLE survey_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL
);

CREATE TABLE LOGINCRED(
      Username VARCHAR(30) PRIMARY KEY,
      Password VARCHAR(30) NOT NULL,
      EMPNO BIGINT REFERENCES EMPLOYEE(EMPNO)
);

INSERT INTO LOGINCRED (Username, Password, EMPNO) VALUES
('john_a_dexter', 'p@55w0rd!', 1),
('jane_m_smith', '1234xyz', 2),
('bob_e_johnson', '!9876word', 3),
('alice_k_williams', '6543abc', 4),
('charlie_r_brown', 'qwerty2345', 5),
('eva_l_davis', 'p@ss8765', 6),
('george_a_johnson', '3456word!', 7),
('helen_s_jones', 'p@55w0rd', 8),
('david_p_clark', '!secure123', 9),
('grace_t_martin', '5678word', 10),
('frank_m_anderson', '!9876p@55', 11),
('irene_b_baker', '6543!word', 12),
('jack_s_evans', 'p@55word2345', 13),
('katherine_c_harris', '8765abc', 14),
('leo_j_wong', '!p@ss3456', 15),
('marilyn_l_miller', '!7890secure', 16),
('nathan_r_turner', 'password!secure', 17),
('olivia_e_barnes', '!5678p@ss', 18),
('peter_w_white', '!9876secure', 19),
('quinn_g_roberts', 'word!6543', 20),
('robert_h_lee', 'p@ss2345!', 21),
('samantha_f_young', '8765p@ss!', 22),
('timothy_j_taylor', '!secure3456', 23),
('ursula_k_brown', 'p@ss7890!', 24),
('vincent_l_garcia', '123!secure', 25),
('wendy_n_cooper', 'p@ss5678!', 26),
('xavier_q_lopez', '!9876qwerty', 27),
('yvonne_r_reyes', '6543p@ss!', 28),
('zachary_s_ward', '!p@ss2345', 29),
('amy_d_hill', '!secure8765', 30);

INSERT INTO LOGINCRED(Username, Password, EMPNO)
VALUES ("vardhandasarly", "cfrgtjae", 31);


CREATE TABLE SURVEYSTAKEN(
    EmpNo BIGINT NOT NULL,
    SURVEYID BIGINT NOT NULL
);

TRUNCATE TABLE SURVEYSTAKEN;

SELECT * FROM SURVEYSTAKEN;


INSERT INTO SURVEYSTAKEN(EmpNo, SURVEYID) VALUES(31, 98765688);

DROP TABLE SURVEYSTAKEN;

CREATE TABLE Responses (
    Revenue TINYINT(1),
    Expenses TINYINT(1),
    NetIncome TINYINT(1),
    Assets TINYINT(1),
    Liabilities TINYINT(1),
    Equity TINYINT(1),
    OperatingCashFlow TINYINT(1),
    Age TINYINT(1),
    Gender TINYINT(1),
    EmploymentStatus TINYINT(1),
    Compensation TINYINT(1),
    CompanyScale TINYINT(1),
    LearningDevelopment TINYINT(1),
    JobDemandsvsControl TINYINT(1),
    JobStrainBurnout TINYINT(1),
    CustomerSegmentation TINYINT(1),
    GeographicSegmentation TINYINT(1)
);

SELECT * FROM Responses;

DELETE FROM Responses WHERE REVENUE LIKE 1 OR REVENUE LIKE 4;

DELETE FROM Responses
WHERE Revenue = -2;

CREATE TABLE EMPLOYEE(
       EMPNO       BIGINT       PRIMARY KEY,
       FIRSTNME    VARCHAR(12)     NOT NULL,
       MIDINIT     CHAR(1)         NOT NULL,
       LASTNAME    VARCHAR(15)     NOT NULL,
       WORKDEPT    INT REFERENCES     DEPT(DeptID),
       PHONENO     BIGINT,
       ADDRESS1    VARCHAR(250),
       ADDRESS2    VARCHAR(250),
       CITY        VARCHAR(50),
       STATES      VARCHAR(50),
       COUNTRY     VARCHAR(50),
       EDLEVEL     SMALLINT        NOT NULL,
       SEX         CHAR(1)                 ,
       BIRTHDATE   DATE                    
)

INSERT INTO EMPLOYEE (EMPNO, FIRSTNME, MIDINIT, LASTNAME, WORKDEPT, PHONENO, ADDRESS1, ADDRESS2, CITY, STATES, COUNTRY, EDLEVEL, SEX, BIRTHDATE)
VALUES
(1, 'John', 'D', 'Doe', 101, '1234', '123 Main St', 'Apt 456', 'Anytown', 'CA', 'USA', 16, 'M', '1990-05-15'),
(2, 'Jane', 'M', 'Smith', 102, '5678', '456 Oak St', 'Unit 789', 'Sometown', 'NY', 'USA', 18, 'F', '1988-12-10'),
(3, 'Bob', 'E', 'Johnson', 101, '9876', '789 Pine St', NULL, 'Othercity', 'TX', 'USA', 14, 'M', '1995-02-28'),
(4, 'Alice', 'K', 'Williams', 103, '6543', '321 Elm St', 'Suite 555', 'Somewhere', 'FL', 'USA', 20, 'F', '1985-08-20'),
(5, 'Charlie', 'R', 'Brown', 102, '2345', '111 Cedar St', NULL, 'Nowhere', 'AZ', 'USA', 16, 'M', '1992-07-03'),
(6, 'Eva', 'L', 'Davis', 103, '8765', '555 Pineapple Ave', 'Apt 123', 'Tropicaltown', 'FL', 'USA', 19, 'F', '1989-11-18'),
(7, 'George', 'A', 'Johnson', 101, '3456', '789 Oak St', 'Unit 456', 'Newcity', 'IL', 'USA', 17, 'M', '1993-04-05'),
(8, 'Helen', 'S', 'Jones', 104, '7890', '222 Maple St', 'Suite 789', 'Maplewood', 'NJ', 'USA', 18, 'F', '1987-09-25'),
(9, 'David', 'P', 'Clark', 102, '1234', '456 Pine St', NULL, 'Pinesville', 'CA', 'USA', 15, 'M', '1996-01-12'),
(10, 'Grace', 'T', 'Martin', 103, '5678', '789 Elm St', 'Apt 987', 'Greenville', 'SC', 'USA', 20, 'F', '1986-06-30'),
(11, 'Frank', 'M', 'Anderson', 101, '9876', '123 Maple St', 'Unit 321', 'Mapletown', 'WA', 'USA', 16, 'M', '1994-03-22'),
(12, 'Irene', 'B', 'Baker', 104, '6543', '555 Oak St', NULL, 'Oakville', 'OH', 'USA', 19, 'F', '1991-08-14'),
(13, 'Jack', 'S', 'Evans', 102, '2345', '321 Pine St', 'Suite 222', 'Pinewood', 'CO', 'USA', 17, 'M', '1990-02-08'),
(14, 'Katherine', 'C', 'Harris', 103, '8765', '789 Cedar St', 'Apt 555', 'Cedarville', 'IN', 'USA', 18, 'F', '1988-07-17'),
(15, 'Leo', 'J', 'Wong', 102, '3456', '111 Oak St', NULL, 'Oaktown', 'OR', 'USA', 15, 'M', '1995-12-03'),
(16, 'Marilyn', 'L', 'Miller', 104, '7890', '222 Pine St', 'Suite 444', 'Pinetown', 'LA', 'USA', 20, 'F', '1989-05-28'),
(17, 'Nathan', 'R', 'Turner', 101, '1234', '456 Cedar St', 'Apt 999', 'Cedarville', 'NV', 'USA', 14, 'M', '1992-10-11'),
(18, 'Olivia', 'E', 'Barnes', 103, '5678', '789 Maple St', 'Unit 777', 'Mapleville', 'MA', 'USA', 17, 'F', '1993-03-01'),
(19, 'Peter', 'W', 'White', 102, '9876', '123 Cedar St', NULL, 'Cedartown', 'WI', 'USA', 19, 'M', '1987-06-23'),
(20, 'Quinn', 'G', 'Roberts', 104, '6543', '555 Elm St', 'Suite 333', 'Elmsville', 'KY', 'USA', 16, 'F', '1996-09-19'),
(21, 'Robert', 'H', 'Lee', 101, '2345', '321 Cedar St', NULL, 'Cedarburg', 'SD', 'USA', 18, 'M', '1985-04-16'),
(22, 'Samantha', 'F', 'Young', 103, '8765', '789 Pine St', 'Apt 888', 'Pinetown', 'NC', 'USA', 20, 'F', '1990-01-30'),
(23, 'Timothy', 'J', 'Taylor', 102, '3456', '111 Oak St', NULL, 'Oakland', 'ID', 'USA', 15, 'M', '1994-07-08'),
(24, 'Ursula', 'K', 'Brown', 104, '7890', '222 Pine St', 'Unit 222', 'Pinesburg', 'KS', 'USA', 19, 'F', '1988-12-05'),
(25, 'Vincent', 'L', 'Garcia', 101, '1234', '456 Elm St', 'Apt 333', 'Elmtown', 'OK', 'USA', 17, 'M', '1992-04-24'),
(26, 'Wendy', 'N', 'Cooper', 103, '5678', '789 Pine St', 'Suite 666', 'Pinewood', 'MS', 'USA', 16, 'F', '1995-11-14'),
(27, 'Xavier', 'Q', 'Lopez', 102, '9876', '123 Oak St', NULL, 'Oakville', 'RI', 'USA', 18, 'M', '1989-08-07'),
(28, 'Yvonne', 'R', 'Reyes', 104, '6543', '321 Cedar St', 'Apt 111', 'Cedartown', 'MO', 'USA', 19, 'F', '1986-03-26'),
(29, 'Zachary', 'S', 'Ward', 101, '2345', '555 Elm St', 'Unit 777', 'Elmville', 'GA', 'USA', 20, 'M', '1991-10-18'),
(30, 'Amy', 'D', 'Hill', 103, '8765', '222 Pine St', 'Suite 444', 'Pinewood', 'AL', 'USA', 15, 'F', '1993-05-02');

INSERT INTO EMPLOYEE (EMPNO, FIRSTNME, MIDINIT, LASTNAME, WORKDEPT, PHONENO, ADDRESS1, ADDRESS2, CITY, STATES, COUNTRY, SEX, BIRTHDATE)
VALUES (31,"SRI VARDHAN REDDY", NULL, "DASARLAPALLI", 105, '9734196893123', "Hyderabad", NULL, "HYD", "TELANGANA", "INDIA", "M", "2003-07-17" );

ALTER TABLE EMPLOYEE
DROP COLUMN EDLEVEL;

ALTER TABLE EMPLOYEE
MODIFY MIDINIT CHAR(1);

ALTER TABLE EMPLOYEE
MODIFY FIRSTNME VARCHAR(50);

ALTER TABLE EMPLOYEE
MODIFY LASTNAME VARCHAR(50);

ALTER TABLE EMPLOYEE
MODIFY PHONENO BIGINT;

CREATE TABLE DEPT(
      DeptID INT PRIMARY KEY,
      DeptName VARCHAR(50) NOT NULL,
      NumberofEmp INT
)

INSERT INTO DEPT (DeptID, DeptName, NumberofEmp)
VALUES (101, "Finance", 8),
(102, "Marketing", 8),
(103, "IT", 8),
(104, "Sales", 6);

INSERT INTO DEPT(DeptID, DeptName, NumberofEmp)
VALUES (105, "ADMINISTRATOR", 1);