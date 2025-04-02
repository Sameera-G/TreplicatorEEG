Sure, Sameera! Here's a cleaned-up and well-structured version of your LaTeX-based research article, converted into **Markdown format suitable for a GitHub `README.md` file**. This version highlights your project, tools, methodology, and links while maintaining clarity for developers and researchers visiting your repo.

---

# EEG-Based Mental Workload Assessment Tools for Software Engineers

This repository provides custom-built data collection tools developed to assess mental workload (MWL) in software engineers. The framework integrates **task simulations**, **self-reported assessments (NASA-TLX)**, and **EEG signal monitoring**, ensuring a dual-source workload evaluation. It follows a **Design Science Research (DSR)** methodology for iterative development and validation.

## Project Title

**Development and Evaluation of Custom Data Collection Tools for Mental Workload Assessment in Software Engineers: A Design Science Research Approach**

---

## Abstract
Mental workload (MWL) assessment is crucial in high-cognitive-demand professions such as software engineering, where mental strain impacts productivity, accuracy, and well-being. Traditional MWL assessment methods, which are based solely on subjective self-reports or physiological signals alone, often lack reliability, real-world applicability, or comprehensive validation. This study introduces a custom-built data collection framework tailored for software engineers, integrating a Task Simulation Desktop Application (TSDA) and a Self-Reporting Mobile Application (SRMA). The TSDA replicates real-world software engineering tasks, while the SRMA collects self-reported workload levels (NASA-TLX) alongside objective electroencephalography (EEG) signals.

The research follows the Design Science Research (DSR) methodology, ensuring iterative development, usability testing, and refinement of the tools based on software engineer feedback. A structured pilot test phase evaluated the effectiveness of the system, leading to improved usability, data synchronization, and reliability. The results demonstrate that the tools developed provide a structured and scalable MWL data collection framework, allowing dual-source workload assessment through synchronized EEG-based physiological monitoring and subjective reporting. Although this study focuses on tool development, future research will employ machine learning-based workload analysis to automate MWL classification, improve real-time workload prediction, and improve adaptive cognitive load management in software engineering workflows. The integration of EEG signals along with task simulations performance and NASA-TLX self-reports provides a dual-validation mechanism, which lays the groundwork for AI-driven cognitive workload prediction models aimed at optimizing task allocation and well-being of Software Engineers.

## Tools Developed

### 1. Task Simulation Desktop Application (TSDA)
Simulates real-world software engineering tasks to collect performance-related data such as:
- Task accuracy
- Completion time
- EEG signal synchronization

🔗 [TSDA Source Code on GitHub](https://github.com/Sameera-G/TreplicatorEEG)

### 2. Self-Reporting Mobile Application (SRMA)
Records self-reported MWL values using NASA-TLX after each simulated task.

🔗 [SRMA Source Code on GitHub](https://github.com/Sameera-G/nasa_tlx_eeg_research)

---

## Methodology

The tools were developed using the **Design Science Research (DSR)** method, consisting of:
- **Relevance Cycle**: Identifying needs and task characteristics
- **Design Cycle**: Gathering requirements and building artifacts
- **Rigor Cycle**: Ensuring scientific validity and alignment with EEG + NASA-TLX standards
- **Evaluation Cycle**: Pilot testing, usability improvements, and validation

 **EEG Band Focus**:
- Theta (4–8 Hz): Mental effort  
- Alpha (8–12 Hz): Inverse workload indicator  
- Beta (13–30 Hz): Active attention  

---

## Key Features

| Feature | TSDA | SRMA |
|--------|------|------|
| Task simulation | ✅ | ❌ |
| EEG integration | ✅ | ❌ |
| NASA-TLX workload rating | ❌ | ✅ |
| Firebase synchronization | ✅ | ✅ |
| Cross-platform support | Windows/macOS | Android |
| Real-time data logging | ✅ | ✅ |

---

## Research Objectives

- Identify EEG-based workload measurement components
- Correlate NASA-TLX with EEG signals
- Evaluate effectiveness through usability testing
- Lay the foundation for machine learning-based MWL prediction

---

## Pilot Testing

Three-phase iterative testing ensured:
- Timestamp-accurate data synchronization
- Realistic task simulation and performance tracking
- Usability validation with software engineers

---

## Results Summary

EEG Data: Synchronized with tasks

NASA-TLX: Captured subjective perception post-task

Performance Metrics: Completion time, accuracy

Data Storage: Firebase real-time cloud database



## 📷 Screenshots

| TSDA Interface | SRMA NASA-TLX Rating |
|----------------|-----------------------|
| ![TSDA](<img width="1280" alt="software_eng_first_page" src="https://github.com/user-attachments/assets/67261453-7b37-49eb-94e0-0679bdbceccf" />) | ![SRMA_pages](https://github.com/user-attachments/assets/e06a0929-0225-40df-a001-664a02c52d96) |

---

## Future Work

- Integration of **machine learning** for real-time workload classification
- Deployment in real software development environments
- Adaptive workload management using AI

---

## Ethical Considerations

- EEG data anonymized and stored securely (Firebase)
- No personal identifiers collected
- GDPR-compliant consent obtained for data collection

---

## Citation

If you use or refer to this project in your work, please cite:

```
Sameera Gamage, Pantea Keikhosrokiani, "Development and Evaluation of Custom Data Collection Tools for Mental Workload Assessment in Software Engineers: A Design Science Research Approach", 2025.
```

---

## Contact

- **Sameera Gamage**  
  University of Oulu  
  [sameera.gamage@oulu.fi](mailto:sameera.gamage@oulu.fi)  
  🔗 [Research Profile](https://www.softwareengineering.fi/researchers/sameera-gamage)

---

Let me know if you'd like me to convert this into a downloadable `README.md` file or want a tailored version for your GitHub Pages, academic CV, or publication abstract.
