%% The first command in your LaTeX source must be the \documentclass command.
%%
%% Options:
%% twocolumn : Two column layout.
%% hf: enable header and footer.
\documentclass[
% twocolumn,
% hf,
]{ceurart}

%%
%% One can fix some overfulls
\sloppy

%%
%% Minted listings support 
%% Need pygment <http://pygments.org/> <http://pypi.python.org/pypi/Pygments>
\usepackage{listings}
\usepackage[authoryear,longnamesfirst]{natbib}

\usepackage{placeins}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{array} % For table formatting
\usepackage{placeins}
\usepackage{graphicx}
\usepackage{svg}  
%% auto break lines
\lstset{breaklines=true}

%%
%% end of the preamble, start of the body of the document source.
\begin{document}

%%
%% Rights management information.
%% CC-BY is default license.
\copyrightyear{2022}
\copyrightclause{Copyright for this paper by its authors.
  Use permitted under Creative Commons License Attribution 4.0
  International (CC BY 4.0).}

%%
%% This command is for the conference information
\conference{Woodstock'22: Symposium on the irreproducible science,
  June 07--11, 2022, Woodstock, NY}

%%
%% The "title" command
\title{Development and Evaluation of Custom Data Collection Tools for Mental Workload Assessment in Software Engineers: A Design Science Research Approach}

\tnotemark[1]
\tnotetext[1]{You can use this document as the template for preparing your
  publication. We recommend using the latest version of the ceurart style.}

%%
%% The "author" command and its associated commands are used to define
%% the authors and their affiliations.
\author[1]{Sameera Gamage}[%
orcid=0000-0002-0877-7063,
email=sameera.gamage@oulu.fi,
url=https://www.softwareengineering.fi/researchers/sameera-gamage/,
]
\cormark[1]
\fnmark[1]
\address[1]{University of Oulu, P.O. Box 123, Oulu, 90014, Northern Ostrobothnia, Finland}



\author[1]{Pantea Keikhosrokiani}[%
orcid=0000-0001-7116-9338,
email=pantea.keikhosrokiani@oulu.fi,
url=https://www.linkedin.com/in/pantea-keikhosrokiani-55145a276/,
]
\fnmark[1]


\begin{comment}
\author[4]{Manfred Jeusfeld}[%
orcid=0000-0002-9421-8566,
email=Manfred.Jeusfeld@acm.org,
url=http://conceptbase.sourceforge.net/mjf/,
]
\fnmark[1]
\address[4]{University of Skövde, Högskolevägen 1, 541 28 Skövde, Sweden}

\end{comment}
%% Footnotes
\cortext[1]{Corresponding author.}
\fntext[1]{These authors contributed equally.}

%%
%% The abstract is a short summary of the work to be presented in the
%% article.
\begin{abstract}
Mental workload (MWL) assessment is crucial in high-cognitive-demand professions such as software engineering, where mental strain impacts productivity, accuracy, and well-being. Traditional MWL assessment methods, which are based solely on subjective self-reports or physiological signals alone, often lack reliability, real-world applicability, or comprehensive validation. This study introduces a custom-built data collection framework tailored for software engineers, integrating a Task Simulation Desktop Application (TSDA) and a Self-Reporting Mobile Application (SRMA). The TSDA replicates real-world software engineering tasks, while the SRMA collects self-reported workload levels (NASA-TLX) alongside objective electroencephalography (EEG) signals.

The research follows the Design Science Research (DSR) methodology, ensuring iterative development, usability testing, and refinement of the tools based on software engineer feedback. A structured pilot test phase evaluated the effectiveness of the system, leading to improved usability, data synchronization, and reliability. The results demonstrate that the tools developed provide a structured and scalable MWL data collection framework, allowing dual-source workload assessment through synchronized EEG-based physiological monitoring and subjective reporting. Although this study focuses on tool development, future research will employ machine learning-based workload analysis to automate MWL classification, improve real-time workload prediction, and improve adaptive cognitive load management in software engineering workflows. The integration of EEG signals along with task simulations performance and NASA-TLX self-reports provides a dual-validation mechanism, which lays the groundwork for AI-driven cognitive workload prediction models aimed at optimizing task allocation and well-being of Software Engineers.
\end{abstract}

%%
%% Keywords. The author(s) should pick words that accurately describe
%% the work being presented. Separate the keywords with commas.
\begin{keywords}
  Development Life-cycle \sep EEG data \sep Mental Workload \sep Task Simulation \sep Artificial Intelligence 
\end{keywords}

%%
%% This command processes the author and affiliation and title
%% information and builds the first part of the formatted document.
\maketitle

\section{Introduction}

Mental workload (MWL) significantly influences task performance, cognitive efficiency, and well-being, particularly in high-demand fields such as software engineering \cite{Munoz2018}. Accurate MWL assessment is essential for enhancing productivity, reducing cognitive strain, and improving decision-making \cite{Ghanavati2019}. Traditional MWL assessment methods—like NASA-TLX and physiological measures such as EEG—have limitations due to subjective bias and sensitivity to external factors.

Software engineering tasks (e.g., debugging, problem solving, multitasking) impose substantial cognitive loads, yet current assessment tools fail to capture real-time workload variations specific to this domain. Existing methods like primary and secondary task performance are influenced by skill levels or introduce additional cognitive burdens, while physiological signals require careful contextual interpretation \cite{Ding2020, Teoh2021, Keikhosrokiani2024}.

This study presents a custom-built MWL assessment framework integrating: 
\begin{enumerate}
    \item \textbf{Task Simulation Desktop Application (TSDA)} – replicates software engineering tasks in a controlled setting.
    \item \textbf{Self-Reporting Mobile Application (SRMA)} – collects NASA-TLX assessments alongside EEG data.
\end{enumerate}

Using synchronized EEG and subjective reports, this dual-source system enables real-time MWL validation tailored to software engineers. The research follows the Design Science Research (DSR) methodology with iterative development and usability testing.

The primary objectives of this study are:
\begin{enumerate}
    \item Identify functional requirements for EEG-based MWL assessment tools in software engineering.
    \item Analyze the relationship between EEG-derived metrics and NASA-TLX self-reports.
    \item Develop secure and user-centered applications for synchronized MWL data collection.
    \item Evaluate the tools’ effectiveness through empirical testing and user feedback.
\end{enumerate}

This work lays the foundation for future ML-based analysis of workload data and provides scalable, structured tools for assessing cognitive load in real-world software engineering scenarios.

\section{Background}

While working on multitasks expecting to achieve critical deadlines, SE face higher levels of Cognitive loads. High cognitive load affects productivity, code quality, and mental well-being, leading to burnout and increased software defects. Tang et al. (2024) analyzed developer behaviors in validating AI-generated code using eye tracking and found high mental demand in IDE-based workflows \cite{Tang2024}. Nakasai et al. (2024) measured the MWL of software developers using physiological indicators, providing objective information on cognitive strain \cite{Nakasai2024}. Astuti et al. (2024) explored the impact of techno-stress on millennial work-life balance in digital work, focusing on its mediating role in employee well-being and job satisfaction \cite{Astuti2024}. Schott et al. (2024) examined usability, cognitive load, and presence in Virtual Reality (VR) environments, emphasizing how copresence and social interaction influence cognitive demands in mixed reality applications \cite{Schott2024}. Dourado et al. (2024) evaluated MWL in Industry 5.0 wearable Augmented Reality (AR) systems, demonstrating high cognitive strain during software-related tasks \cite{10718838}. These studies emphasize the need for workload optimization strategies to improve developer efficiency and well-being while reducing defects and cognitive overload in software engineering. It is important to identify tasks that increase the mental workload of SE.  

\subsection{Mental Workload (MWL): Concepts and Definitions}

Mental workload (MWL) refers to the cognitive effort required to complete a task and is understood through resource-based and subjective perspectives \cite{Ding2020}. The Multi-Resource Model (MRM) and Yerkes-Dodson law provide foundational models for understanding how MWL influences performance \cite{Teoh2021, Ghanavati2019}. MWL is critical to optimize in high-demand domains like software engineering, HCI, and aviation, where poor workload management can impact productivity and safety \cite{Keikhosrokiani2024}. Understanding MWL supports designing effective tools for workload evaluation in dynamic environments.

\subsection{Traditional Techniques for Mental Workload Measurement}

MWL measurement techniques fall into three categories: primary task performance, secondary task performance, and subjective rating scales. Each has specific strengths and limitations.

\subsubsection{Primary Task Performance}
Assesses accuracy, speed, or decision-making under load, but results may be influenced by individual differences or ceiling/floor effects. Combined use with physiological and subjective metrics can improve assessment precision \cite{Ghanavati2019}.

\subsubsection{Secondary Task Performance}
Introduces a parallel task to evaluate the reduction in performance under load. While effective for detecting moderate workload changes, it may increase total cognitive load and interfere with task execution \cite{Tang2024}.

\subsubsection{Subjective Rating Scales}
Subjective assessments, especially NASA-TLX, are widely used due to their simplicity and applicability, despite susceptibility to bias. Table~\ref{tab:subjective_comparison} compares popular subjective MWL scales.

\begin{table}[h]
\caption{Comparison of Subjective Mental Workload Assessment Methods}
\label{tab:subjective_comparison}
    \centering
    \renewcommand{\arraystretch}{1.2}
    \begin{tabular}{p{1.7cm} p{5cm} p{3.3cm} p{4.7cm}}
        \toprule
        \textbf{Method} & \textbf{Pros} & \textbf{Cons} & \textbf{Comparison with NASA-TLX} \\
        \midrule
        NASA-TLX & Multi-dimensional (mental, physical, temporal demand, effort, performance, frustration), widely validated, sensitive to task variations [1] & Subject to bias and retrospective recall errors [2] & Baseline reference method \\
        \midrule
        SWAT & Accounts for time, effort, and stress components [3] & Requires pre-task ranking, complex interpretation [4] & More structured but less flexible than NASA-TLX \\
        \midrule
        Workload Profile (WP) & Provides an in-depth breakdown of cognitive demands [5] & Overly detailed, complex scoring [6] & More detailed but impractical for quick assessments \\
        \midrule
        RSME & Simple and real-time workload assessment [7] & Single-dimension, lacks detailed insights & NASA-TLX offers more dimensions and analytical depth \\
        \midrule
        DSSQ & Measures workload and emotional states [8] & Best suited for stress analysis, not pure MWL & NASA-TLX is more relevant for cognitive workload assessments \\
        \midrule
        SCWL & Simpler workload classification [9] & Lacks granularity and validation & NASA-TLX is more robust and widely tested \\
        \midrule
        CHRS & Useful for piloting and aviation [10] & Task-specific, not generalizable & NASA-TLX is more versatile across domains \\
        \midrule
        ISA & Real-time assessment [11] & Interrupts task flow, lacks detailed workload analysis & NASA-TLX provides better workload breakdown while ISA is better for momentary assessments \\
        \midrule
        WEAS & Straightforward workload comparison [12] & Lacks specificity & NASA-TLX provides task-specific workload details, making it more informative \\
        \bottomrule
    \end{tabular}
\end{table}

\subsection{Physiological signal analysis in MWL}

Modern sensing technologies allow for precise detection of physiological responses to cognitive stressors. Table~\ref{Comparison of Physiological Measures Used in MWL analysis} outlines the key physiological signals used in MWL assessment.

\begin{table}[H]
\caption{Comparison of Physiological Measures Used in MWL Analysis}
    \label{Comparison of Physiological Measures Used in MWL analysis}
    \centering
    \fontsize{8}{9}\selectfont
    \renewcommand{\arraystretch}{1.2}
    \begin{tabular}{p{3.7cm} p{11.9cm}}
        \toprule
        \textbf{Physiological Measure} & \textbf{Advantage} \\
        \midrule
        Heart Rate (HR) & Provides real-time data on cardiovascular strain (Chen \& Tserng, 2022 \cite{chen2022real}). \\
        \midrule
        Electroencephalography (EEG) & Captures brain activity, offering insights into cognitive workload (Zanetti et al., 2022 \cite{9464276}). \\
        \midrule
        Galvanic Skin Response (GSR) & Measures skin conductance, reflecting emotional and stress responses (Nechyporenko et al., 2024 \cite{nechyporenko2024galvanic}). \\
        \midrule
        Pupil Dilation & Indicates changes in cognitive load and emotional state (Bauer et al., 2022 \cite{bauer2022pupillometry}). \\
        \midrule
        Blood Pressure & Assesses cardiovascular responses to mental workload and stress (Ahmed et al., 2023 \cite{ahmed2023effects}). \\
        \midrule
        Respiration Rate & Provides data on breathing patterns and stress levels (Siddiqui et al., 2021 \cite{siddiqui2021respiration}). \\
        \midrule
        Eye Blink Rate & Reflects cognitive load and fatigue levels (Hu \& Lodewijks, 2021 \cite{HU2021150}). \\
        \midrule
        Functional Near-Infrared Spectroscopy (fNIRS) & Non-invasively measures cerebral blood flow related to brain activity (Scholkmann et al., 2022 \cite{scholkmann2022systemic}). \\
        \midrule
        Skin Temperature & Changes in temperature can indicate stress and emotional states (Kumar et al., 2021 \cite{KUMAR202181}). \\
        \bottomrule
    \end{tabular}
\end{table}

EEG stands out due to its sensitivity to brain activity variations related to cognitive effort. It is non-invasive and provides real-time insights into workload changes.

\begin{enumerate}
    \item \textbf{Theta (4–8 Hz):} Associated with increased mental effort \cite{Ding2020}.
    \item \textbf{Alpha (8–12 Hz):} Reduced alpha power indicates higher cognitive workload \cite{Teoh2021}.
    \item \textbf{Beta (13–30 Hz):} Linked to attention and active processing \cite{Keikhosrokiani2024}.
\end{enumerate}

EEG-based MWL analysis aligns well with NASA-TLX, and using both ensures a more robust and accurate workload assessment \cite{Gogna2024}. This dual-source approach addresses limitations of either method alone, improving validation and reliability in software engineering contexts \cite{Zhou2021, DasChakladar2024}.

\subsection{Design Science Research Method}

Design Science Research Methodology (DSRM) enables structured artifact development through iterative cycles of relevance, rigor, and evaluation \cite{Hevner2004, Peffers2007}. Figure~\ref{dsr_steps} outlines the six DSRM stages used in this study. 

\begin{figure}[htbp]
    \centering    \includesvg[width=\textwidth]{figs/dsr_steps.svg}   
    \caption{Design Science Research Steps}   
    \label{dsr_steps}
\end{figure}

This study follows the combined DSR and Action Research (DSAR) approach \cite{Drechsler2019, Castro2025}, supporting the iterative development of task simulation and EEG-based assessment tools through mixed-method requirement gathering and empirical feedback. The method ensures the research remains both scientifically rigorous and practically applicable in real-world software engineering settings.
 
\section{Methodology}\label{sec:method}

Considering the DSR method, four cycles—Relevance, Design, Rigor, and Evaluation—were defined. Figure \ref{fig:relevant_dsr_steps} presents the inputs and outputs of each cycle in the artifact development process.

\subsection{Relevance Cycle}

This cycle focused on identifying problems related to MWL, workforce efficiency, and well-being in software engineering. The literature highlighted the need for optimized workload distribution and improved performance through accurate MWL detection. Traditional methods were found inadequate due to the dynamic nature of software engineering tasks. Consequently, this phase defined core components such as task types, data collection approaches, involved physiological signals, and contributing cognitive organs.

\subsection{Design Cycle}

Key system requirements were defined, including performance metrics collection and controlled task simulations to ensure unbiased data. Company environments were unsuitable due to operational interference. Preliminary interviews with software engineers identified real-world task themes such as deadlines, multitasking, and R\&D workflows. These insights informed the task simulation design and system functionality.

\subsection{Rigor Cycle}

The TSDA and SRMA were built on validated cognitive load models and usability principles. Existing research on EEG-based estimation and NASA-TLX was integrated for development guidance. Continuous EEG data necessitated non-overlapping tasks to ensure traceability. Empirical testing and iterative refinement ensured scientific validity and practical utility. EEG fluctuations were mapped to individual tasks to support accurate MWL interpretation.

\subsection{Evaluation Cycle}

This phase involved systematic testing and refinement of TSDA and SRMA. Effectiveness was measured through correlations between EEG signals and NASA-TLX scores, as well as task performance metrics (e.g., accuracy, time). Usability testing improved interface design and task integration. Visual comparisons of data sets validated tool interoperability. Participant feedback informed refinements, enhancing system stability and data reliability. Table \ref{tab:dsrm_6_stages} summarizes the stages and their corresponding DSRM cycles.

\begin{figure}[htbp]
    \centering    \includesvg[width=\textwidth]{figs/relevant_dsr_steps.svg}   
    \caption{Relevant Design Science Research Steps}   \label{fig:relevant_dsr_steps}
\end{figure}

\begin{table}[htbp]
    \centering    
    \caption{Design Science Research Methodology (DSRM) Steps and Relevant Cycles}
    \label{tab:dsrm_6_stages} \renewcommand{\arraystretch}{1.3}
    \begin{tabular}{p{3cm} p{4.5cm} p{7.6cm}}
        \toprule
        \textbf{DSRM Stages} & \textbf{Interaction of DSRM Cycles and Stages} & \textbf{Approaches} \\
        \midrule
        Stage 1: Problem Identification and Motivation & Cycle 1: Relevance Cycle impacts this stage & Review MWL research in software engineering. Identify gaps in workload assessment methods. Define MWL tool requirements. \\
        
        Stage 2: Definition of Objectives & Cycle 1: Relevance Cycle continues to impact this stage & Identify key MWL factors. Define software engineering task simulations. Select MWL assessment techniques. \\
        
        Stage 3: Design \& Development & Cycle 2: Relevance, Cycle 3: Design, Cycle 4: Rigor impact this stage & Develop task simulation and self-reporting applications. Integrate EEG data collection. Ensure data synchronization across all components. \\
        
        Stage 4: Demonstration & Cycle 4: Rigor Cycle impacts this stage & Conduct pilot tests with software engineers. Collect usability feedback. Assess software and EEG data integration. \\
        
        Stage 5: Evaluation & Cycle 4: Rigor Cycle, Cycle 5: Evaluation Cycle influence Cycle 3 (Design) \& Cycle 4 (Rigor) & Compare self-reported vs. EEG-based workload. Measure task performance (time, accuracy). Refine tools based on user feedback. \\
        
        Stage 6: Communication & Cycle 6: Communication Cycle impacts Cycle 3 (Design) & Publish findings in journals/conferences. Conduct industry workshops. Share tools via GitHub and research platforms. \\
        \bottomrule
    \end{tabular}
\end{table}

\subsection{Overall process of data collection}

The data collection process was defined based on literature and DSR principles. The complete workflow is illustrated in Figure \ref{overall_data_collection_steps}.

\begin{figure}[htbp]
    \centering    \includesvg[width=0.6\textwidth]{figs/data_collection_steps.svg}   
    \caption{Overall data collection process flow}   \label{overall_data_collection_steps}
\end{figure}

\subsection{Artifact Development phase}

The TSDA and SRMA were developed using Agile methodology in iterative sprints. Interviews guided task realism, UI design, and system requirements. Features of both applications are detailed in Table \ref{tab:simulation_nasatlx}. TSDA replicates real-world SE tasks; SRMA captures NASA-TLX self-reports.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.6\textwidth]{figs/wbs_dev.png}
\caption{Work breakdown structure for development}
\label{wbs_dev}
\end{figure}

\begin{table}[htbp]
\caption{Simulation Application and NASA-TLX Self-Reporting Application Features}
\label{tab:simulation_nasatlx}
\centering
\fontsize{8}{9}\selectfont
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{p{7.8cm} p{7.8cm}}
    \toprule
    \textbf{Simulation Application} & \textbf{NASA-TLX Self-Reporting Application} \\ 
    \midrule
    \multicolumn{2}{c}{\textbf{1. User Interface}} \\ 
    \midrule
    \begin{itemize}
        \item Provides basic explanations about the experiment and its procedures on the main page.
        \item Displays detailed descriptions of specific tasks on subsequent pages.
        \item Presents a final page summarizing Treplicator data collected during the session.
    \end{itemize} &
    \begin{itemize}
        \item Presents clear and concise instructions for users.
        \item Provides six visual analog scales (VAS) representing the different workload dimensions, such as:
        \begin{itemize}
            \item Mental Demand
            \item Physical Demand
            \item Temporal Demand
            \item Performance
            \item Effort
            \item Frustration
        \end{itemize}
        \item Offers options for users to rate their experience on each scale using sliders or touch gestures.
        \item Displays a message confirming the data has been uploaded to Firebase successfully.
        \item Shows an error message if there is an issue during the process or while uploading data to Firebase.
    \end{itemize} \\ 
    \midrule
    \multicolumn{2}{c}{\textbf{2. Task Simulation}} \\ 
    \midrule
    \begin{itemize}
        \item Simulates various tasks relevant to the software engineering career path.
        \item Offers a range of task difficulty levels to cater to different user abilities.
        \item Tracks the time taken to complete each task.
        \item Records the accuracy of user performance within the simulated tasks.
    \end{itemize} & 
    \begin{itemize}
        \item This application should integrate the NASA-TLX form. 
        \item Self-reporting MWL in this application is also considered a secondary task performance since it occupies cognitive resources.
    \end{itemize} \\ 
    \midrule
    \multicolumn{2}{c}{\textbf{3. Data Management}} \\ 
    \midrule
    \begin{itemize}
        \item Integrates with Firebase, a real-time database, for data storage.
        \item Stores user data (career path selection, etc.).
        \item Stores task results (completion time, accuracy).
    \end{itemize} & 
    \begin{itemize}
        \item Provides the ability for users to securely transmit data to cloud storage (requires an internet connection).
        \item Includes data anonymization features to protect user privacy.
    \end{itemize} \\ 
    \bottomrule
\end{tabular}
\end{table}

Non-functional requirements (Table~\ref{tab:NFRs}) focus on usability, performance, security, and compatibility to ensure robustness. Table~\ref{tab:limitations} outlines current limitations in real-world simulation and self-reporting accuracy.

\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.3}
    \caption{Non-Functional Requirements}
    \label{tab:NFRs}
    \begin{tabular}{p{7.8cm} p{7.8cm}}
        \toprule
        \textbf{Treplicator Software} & \textbf{NASA-TLX Mobile Application} \\
        \midrule
        \multicolumn{2}{c}{\textbf{Performance}} \\
        \midrule
        1. Fast response to user actions. & Quick app launch and interaction. \\
        2. Smooth task simulations. & \\
        \midrule
        \multicolumn{2}{c}{\textbf{Usability}} \\
        \midrule
        1. Intuitive UI for all users. & 1. Clear, easy-to-use UI on mobile. \\
        2. Clear instructions and task descriptions. & 2. Works smoothly on Android. \\
        \midrule
        \multicolumn{2}{c}{\textbf{Security}} \\
        \midrule
        1. Secure data storage in Firebase. & 1. Data encryption for privacy. \\
        2. Access control to prevent unauthorized use. & 2. Secure user data storage. \\
        \midrule
        \textbf{Compatibility} & \textbf{Battery Consumption} \\
        \midrule
        Works on Windows, macOS, and supports various screen sizes. & Optimized for minimal battery usage. \\
        \bottomrule
    \end{tabular}
\end{table}

\begin{table}[htbp]
\caption{Limitations of the Treplicator and NASA-TLX Mobile Application}
\label{tab:limitations}
\centering
\fontsize{8}{9}\selectfont
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{p{7.8cm} p{7.8cm}}
    \toprule
    \textbf{Simulator application} & \textbf{NASA-TLX self reporting Application} \\ 
    \midrule
    Relies on user honesty and accurate task performing during the test. & 
    Relies on user honesty and accurate self-reporting, which can be susceptible to bias. \\ 
    \midrule
    The simulated tasks may not perfectly replicate real-world experiences in chosen career paths. & 
    Requires users to understand the meaning of each workload dimension. \\ 
    \midrule
    Users may perform with lower stress in controlled environments. & 
    May not capture the full user experience. \\ 
    \midrule
    Student participants may not fully reflect real-world cognitive demands. & 
    Data transmission requires secure handling. \\ 
    \midrule
    ~ & Limited mobile UI space. \\ 
    \bottomrule
\end{tabular}
\end{table}

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figs/usecase_diagrams.png}
\caption{Usecase diagrams for both the applications}
\label{usecase}
\end{figure}

\subsection{Implementation of the artifact development}

TSDA includes subtasks that simulate a complete sprint cycle, from planning to deployment and learning. SRMA includes the validated NASA-TLX form for capturing perceived workload.

\subsubsection{List of simulated sub tasks for TSDA}
\label{sub_task_set}

This task aimed to replicate the high workload scenario experienced by software engineers during a typical software development sprint. The sprint focuses on the development of a new login feature for an existing software application. A typical process for developing a login feature task flow follows the steps below.

\begin{enumerate}
    \item \textbf{Sprint Planning Meeting:}
Attend a Sprint Planning Meeting to discuss goals and scope, review user stories and prioritize tasks for the sprint, and estimate the effort required for each user story and task.

    \item \textbf{Refinement of User Stories:}
Collaborate with the product owner and stakeholders to clarify requirements, break down user stories into smaller actionable tasks, and define the acceptance criteria for each user story.

    \item \textbf{Development Tasks:}
Start coding assigned user stories using the selected programming language and framework, Write clean, modular, and maintainable code following best practices. Also, commit code changes regularly to version control (e.g., Git) and create pull requests.
    
    \item \textbf{Code Review:}
Participate in code review sessions to provide and receive feedback, address issues or suggestions raised, and update the code accordingly.

    \item \textbf{Testing and Quality Assurance:}
Write unit tests to ensure functionality, perform integration tests to verify interactions between components, and regression testing to identify and fix unintended issues.

    \item \textbf{Documentation:}
Document implemented features, including technical specifications and usage, and update existing documentation to reflect changes introduced during the sprint.
    
    \item \textbf{Sprint Review:}
Participate in a sprint review meeting to demonstrate completed features and collect feedback, reflect on sprint goals, team dynamics, and improvements during the sprint retrospective, and identify areas for improvement and action items for the next sprint.
    
    \item \textbf{Continuous Learning and Improvement:}
Stay up-to-date with new technologies, tools, and best practices and seek opportunities for skill development and knowledge sharing within the team.

\end{enumerate}

\subsection{Usability Testing, Qualitative Feedback, and Refinement}

An iterative feedback process was used for refinement. Think-Aloud and post-test questionnaires helped identify usability issues. Adjustments included improving UI transitions, increasing task realism, and ensuring data consistency. Key feedback and actions are shown in Table~\ref{tab:qualitative_feedback}.

\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.3}
    \caption{Summary of Qualitative User Feedback and Implemented Changes}
    \label{tab:qualitative_feedback}
    \begin{tabular}{p{3.4cm} p{5.3cm} p{6.5cm}}
        \toprule
        \textbf{Feedback Theme} & \textbf{Participant Insights} & \textbf{Implemented Changes} \\
        \midrule
        Usability \& Interaction & Interface was intuitive but needed smoother transitions. & Improved UI design and optimized workflow transitions. \\
        \midrule
        Task Simulation Realism & Coding tasks lacked complexity. & Increased task complexity and added IDE integration. \\
        \midrule
        MWL Data Collection & Self-reported scores lacked consistency. & Implemented real-time validation between EEG and self-reported data. \\
        \midrule
        Technical Issues & Occasional delays in Firebase data syncing. & Optimized data handling and added confirmation messages. \\
        \bottomrule
    \end{tabular}
\end{table}

\subsection{Pilot Testing and System Performance Evaluation}

A three-phase pilot study confirmed data synchronization, ease of workload entry, and log accuracy. This ensured task timestamps aligned with MWL ratings. Post-test refinements addressed stability, clarity, and response times.

\subsection{Final Validation and Data Collection Workflow}

To ensure that TSDA and SRMA collect and synchronize MWL data effectively, a structured validation process was conducted before large-scale deployment. This phase focused on verifying the accuracy of the data synchronization and logging processes. The validation process ensured that the recorded workload values were correctly stored in Firebase and cross-checked with task execution logs to prevent inconsistencies.

Further analysis was performed to validate data synchronization and system reliability. The system logs were reviewed to confirm that no workload submission attempts were lost, corrupted, or unsynchronized. By ensuring that the workload entries aligned precisely with task timestamps, the validation process reinforced data integrity and ensured that the developed tools provide a reliable foundation for future MWL analysis and machine learning-based workload predictions.


\section{Results}

In this research, software development processes were followed to develop specific and relevant applications for data collection for MWL analysis of employees in an organization. As a profession, software engineers were selected as there was a lack of research conducted on SE MWL analysis. Two applications were developed to collect data while performing their usual tasks. Primary and secondary tasks were considered to collect MWL data. Task performance data, such as,
\begin{enumerate}
    \item Task performance accuracy and task completion time (collected from TSDA),
    \item Self reported MWL as a secondary data collection (collected from SRMA),
\end{enumerate}
 were collected while recording the behavior of the cognitive load using the Emotive EEG signal sensing wireless device.

\subsection{Task simulation desktop application}

TSDA was developed using the Python language and consisted of a landing page to explain the task using text and audio. Then in the next page, the user id and the initial level of workload are recorded according to the initial explanation of the tasks to be completed. The explanation is displayed on the page, and the workload related to the first impression is considered here as the initial MWL. The researcher or assessor can provide the user id at the time of data collection. The introduction page of the TSDA along with more information are available on GitHub for reference \footnote{The complete implementation can be found at: 
\begin{itemize}
    \item TSDA Development: \href{https://github.com/Sameera-G/TreplicatorEEG}{https://github.com/Sameera-G/TreplicatorEEG}
\end{itemize}}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.7\textwidth]{figs/software_eng_first_page.png}
\caption{Introduction page of the TSDA and self reporting page of SRMA for software engineers}
\label{softeng_first_page}
\end{figure}

As seen in section \ref{sub_task_set}, TSDA has 8 sub tasks for a software engineer to complete in order to collect MWL data for one session. As an example, activities related to Refinement of user stories page have been shown in Figure \ref{softeng_task_page}.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.7\textwidth]{figs/software_eng_task_page.png}
\caption{Page for activities related to Refinement of user stories}
\label{softeng_task_page}
\end{figure}

\subsection{Self reporting mobile application}

This application is used to record the self-felt MWL after each sub-task conducted at the TSDA. In order to record the MWL, the NASA task load index (NASA-TLX) form is used in this mobile application. The same user id which was entered in the TSDA, should be entered on the landing page of this application too. Then, according to the six components of the NASA-TLX, the MWL values should be marked using the sliders in the following pages. Figure \ref{SRMA_pages} shows the pages of the SRMA.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.7\textwidth]{figs/SRMA_pages_001.png}
\caption{Pages of SRMA to mark and upload self reported MWL values}
\label{SRMA_pages}
\end{figure}

The full source code and all developed data collection tools' interfaces are available on GitHub for access and further reference.\footnote{The complete implementation can be found at: 
\begin{itemize}
    \item TSDA Development: \href{https://github.com/Sameera-G/TreplicatorEEG}{https://github.com/Sameera-G/TreplicatorEEG}
    \item SRMA Development: \href{https://github.com/Sameera-G/nasa_tlx_eeg_research}{https://github.com/Sameera-G/nasa\_tlx\_eeg\_research}
\end{itemize}}

\section{Discussion}

During the development process of two artifacts, TSDA and SRMA, a comprehensive design approach was used following the DSR method. Figure \ref{apps_usage} shows the application of the newly developed artifacts for the MWL measurement experiment.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.7\textwidth]{figs/app_usage.jpg}
\caption{Developed appöications are in action}
\label{apps_usage}
\end{figure}

Traditional MWL assessment tools such as NASA-TLX and SWAT have been widely used for mental workload evaluation. However, these methods are based solely on subjective self-reports, making them prone to user bias, retrospective recall issues, and individual perception variability. In contrast, physiological signal-based methods (e.g., heart rate variability, galvanic skin response, and pupil dilation) provide objective workload indicators, but lack specificity to cognitive workload and are influenced by external stressors (Zhou et al., 2021).

Recent studies highlight EEG-based MWL measurement as a highly accurate and real-time assessment method, effectively capturing cognitive load variations specific to software engineering tasks (Keshvarparast et al., 2024). However, EEG alone has challenges, including data noise, complex setup, and the need for expert analysis.

Based on the latest literature and research findings, Table \ref{tab:MWL_comparison} compares traditional and modern MWL assessment tools in terms of accuracy, usability, real-world applicability, and suitability for software engineering tasks.

\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.3} % Adjust row height for better readability
    \caption{Comparison of Mental Workload Assessment Tools for Software Engineers}
    \label{tab:MWL_comparison}
    \begin{tabular}{p{3cm} p{2.3cm} p{2cm} p{2cm} p{2cm} p{2.5cm}}
        \toprule
        \textbf{Method} & \textbf{Measurement Type} & \textbf{Accuracy} & \textbf{Usability} & \textbf{Real-World Applicability} & \textbf{Suitability for Software Engineering} \\
        \midrule
        NASA-TLX \textit{(Hart \& Staveland, 1988)} & Subjective (Self-report) & Moderate (User Bias) & High (Easy to Use) & Moderate & Limited (Subjective Bias) \\
        \midrule
        SWAT (Subjective Workload Assessment Technique) & Subjective & Moderate & Moderate & Moderate & Limited \\
        \midrule
        Physiological Signals (Heart Rate, GSR, Pupil Dilation, etc.) & Physiological & High & Low (Requires Equipment) & High (Real-Time Monitoring) & Partial (Non-Cognitive Load Specific) \\
        \midrule
        EEG-Based MWL Analysis & Neurophysiological & Very High & Moderate & High (Real-Time and Objective) & Strong (Captures Cognitive Load) \\
        \midrule
        \textbf{This Developed Tool (TSDA and SRMA)} & Combined (Objective + Subjective) & Very High (Dual-Validation) & High & Very High & Strong (Custom-Built for Software Engineers) \\
        \bottomrule
    \end{tabular}
\end{table}

\subsection{Novelty of the developed applications}
To overcome the limitations of subjective and objective MWL assessment methods, this research introduces custom-built data collection tools that integrate task simulation (realistic software engineering scenarios),
EEG-based physiological measurement (objective cognitive load tracking), and
NASA-TLX self-reporting (subjective workload validation).
The combination of EEG signals and self-reported workload ratings enhances the accuracy and reliability of MWL assessment, ensuring a multi-source validation approach. Unlike existing methods, which rely on a single data source, the developed tool provides dual-modality verification, making it highly suitable for software engineering environments.

\subsection{Real-World applicability and industry relevance}
One of the key advantages of the proposed system is its applicability to real-world software development workflows. By integrating task simulations that mimic real engineering tasks (e.g., debugging, coding, reviewing), this tool allows researchers and industry professionals to assess cognitive workload variations during software development tasks, Identify cognitive bottlenecks and high-load scenarios that may impact productivity, Optimize work schedules and introduce cognitive load balancing mechanisms, and Improve workplace well-being by monitoring mental strain levels over time.
Compared with traditional MWL tools, this system ensures higher ecological validity, as it captures real-world task execution dynamics rather than abstracted task assessments.

Considering practical implications,
the developed data collection tools offer significant potential for real-world application in software engineering work environments. By integrating EEG-based MWL monitoring with self-reported data, this system can help software development teams optimize task assignments based on cognitive load analysis, assist project managers in identifying workload-induced burnout risks, and enable adaptive work environments, where real-time workload feedback informs task scheduling and break recommendations.

\subsection{Future Research and Integration with Machine Learning}
Although this article focuses on the development of data collection tools, the next phase of this research will utilize machine learning-based approaches to analyze EEG data and trends in self-reported workload. Advanced techniques such as deep learning classifiers, time-series analysis, and feature extraction models will be explored, to provide automated real-time workload predictions. Future work will focus on developing AI-driven workload classification models, automating the identification of high cognitive load patterns, and integrating real-time feedback mechanisms to optimize workload distribution in software teams.
By implementing data-driven workload management, this research aims to improve software engineering productivity, cognitive well-being, and efficiency.

\section{Ethical Considerations \& Limitations}
 
\begin{itemize}
    \item Participant privacy: EEG recordings contain biometric data, necessitating strict data anonymization and secure storage. In this research, none of the data collection tools collects participants' personal data. In addition, participants gave their informed consent prior to data collection.
    \item Experimental Bias: Self-reported NASA-TLX scores can introduce subjective bias, which will be considered during data analysis in a subsequent study. 
    \item Generalizability: Although the tasks simulated real-world software engineering workflows, the actual workplace distractions and collaboration dynamics were not fully replicated.
    \item Data handling: The study ensures compliance with GDPR and research ethics for handling EEG and self-reported data.
\end{itemize}

\section{Conclusion}\label{sec:conclusion}

This study introduced the development and evaluation of custom-built data collection tools for mental workload (MWL) assessment in software engineers, following the Design Science Research (DSR) methodology. The research successfully designed and implemented two key artifacts: the Task Simulation Desktop Application (TSDA) and the Self-Reporting Mobile Application (SRMA), which together facilitate the synchronized collection of EEG-based physiological signals and subjective workload reports. These tools bridge the gap between traditional workload assessment methods and real-world software engineering environments, ensuring a more structured, reliable, and domain-specific MWL evaluation framework.

The iterative development and refinement cycles followed a user-centered approach, incorporating feedback from software engineers to optimize usability, task realism, and data synchronization. By simulating real-world software engineering tasks and integrating objective and subjective MWL measurement methods, the developed tools offer a novel and scalable solution for cognitive workload monitoring in high-demand professional settings.

Although this study primarily focused on the development and validation of these data collection tools, the subsequent phase of this research will utilize machine learning techniques to analyze the collected EEG and self-reported workload data. Future work will explore automated cognitive workload classification, adaptive workload balancing in real time, and personalized work environment optimizations, enhancing both developer productivity and well-being.

This research contributes significantly to the evaluation of MWL assessment in software engineering by providing a validated, task-specific, and technologically enhanced data collection framework. By integrating cutting-edge neuroscience, cognitive psychology, and software engineering principles, this study lays the foundation for future advancements in workload-aware software development environments.

%% Define the bibliography file to be used
\bibliography{sample-ceur}

\end{document}

%%
%% End of file
